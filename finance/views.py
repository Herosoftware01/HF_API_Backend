from .models import ( 
    VueHoldwage,
    Holdwagepaid,
    BillAge,
    BillMdapprove,
    BillPass)
from django.db.models import (
    F,
    Q,
    IntegerField,
    DateField,
    Case,
    When,
    Value,
    CharField,
    Count,
    Sum
)
from django.http import JsonResponse
import os
import json
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import OuterRef, Subquery
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.conf import settings
from django.db.models.functions import TruncDate, TruncDay, Cast, Coalesce
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.db.models.expressions import ExpressionWrapper
from django.core.paginator import Paginator
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def holdwage_report(request):
    if request.method == "GET":
        try:
            code = request.GET.get("code")

            qs = VueHoldwage.objects.using("demo")

            if code:
                qs = qs.filter(code=code)

            data = list(qs.values())

            return JsonResponse(data, safe=False)
        except OSError as e:
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error retrieving holdwage data: {str(e)}"}, status=500
            )



@csrf_exempt
def holdwagepaid_api(request):

    # ✅ GET
    if request.method == "GET":
        entry_no = request.GET.get("entry_no")
        aadhar = request.GET.get("aadhar")

        try:
            # 👉 Single record
            if entry_no:
                obj = Holdwagepaid.objects.using("demo").get(entry_no=entry_no)
                return JsonResponse(
                    {
                        "entry_no": obj.entry_no,
                        "dt": obj.dt.strftime("%Y-%m-%d"),
                        "aadhar_no": obj.aadhar_no,
                        "code": obj.code,
                        "emp_name": obj.emp_name,
                        "t_period": obj.t_period,
                        "paid_amt": float(obj.paid_amt),
                        "remarks": obj.remarks,
                    }
                )

            # 👉 Filter by Aadhaar
            if aadhar:
                data = list(
                    Holdwagepaid.objects.using("demo").filter(aadhar_no=aadhar).values()
                )
                return JsonResponse(data, safe=False)

            # 👉 All records
            data = list(Holdwagepaid.objects.using("demo").all().values())
            return JsonResponse(data, safe=False)

        except Holdwagepaid.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        except OSError as e:
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error retrieving holdwage data: {str(e)}"}, status=500
            )

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
            exists = (
                Holdwagepaid.objects.using("demo")
                .filter(
                    aadhar_no=aadhar, t_period__iexact=t_period  # 🔥 case-insensitive
                )
                .exists()
            )

            if exists:
                return JsonResponse(
                    {"error": f"Already paid for {t_period}"}, status=400
                )

            # 🔢 Auto entry_no
            last = Holdwagepaid.objects.using("demo").order_by("-entry_no").first()
            next_entry = (last.entry_no + 1) if last else 1

            obj = Holdwagepaid.objects.using("demo").create(
                entry_no=next_entry,
                dt=dt,
                aadhar_no=aadhar,
                code=code,
                emp_name=data.get("emp_name"),
                t_period=t_period,  # ✅ save normalized
                paid_amt=paid_amt,
                remarks=data.get("remarks"),
            )

            return JsonResponse({"message": "Created", "entry_no": obj.entry_no})

        except OSError as e:
            print("DATABASE ERROR:", e)
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=400)
    # ✅ PUT (UPDATE)
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            entry_no = data.get("entry_no")

            obj = Holdwagepaid.objects.using("demo").get(entry_no=entry_no)

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
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # ✅ DELETE
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            entry_no = data.get("entry_no")

            obj = Holdwagepaid.objects.using("demo").get(entry_no=entry_no)
            obj.delete()

            return JsonResponse({"message": "Deleted successfully"})

        except Holdwagepaid.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        except OSError as e:
            return JsonResponse(
                {"error": f"Database connection error: {str(e)}"}, status=500
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


#  Finance Reports API


def bill(request):
    qs = BillAge.objects.using("demo1")

    # ---------------- FILTERS ----------------
    supplier = request.GET.get("supplier")
    module = request.GET.get("module")
    employee = request.GET.get("employees")
    company = request.GET.get("company")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

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
            Cast(F("edate"), IntegerField()) - Cast(F("billdate"), IntegerField()),
            output_field=IntegerField(),
        )
    )

    # ---------------- SORTING ----------------
    qs = qs.order_by("module", "-aging")

    # ⚠️ SAFETY LIMIT (remove only if data < 50k)

    # ---------------- SERIALIZE ----------------
    data = []
    for idx, item in enumerate(qs, start=1):
        data.append(
            {
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
            }
        )

    return JsonResponse({"count": len(data), "results": data}, safe=False)


