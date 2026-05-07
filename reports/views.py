from .models import VueHoldwage, Empwisesal, Employeeworking, Holdwagepaid,ResignDtls,Empjoin,AttStaff,StaffAbsent,StaffAtt,ContractSec
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from datetime import datetime
from .models import LaySp, MasterFinalMistake, UnitBundlereport, FinalPlans,Corarlck1,CoraRollcheck,AttUnt,EmbAbsetnt,Holiday,LabAtt,RptCutting,VueOrdersinhand
from .models import BillAge,BillMdapprove,BillPass
from django.db.models import F, Q , IntegerField,DateField,Case, When, Value,CharField
from django.db import connections
from django.db.models import OuterRef, Subquery
from django.db.models import Sum
from datetime import datetime, timedelta,date
from django.utils import timezone
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncDay,Cast,Coalesce
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.utils import timezone
from django.db.models.expressions import ExpressionWrapper
from django.core.paginator import Paginator



# dt_timezone = timezone.make_aware(timezone.datetime(2012, 1, 1), timezone=timezone.UTC)

@csrf_exempt
def holdwage_report(request):
    if request.method == 'GET':
        try:
            code = request.GET.get("code")

            qs = VueHoldwage.objects.using('demo')

            if code:
                qs = qs.filter(code=code)

            data = list(qs.values())

            return JsonResponse(data, safe=False)
        except OSError as e:
            return JsonResponse({'error': f'Database connection error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error retrieving holdwage data: {str(e)}'}, status=500)
    
@csrf_exempt
def empwisesal(request):
    if request.method == 'GET':
        
        # Step 1: Get working employees with monthly salary
        qs = Empwisesal.objects.using('main').filter(
            status='working'
        )

        # Step 2: Fetch category mapping from EmployeeWorking
        working_map = {
            emp.code: emp.category
            for emp in Employeeworking.objects.using('main').all()
        }

        data = []

        for rec in qs:
            # Photo URL
            if rec.photo:
                filename = os.path.basename(rec.photo)
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None

            # Get designation from EmployeeWorking
            designation = working_map.get(rec.code)

            data.append({
                "code": rec.code,
                "name": rec.name,
                "dept": rec.dept,
                "salary": float(rec.salary) if rec.salary else None,
                "wrkunit": rec.wrkunit,
                "designation": designation,   # ✅ replaced
                "monthlysalary": rec.monthlysalary,
                "accountdetails1": rec.accountdetails1,
                "photo": photo_url
            })

        return JsonResponse(data, safe=False)
    

