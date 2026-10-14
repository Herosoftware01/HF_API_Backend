from .models import (
    ViewRepcutPend,
    Repcutpending,
    View_Master_RepcutPend,
    Master_Replace_Cutpend,
    VueRepCutPend,
    VueDyeingRatenew,
    Txorderdetstyles,
    LaySp,
    MasterFinalMistake,
    UnitBundlereport,
    FinalPlans,
    Corarlck1,
    CoraRollcheck,
    RptCutting,
    Empwisesal,
    Employeeworking,
    VueOrdersinhand,
    LaySpreadingLayemployee,
    HrLabourattendence,
    Employeeworking1,
    BitcheckHour,
    StickerHour,
)
from django.http import JsonResponse
import os
import json
from django.db.models import (
    Q,
    Count,
    Sum,
    Max
)
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import OuterRef, Subquery
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.conf import settings
from django.db.models.functions import TruncDate, TruncDay
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import calendar
from collections import OrderedDict

# dt_timezone = timezone.make_aware(timezone.datetime(2012, 1, 1), timezone=timezone.UTC)


@csrf_exempt
def get_lay_sp_data(request):
    if request.method == "GET":
        # 1. Define the FinalPlans Subquery
        # We use .strip() logic conceptually, but in SQL, ensure these match.
        final_plan_qs = FinalPlans.objects.using("app").filter(
            plan_no=OuterRef("plan_no"), job_no=OuterRef("job_no")
        )

        # 2. Define the Employee/Table Subquery
        # Joining based on the table_id and date from the FinalPlans
        # (Since LaySp doesn't have table_id directly)
        emp_qs = LaySpreadingLayemployee.objects.using("app").filter(
            table=OuterRef("final_plans__table_id"), date=OuterRef("date")
        )

        data = (
            LaySp.objects.using("app")
            .annotate(
                # Fetching fields from FinalPlans
                final_plans__pcs=Subquery(final_plan_qs.values("pcs")[:1]),
                final_plans__empid=Subquery(final_plan_qs.values("empid")[:1]),
                final_plans__marker_no=Subquery(final_plan_qs.values("marker_no")[:1]),
                final_plans__lot_no=Subquery(final_plan_qs.values("lot_no")[:1]),
                final_plans__fabric_color=Subquery(
                    final_plan_qs.values("fabric_color")[:1]
                ),
                final_plans__date_time_fp=Subquery(
                    final_plan_qs.values("date_time")[:1]
                ),
                # Fetching Employee Data using the annotated table_id
                emp_name_1=Subquery(emp_qs.values("emp1")[:1]),
                emp_name_2=Subquery(emp_qs.values("emp2")[:1]),
                table_id=Subquery(emp_qs.values("table")[:1]),
            )
            .values(
                "date",
                "timer",
                "plan_no",
                "job_no",
                "roll_no",
                "f_dia",
                "plan_ply",
                "scl_wgt",
                "plan_obwgt",
                "req_wgt",
                "actual_dia",
                "actual_ply",
                "actual_obwgt",
                "end_bit",
                "bal_wgt",
                "debit_kg",
                "roll_time",
                "remarks",
                "bit_wgt",
                "date_time",
                "final_plans__pcs",
                "final_plans__empid",
                "final_plans__marker_no",
                "final_plans__lot_no",
                "final_plans__fabric_color",
                "final_plans__date_time_fp",
                "emp_name_1",
                "emp_name_2",
                "table_id",
            )
        )

        return JsonResponse(list(data), safe=False)


@csrf_exempt
def get_master_final_mistake_data(request):
    if request.method == "GET":
        data = MasterFinalMistake.objects.using("app").all().values()
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
        with connections["app"].cursor() as cursor:
            cursor.execute("EXEC sp_GetBitCheckMistakeSummary")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = []

        for row in rows:
            row_dict = dict(zip(columns, row))

            data.append(
                {
                    "JobNo": row_dict.get("JobNo"),
                    "lotno": row_dict.get("lotno"),
                    "rotiono": row_dict.get("rationo"),
                    "TopBottom_des": row_dict.get("TopBottom_des"),
                    "Name": row_dict.get("Name"),
                    "clrcombo": row_dict.get("clrcombo"),
                    "mistpc": row_dict.get("mistpc"),
                    "Indparts": row_dict.get("Indparts"),
                }
            )

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": False, "error": str(e)})