# --- 2. API View (Handles AJAX Data) ---
def pass_data_api(request):
    # Base Queryset
    qs = BillPass.objects.using("demo1").all()

    # --- NEW: Get unique lists for dropdowns ---
    # This ensures your dropdowns always match the data available
    modules_list = list(
        BillPass.objects.using("demo1")
        .values_list("module1", flat=True)
        .distinct()
        .order_by("module1")
    )
    suppliers_list = list(
        BillPass.objects.using("demo1")
        .values_list("suppliers", flat=True)
        .distinct()
        .order_by("suppliers")
    )
    incharges_list = list(
        BillPass.objects.using("demo1")
        .values_list("employees", flat=True)
        .distinct()
        .order_by("employees")
    )

    # --- FILTERS ---
    module_param = request.GET.get("module1")
    if module_param:
        qs = qs.filter(module1=module_param)

    emp = request.GET.get("employees")
    if emp and emp != "ALL":
        qs = qs.filter(employees=emp)

    supplier = request.GET.get("supplier")
    if supplier and supplier != "ALL":
        qs = qs.filter(suppliers=supplier)

    status = request.GET.get("payment_status")
    if status and status != "ALL":
        qs = qs.filter(paymentstatus__iexact=status)

    # Bill Date Range
    bill_from = request.GET.get("bill_from")
    bill_to = request.GET.get("bill_to")
    if bill_from and bill_to:
        qs = qs.filter(billdate__range=[bill_from, bill_to])

    # Payment Date Range (New)
    pay_from = request.GET.get("pay_from")
    pay_to = request.GET.get("pay_to")
    if pay_from and pay_to:
        qs = qs.filter(paymentdate__range=[pay_from, pay_to])

    # --- AGING LOGIC ---
    qs = qs.annotate(
        calculated_aging=Coalesce(F("paymentdate"), Cast(timezone.now(), DateField()))
        - F("billdate")
    )

    # --- STATS ---
    stats_data = qs.aggregate(
        normal_count=Count("no", filter=Q(calculated_aging__lte=timedelta(days=30))),
        risk_count=Count(
            "no",
            filter=Q(
                calculated_aging__gt=timedelta(days=30),
                calculated_aging__lte=timedelta(days=45),
            ),
        ),
        high_risk_count=Count("no", filter=Q(calculated_aging__gt=timedelta(days=45))),
        total_sum=Sum("amount"),
    )

    # Risk Category Filter
    risk_cat = request.GET.get("risk_category")
    if risk_cat == "Normal":
        qs = qs.filter(calculated_aging__lte=timedelta(days=30))
    elif risk_cat == "Risk":
        qs = qs.filter(
            calculated_aging__gt=timedelta(days=30),
            calculated_aging__lte=timedelta(days=45),
        )
    elif risk_cat == "High Risk":
        qs = qs.filter(calculated_aging__gt=timedelta(days=45))

    # Pagination
    qs = qs.order_by("module", "billdate")
    paginator = Paginator(qs, 500)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    results = [
        {
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
            "amount": float(x.amount or 0),
        }
        for x in page_obj
    ]

    return JsonResponse(
        {
            "results": results,
            "modules_list": modules_list,
            "suppliers_list": suppliers_list,  # Send to frontend
            "incharges_list": incharges_list,  # Send to frontend
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
            "total_count": paginator.count,
            "stats": {
                "normal": stats_data["normal_count"] or 0,
                "risk": stats_data["risk_count"] or 0,
                "high_risk": stats_data["high_risk_count"] or 0,
                "total_amount": float(stats_data["total_sum"] or 0),
            },
        }
    )


