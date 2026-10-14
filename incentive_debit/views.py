from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Staffodtls,Empwisesal,IncdebStatus,Employeeworking,IncdebPurpose,IncdebUsers
from rest_framework import status
from django.conf import settings
import os
import json
from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny



@api_view(['GET'])
def staff_full_details(request):
    qs = (
        Staffodtls.objects.using('main')
        .filter(status='Working')
        .exclude(Designation__in=[
            'Security',
            'Warehouse Associate',
            'Driver'
        ])
        .select_related('code')
    )

    data = []
    for rec in qs:
        staff = rec.code  # OneToOne FK → Staffdtls

        # PHOTO CONVERSION (unchanged)
        if getattr(staff, 'photo', None):
            filename = os.path.basename(staff.photo)
            if getattr(settings, 'DEBUG', False):
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None
        else:
            photo_url = None

        data.append({
            "code": staff.code,
            "name": staff.name,
            "photo": photo_url,
            "dept": rec.dept,
            "designation": rec.Designation,
            "status": rec.status
        })

    return Response(data)



@api_view(['GET'])
def empwise_salary_api(request):

    category_subquery = Employeeworking.objects.using('main').filter(
        code=OuterRef('code')
    ).values('category')[:1]

    qs = (
        Empwisesal.objects.using('main')
        .filter(status='Working')
        .annotate(
            final_designation=Coalesce(
                F('designation'),
                Subquery(category_subquery)
            )
        )
    )

    data = []

    for rec in qs:
        # PHOTO LOGIC (UNCHANGED)
        if rec.photo:
            filename = os.path.basename(rec.photo)
            if settings.DEBUG:
                photo_url = f"https://app.herofashion.com/staff_images/{filename}"
            else:
                photo_url = None
        else:
            photo_url = None

        data.append({
            "code": rec.code,
            "name": rec.name,
            "dept": rec.dept,
            "status": rec.status,
            "designation": rec.final_designation,
            "photo": photo_url
        })

    return Response(data)




@api_view(['GET', 'POST','DELETE'])
def incdeb_list_create(request):

    # 🔹 GET (LIST / FILTER)
    if request.method == 'GET':
        qs = IncdebStatus.objects.using('demo').all()

        code = request.GET.get('code')
        status_val = request.GET.get('status')

        if code:
            qs = qs.filter(code=code)
        if status_val:
            qs = qs.filter(status=status_val)

        data = []
        for rec in qs:
            data.append({
                "req_id": rec.req_id,
                "req_dt": rec.req_dt,
                "req_type": rec.req_type,
                "code": rec.code,
                "name": rec.name,
                "dept_unit": rec.dept_unit,
                "design_category": rec.design_category,
                "purpose": rec.purpose,
                "amt": rec.amt,
                "reason": rec.reason,
                "status": rec.status,
                "status_dt": rec.status_dt,
                "jobno": rec.jobno
            })

        return Response(data, status=status.HTTP_200_OK)

    # 🔹 POST (CREATE)
    elif request.method == 'POST':
        data = request.data

        rec = IncdebStatus.objects.using('demo').create(
            req_dt=data.get('req_dt'),
            req_type=data.get('req_type'),
            code=data.get('code'),
            name=data.get('name'),
            dept_unit=data.get('dept_unit'),
            design_category=data.get('design_category'),
            purpose=data.get('purpose'),
            amt=data.get('amt'),
            reason=data.get('reason'),
            status=data.get('status'),
            status_dt=data.get('status_dt'),
            jobno=data.get('jobno')
        )


    return Response(
        {"message": "Record created", "req_id": rec.req_id},
            status=status.HTTP_201_CREATED
        )