@csrf_exempt
def cora(request):
    if request.method == "GET":

        # 👇 FIXED HERE
        roll_data = CoraRollcheck.objects.using("app").filter(rlno=OuterRef("roll_id"))

        data = (
            Corarlck1.objects.using("app")
            .annotate(
                jobno=Subquery(roll_data.values("jobno")[:1]),
                colour=Subquery(roll_data.values("colour")[:1]),
                gsm=Subquery(roll_data.values("gsm")[:1]),
                company=Subquery(roll_data.values("company")[:1]),
                fabric=Subquery(roll_data.values("fabricdescription")[:1]),
            )
            .values(
                "sl",
                "dt",
                "roll_id",  # 👈 this is your rlno now
                "hole",
                "setoff",
                "needle_line",
                "oil_line",
                "oil_drops",
                "remark",
                "poovari",
                "yarn_mistake",
                "lycra_cut",
                "yarn_uneven",
                "neps",
                "empid",
                "timer",
                "dia",
                "na_holes",
                "m12",
                "loop_len",
                "image",
                "submit",
                "mach_id",
                "time1",
                "time2",
                # merged fields
                "jobno",
                "colour",
                "gsm",
                "company",
                "fabric",
            )
        )

        return JsonResponse(list(data), safe=False)


@csrf_exempt
def cutdel(request):
    if request.method == "GET":
        try:
            # Get filter values from query params
            jobno = request.GET.get("jobno")
            planno = request.GET.get("planno")
            topbottom = request.GET.get("topbottom")
            lot = request.GET.get("lot")

            # Fetch order numbers from test DB
            orderno_list = list(
                VueOrdersinhand.objects.using("test").values_list("orderno", flat=True)
            )

            # Base queryset
            data = RptCutting.objects.using("demo").filter(jobno__in=orderno_list)

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
                "jobno",
                "dt",
                "planno",
                "sample_descr",
                "per",
                "topbottom_des",
                "lot",
                "rls",
                "fdeldt",
                "plan_kg",
                "mtr",
                "cutdt",
                "tply",
                "aply",
                "ratio_stick_dt",
                "bitcheck_dt",
                "mas_bud_dt",
                "unitdel_dt",
            )

            result = list(data)
            print("Total records:", len(result))

            return JsonResponse(result, safe=False)

        except OSError as e:
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error retrieving cutting data: {str(e)}"}, status=500
            )


# HR Report APIs

@csrf_exempt
def empwisesal(request):
    if request.method == "GET":

        # Step 1: Get working employees with monthly salary
        qs = Empwisesal.objects.using("main").filter(status="working")

        # Step 2: Fetch category mapping from EmployeeWorking
        working_map = {
            emp.code: emp.category
            for emp in Employeeworking.objects.using("main").all()
        }

        data = []

        for rec in qs:
            # Photo URL
            if rec.photo:
                filename = os.path.basename(rec.photo)
                photo_url = f"https://hfapi.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None

            # Get designation from EmployeeWorking
            designation = working_map.get(rec.code)

            data.append(
                {
                    "code": rec.code,
                    "name": rec.name,
                    "dept": rec.dept,
                    "salary": float(rec.salary) if rec.salary else None,
                    "wrkunit": rec.wrkunit,
                    "designation": designation,  # ✅ replaced
                    "monthlysalary": rec.monthlysalary,
                    "accountdetails1": rec.accountdetails1,
                    "photo": photo_url,
                }
            )

        return JsonResponse(data, safe=False)


