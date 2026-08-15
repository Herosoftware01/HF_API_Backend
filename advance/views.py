from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json
from .models import  Adreq, Empwisesal,Employeeworking,HrWrkdtlsnew,RptCut002,Monthlysaltime
from django.db import connections
import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from email.mime.image import MIMEImage
import threading
from django.core.cache import cache
from django.utils.timezone import now
from datetime import datetime

@csrf_exempt
def request_advance(request):

    # ================= GET =================
    if request.method == 'GET':
        empid = request.GET.get('empid')
        smon  = request.GET.get('smon')
        syear = request.GET.get('syear')

        qs = Adreq.objects.using('mssql1').all().order_by('-entryno')

        if empid:
            qs = qs.filter(empid=empid)
        if smon:
            qs = qs.filter(smon=smon)
        if syear:
            qs = qs.filter(syear=syear)

        return JsonResponse(list(qs.values()), safe=False)

    # ================= POST =================
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            empid = data.get('empid')
            smon  = data.get('smon')
            syear = data.get('syear')

            # The validation check that blocked multiple submissions has been removed here.

            last = Adreq.objects.using('mssql1').aggregate(Max('entryno'))['entryno__max'] or 0

            obj = Adreq.objects.using('mssql1').create(
                entryno=last + 1,
                dt=data.get('dt'),
                empid=empid,
                amt=data.get('amt'),
                remarks=data.get('remarks', '')[:80],
                smon=smon,
                syear=syear,
                elig=data.get('elig'),
                status=data.get('status'),
                comments=data.get('comments', '')[:150],
                mail_sent=False,  # initially false
            )

            # A successful write must always produce a response.  Without this,
            # Django raises a debug error after inserting the record and callers
            # receive its HTML error page instead of a success payload.
            return JsonResponse({"message": "Created", "id": obj.entryno}, status=201)

            # # ================= SEND EMAIL =================
            # try:
            #     subject = "🧾 New Advance Request Submitted"

            #     message = f"""
            #         Employee ID : {empid}
            #         Month       : {smon}-{syear}
            #         Amount      : ₹{data.get('amt')}
            #         Eligible    : ₹{data.get('elig')}
            #         Remarks     : {data.get('remarks')}
            #         """

            #     send_mail(
            #         subject,
            #         message,
            #         settings.EMAIL_HOST_USER,   # from email
            #         ['hfautomation2026@gmail.com','design@herofashion.com'],    # 👈 change to real email
            #         fail_silently=False,
            #     )

            #     # ✅ update mail_sent = True
            #     obj.mail_sent = True
            #     obj.save()

            # return JsonResponse({"message": "Created", "id": obj.entryno})

            # except Exception as mail_error:
            #     print("MAIL ERROR:", str(mail_error))

                # Note: If email fails, the advance record is still created in the DB above.
                # Returning a 500 here might confuse the frontend since the save was actually successful.
                # You might want to return 200 with a warning message instead in production.
                # return JsonResponse({"error": str(mail_error)}, status=500)

        except Exception:
            # Log the detailed exception server-side; do not return database or
            # configuration details to the browser.
            import logging
            logging.getLogger(__name__).exception("Unable to create advance request")
            return JsonResponse({"error": "Unable to save the advance request."}, status=500)

    # ================= DELETE =================
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            obj_id = data.get('id')

            obj = Adreq.objects.using('mssql1').get(entryno=obj_id)  # ✅ FIXED
            obj.delete()

            return JsonResponse({"message": "Deleted"}, status=200)

        except Adreq.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        except Exception as e:
            print("DELETE REQUEST ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# views.py — Add this new view
# ==============================
# 🔥 BACKGROUND EMAIL SENDER
# ==============================
def send_mail_async(email):
    try:
        email.send()
        print("✅ Email sent in background")
    except Exception as e:
        print("❌ Email failed:", str(e))


# ==============================
# 🔥 EMPLOYEE CACHE (5 mins)
# ==============================
def get_employee_data(api_url):
    cache_key = "employee_data"

    data = cache.get(cache_key)
    if not data:
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, timeout=300)  # 5 mins
        except Exception as e:
            print("⚠️ API ERROR:", str(e))
            data = []

    return data


# ==============================
# 🔥 FAST LOOKUP
# ==============================
def get_employee_map(employees):
    return {str(emp.get('code')).strip(): emp for emp in employees}


# @csrf_exempt
# def send_advance_mail(request):
#     if request.method == 'POST':
#         try:
#             print("\n=====  FAST MAIL API START =====")

#             data = json.loads(request.body)
#             entryno = data.get('entryno')

#             # OPTIMIZED DB QUERY
#             obj = Adreq.objects.using('demo').only('empid', 'amt', 'remarks').get(entryno=entryno)

#             # API CACHE
#             api_url = "https://app.herofashion.com/incentive/api/emp/"
#             employees = get_employee_data(api_url)
#             emp_map = get_employee_map(employees)

#             emp = emp_map.get(str(obj.empid).strip(), {})
#             emp_name = emp.get('name', 'Not Found')
#             emp_dept = emp.get('dept', 'Not Found')
#             photo_name = emp.get('photo')