@csrf_exempt
def holdwagepaid_api(request):

    # ✅ GET
    if request.method == "GET":
        entry_no = request.GET.get("entry_no")
        aadhar = request.GET.get("aadhar")

        try:
            # 👉 Single record
            if entry_no:
                obj = Holdwagepaid.objects.using('demo').get(entry_no=entry_no)
                return JsonResponse({
                    "entry_no": obj.entry_no,
                    "dt": obj.dt.strftime("%Y-%m-%d"),
                    "aadhar_no": obj.aadhar_no,
                    "code": obj.code,
                    "emp_name": obj.emp_name,
                    "t_period": obj.t_period,
                    "paid_amt": float(obj.paid_amt),
                    "remarks": obj.remarks,
                })

            # 👉 Filter by Aadhaar
            if aadhar:
                data = list(
                    Holdwagepaid.objects.using('demo')
                    .filter(aadhar_no=aadhar)
                    .values()
                )
                return JsonResponse(data, safe=False)

            # 👉 All records
            data = list(Holdwagepaid.objects.using('demo').all().values())
            return JsonResponse(data, safe=False)

        except Holdwagepaid.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        except OSError as e:
            return JsonResponse({"error": f"Database connection error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Error retrieving holdwage data: {str(e)}"}, status=500)

    # ✅ POST (CREATE)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            if not all(k in data for k in ["dt", "code", "aadhar_no", "paid_amt"]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            dt = datetime.strptime(data["dt"], "%Y-%m-%d").date()
            code = int(data["code"])
            aadhar = str(data["aadhar_no"]).strip()
            paid_amt = float(data["paid_amt"])

            # ✅ NORMALIZE PERIOD (🔥 VERY IMPORTANT)
            t_period = str(data.get("t_period", "")).strip().upper()

            if not t_period:
                return JsonResponse({"error": "Period is required"}, status=400)

            print("CHECK:", aadhar, t_period)  # 🔍 debug

            # 🚫 DUPLICATE CHECK (FIXED PROPERLY)
            exists = Holdwagepaid.objects.using('demo').filter(
                aadhar_no=aadhar,
                t_period__iexact=t_period   # 🔥 case-insensitive
            ).exists()

            if exists:
                return JsonResponse({
                    "error": f"Already paid for {t_period}"
                }, status=400)

            # 🔢 Auto entry_no
            last = Holdwagepaid.objects.using('demo').order_by('-entry_no').first()
            next_entry = (last.entry_no + 1) if last else 1

            obj = Holdwagepaid.objects.using('demo').create(
                entry_no=next_entry,
                dt=dt,
                aadhar_no=aadhar,
                code=code,
                emp_name=data.get("emp_name"),
                t_period=t_period,   # ✅ save normalized
                paid_amt=paid_amt,
                remarks=data.get("remarks"),
            )

            return JsonResponse({
                "message": "Created",
                "entry_no": obj.entry_no
            })

        except OSError as e:
            print("DATABASE ERROR:", e)
            return JsonResponse({"error": f"Database connection error: {str(e)}"}, status=500)
        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=400)
    # ✅ PUT (UPDATE)
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            entry_no = data.get("entry_no")

            obj = Holdwagepaid.objects.using('demo').get(entry_no=entry_no)

            if "dt" in data:
                obj.dt = datetime.strptime(data["dt"], "%Y-%m-%d").date()

            if "aadhar_no" in data:
                obj.aadhar_no = str(data["aadhar_no"])

            if "code" in data:
                obj.code = int(data["code"])

            obj.emp_name = data.get("emp_name", obj.emp_name)
            obj.t_period = data.get("t_period", obj.t_period)

            if "paid_amt" in data:
                obj.paid_amt = float(data["paid_amt"])

            obj.remarks = data.get("remarks", obj.remarks)

            obj.save()

            return JsonResponse({"message": "Updated successfully"})

        except Holdwagepaid.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        except OSError as e:
            return JsonResponse({"error": f"Database connection error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # ✅ DELETE
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            entry_no = data.get("entry_no")

            obj = Holdwagepaid.objects.using('demo').get(entry_no=entry_no)
            obj.delete()

            return JsonResponse({"message": "Deleted successfully"})

        except Holdwagepaid.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        except OSError as e:
            return JsonResponse({"error": f"Database connection error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def get_lay_sp_data(request):
    if request.method == 'GET':
        # Subquery definition
        final_plan_qs = FinalPlans.objects.using('app').filter(
            plan_no=OuterRef('plan_no'),
            job_no=OuterRef('job_no')
        )

        data = (
            LaySp.objects.using('app')
            .annotate(
                # Use double underscores to match your React component's logic
                final_plans__pcs=Subquery(final_plan_qs.values('pcs')[:1]),
                final_plans__table_id=Subquery(final_plan_qs.values('table_id')[:1]),
                final_plans__empid=Subquery(final_plan_qs.values('empid')[:1]),
                final_plans__marker_no=Subquery(final_plan_qs.values('marker_no')[:1]),
                final_plans__lot_no=Subquery(final_plan_qs.values('lot_no')[:1]),
                final_plans__fabric_color=Subquery(final_plan_qs.values('fabric_color')[:1]),
            )
            .values(
                'date', 'timer', 'plan_no', 'job_no', 'roll_no', 'f_dia',
                'plan_ply', 'scl_wgt', 'plan_obwgt', 'req_wgt', 'actual_dia',
                'actual_ply', 'actual_obwgt', 'end_bit', 'bal_wgt', 'debit_kg',
                'roll_time', 'remarks', 'bit_wgt', 'date_time',
                'final_plans__pcs', 'final_plans__table_id', 'final_plans__empid',
                'final_plans__marker_no', 'final_plans__lot_no', 'final_plans__fabric_color','final_plans__date_time'
            )
        )

        return JsonResponse(list(data), safe=False)
    
    
@csrf_exempt
def get_master_final_mistake_data(request):
    if request.method == 'GET':
        data = MasterFinalMistake.objects.using('app').all().values()
        data_list = list(data)
        return JsonResponse(data_list, safe=False)
    
@csrf_exempt
def get_unit_bundle_report_data(request):

    if request.method == "GET":

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        unit = request.GET.get("unit")

        queryset = UnitBundlereport.objects.using("app").all()

        if start_date and end_date:
            queryset = queryset.filter(s_date__range=[start_date, end_date])

        if unit and unit != "all":
            queryset = queryset.filter(tb_name=unit)

        data = list(queryset.values())

        return JsonResponse(data, safe=False)

def mistake_summary(request):
    try:
        with connections['app'].cursor() as cursor:
            cursor.execute("EXEC sp_GetBitCheckMistakeSummary")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = []

        for row in rows:
            row_dict = dict(zip(columns, row))

            data.append({
                "JobNo": row_dict.get("JobNo"),
                "lotno": row_dict.get("lotno"),
                "rotiono": row_dict.get("rationo"),
                "TopBottom_des": row_dict.get("TopBottom_des"),
                "Name": row_dict.get("Name"),
                "clrcombo": row_dict.get("clrcombo"),
                "mistpc": row_dict.get("mistpc"),
                "Indparts": row_dict.get("Indparts"),
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({
            "status": False,
            "error": str(e)
        })
    

@csrf_exempt
def cora(request):
    if request.method == 'GET':

        # 👇 FIXED HERE
        roll_data = CoraRollcheck.objects.using('app').filter(
            rlno=OuterRef('roll_id')
        )

        data = Corarlck1.objects.using('app').annotate(
            jobno=Subquery(roll_data.values('jobno')[:1]),
            colour=Subquery(roll_data.values('colour')[:1]),
            gsm=Subquery(roll_data.values('gsm')[:1]),
            company=Subquery(roll_data.values('company')[:1]),
            fabric=Subquery(roll_data.values('fabricdescription')[:1]),
        ).values(
            'sl',
            'dt',
            'roll_id',   # 👈 this is your rlno now
            'hole',
            'setoff',
            'needle_line',
            'oil_line',
            'oil_drops',
            'remark',
            'poovari',
            'yarn_mistake',
            'lycra_cut',
            'yarn_uneven',
            'neps',
            'empid',
            'timer',
            'dia',
            'na_holes',
            'm12',
            'loop_len',
            'image',
            'submit',
            'mach_id',
            'time1',
            'time2',

            # merged fields
            'jobno',
            'colour',
            'gsm',
            'company',
            'fabric',
        )

        return JsonResponse(list(data), safe=False)
    

@csrf_exempt
def cutdel(request):
    if request.method == 'GET':
        try:
            # Get filter values from query params
            jobno = request.GET.get('jobno')
            planno = request.GET.get('planno')
            topbottom = request.GET.get('topbottom')
            lot = request.GET.get('lot')

            # Fetch order numbers from test DB
            orderno_list = list(
                VueOrdersinhand.objects.using('test')
                .values_list('orderno', flat=True)
            )

            # Base queryset
            data = RptCutting.objects.using('demo').filter(
                jobno__in=orderno_list
            )

            # Apply filters dynamically
            if jobno:
                data = data.filter(jobno__icontains=jobno)

            if planno:
                data = data.filter(planno__icontains=planno)

            if topbottom:
                data = data.filter(topbottom_des__icontains=topbottom)

            if lot:
                data = data.filter(lot__icontains=lot)

            # Select required fields and convert to list
            data = data.values(
                'jobno',
                'dt',
                'planno',
                'sample_descr',
                'per',
                'topbottom_des',
                'lot',
                'rls',
                'fdeldt',
                'plan_kg',
                'mtr',
                'cutdt',
                'tply',
                'aply',
                'ratio_stick_dt',
                'bitcheck_dt',
                'mas_bud_dt',
                'unitdel_dt',
            )

            result = list(data)
            print("Total records:", len(result))

            return JsonResponse(result, safe=False)
        
        except OSError as e:
            return JsonResponse({'error': f'Database connection error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error retrieving cutting data: {str(e)}'}, status=500)
        

#HR Report APIs

def get_friday_thursday_range(reference_date=None):
    if reference_date is None:
        reference_date = datetime.now().date()

    current_weekday = reference_date.weekday()

    # Last Friday
    if current_weekday >= 4:
        days_since_last_friday = current_weekday - 4
    else:
        days_since_last_friday = current_weekday + 3

    last_friday = reference_date - timedelta(days=days_since_last_friday)

    # This Thursday
    if current_weekday <= 3:
        days_until_thursday = 3 - current_weekday
    else:
        days_until_thursday = 10 - current_weekday

    this_thursday = reference_date + timedelta(days=days_until_thursday)

    return last_friday, this_thursday


# ===============================
# Attendance JSON API
# ===============================
def attendance(request):
    try:
        dept = request.GET.get("dept", "ALL")
        start_date_str = request.GET.get("startDate")
        end_date_str = request.GET.get("endDate")

        queryset = AttUnt.objects.using("demo").all()

        # Department filter
        if dept != "ALL":
            queryset = queryset.filter(dept__iexact=dept)

        # Date filter
        if not start_date_str or not end_date_str:
            start_date, end_date = get_friday_thursday_range()
        else:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except:
                start_date, end_date = get_friday_thursday_range()

        queryset = queryset.filter(dt__date__range=[start_date, end_date])

        # Aggregate data
        data_qs = queryset.values("dt").annotate(
            total=Sum("onroll"),
            tail_onr=Sum("tail_onr"),
            ntail_onr=Sum("ntail_onr"),
            present=Sum("present"),
            tailor=Sum("tailor"),
            n_tailor=Sum("n_tailor"),
            absent=Sum("absent"),
            tabsent=Sum("tabsent"),
            ntabsent=Sum("ntabsent"),
            le=Sum("le"),
            tlv=Sum("tlv"),
            ntlv=Sum("ntlv"),
        ).order_by("dt")

        result = []

        for row in data_qs:
            total = row["total"] or 0

            def pct(val):
                return round((val / total) * 100) if total else 0

            result.append({
                "date": row["dt"].strftime("%Y-%m-%d"),
                "total": total,
                "present": row["present"] or 0,
                "present_pct": pct(row["present"] or 0),
                "absent": row["absent"] or 0,
                "absent_pct": pct(row["absent"] or 0),
                "le": row["le"] or 0,
                "le_pct": pct(row["le"] or 0),
                "tlv": row["tlv"] or 0,
                "tlv_pct": pct(row["tlv"] or 0),
                "ntlv": row["ntlv"] or 0,
                "ntlv_pct": pct(row["ntlv"] or 0),
                "tail_onr": row["tail_onr"] or 0,
                "ntail_onr": row["ntail_onr"] or 0,
                "tailor": row["tailor"] or 0,
                "n_tailor": row["n_tailor"] or 0,
                "tabsent": row["tabsent"] or 0,
                "ntabsent": row["ntabsent"] or 0,
            })

        # Holidays
        holidays_qs = Holiday.objects.using("main").filter(
            dt__date__range=[start_date, end_date]
        ).values("dt", "descr")

        holidays = {
            h["dt"].strftime("%Y-%m-%d"): h["descr"]
            for h in holidays_qs
        }

        return JsonResponse({
            "status": "success",
            "unit": dept,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "holidays": holidays,
            "data": result
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


# ===============================
# Present Details JSON API
# ===============================
def present_details(request):
    try:
        date_str = request.GET.get("date")
        dept = request.GET.get("dept", "ALL")

        qs = LabAtt.objects.using("demo1").all()

        if date_str:
            sel_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            qs = qs.filter(date__date=sel_date)

        if dept != "ALL":
            qs = qs.filter(dept__iexact=dept)

        qs = qs.filter(intime__isnull=False)

        qs = qs.values(
            "code_emb_attendance_fact",
            "name",
            "dept",
            "emppic",
            "category"
        ).distinct().order_by("name")

        data = []

        for emp in qs:
            photo_url = None

            if emp["emppic"]:
                filename = os.path.basename(str(emp["emppic"]))
                photo_url = f"https://hf.herofashion.com/staff_images/{filename}"

            data.append({
                "code": emp["code_emb_attendance_fact"],
                "name": emp["name"],
                "dept": emp["dept"],
                "category": emp["category"],
                "photo": photo_url
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


# ===============================
# Absent Details JSON API
# ===============================
def abs_details(request):
    try:
        date_str = request.GET.get("date")
        dept = request.GET.get("dept", "ALL")

        queryset = EmbAbsetnt.objects.using("demo").all()

        if date_str:
            queryset = queryset.filter(dt__date=date_str)

        if dept != "ALL":
            queryset = queryset.filter(dept__iexact=dept)

        data = []

        for emp in queryset:
            photo_url = None

            if emp.photo:
                filename = os.path.basename(str(emp.photo))
                photo_url = f"https://hf.herofashion.com/staff_images/{filename}"

            data.append({
                "date": emp.dt.strftime("%Y-%m-%d") if emp.dt else "",
                "code": emp.code,
                "name": emp.name,
                "dept": emp.dept,
                "category": emp.category,
                "mobile": emp.mobile,
                "status": emp.s,
                "photo": photo_url
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
    

def resign_report(request):
    try:
        # =========================
        # GET FILTERS
        # =========================
        unit_filter = request.GET.get('unit', 'ALL')

        # IMPORTANT FIX
        from_date = request.GET.get('from_date') or None
        to_date = request.GET.get('to_date') or None

        # =========================
        # BASE QUERY
        # =========================
        resign = ResignDtls.objects.using('main').all()

        # =========================
        # UNIT FILTER
        # =========================
        if unit_filter and unit_filter != 'ALL':
            resign = resign.filter(dept=unit_filter)

        # =========================
        # DATE CALCULATION
        # =========================
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)

        # =========================
        # DATE FILTERS
        # =========================
        if not from_date and not to_date:

            # Default current month
            resign = resign.filter(
                resigndt__date__range=(first_day_of_month, today)
            )

            effective_from = first_day_of_month
            effective_to = today

        elif from_date and to_date:

            resign = resign.filter(
                resigndt__date__range=(from_date, to_date)
            )

            effective_from = from_date
            effective_to = to_date

        elif from_date:

            resign = resign.filter(
                resigndt__date__gte=from_date
            )

            effective_from = from_date
            effective_to = None

        elif to_date:

            resign = resign.filter(
                resigndt__date__lte=to_date
            )

            effective_from = None
            effective_to = to_date

        # =========================
        # ORDER
        # =========================
        resign = resign.order_by('-resigndt')

        # DEBUG
        print("FROM DATE:", from_date)
        print("TO DATE:", to_date)
        print("TOTAL RECORDS:", resign.count())

        # =========================
        # RESPONSE DATA
        # =========================
        resign_list = []

        for r in resign:

            # PHOTO URL
            if getattr(r, 'photo', None):
                filename = os.path.basename(str(r.photo))
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None

            resign_list.append({
                "id": r.code,
                "emp_name": r.name,
                "dept": getattr(r, "dept", ""),
                "joindt": r.joindt,
                "resign_date": r.resigndt,
                "category": getattr(r, "category", ""),
                "mobile": getattr(r, "mobile", ""),
                "days_worked": getattr(r, "days_worked", 0),
                "photo": photo_url
            })

        # =========================
        # STATS
        # =========================
        total_resignations = len(resign_list)

        avg_days = 0

        if total_resignations > 0:

            total_days = sum([
                r["days_worked"]
                for r in resign_list
                if r["days_worked"]
            ])

            avg_days = int(total_days / total_resignations)

        # THIS MONTH COUNT
        this_month_count = (
            ResignDtls.objects.using('main')
            .filter(
                resigndt__date__gte=first_day_of_month,
                resigndt__date__lte=today
            )
            .count()
        )

        # DEPARTMENTS
        departments = list(
            ResignDtls.objects.using('main')
            .exclude(dept__isnull=True)
            .exclude(dept__exact='')
            .values_list('dept', flat=True)
            .distinct()
            .order_by('dept')
        )

        # =========================
        # FINAL RESPONSE
        # =========================
        data = {
            "resign": resign_list,
            "departments": departments,
            "unit": unit_filter,
            "from_date": str(effective_from) if effective_from else None,
            "to_date": str(effective_to) if effective_to else None,
            "total_resignations": total_resignations,
            "avg_days": avg_days,
            "this_month_count": this_month_count,
        }

        return JsonResponse(data, safe=False)

    except Exception as e:

        print("RESIGN API ERROR:", str(e))

        return JsonResponse({
            "status": False,
            "message": str(e),
            "resign": [],
            "departments": [],
            "total_resignations": 0,
            "avg_days": 0,
            "this_month_count": 0
        }, status=500)
    

def join_data(request):
    # Read GET params
    unit = request.GET.get('unit') or 'ALL'
    start_str = request.GET.get('start') or ''
    end_str = request.GET.get('end') or ''

    # Default to current month when no dates provided
    today = date.today()
    if not start_str and not end_str:
        first_day = today.replace(day=1)
        start_str = first_day.isoformat()
        end_str = today.isoformat()

    # Base queryset
    qs = Empjoin.objects.using('main').all()

    # Unit filter
    if unit and unit != 'ALL':
        qs = qs.filter(dept=unit)

    # Date filters
    if start_str and end_str:
        qs = qs.filter(joindt__date__range=[start_str, end_str])
    elif start_str:
        qs = qs.filter(joindt__date__gte=start_str)
    elif end_str:
        qs = qs.filter(joindt__date__lte=end_str)

    # Convert queryset to JSON serializable list
    rows = []

    for rec in qs:
        # Photo handling
        if getattr(rec, 'photo', None):
            filename = os.path.basename(str(rec.photo))

            if getattr(settings, 'DEBUG', False):
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = rec.photo.url if hasattr(rec.photo, 'url') else str(rec.photo)
        else:
            photo_url = None

        rows.append({
            "id": rec.id,
            "empcode": getattr(rec, 'code', ''),
            "name": getattr(rec, 'name', ''),
            "dept": getattr(rec, 'dept', ''),
            "designation": getattr(rec, 'category', ''),
            "joindt": rec.joindt.strftime("%Y-%m-%d %H:%M:%S") if rec.joindt else None,
            "photo": photo_url,
        })

    total_joins = qs.count()

    # Departments list
    departments = list(
        Empjoin.objects.using('main')
        .values_list('dept', flat=True)
        .distinct()
        .order_by('dept')
    )

    data = {
        "success": True,
        "filters": {
            "unit": unit,
            "start": start_str,
            "end": end_str,
        },
        "total_joins": total_joins,
        "departments": departments,
        "rows": rows,
    }

    return JsonResponse(data, safe=False)


def week_bounds_mon_sat():
    """Return Monday–Saturday of the current week."""
    today = date.today()
    dow = today.weekday()
    monday = today - timedelta(days=dow)
    saturday = monday + timedelta(days=5)
    return monday, saturday

EXCLUDED_DEPTS = [
    "Maintenance",
    "Maintanence",
    "Maintainence",
    "Maintenanace",
    "Maintaince",
    "Service"
]


EXCLUDED_DEPTS = [
    "Maintenance",
    "Maintanence",
    "Maintainence",
    "Maintenanace",
    "Maintaince",
    "Service",
]


def week_bounds_mon_sat():
    today = date.today()

    monday = today - timedelta(days=today.weekday())
    saturday = monday + timedelta(days=5)

    return monday, saturday


def staff_overview(request):

    # ---------------------------------------------------
    # 1. Filters
    # ---------------------------------------------------
    dept = request.GET.get("dept", "ALL")

    start_date_str = request.GET.get("startDate")
    end_date_str = request.GET.get("endDate")

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(
                start_date_str,
                "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_date_str,
                "%Y-%m-%d"
            ).date()

        except Exception:
            start_date, end_date = week_bounds_mon_sat()

    else:
        start_date, end_date = week_bounds_mon_sat()

    today = date.today()

    iter_end = min(end_date, today)

    # ---------------------------------------------------
    # 2. Base Query
    # ---------------------------------------------------
    qs = (
        AttStaff.objects.using("demo")
        .annotate(date_only=TruncDate("dt"))
        .filter(date_only__range=[start_date, iter_end])
        .exclude(dept__in=EXCLUDED_DEPTS)
        .exclude(dept__iexact="All")
    )

    if dept and dept.upper() != "ALL":
        qs = qs.filter(dept=dept)

    # ---------------------------------------------------
    # 3. Get Dynamic Department List
    # ---------------------------------------------------
    dept_list = list(
        qs.values_list("dept", flat=True)
        .distinct()
        .order_by("dept")
    )

    # ---------------------------------------------------
    # 4. Department Wise Aggregation
    # ---------------------------------------------------
    agg = (
        qs.values("date_only", "dept")
        .annotate(
            total=Sum("onroll"),
            present=Sum("present"),
            absent=Sum("absent"),
            leave=Sum("leave"),
        )
        .order_by("date_only", "dept")
    )

    dept_map = {}

    for r in agg:

        d = r["date_only"]

        if d not in dept_map:
            dept_map[d] = {}

        dept_name = (r["dept"] or "").strip()

        dept_map[d][dept_name] = {
            "total": r["total"] or 0,
            "present": r["present"] or 0,
            "absent": r["absent"] or 0,
            "leave": r["leave"] or 0,
        }

    # ---------------------------------------------------
    # 5. Daily Totals
    # ---------------------------------------------------
    agg_table = (
        qs.values("date_only")
        .annotate(
            total=Sum("onroll"),
            present=Sum("present"),
            absent=Sum("absent"),
            leave=Sum("leave"),
        )
        .order_by("date_only")
    )

    table_map = {
        r["date_only"]: r
        for r in agg_table
    }

    # ---------------------------------------------------
    # 6. Build Response Data
    # ---------------------------------------------------
    response_data = []

    current_date = start_date

    while current_date <= iter_end:

        row = table_map.get(
            current_date,
            {
                "total": 0,
                "present": 0,
                "absent": 0,
                "leave": 0,
            },
        )

        total = row["total"] or 0
        present = row["present"] or 0
        absent = row["absent"] or 0
        leave = row["leave"] or 0

        # -----------------------------------------------
        # Department Structure
        # -----------------------------------------------
        departments = {}

        for dep in dept_list:

            departments[dep] = dept_map.get(
                current_date,
                {}
            ).get(
                dep,
                {
                    "total": 0,
                    "present": 0,
                    "absent": 0,
                    "leave": 0,
                },
            )

        # -----------------------------------------------
        # Main Row
        # -----------------------------------------------
        response_data.append({

            "unit": dept,

            "date": current_date.strftime("%Y-%m-%d"),

            "total": total,

            "present": present,
            "present_pct": round(
                (present / total) * 100,
                1
            ) if total else 0,

            "absent": absent,
            "absent_pct": round(
                (absent / total) * 100,
                1
            ) if total else 0,

            "leave": leave,
            "leave_pct": round(
                (leave / total) * 100,
                1
            ) if total else 0,

            "departments": departments,
        })

        current_date += timedelta(days=1)

    # ---------------------------------------------------
    # 7. Department Dropdown
    # ---------------------------------------------------
    dropdown_departments = list(
        AttStaff.objects.using("demo")
        .exclude(dept__iexact="All")
        .exclude(dept__in=EXCLUDED_DEPTS)
        .values_list("dept", flat=True)
        .distinct()
        .order_by("dept")
    )

    # ---------------------------------------------------
    # 8. Holiday Data
    # ---------------------------------------------------
    holidays_qs = (
        Holiday.objects.using("main")
        .all()
        .values("dt", "descr")
    )

    holidays_dict = {}

    for h in holidays_qs:

        holidays_dict[
            h["dt"].strftime("%Y-%m-%d")
        ] = h["descr"]

    # ---------------------------------------------------
    # 9. Final JSON Response
    # ---------------------------------------------------
    return JsonResponse({

        "status": True,

        "filters": {
            "department": dept,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        },

        "departments": dropdown_departments,

        "holidays": holidays_dict,

        "count": len(response_data),

        "data": response_data,

    }, safe=False)

def staff_pre(request):
    try:
        date_str = request.GET.get('date')
        dept = request.GET.get('dept', 'ALL')

        # 1. Use the correct Model (StaffAtt) and Database ('demo1')
        staff = StaffAtt.objects.using('demo1').filter(intime__isnull=False)

        # 2. Date Filtering
        if date_str and date_str.strip() != 'undefined':
            try:
                sel_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # --- FIX 1: Changed 'dt__date' to 'date__date' ---
                # The StaffAtt model uses 'date', not 'dt'
                staff = staff.filter(date__date=sel_date)
                
            except ValueError:
                print(f"Date format error: {date_str}")
                return JsonResponse({'error': 'Invalid date format'}, status=400)

        # 3. Dept Filtering
        if dept and dept != 'ALL':
            staff = staff.filter(dept=dept)

        # 4. Get Values
        # --- FIX 2: Changed 'code' to 'code_emb_attendance_fact' ---
        # The StaffAtt model does not have a 'code' field.
        staff = staff.values(
            'code_emb_attendance_fact', 
            'name',
            'dept',
            'img'
        ).distinct().order_by('name')

        data = []
        for emp in staff:
            photo_url = None
            if emp['img']:
                try:
                    # Fix: Safely handle image path
                    filename = os.path.basename(str(emp['img']))
                    photo_url = f"https://app.herofashion.com/staff_images/{filename}"
                except Exception:
                    photo_url = None

            data.append({
                # Map the database field to 'code' so the frontend works
                'code': emp['code_emb_attendance_fact'], 
                'name': emp['name'],
                'dept': emp['dept'],
                'img': photo_url
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        # Debugging: This prints the specific error to your terminal
        print(f"CRITICAL ERROR in staff_pre: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)



def staff_abe(request):
    try:
        # Get parameters from request
        date_str = request.GET.get('date')
        dept_param = request.GET.get('dept', 'ALL') 

        # 1. Use the 'demo' database
        staff_qs = StaffAbsent.objects.using('demo').all()

        # 2. Date Filtering (using 'dt' field from your model)
        if date_str and date_str != 'undefined':
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                # Filter datetime field by date component
                staff_qs = staff_qs.filter(dt__date=target_date)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

        # 3. Department Filtering (using 'wunit' field)
        if dept_param and dept_param != 'ALL':
            staff_qs = staff_qs.filter(wunit=dept_param)

        # 4. Select fields and order
        # We fetch 'wunit' but will rename it to 'dept' in the loop for the frontend
        staff_data = staff_qs.values('code', 'name', 'wunit', 'photo').order_by('name')

        data = []
        for emp in staff_data:
            # Handle Photo URL logic
            photo_url = None
            if emp['photo']:
               
                    filename = os.path.basename(str(emp['photo']))
                    photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None

            data.append({
                'code': emp['code'],
                'name': emp['name'],
                'dept': emp['wunit'], # Mapping wunit -> dept for the JS to read
                'photo': photo_url
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        print(f"Error in staff_abe: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


EXCLUDED_DEPTS = [
    "Maintenance", 
    "Maintanence", 
    "Maintainence", 
    "Maintenanace", 
    "Maintaince",
    "Service"
]

def staff_report_api(request):
    unit = request.GET.get('dept', 'ALL')

    today = date.today()
    date_str = request.GET.get('date', today.isoformat())

    try:
        selected_date = date.fromisoformat(date_str)
    except:
        selected_date = today

    # Get departments
    departments = list(
        AttStaff.objects.using('demo')
        .exclude(dept__in=EXCLUDED_DEPTS)
        .values_list('dept', flat=True)
        .distinct()
        .order_by('dept')
    )

    # Base queryset
    queryset = (
        AttStaff.objects.using('demo')
        .filter(dt__date=selected_date)
        .exclude(dept__in=EXCLUDED_DEPTS)
    )

    if unit != 'ALL':
        queryset = queryset.filter(dept=unit)

    # Aggregation
    unit_data_agg = queryset.values('dept').annotate(
        total=Sum('onroll'),
        present=Sum('present'),
        absent=Sum('absent')
    ).order_by('dept')

    # Build response data
    unit_data_list = []
    for item in unit_data_agg:
        total = item['total'] or 0
        present = item['present'] or 0
        absent = item['absent'] or 0

        unit_data_list.append({
            'unit': item['dept'],
            'total': total,
            'present': present,
            'absent': absent,
            'present_pct': round((present * 100 / total), 2) if total else 0,
            'absent_pct': round((absent * 100 / total), 2) if total else 0,
        })

    response_data = {
        'status': 'success',
        'filters': {
            'department': unit,
            'date': selected_date.isoformat(),
            'date_display': selected_date.strftime('%d-%m-%Y'),
        },
        'departments': departments,
        'data': unit_data_list,
    }

    return JsonResponse(response_data, safe=True) 

def oneday_api(request):
    day_str = request.GET.get('date')

    if day_str:
        try:
            day = datetime.strptime(day_str, "%Y-%m-%d").date()
        except ValueError:
            day = datetime.now().date()
    else:
        day = datetime.now().date()

    dept_filter = request.GET.get('dept', 'ALL')

    # Base queryset
    queryset = AttUnt.objects.using("demo").filter(dt__date=day)

    if dept_filter != 'ALL':
        queryset = queryset.filter(dept__iexact=dept_filter)

    # Aggregation
    units_qs = queryset.values('dept').annotate(
        total=Sum('onroll'),
        present=Sum('present'),
        absent=Sum('absent'),
        le=Sum('le'),
        tlv=Sum('tlv'),
        ntlv=Sum('ntlv'),
    ).order_by('dept')

    unit_data = []

    for row in units_qs:
        total = row['total'] or 0

        def get_pct(part):
            part = part or 0
            return round((part / total) * 100, 2) if total > 0 else 0

        unit_data.append({
            'unit': row['dept'],
            'total': total,
            'present': row['present'] or 0,
            'present_pct': get_pct(row['present']),
            'absent': row['absent'] or 0,
            'absent_pct': get_pct(row['absent']),
            'le': row['le'] or 0,
            'le_pct': get_pct(row['le']),
            'tlv': row['tlv'] or 0,
            'tlv_pct': get_pct(row['tlv']),
            'ntlv': row['ntlv'] or 0,
            'ntlv_pct': get_pct(row['ntlv']),
        })

    response_data = {
        "status": "success",
        "filters": {
            "department": dept_filter,
            "date": day.strftime("%Y-%m-%d"),
            "date_display": day.strftime("%d-%m-%Y"),
        },
        "data": unit_data
    }

    return JsonResponse(response_data, safe=True)


def security_list(request):

    # Codes to exclude
    exclude_codes = [
        '11765', '11762', '11599', '11220',
        '10906', '11734', '11533'
    ]

    qs = ContractSec.objects.using('main').filter(
        cat__iexact="Security"
    ).exclude(
        code__in=exclude_codes   # 🔥 exclude these codes
    ).values(
        'code', 'name', 'date', 'intime', 'outtime'
    )

    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    person = request.GET.get("person")

    # Filter by person
    if person and person.strip():
        qs = qs.filter(code=person.strip())

    # From date
    if date_from and date_from.strip():
        try:
            from_dt = datetime.strptime(date_from.strip(), '%Y-%m-%d').date()
            qs = qs.filter(date__gte=from_dt)
        except ValueError:
            pass

    # To date
    if date_to and date_to.strip():
        try:
            to_dt = datetime.strptime(date_to.strip(), '%Y-%m-%d').date()
            qs = qs.filter(date__lte=to_dt)
        except ValueError:
            pass

    # Order once
    qs = qs.order_by("-date", "intime")

    return JsonResponse(list(qs), safe=False)

def _month_range(start, end):
    """Yield first day of each month between start and end (inclusive)."""
    cur = date(start.year, start.month, 1)
    last = date(end.year, end.month, 1)
    out = []
    while cur <= last:
        out.append(cur)
        # next month
        if cur.month == 12:
            cur = date(cur.year + 1, 1, 1)
        else:
            cur = date(cur.year, cur.month + 1, 1)
    return out

def _fill_months(counts_by_month, months):
    """Ensure every month key exists with 0."""
    return [counts_by_month.get(m, 0) for m in months]

def _to_js_ts(d):
    """Convert Python date to JavaScript timestamp (milliseconds since epoch)."""
    from datetime import datetime, timezone as dt_timezone  # ensure we use stdlib timezone
    dt = datetime(d.year, d.month, 1, tzinfo=dt_timezone.utc)
    return int(dt.timestamp() * 1000)

def _day_range(start, end):
    today = date.today()
    days = []
    cur = start
    while cur <= end and cur <= today:
        days.append(cur)
        cur += timedelta(days=1)
    return days

def _fill_days(counts_by_day, days):
    return [counts_by_day.get(d, 0) for d in days]

def _to_js_ts(d):
    if isinstance(d, (datetime, date)):
        dt = datetime(d.year, d.month, getattr(d, "day", 1), tzinfo=dt_timezone.utc)
        return int(dt.timestamp() * 1000)

    if isinstance(d, str):
        if not any(ch.isdigit() for ch in d):
            return None
        try:
            d = datetime.fromisoformat(d).date()
        except Exception:
            try:
                d = datetime.strptime(d.split(" ")[0], "%Y-%m-%d").date()
            except Exception:
                return None
        dt = datetime(d.year, d.month, d.day, tzinfo=dt_timezone.utc)
        return int(dt.timestamp() * 1000)

    return None

def workforce_trends_api(request):

    rng = (request.GET.get("range") or "1M").upper()
    dept = request.GET.get("dept", "ALL")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    today = date.today()

    # DATE FILTER
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except:
            start = today.replace(day=1)
            end = today
    else:
        if rng == "1M":
            start = today.replace(day=1)
        elif rng == "6M":
            start = today - relativedelta(months=6)
        elif rng == "1Y":
            start = today - relativedelta(years=1)
        elif rng == "MAX":
            first_join = Empjoin.objects.using("main").order_by("joindt").first()
            first_resign = ResignDtls.objects.using("main").order_by("resigndt").first()

            earliest = today
            if first_join: earliest = min(earliest, first_join.joindt.date())
            if first_resign: earliest = min(earliest, first_resign.resigndt.date())

            start = earliest
        else:
            start = today.replace(day=1)

        end = today

    cats = ["TAILOR", "CHECKING", "IRONING", "PACKING"]

    join_qs = Empjoin.objects.using("main").filter(category__in=cats)
    resign_qs = ResignDtls.objects.using("main").filter(category__in=cats)

    join_qs = join_qs.filter(joindt__date__range=[start, end])
    resign_qs = resign_qs.filter(resigndt__date__range=[start, end])

    if dept != "ALL":
        join_qs = join_qs.filter(dept=dept)
        resign_qs = resign_qs.filter(dept=dept)

    # DAILY
    join_days = join_qs.annotate(d=TruncDay("joindt")).values("d").annotate(c=Count("id"))
    resign_days = resign_qs.annotate(d=TruncDay("resigndt")).values("d").annotate(c=Count("slno"))

    days = _day_range(start, end)

    counts_join = {i["d"].date(): i["c"] for i in join_days}
    counts_resign = {i["d"].date(): i["c"] for i in resign_days}

    join_series = _fill_days(counts_join, days)
    resign_series = _fill_days(counts_resign, days)
    x_ts = [_to_js_ts(d) for d in days]

    # CATEGORY TOTALS
    cat_idx = {c: i for i, c in enumerate(cats)}
    cat_join_vals = [0] * len(cats)
    cat_resign_vals = [0] * len(cats)

    for row in join_qs.values("category").annotate(c=Count("id")):
        cat_join_vals[cat_idx[row["category"].upper()]] = row["c"]

    for row in resign_qs.values("category").annotate(c=Count("slno")):
        cat_resign_vals[cat_idx[row["category"].upper()]] = row["c"]

    # DAILY CATEGORY
    daily_join = defaultdict(lambda: defaultdict(int))
    daily_resign = defaultdict(lambda: defaultdict(int))

    for row in join_qs.annotate(d=TruncDay("joindt")).values("d", "category").annotate(c=Count("id")):
        daily_join[row["category"].upper()][row["d"].date()] = row["c"]

    for row in resign_qs.annotate(d=TruncDay("resigndt")).values("d", "category").annotate(c=Count("slno")):
        daily_resign[row["category"].upper()][row["d"].date()] = row["c"]

    daily_join_series = []
    daily_resign_series = []

    for cat in cats:
        daily_join_series.append({
            "name": cat,
            "data": [daily_join[cat].get(d, 0) for d in days]
        })
        daily_resign_series.append({
            "name": cat,
            "data": [daily_resign[cat].get(d, 0) for d in days]
        })

    return JsonResponse({
        "status": "success",
        "filters": {
            "range": rng,
            "department": dept,
            "start_date": start.isoformat(),
            "end_date": end.isoformat()
        },
        "x_ts": x_ts,
        "join_series": join_series,
        "resign_series": resign_series,
        "categories": cats,
        "category_join": cat_join_vals,
        "category_resign": cat_resign_vals,
        "daily_join_series": daily_join_series,
        "daily_resign_series": daily_resign_series
    })

def workforce_unit_trends_api(request):

    rng = (request.GET.get("range") or "1M").upper()
    unit_filter = request.GET.get("unit", "ALL")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    today = date.today()

    # DATE FILTER
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except:
            start = today.replace(day=1)
            end = today
    else:
        if rng == "1M":
            start = today.replace(day=1)
        elif rng == "6M":
            start = today - relativedelta(months=6)
        elif rng == "1Y":
            start = today - relativedelta(years=1)
        elif rng == "MAX":
            first_join = Empjoin.objects.using("main").order_by("joindt").first()
            first_resign = ResignDtls.objects.using("main").order_by("resigndt").first()

            earliest = today
            if first_join: earliest = min(earliest, first_join.joindt.date())
            if first_resign: earliest = min(earliest, first_resign.resigndt.date())

            start = earliest
        else:
            start = today.replace(day=1)

        end = today

    join_qs = Empjoin.objects.using("main").filter(joindt__date__range=[start, end])
    resign_qs = ResignDtls.objects.using("main").filter(resigndt__date__range=[start, end])

    if unit_filter != "ALL":
        join_qs = join_qs.filter(dept=unit_filter)
        resign_qs = resign_qs.filter(dept=unit_filter)

    # UNITS
    units = sorted(list({
        (u or "Unknown").upper()
        for u in list(join_qs.values_list('dept', flat=True)) +
                 list(resign_qs.values_list('dept', flat=True))
    }))

    # DAILY TOTAL
    join_days = join_qs.annotate(d=TruncDay("joindt")).values("d").annotate(c=Count("id"))
    resign_days = resign_qs.annotate(d=TruncDay("resigndt")).values("d").annotate(c=Count("slno"))

    days = _day_range(start, end)

    counts_join = {i["d"].date(): i["c"] for i in join_days}
    counts_resign = {i["d"].date(): i["c"] for i in resign_days}

    join_series = _fill_days(counts_join, days)
    resign_series = _fill_days(counts_resign, days)
    x_ts = [_to_js_ts(d) for d in days]

    # TOTALS
    join_totals = {r['dept'].upper(): r['c'] for r in join_qs.values('dept').annotate(c=Count('id'))}
    resign_totals = {r['dept'].upper(): r['c'] for r in resign_qs.values('dept').annotate(c=Count('slno'))}

    unit_join_vals = [join_totals.get(u, 0) for u in units]
    unit_resign_vals = [resign_totals.get(u, 0) for u in units]

    # DAILY UNIT
    unit_daily_join = defaultdict(lambda: defaultdict(int))
    unit_daily_resign = defaultdict(lambda: defaultdict(int))

    for row in join_qs.annotate(d=TruncDay("joindt")).values("d", "dept").annotate(c=Count("id")):
        unit_daily_join[(row["dept"] or "Unknown").upper()][row["d"].date()] = row["c"]

    for row in resign_qs.annotate(d=TruncDay("resigndt")).values("d", "dept").annotate(c=Count("slno")):
        unit_daily_resign[(row["dept"] or "Unknown").upper()][row["d"].date()] = row["c"]

    unit_daily_join_series = []
    unit_daily_resign_series = []

    for u in units:
        unit_daily_join_series.append({
            "name": u,
            "data": [unit_daily_join[u].get(d, 0) for d in days]
        })
        unit_daily_resign_series.append({
            "name": u,
            "data": [unit_daily_resign[u].get(d, 0) for d in days]
        })

    return JsonResponse({
        "status": "success",
        "filters": {
            "range": rng,
            "unit": unit_filter,
            "start_date": start.isoformat(),
            "end_date": end.isoformat()
        },
        "units": units,
        "x_ts": x_ts,
        "join_series": join_series,
        "resign_series": resign_series,
        "unit_join_vals": unit_join_vals,
        "unit_resign_vals": unit_resign_vals,
        "unit_daily_join_series": unit_daily_join_series,
        "unit_daily_resign_series": unit_daily_resign_series
    })


    # Finance REports API



#  Finance Reports API


def bill(request):
    qs = BillAge.objects.using('demo1')

    # ---------------- FILTERS ----------------
    supplier = request.GET.get('supplier')
    module = request.GET.get('module')
    employee = request.GET.get('employees')
    company = request.GET.get('company')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if supplier and supplier != "ALL":
        qs = qs.filter(suppliers=supplier)

    if module and module != "ALL":
        qs = qs.filter(module=module)

    if employee and employee != "ALL":
        qs = qs.filter(employees=employee)

    if company and company != "ALL":
        qs = qs.filter(company=company)

    if from_date:
        qs = qs.filter(billdate__date__gte=from_date)

    if to_date:
        qs = qs.filter(billdate__date__lte=to_date)

    # ---------------- AGING (DB SIDE) ----------------
    qs = qs.annotate(
        aging=ExpressionWrapper(
            Cast(F('edate'), IntegerField()) -
            Cast(F('billdate'), IntegerField()),
            output_field=IntegerField()
        )
    )

    # ---------------- SORTING ----------------
    qs = qs.order_by('module', '-aging')

    # ⚠️ SAFETY LIMIT (remove only if data < 50k)
    

    # ---------------- SERIALIZE ----------------
    data = []
    for idx, item in enumerate(qs, start=1):
        data.append({
            "no": idx,
            "supplier": item.suppliers,
            "company": item.company,
            "module": item.module,
            "employee": item.employees,
            "billdate": item.billdate,
            "edate": item.edate,
            "aging": item.aging,
            "amount": item.amount,
            "billno": item.billno,
        })

    return JsonResponse({
        "count": len(data),
        "results": data
    }, safe=False)


# --- 2. API View (Handles AJAX Data) ---
def pass_data_api(request):
    # Base Queryset
    qs = BillPass.objects.using('demo1').all()

    # --- NEW: Get unique lists for dropdowns ---
    # This ensures your dropdowns always match the data available
    modules_list = list(BillPass.objects.using('demo1').values_list('module1', flat=True).distinct().order_by('module1'))
    suppliers_list = list(BillPass.objects.using('demo1').values_list('suppliers', flat=True).distinct().order_by('suppliers'))
    incharges_list = list(BillPass.objects.using('demo1').values_list('employees', flat=True).distinct().order_by('employees'))

    # --- FILTERS ---
    module_param = request.GET.get('module1')
    if module_param:
        qs = qs.filter(module1=module_param)

    emp = request.GET.get('employees')
    if emp and emp != 'ALL':
        qs = qs.filter(employees=emp)

    supplier = request.GET.get('supplier')
    if supplier and supplier != 'ALL':
        qs = qs.filter(suppliers=supplier)

    status = request.GET.get('payment_status')
    if status and status != 'ALL':
        qs = qs.filter(paymentstatus__iexact=status)

    # Bill Date Range
    bill_from = request.GET.get('bill_from')
    bill_to = request.GET.get('bill_to')
    if bill_from and bill_to:
        qs = qs.filter(billdate__range=[bill_from, bill_to])
    
    # Payment Date Range (New)
    pay_from = request.GET.get('pay_from')
    pay_to = request.GET.get('pay_to')
    if pay_from and pay_to:
        qs = qs.filter(paymentdate__range=[pay_from, pay_to])

    # --- AGING LOGIC ---
    qs = qs.annotate(
        calculated_aging=Coalesce(F('paymentdate'), Cast(timezone.now(), DateField())) - F('billdate')
    )

    # --- STATS ---
    stats_data = qs.aggregate(
        normal_count=Count('no', filter=Q(calculated_aging__lte=timedelta(days=30))),
        risk_count=Count('no', filter=Q(calculated_aging__gt=timedelta(days=30), calculated_aging__lte=timedelta(days=45))),
        high_risk_count=Count('no', filter=Q(calculated_aging__gt=timedelta(days=45))),
        total_sum=Sum('amount')
    )

    # Risk Category Filter
    risk_cat = request.GET.get('risk_category')
    if risk_cat == 'Normal':
        qs = qs.filter(calculated_aging__lte=timedelta(days=30))
    elif risk_cat == 'Risk':
        qs = qs.filter(calculated_aging__gt=timedelta(days=30), calculated_aging__lte=timedelta(days=45))
    elif risk_cat == 'High Risk':
        qs = qs.filter(calculated_aging__gt=timedelta(days=45))

    # Pagination
    qs = qs.order_by('module', 'billdate')
    paginator = Paginator(qs, 500)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    results = [{
        "id": x.no,
        "billdate": x.billdate,
        "paymentdate": x.paymentdate,
        "calculated_aging": x.calculated_aging.days if x.calculated_aging else 0,
        "paymentstatus": x.paymentstatus,
        "module1": x.module1,
        "suppliers": x.suppliers,
        "employees": x.employees,
        "user_name": "Admin",
        "billno": x.billno,
        "amount": float(x.amount or 0)
    } for x in page_obj]

    return JsonResponse({
        "results": results,
        "modules_list": modules_list,
        "suppliers_list": suppliers_list, # Send to frontend
        "incharges_list": incharges_list, # Send to frontend
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_count": paginator.count,
        "stats": {
            "normal": stats_data['normal_count'] or 0,
            "risk": stats_data['risk_count'] or 0,
            "high_risk": stats_data['high_risk_count'] or 0,
            "total_amount": float(stats_data['total_sum'] or 0)
        }
    })



# --- 2. API View (Handles Data & Filters) ---
def approval_api(request):
    qs = BillMdapprove.objects.using('demo1').all()

    # --- Filters ---
    module = request.GET.get('module')
    supplier = request.GET.get('supplier')
    incharge = request.GET.get('employees') # Receiving Name directly
    md_status = request.GET.get('mdapproval')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if module and module != "ALL":
        qs = qs.filter(lz_module_name1=module) # Note: Checked field name from your code
    
    if supplier and supplier != "ALL":
        qs = qs.filter(lz_supplier=supplier)
        
    if incharge and incharge != "ALL":
        qs = qs.filter(lz_incharge=incharge)

    # --- MD Approval Mapping (Database Level) ---
    md_map_yes = ["1", "yes", "y", "Approved", "approved", "approved by md"]
    md_map_no = ["0", "no", "n", "Not approved", "not approved", "rejected"]

    if md_status:
        if md_status.lower() == "yes":
            qs = qs.filter(mdapproval__in=md_map_yes)
        elif md_status.lower() == "no":
            qs = qs.filter(mdapproval__in=md_map_no)

    # --- Date Filter ---
    if from_date:
        qs = qs.filter(billdate__date__gte=from_date)
    if to_date:
        qs = qs.filter(billdate__date__lte=to_date)

    # --- Sorting ---
    # Incharge ASC -> Bill Date DESC -> E-Date ASC
    qs = qs.order_by('lz_incharge', '-billdate', 'edate')

    # --- Pagination ---
    paginator = Paginator(qs, 500) # 500 records per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # --- Serialization ---
    results = []
    start_idx = page_obj.start_index()

    for idx, item in enumerate(page_obj, start=start_idx):
        # Normalize MD Status
        raw_md = (item.mdapproval or "").lower().strip()
        md_norm = "Yes" if raw_md in md_map_yes else ("No" if raw_md in md_map_no else "-")

        results.append({
            "no": idx,
            "billdate": item.billdate,
            "edate": item.edate,
            "module1": item.lz_module_name1,
            "supplier": item.supplier, # Display name
            "supplier": item.supplier, # Filter name
            "username": item.username,
            "incharge": item.lz_incharge,
            "company": item.company_name,
            "billno": item.billno1,
            "md_status": md_norm,
            "amount": item.ra_billvalue
        })

    return JsonResponse({
        "results": results,
        "total_records": paginator.count,
        "page": page_obj.number,
        "num_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })
# Adjust import based on your app structure
# from .models import BillAge 

def bill_details(request):
    employee = request.GET.get('employee')
    module = request.GET.get('module')
    bucket = request.GET.get('bucket')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search_query = request.GET.get('search')

    bills = BillAge.objects.using('demo1').all()

    if employee:
        if employee == 'Ganesh & Vijaya Kumar':
            bills = bills.filter(employees__in=['Ganesh', 'Vijaya Kumar'])
        else:
            bills = bills.filter(employees__iexact=employee.strip())

    if module and module.lower() != 'none':
        bills = bills.filter(module__iexact=module.strip())

    if from_date and to_date:
        bills = bills.filter(
            Q(billdate__date__range=[from_date, to_date]) |
            Q(edate__date__range=[from_date, to_date])
        )

    if bucket == 'less_3':
        bills = bills.filter(ageing__lt=3)
    elif bucket == 'eq_3':
        bills = bills.filter(ageing=3)
    elif bucket == 'more_3':
        bills = bills.filter(ageing__gt=3)

    if search_query:
        bills = bills.filter(
            Q(suppliers__icontains=search_query) |
            Q(billno__icontains=search_query)
        )

    bills = bills.order_by('-ageing', '-billdate')

    data = list(bills.values())

    return JsonResponse({"bills": data}, safe=False)


def pay_dashboard(request):
    target_employees = ['Vijaya Kumar', 'Accessory', 'Senthil', 'Ganesh']

    qs = BillPass.objects.using('demo1').filter(
        employees__in=target_employees
    )

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        qs = qs.filter(
            Q(billdate__date__range=[from_date, to_date]) |
            Q(edate__date__range=[from_date, to_date])
        )

    today = timezone.now().date()
    date_30_days_ago = today - timedelta(days=30)
    date_45_days_ago = today - timedelta(days=45)

    qs = qs.annotate(
        display_name=Case(
            When(employees__in=['Ganesh', 'Vijaya Kumar'], then=Value('Ganesh & Vijaya Kumar')),
            default=F('employees'),
            output_field=CharField(),
        )
    )

    entry = (
        qs.values('display_name', 'module')
        .annotate(
            total_bills=Count('no'),
            paid_count=Count(Case(When(paymentdate__isnull=False, then=1), output_field=IntegerField())),

            paid_lt_30=Count(Case(When(paymentdate__isnull=False, billdate__gte=date_30_days_ago, then=1), output_field=IntegerField())),
            paid_30_45=Count(Case(When(paymentdate__isnull=False, billdate__lt=date_30_days_ago, billdate__gte=date_45_days_ago, then=1), output_field=IntegerField())),
            paid_gt_45=Count(Case(When(paymentdate__isnull=False, billdate__lt=date_45_days_ago, then=1), output_field=IntegerField())),

            unpaid_count=Count(Case(When(paymentdate__isnull=True, then=1), output_field=IntegerField())),

            unpaid_lt_30=Count(Case(When(paymentdate__isnull=True, billdate__gte=date_30_days_ago, then=1), output_field=IntegerField())),
            unpaid_30_45=Count(Case(When(paymentdate__isnull=True, billdate__lt=date_30_days_ago, billdate__gte=date_45_days_ago, then=1), output_field=IntegerField())),
            unpaid_gt_45=Count(Case(When(paymentdate__isnull=True, billdate__lt=date_45_days_ago, then=1), output_field=IntegerField())),
        )
        .order_by('display_name', 'module')
    )

    return JsonResponse({
        "data": list(entry),
        "from_date": from_date,
        "to_date": to_date
    }, safe=False)


def pay_bill_details(request):
    employee = request.GET.get('employee')
    module = request.GET.get('module')
    status = request.GET.get('status')
    aging = request.GET.get('aging')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search_query = request.GET.get('search')

    bills = BillPass.objects.using('demo1').all()

    today = timezone.now().date()
    date_30_days_ago = today - timedelta(days=30)
    date_45_days_ago = today - timedelta(days=45)

    if employee:
        if employee == 'Ganesh & Vijaya Kumar':
            bills = bills.filter(employees__in=['Ganesh', 'Vijaya Kumar'])
        else:
            bills = bills.filter(employees__iexact=employee.strip())

    if module:
        clean_module = module.strip()
        if clean_module.lower() == 'none' or clean_module == '':
            bills = bills.filter(
                Q(module__isnull=True) |
                Q(module__exact='') |
                Q(module__iexact='None')
            )
        else:
            bills = bills.filter(module__iexact=clean_module)

    if from_date and to_date:
        bills = bills.filter(
            Q(billdate__date__range=[from_date, to_date]) |
            Q(edate__date__range=[from_date, to_date])
        )

    if status == 'paid':
        bills = bills.filter(paymentdate__isnull=False)
    elif status == 'unpaid':
        bills = bills.filter(paymentdate__isnull=True)

    if aging == 'lt30':
        bills = bills.filter(billdate__gte=date_30_days_ago)
    elif aging == '30to45':
        bills = bills.filter(billdate__lt=date_30_days_ago, billdate__gte=date_45_days_ago)
    elif aging == 'gt45':
        bills = bills.filter(billdate__lt=date_45_days_ago)

    if search_query:
        bills = bills.filter(
            Q(suppliers__icontains=search_query) |
            Q(billno__icontains=search_query) |
            Q(billno1__icontains=search_query)
        )

    bills = bills.order_by('-billdate')

    return JsonResponse({
        "bills": list(bills.values())
    }, safe=False)