@api_view(['PUT', 'DELETE'])
def incdeb_update(request, req_id):
    # Fetch the record from the correct database
    rec = get_object_or_404(
        IncdebStatus.objects.using('demo'), 
        req_id=req_id
    )

    # --- HANDLE DELETE ---
    if request.method == 'DELETE':
        rec.delete(using='demo')
        return Response(
            {"message": "Record deleted successfully"}, 
            status=status.HTTP_200_OK
        )

    # --- HANDLE UPDATE (PUT) ---
    elif request.method == 'PUT':
        data = request.data
        
        # Update fields only if they exist in the request data
        rec.req_dt = data.get('req_dt', rec.req_dt)
        rec.req_type = data.get('req_type', rec.req_type)
        rec.code = data.get('code', rec.code)
        rec.name = data.get('name', rec.name)
        rec.dept_unit = data.get('dept_unit', rec.dept_unit)
        rec.design_category = data.get('design_category', rec.design_category)
        rec.purpose = data.get('purpose', rec.purpose)
        rec.amt = data.get('amt', rec.amt)
        rec.reason = data.get('reason', rec.reason)
        rec.status = data.get('status', rec.status)
        rec.status_dt = data.get('status_dt', rec.status_dt)
        rec.jobno = data.get('jobno', rec.jobno)


        rec.save(using='demo')
        
        return Response(
            {"message": "Record updated"}, 
            status=status.HTTP_200_OK
        )

def incdeb_status_api(request):
    qs = IncdebStatus.objects.using('demo').all()

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    dept_unit = request.GET.get("dept_unit")

    if from_date:
        qs = qs.filter(req_dt__gte=from_date)
    if to_date:
        qs = qs.filter(req_dt__lte=to_date)
    if dept_unit:
        qs = qs.filter(dept_unit__icontains=dept_unit)

    data = list(qs.values())
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def incdeb_purpose_api(request):
    """Handles Listing (GET) and Creating (POST) Purposes"""
    
    # 🔹 GET LIST
    if request.method == 'GET':
        qs = IncdebPurpose.objects.using('demo').all()
        
        ste = request.GET.get("ste")
        type_val = request.GET.get("type")

        if ste:
            qs = qs.filter(ste__iexact=ste)
        if type_val:
            qs = qs.filter(type__iexact=type_val)

        data = list(qs.values())
        return JsonResponse(data, safe=False)

    # 🔹 POST CREATE
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            rec = IncdebPurpose.objects.using('demo').create(
                ste=body.get('ste'),
                type=body.get('type'),
                purpose=body.get('purpose')
            )
            return JsonResponse({"message": "Record created", "id": rec.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def incdeb_purpose_detail_api(request, pk):
    """Handles Deleting a specific Purpose by ID"""
    
    try:
        # Fetch object ensuring we use the correct database
        rec = get_object_or_404(IncdebPurpose.objects.using('demo'), pk=pk)
        rec.delete()
        return JsonResponse({"message": "Purpose deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ==========================================
#  USER VIEWS
# ==========================================

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def incdeb_users_api(request):
    """Handles Listing (GET) and Creating (POST) Users"""

    # 🔹 GET LIST
    if request.method == 'GET':
        qs = IncdebUsers.objects.using('demo').all()
        username = request.GET.get("username")
        user = IncdebUsers.objects.using('demo').first()


        if username:
            qs = qs.filter(username__iexact=username)

        if user:
            if user.app_n not in [1, None]:
                return JsonResponse({"error": "Invalid user"}, status=403)
            
        data = list(qs.values())
        return JsonResponse(data, safe=False)
        

    # 🔹 POST CREATE
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            rec = IncdebUsers.objects.using('demo').create(
                username=body.get('username'),
                password=body.get('password'),
                screen_per=body.get('role') ,
                app_n=body.get('app_n')
            )
            return JsonResponse({"message": "User created", "id": rec.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def incdeb_users_detail_api(request, pk):
    """Handles Deleting a specific User by ID"""

    try:
        rec = get_object_or_404(IncdebUsers.objects.using('demo'), pk=pk)
        rec.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)