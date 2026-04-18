from .models import VueHoldwage, Empwisesal, Employeeworking, Holdwagepaid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from datetime import datetime
from .models import LaySp, MasterFinalMistake, UnitBundlereport, FinalPlans,Corarlck1,CoraRollcheck,AttUnt,EmbAbsetnt,Holiday,LabAtt
from django.db.models import Q
from django.db.models import F
from django.db import connections
from django.db.models import OuterRef, Subquery
from django.db.models import Sum
from datetime import datetime, timedelta
import os

@csrf_exempt
def holdwage_report(request):
    if request.method == 'GET':
        code = request.GET.get("code")

        qs = VueHoldwage.objects.using('demo')

        if code:
            qs = qs.filter(code=code)

        data = list(qs.values())

        return JsonResponse(data, safe=False)
    
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
    

#HR Report




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
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"

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
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"

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