# --- 2. API View (Handles Data & Filters) ---
def approval_api(request):
    qs = BillMdapprove.objects.using("demo1").all()

    # --- Filters ---
    module = request.GET.get("module")
    supplier = request.GET.get("supplier")
    incharge = request.GET.get("lz_incharge")  # Receiving Name directly
    md_status = request.GET.get("mdapproval")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if module and module != "ALL":
        qs = qs.filter(
            lz_module_name1=module
        )  # Note: Checked field name from your code

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
    qs = qs.order_by("lz_incharge", "-billdate", "edate")

    # --- Pagination ---
    paginator = Paginator(qs, 500)  # 500 records per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # --- Serialization ---
    results = []
    start_idx = page_obj.start_index()

    for idx, item in enumerate(page_obj, start=start_idx):
        # Normalize MD Status
        raw_md = (item.mdapproval or "").lower().strip()
        md_norm = (
            "Yes" if raw_md in md_map_yes else ("No" if raw_md in md_map_no else "-")
        )

        results.append(
            {
                "no": idx,
                "billdate": item.billdate,
                "edate": item.edate,
                "module1": item.lz_module_name1,
                "supplier": item.supplier,  # Display name
                "supplier": item.supplier,  # Filter name
                "username": item.username,
                "incharge": item.lz_incharge,
                "company": item.company_name,
                "billno": item.billno1,
                "md_status": md_norm,
                "amount": item.ra_billvalue,
            }
        )

    return JsonResponse(
        {
            "results": results,
            "total_records": paginator.count,
            "page": page_obj.number,
            "num_pages": paginator.num_pages,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        }
    )


# Adjust import based on your app structure
# from .models import BillAge


def bill_dashboard(request):
    target_employees = ["Vijaya Kumar", "Accessory", "Senthil", "Ganesh"]

    qs = BillAge.objects.using("demo1").filter(employees__in=target_employees)

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date and to_date:
        qs = qs.filter(
            Q(billdate__date__range=[from_date, to_date])
            | Q(edate__date__range=[from_date, to_date])
        )

    qs = qs.annotate(
        display_name=Case(
            When(
                employees__in=["Ganesh", "Vijaya Kumar"],
                then=Value("Ganesh & Vijaya Kumar"),
            ),
            default=F("employees"),
            output_field=CharField(),
        )
    )

    entry = list(
        qs.values("display_name", "module")
        .annotate(
            total_bills=Count("no"),
            less_3=Count(Case(When(ageing__lt=3, then=1), output_field=IntegerField())),
            eq_3=Count(Case(When(ageing=3, then=1), output_field=IntegerField())),
            more_3=Count(Case(When(ageing__gt=3, then=1), output_field=IntegerField())),
        )
        .order_by("display_name", "module")
    )

    return JsonResponse(
        {"status": "success", "from_date": from_date, "to_date": to_date, "data": entry}
    )


def bill_details(request):
    employee = request.GET.get("employee")
    module = request.GET.get("module")
    bucket = request.GET.get("bucket")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    search_query = request.GET.get("search")

    bills = BillAge.objects.using("demo1").all()

    if employee:
        if employee == "Ganesh & Vijaya Kumar":
            bills = bills.filter(employees__in=["Ganesh", "Vijaya Kumar"])
        else:
            bills = bills.filter(employees__iexact=employee.strip())

    if module and module.lower() != "none":
        bills = bills.filter(module__iexact=module.strip())

    if from_date and to_date:
        bills = bills.filter(
            Q(billdate__date__range=[from_date, to_date])
            | Q(edate__date__range=[from_date, to_date])
        )

    if bucket == "less_3":
        bills = bills.filter(ageing__lt=3)
    elif bucket == "eq_3":
        bills = bills.filter(ageing=3)
    elif bucket == "more_3":
        bills = bills.filter(ageing__gt=3)

    if search_query:
        bills = bills.filter(
            Q(suppliers__icontains=search_query) | Q(billno__icontains=search_query)
        )

    bills = bills.order_by("-ageing", "-billdate")

    data = list(bills.values())

    return JsonResponse({"bills": data}, safe=False)