def labour_attendance_api(request):

    attendance_data = HrLabourattendence.objects.using("demo1").all()

    data = []

    for att in attendance_data:

        emp = Employeeworking1.objects.using("main").filter(code=att.code).first()

        # PHOTO URL
        photo_url = None

        if att.empimage:
            filename = os.path.basename(str(att.empimage))
            photo_url = f"https://hfapi.herofashion.com/staff_images/{filename}"

        data.append(
            {
                # HrLabourattendence ALL COLUMNS
                "unit": att.unit,
                "code": att.code,
                "name": att.name,
                "joindt": att.joindt,
                "dept": att.dept,
                "cat": att.cat,
                "mobile": att.mobile,
                "subcat": att.subcat,
                "shift_contract": att.shift_contract,
                "hostel": att.hostel,
                "gender": att.gender,
                "photo_url": photo_url,
                "status": att.status,
                "date": att.date,
                "intime": att.intime,
                "attendence_status": att.attendence_status,
                "photo": att.photo,
                "status1": att.status1,
                # Employeeworking ALL COLUMNS
                "code": emp.code if emp else None,
                "name": emp.name if emp else None,
                "workunit": emp.workunit if emp else None,
                "category": emp.category if emp else None,
                "type": emp.type if emp else None,
            }
        )

    return JsonResponse(data, safe=False)


def bitcheckhour(request):
    date_str = request.GET.get("date")

    if date_str:
        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse(
                {"error": "Invalid date format. Use YYYY-MM-DD"}, status=400
            )
    else:
        filter_date = timezone.now().date()

    data = BitcheckHour.objects.using("demo").filter(dt__date=filter_date)

    return JsonResponse(list(data.values()), safe=False)


def stickerHour(request):
    data = StickerHour.objects.using("demo").all()

    start_date = request.GET.get("startDate")
    end_date = request.GET.get("endDate")

    if start_date and end_date:
        data = data.filter(dt__range=[start_date, end_date])
    else:
        data = data.filter(dt=date.today())

    return JsonResponse(list(data.values()), safe=False)


def measurement_report(request):
    try:
        ordid = request.GET.get("ordid")
        topbottom_des = request.GET.get("TopBottom_des")

        with connections["demo"].cursor() as cursor:
            cursor.execute(
                "EXEC sp_OrderMeasurementPivot %s, %s", [ordid, topbottom_des]
            )

            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": False, "error": str(e)})


def dyeing_data(request):
    qs = VueDyeingRatenew.objects.using("test").values().order_by("-date")
    data = list(qs)

    # Convert datetime -> date string (YYYY-MM-DD) to avoid timezone shifts on the client
    for item in data:
        dt = item.get("date")
        if dt:
            try:
                # convert to localtime if using timezones
                if getattr(settings, "USE_TZ", False):
                    dt_local = timezone.localtime(dt)
                else:
                    dt_local = dt
                item["date"] = dt_local.strftime("%Y-%m-%d")
            except Exception:
                # fallback: stringify date portion
                try:
                    item["date"] = str(dt).split(" ")[0]
                except Exception:
                    pass

    return JsonResponse(data, safe=False)


def dyeing_order_details(request):
    orderno = request.GET.get("orderno")
    print("orderno==", orderno)

    queryset = Txorderdetstyles.objects.using("test").filter(orderno=orderno).values()

    data = []

    for obj in queryset:
        raw_path = obj.get("mainimagepath")

        if raw_path:
            filename = raw_path.replace("\\", "/").split("/")[-1]
            obj["mainimagepath"] = (
                f"https://hfapi.herofashion.com/Order_images/{filename}"
            )
        else:
            obj["mainimagepath"] = ""

        data.append(obj)

    return JsonResponse(data[0] if data else {}, safe=False)


def GetCuttingDetails(request):
    jobno = request.GET.get("jobno")
    TopBottomDes = request.GET.get("TopBottomDes")

    if not jobno:
        return JsonResponse({"error": "jobno parameter is required"}, status=400)

    if not TopBottomDes:
        return JsonResponse({"error": "TopBottomDes parameter is required"}, status=400)

    with connections["demo"].cursor() as cursor:
        cursor.execute(
            "EXEC sp_GetCuttingDetails @jobno=%s, @TopBottomDes=%s",
            [jobno, TopBottomDes],
        )

        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse(data, safe=False)


def GetAprodDetails(request):
    jobno = request.GET.get("jobno")

    if not jobno:
        return JsonResponse({"error": "jobno parameter is required"}, status=400)

    with connections["demo"].cursor() as cursor:
        cursor.execute("EXEC sp_GetAprodDetails @jobno=%s", [jobno])

        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse(data, safe=False)


def RepCutPending(request):
    jobno = request.GET.get("jobno")
    queryset = VueRepCutPend.objects.using("demo").all()

    if jobno:
        queryset = queryset.filter(jobno=jobno)

    data = list(queryset.values())

    return JsonResponse(data, safe=False)


