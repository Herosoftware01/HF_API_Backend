from .models import VueHoldwage, Empwisesal, Employeeworking, Holdwagepaid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from datetime import datetime

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