def pay_dashboard(request):
    target_employees = ["Vijaya Kumar", "Accessory", "Senthil", "Ganesh"]

    qs = BillPass.objects.using("demo1").filter(employees__in=target_employees)

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date and to_date:
        qs = qs.filter(
            Q(billdate__date__range=[from_date, to_date])
            | Q(edate__date__range=[from_date, to_date])
        )

    today = timezone.now().date()
    date_30_days_ago = today - timedelta(days=30)
    date_45_days_ago = today - timedelta(days=45)

    qs = qs.annotate(
        display_name=Case(
            When(
                employees__in=["Ganesh", "Vijaya Kumar"],
                then=Value("Ganesh & Vijaya Kumar"),
            ),
            default=F("employees"),
            output_field=CharField(),
        )
    )

    entry = (
        qs.values("display_name", "module")
        .annotate(
            total_bills=Count("no"),
            paid_count=Count(
                Case(
                    When(paymentdate__isnull=False, then=1), output_field=IntegerField()
                )
            ),
            paid_lt_30=Count(
                Case(
                    When(
                        paymentdate__isnull=False,
                        billdate__gte=date_30_days_ago,
                        then=1,
                    ),
                    output_field=IntegerField(),
                )
            ),
            paid_30_45=Count(
                Case(
                    When(
                        paymentdate__isnull=False,
                        billdate__lt=date_30_days_ago,
                        billdate__gte=date_45_days_ago,
                        then=1,
                    ),
                    output_field=IntegerField(),
                )
            ),
            paid_gt_45=Count(
                Case(
                    When(
                        paymentdate__isnull=False, billdate__lt=date_45_days_ago, then=1
                    ),
                    output_field=IntegerField(),
                )
            ),
            unpaid_count=Count(
                Case(
                    When(paymentdate__isnull=True, then=1), output_field=IntegerField()
                )
            ),
            unpaid_lt_30=Count(
                Case(
                    When(
                        paymentdate__isnull=True, billdate__gte=date_30_days_ago, then=1
                    ),
                    output_field=IntegerField(),
                )
            ),
            unpaid_30_45=Count(
                Case(
                    When(
                        paymentdate__isnull=True,
                        billdate__lt=date_30_days_ago,
                        billdate__gte=date_45_days_ago,
                        then=1,
                    ),
                    output_field=IntegerField(),
                )
            ),
            unpaid_gt_45=Count(
                Case(
                    When(
                        paymentdate__isnull=True, billdate__lt=date_45_days_ago, then=1
                    ),
                    output_field=IntegerField(),
                )
            ),
        )
        .order_by("display_name", "module")
    )

    return JsonResponse(
        {"data": list(entry), "from_date": from_date, "to_date": to_date}, safe=False
    )


def pay_bill_details(request):
    employee = request.GET.get("employee")
    module = request.GET.get("module")
    status = request.GET.get("status")
    aging = request.GET.get("aging")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    search_query = request.GET.get("search")

    bills = BillPass.objects.using("demo1").all()

    today = timezone.now().date()
    date_30_days_ago = today - timedelta(days=30)
    date_45_days_ago = today - timedelta(days=45)

    if employee:
        if employee == "Ganesh & Vijaya Kumar":
            bills = bills.filter(employees__in=["Ganesh", "Vijaya Kumar"])
        else:
            bills = bills.filter(employees__iexact=employee.strip())

    if module:
        clean_module = module.strip()
        if clean_module.lower() == "none" or clean_module == "":
            bills = bills.filter(
                Q(module__isnull=True) | Q(module__exact="") | Q(module__iexact="None")
            )
        else:
            bills = bills.filter(module__iexact=clean_module)

    if from_date and to_date:
        bills = bills.filter(
            Q(billdate__date__range=[from_date, to_date])
            | Q(edate__date__range=[from_date, to_date])
        )

    if status == "paid":
        bills = bills.filter(paymentdate__isnull=False)
    elif status == "unpaid":
        bills = bills.filter(paymentdate__isnull=True)

    if aging == "lt30":
        bills = bills.filter(billdate__gte=date_30_days_ago)
    elif aging == "30to45":
        bills = bills.filter(
            billdate__lt=date_30_days_ago, billdate__gte=date_45_days_ago
        )
    elif aging == "gt45":
        bills = bills.filter(billdate__lt=date_45_days_ago)

    if search_query:
        bills = bills.filter(
            Q(suppliers__icontains=search_query)
            | Q(billno__icontains=search_query)
            | Q(billno1__icontains=search_query)
        )

    bills = bills.order_by("-billdate")

    return JsonResponse({"bills": list(bills.values())}, safe=False)