#             #  EMAIL OBJECT
#             email = EmailMultiAlternatives(
#                 "🧾 New Advance Request Submitted",
#                 "",
#                 settings.EMAIL_HOST_USER,
#                 ['hfautomation2026@gmail.com',"design@herofashion.com"],
#             )

#             # IMAGE ATTACH (optional)
#             photo_cid = None
#             if photo_name:
#                 try:
#                     filename = os.path.basename(photo_name)
#                     local_path = os.path.join(settings.STAFF_IMAGES_ROOT, filename)

#                     if os.path.exists(local_path):
#                         with open(local_path, "rb") as f:
#                             img = MIMEImage(f.read())
#                             photo_cid = f"photo_{obj.empid}"
#                             img.add_header("Content-ID", f"<{photo_cid}>")
#                             email.attach(img)
#                 except Exception as e:
#                     print("⚠️ Image error:", str(e))

#             # TEMPLATE
#             html_content = render_to_string('mail.html', {
#                 'name': emp_name,
#                 'dept': emp_dept,
#                 'empid': obj.empid,
#                 'amt': obj.amt,
#                 'remarks': obj.remarks,
#                 'approve_url': f"https://hf.herofashion.com/approve?entryno={entryno}&status=Y",
#                 'reject_url': f"https://hf.herofashion.com/approve?entryno={entryno}&status=N",
#                 'photo_cid': photo_cid
#             })

#             text_content = strip_tags(html_content)

#             email.body = text_content
#             email.attach_alternative(html_content, "text/html")

#             # BACKGROUND SEND
#             threading.Thread(target=send_mail_async, args=(email,)).start()

#             return JsonResponse({"message": "Mail queued (fast 🚀)"})

#         except Exception as e:
#             print("❌ ERROR:", str(e))
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request"}, status=400)
        

