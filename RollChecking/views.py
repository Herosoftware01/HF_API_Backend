from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.db import IntegrityError, transaction
import json
import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from datetime import date
from django.db.models import OuterRef, Subquery

from .models import RollEmployee, RollEmpDetails, RollChecking, RollCheckingDetails, MasterMistakes

def Roll_Employee(request):

    queryset = RollEmployee.objects.using('main').all().values()
    data = list(queryset)

    for obj in data:
        raw_path = obj.get('photo')

        if raw_path:
            filename = raw_path.replace('\\', '/').split('/')[-1]
            obj['photo'] = f"https://hfapi.herofashion.com/staff_images/{filename}"
        else:
            obj['photo'] = ""

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def Roll_Employee_Details(request):

    if request.method == "GET":
        today = date.today()

        queryset = RollEmpDetails.objects.using("default").filter(
            date__date=today
        )

        machine_id = request.GET.get("machine_id")
        if machine_id:
            queryset = queryset.filter(machine_id=machine_id)

        latest = queryset.filter(
            machine_id=OuterRef("machine_id")
        ).order_by("-date", "-sl")

        data = list(
            queryset.filter(
                sl=Subquery(latest.values("sl")[:1])
            ).values(
                "sl", "machine_id", "c_code", "c_name",
                "h_code", "h_name", "date"
            ).order_by("machine_id")
        )

        for row in data:
            if row["date"]:
                row["date"] = row["date"].isoformat()

        return JsonResponse(data, safe=False)

    try:
        body = json.loads(request.body)

        machine_id = body.get("machine_id")
        c_code = body.get("c_code")

        if not machine_id or not c_code:
            return JsonResponse({
                "error": "machine_id and checker_code are required"
            }, status=400)

        today = date.today()

        exists = RollEmpDetails.objects.using("default").filter(
            machine_id=machine_id,
            c_code=c_code,
            date__date=today
        ).exists()

        if exists:
            return JsonResponse({
                "message": "Machine and checker already exist today",
                "saved": False
            }, status=409)

        obj = RollEmpDetails.objects.using("default").create(
            machine_id=machine_id,
            c_code=c_code,
            c_name=body.get("c_name"),
            h_code=body.get("h_code") or None,
            h_name=body.get("h_name") or None
        )

        return JsonResponse({
            "message": "Saved successfully",
            "saved": True,
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON body"
        }, status=400)