def RepcutPending(request):
    jobno = request.GET.get("jobno")
    queryset = ViewRepcutPend.objects.using("demo").all()

    if jobno:
        queryset = queryset.filter(jobno=jobno).order_by("slno")

    data = list(queryset.values())

    return JsonResponse(data, safe=False)


@csrf_exempt
def Cutting_Replace_Pending(request):

    if request.method == "GET":

        jobno = request.GET.get("jobno")
        topbottom = request.GET.get("topbottom")
        styleid = request.GET.get("styleid")
        
        queryset = Repcutpending.objects.using("demo").all()

        if jobno:
            queryset = queryset.filter(jobno=jobno)

        if topbottom:
            queryset = queryset.filter(topbottom=topbottom)

        if styleid:
            queryset = queryset.filter(styleid=styleid)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == "POST":

        data = json.loads(request.body)

        for item in data:

            exists = (
                Repcutpending.objects.using("demo")
                .filter(
                    jobno=item["jobno"],
                    styleid=item["styleid"],
                    size=item["size"],
                    topbottom=item["topbottom"],
                    parts=item["parts"],
                )
                .exists()
            )

            if not exists:
                Repcutpending.objects.using("demo").create(
                    jobno=item["jobno"],
                    styleid=item["styleid"],
                    size=item["size"],
                    topbottom=item["topbottom"],
                    parts=item["parts"],
                    weight=item["weight"],
                    average=item["average"],
                    percentage=item["percentage"],
                    totalavg=item["totalavg"],
                )

        return JsonResponse({"message": "Records created"}, status=201)

    elif request.method == "PUT":

        data = json.loads(request.body)

        for item in data:

            Repcutpending.objects.using("demo").filter(slno=item["slno"]).update(
                weight=item["weight"],
                average=item["average"],
                percentage=item["percentage"],
                totalavg=item["totalavg"],
            )

        return JsonResponse({"message": "Record updated"})

    return JsonResponse({"message": "Method not allowed"}, status=405)


def Master_Repcut(request):

    queryset = View_Master_RepcutPend.objects.using("demo").all()
    data = list(queryset.values())
    return JsonResponse(data, safe=False)


@csrf_exempt
def Master_Repcut_Details(request):

    if request.method == "GET":

        styleid = request.GET.get("styleid")
        queryset = Master_Replace_Cutpend.objects.using("demo").all()

        if styleid:
            queryset = queryset.filter(styleid=styleid)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == "POST":

        data = json.loads(request.body)

        for item in data:

            exists = (
                Master_Replace_Cutpend.objects.using("demo")
                .filter(
                    styleid=item["styleid"],
                    size=item["size"],
                    topbottom=item["topbottom"],
                    parts=item["parts"],
                )
                .exists()
            )

            if not exists:
                Master_Replace_Cutpend.objects.using("demo").create(
                    styleid=item["styleid"],
                    size=item["size"],
                    topbottom=item["topbottom"],
                    parts=item["parts"],
                    weight=item["weight"],
                    average=item["average"],
                    percentage=item["percentage"],
                    grandtotal=item["grandtotal"],
                    totalavg=item["totalavg"],
                    partavg=item["partavg"],
                    omspcs=item["omspcs"],
                    omsexcess=item["omsexcess"],
                )

        return JsonResponse({"message": "Records created"}, status=201)

    elif request.method == "PUT":

        data = json.loads(request.body)

        for item in data:

            Master_Replace_Cutpend.objects.using("demo").filter(
                slno=item["slno"]
            ).update(
                weight=item["weight"],
                parts=item["parts"],
                size=item["size"],
                topbottom=item["topbottom"],
                average=item["average"],
                percentage=item["percentage"],
                grandtotal=item["grandtotal"],
                totalavg=item["totalavg"],
                partavg=item["partavg"],
                omspcs=item["omspcs"],
                omsexcess=item["omsexcess"],
            )

        return JsonResponse({"message": "Record updated"})

    elif request.method == "DELETE":

        data = json.loads(request.body)

        for item in data:
            Master_Replace_Cutpend.objects.using("demo").filter(
                slno=item["slno"]
            ).delete()

        return JsonResponse({"message": "Records deleted successfully"})