@csrf_exempt
def send_approval_mail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entryno = data.get('entryno')
            status = data.get('status')

            # FAST DB
            obj = Adreq.objects.using('mssql1').only('empid', 'amt', 'remarks').get(entryno=entryno)

            # CACHE API
            api_url = "https://app.herofashion.com/incentive/api/emp/"
            employees = get_employee_data(api_url)
            emp_map = get_employee_map(employees)

            emp = emp_map.get(str(obj.empid).strip(), {})
            emp_name = emp.get('name', 'Not Found')
            emp_dept = emp.get('dept', 'Not Found')

            status_text = "APPROVED ✅" if status == "Y" else "REJECTED ❌"

            subject = f"Advance Request {status_text}"

            html_content = render_to_string('app.html', {
                'name': emp_name,
                'dept': emp_dept,
                'empid': obj.empid,
                'amt': obj.amt,
                'remarks': obj.remarks,
                'status': status_text,
                'entryno': obj.entryno,
            })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                ['hfautomation2026@gmail.com',"design@herofashion.com"],
            )

            email.attach_alternative(html_content, "text/html")

            # BACKGROUND SEND
            threading.Thread(target=send_mail_async, args=(email,)).start()

            return JsonResponse({"message": "Approval mail queued "})
        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def ad_approve(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            obj_id = data.get('id')

            obj = Adreq.objects.using('mssql1').get(entryno=obj_id)
            obj.status = data.get('status')
            obj.status_dt = data.get('status_dt')
            obj.save()

            

            return JsonResponse({"message": "Updated"}, status=200)

        except Adreq.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def get_eligibleamt(request):
    try:
        emp_id = request.GET.get('id')
        mon = request.GET.get('mon')
        year = request.GET.get('year')

        if not emp_id or not mon or not year:
            return JsonResponse({"error": "id, mon and year are required"}, status=400)

        with connections['main'].cursor() as cursor:
            # ✅ Pass all 3 parameters to the stored procedure
            cursor.execute(
                "EXEC GetEligibleamt @id=%s, @mon=%s, @year=%s",
                [emp_id, mon, year]
            )
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            data.append({
                "shift":   row_dict.get("shift"),
                "Wage":    row_dict.get("Wage"),
                "salary":  row_dict.get("salary"),
                "Eligible": row_dict.get("Eligible"),
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": False, "error": str(e)}, status=500)
    



@csrf_exempt
def empwisesal(request):
    if request.method == 'GET':
        
        # Step 1: Get working employees with monthly salary
        qs = Empwisesal.objects.using('main').filter(
            monthlysalary='Y',
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
                photo_url = f"https://hfapi.herofashion.com/staff_images/{filename}"
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
                "mobile": rec.mobile,
                "accountdetails": rec.accountdetails,
                "ifscno": rec.ifscno,
                "designation": designation,   # ✅ replaced
                "monthlysalary": rec.monthlysalary,
                "photo": photo_url
            })

        return JsonResponse(data, safe=False)
    

@csrf_exempt
def state(request):
    if request.method == 'GET':
        data = Adreq.objects.using('mssql1').all().order_by('-entryno')

        # 🔍 Get query params
        empid = request.GET.get('empid')
        status = request.GET.get('status')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # 👤 EmpID filter
        if empid:
            data = data.filter(empid=empid)

        # 📌 Status filter
        if status == 'P':
            data = data.filter(status__isnull=True)
        elif status:
            data = data.filter(status=status)


        # 📅 Date range filter
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d")
                to_date = datetime.strptime(to_date, "%Y-%m-%d")
                data = data.filter(dt__range=[from_date, to_date])
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        

        current_year = datetime.now().year
        data = data.filter(dt__year=current_year)

        # 🔄 Convert queryset to list
        result = list(data.values())

        return JsonResponse(result, safe=False)


@csrf_exempt
def monthlysaltime_api(request, id=None):

    # ================= GET =================
    if request.method == "GET":
        if id:
            try:
                obj = Monthlysaltime.objects.using('demo').get(id=id)

                data = {
                    "id": obj.id,
                    "modulename": obj.modulename,
                    "dayofweek": obj.dayofweek,
                    "isactive": obj.isactive,
                    "starttime": obj.starttime.strftime("%H:%M:%S") if obj.starttime else None,
                    "endtime": obj.endtime.strftime("%H:%M:%S") if obj.endtime else None,
                    "updatedat": obj.updatedat.strftime("%Y-%m-%d %H:%M:%S") if obj.updatedat else None,
                }

                return JsonResponse({
                    "status": True,
                    "data": data
                })

            except Monthlysaltime.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "Record not found"
                }, status=404)

        else:
            data = []

            for obj in Monthlysaltime.objects.using('demo').all().order_by("id"):
                data.append({
                    "id": obj.id,
                    "modulename": obj.modulename,
                    "dayofweek": obj.dayofweek,
                    "isactive": obj.isactive,
                    "starttime": obj.starttime.strftime("%H:%M:%S") if obj.starttime else None,
                    "endtime": obj.endtime.strftime("%H:%M:%S") if obj.endtime else None,
                    "updatedat": obj.updatedat.strftime("%Y-%m-%d %H:%M:%S") if obj.updatedat else None,
                })

            return JsonResponse({
                "status": True,
                "data": data
            })

    # ================= POST =================
    elif request.method == "POST":
        try:
            body = json.loads(request.body)

            obj = Monthlysaltime.objects.using('demo').create(
                modulename=body.get("modulename"),
                dayofweek=body.get("dayofweek"),
                isactive=body.get("isactive", True),
                starttime=body.get("starttime"),
                endtime=body.get("endtime"),
                updatedat=datetime.now()
            )

            return JsonResponse({
                "status": True,
                "message": "Created Successfully",
                "id": obj.id
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    # ================= PUT =================
    elif request.method == "PUT":
        if not id:
            return JsonResponse({
                "status": False,
                "message": "ID is required"
            }, status=400)

        try:
            obj = Monthlysaltime.objects.using('demo').get(id=id)
            body = json.loads(request.body)

            obj.modulename = body.get("modulename", obj.modulename)
            obj.dayofweek = body.get("dayofweek", obj.dayofweek)
            obj.isactive = body.get("isactive", obj.isactive)

            if body.get("starttime"):
                obj.starttime = body.get("starttime")

            if body.get("endtime"):
                obj.endtime = body.get("endtime")

            obj.updatedat = datetime.now()
            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Updated Successfully"
            })

        except Monthlysaltime.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Record not found"
            }, status=404)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    # ================= DELETE =================
    elif request.method == "DELETE":
        if not id:
            return JsonResponse({
                "status": False,
                "message": "ID is required"
            }, status=400)

        try:
            obj = Monthlysaltime.objects.using('demo').get(id=id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "Deleted Successfully"
            })

        except Monthlysaltime.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Record not found"
            }, status=404)

    return JsonResponse({
        "status": False,
        "message": "Method Not Allowed"
    }, status=405)

# google contact API
def google_contact_api(request):
    if request.method == 'GET':
        # Fetch Google Contacts
        contacts = HrWrkdtlsnew.objects.using('main').all()
        contacts_data = []
        for contact in contacts:
            contacts_data.append({
                "photo_url": contact.photo_url,
                "code": contact.code,
                "name": contact.name,
                "dept": contact.dept,
                "category": contact.category,
                "phone": contact.mobile,
                "sc": contact.sc,
                "joindt": contact.joindt,
            })
        return JsonResponse(contacts_data, safe=False)



def new_pros(request):
    rec = request.GET.get('rec')
    with connections['demo'].cursor() as cursor:
        cursor.execute(
            """
            EXEC usp_GetProductionDetails
                @rec=%s               
            """,
            [rec]
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    result = [
        dict(zip(columns, row))
        for row in rows
    ]
    return JsonResponse({
        "status": "success",
        "data": result
    })
    

def fabric_cutting(request):

    if request.method == 'GET':
        data = RptCut002.objects.using('demo').all()

        # Get query params
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # --- 1. Today Filter (default if no dates passed) ---
        if not from_date and not to_date:
            today = now().date()
            data = data.filter(dt=today)

        # --- 2. Date Range Filter ---
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
                to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

                data = data.filter(dt__range=[from_date, to_date])

            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        return JsonResponse(list(data.values()), safe=False)



        