def Roll_Checking(request):
    rlno = request.GET.get('rlno')
    dc = request.GET.get('dc')
    colour = request.GET.get('colour')

    queryset = RollChecking.objects.using('demo').all()

    if rlno and dc and colour:

        # Check RollCheckingDetails table
        detail = RollCheckingDetails.objects.using("default").filter(rlno=rlno.strip(), dcno=dc.strip(), colour=colour.strip()).first()

        if detail:
            if detail.submit == 1:
                status = "Roll Already Scanning"
            else:
                status = "Roll Checking Progress"
        else:
            status = "Ready to Roll Checking"

        queryset = queryset.filter(rlno=rlno.strip(), dc=dc.strip(), colour=colour.strip())
        data = list(queryset.order_by("-dt").values())

        return JsonResponse({
            "status": status,
            "data": data
        })

    elif rlno:
        queryset = queryset.filter(rlno=rlno.strip())

        if not queryset.exists():
            return JsonResponse({
                "status": "Roll Number Not Found",
                "data": []
            })
        
        data = list(queryset.order_by("-dt").values('rlno', 'dc', 'colour'))

    else:
        data = list(queryset.order_by("-dt").values())

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT"])
def RollChecking_Details(request):

    if request.method == "GET":
        rlno = request.GET.get("rlno")

        queryset = RollCheckingDetails.objects.using("default").all()

        if rlno:
            queryset = queryset.filter(rlno=rlno.strip())

        data = list(queryset.values().order_by("-date"))

        for obj in data:
            if obj.get("date"):
                obj["date"] = obj["date"].isoformat()

        return JsonResponse(data, safe=False)

    body = json.loads(request.body)

    if request.method == "POST":
        rlno = body.get("rlno")
        dcno = body.get("dcno")
        colour = body.get("colour")

        if not rlno or not dcno or not colour:
            return JsonResponse(
                {"error": "rlno, dcno, and colour are required"},
                status=400
            )

        if RollCheckingDetails.objects.using("default").filter(
            rlno=rlno, dcno=dcno, colour=colour
        ).exists():
            return JsonResponse(
                {"error": "Roll number already exists"},
                status=409
            )

        fields = [
            'empid_checker', 'checker_name', 'empid_helper', 'helper_name', 'mach_id', 'jobno', 
            'colour', 'dcno', 'dia', 'lotno', 'type', 'fabric', 'weight', 'meter', 'gsm', 'a_gsm', 'f_dia', 
            'remark', 'timer', 'points', 'image', 'submit', 'submit_date', 'oil', 'stain', 'holes', 
            'setoff', 'needle_line', 'compact_kadi', 'sidepin_hole', 'streaks', 'roll_joint', 'yarn_mistake', 
            'patches', 'gsm_hole', 'print_mistake'
        ]

        values = {
            field: body[field]
            for field in fields
            if field in body
        }

        try:
            with transaction.atomic(using="default"):
                obj = RollCheckingDetails.objects.using("default").create(
                    rlno=rlno,
                    **values
                )
        except IntegrityError:
            return JsonResponse(
                {"error": "This rlno, dcno and colour combination already exists"},
                status=409
            )

        return JsonResponse({
            "message": "Created successfully",
            "rlno": obj.rlno
        }, status=201)

    if request.method == "PUT":
        rlno = body.get("rlno")
        dcno = body.get("dcno")
        colour = body.get("colour")

        if not rlno or not dcno or not colour:
            return JsonResponse(
                {"error": "rlno, dcno, and colour are required"},
                status=400
            )

        try:
            obj = RollCheckingDetails.objects.using("default").get(
                rlno=rlno, dcno=dcno, colour=colour
            )
        except RollCheckingDetails.DoesNotExist:
            return JsonResponse(
                {"error": "Roll number not found"},
                status=404
            )

        fields = [
            'oil', 'stain', 'holes', 'setoff', 'needle_line',
            'compact_kadi', 'sidepin_hole', 'streaks', 'roll_joint',
            'yarn_mistake', 'patches', 'gsm_hole', 'print_mistake',
            'remark', 'timer', 'submit', 'submit_date', 'points',
            'a_gsm', 'f_dia', 'meter'
        ]

        for field in fields:
            if field in body:
                setattr(obj, field, body[field])

        obj.save(using="default", update_fields=[
            field for field in fields if field in body
        ] or ["submit"])

        return JsonResponse({
            "message": "Updated successfully",
            "rlno": obj.rlno,
            "dcno": obj.dcno,
            "colour": obj.colour
        })

    
@csrf_exempt
@require_POST
def RollChecking_ImageUpload(request):
    rlno = request.POST.get('rlno')
    dcno = request.POST.get('dcno')
    colour = request.POST.get('colour')
    image = request.FILES.get('c_img')

    if not rlno or not dcno or not colour or not image:
        return JsonResponse(
            {'error': 'rlno, dcno, colour, and c_img are required'},
            status=400
        )

    try:
        obj = RollCheckingDetails.objects.using('default').get(rlno=rlno, dcno=dcno, colour=colour)
    except RollCheckingDetails.DoesNotExist:
        return JsonResponse({'error': 'Roll number not found'}, status=404)
    except RollCheckingDetails.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple matching records found'}, status=409)

    os.makedirs(settings.ROLL_CHECKING_IMAGES_ROOT, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{os.path.basename(image.name)}"
    filepath = os.path.join(settings.ROLL_CHECKING_IMAGES_ROOT, filename)

    with open(filepath, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    obj.c_img = f"{settings.ROLL_CHECKING_IMAGES_URL}{filename}"
    obj.save(using='default', update_fields=['c_img'])

    return JsonResponse({
        'message': 'Image uploaded successfully',
        'rlno': obj.rlno,
        'dcno': obj.dcno,
        'colour': obj.colour,
        'c_img': obj.c_img
    }, status=200)


def MasterMistakesList(request):
    type = request.GET.get('type')
    queryset = MasterMistakes.objects.all()

    if type:
        queryset = queryset.filter(type=type)

    data = list(queryset.values())
    return JsonResponse(data, safe=False)
