from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.db import IntegrityError, transaction
import json
import os, re
import uuid
from django.conf import settings
from django.http import JsonResponse
from datetime import date
from django.db.models import OuterRef, Subquery

from .models import RollEmployee, RollEmpDetails, RollChecking, RollCheckingDetails, RollCheckingDefect, MasterMistakes, DefectCategory, DefectMaster

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
            'remark', 'timer', 'image', 'submit', 'submit_date'
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
            'remark', 'timer', 'submit', 'submit_date',
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


@csrf_exempt
def RollChecking_Defect(request):

    if request.method == 'GET':
        rlno = request.GET.get('rlno')
        colour = request.GET.get('colour')
        dcno = request.GET.get('dcno')

        qs = RollCheckingDefect.objects.all()

        if rlno:
            qs = qs.filter(rlno=rlno)
        if colour:
            qs = qs.filter(colour=colour)
        if dcno:
            qs = qs.filter(dcno=dcno)

        return JsonResponse(list(qs.values()), safe=False)

    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if request.method == 'POST':
        try:
            obj = RollCheckingDefect.objects.create(
                rlno=data['rlno'],
                colour=data.get('colour'),
                dcno=data.get('dcno'),
                defectcode=data['defectcode'],
                defectname=data['defectname'],
                subname=data.get('subname'),
                points=data.get('points'),
                holes=data.get('holes'),
                inches=data.get('inches'),
                counts=data.get('counts'),
                tcounts=data.get('tcounts'),
                tpoints=data.get('tpoints'),
                entrytype=data.get('entrytype')
            )
            return JsonResponse({'message': 'Roll checking defect created successfully', 'sl': obj.sl}, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e.args[0]}'}, status=400)

    if request.method == 'PUT':
        sl = data.get('sl') or request.GET.get('sl')

        if not sl:
            return JsonResponse({'error': 'sl is required'}, status=400)

        try:
            obj = RollCheckingDefect.objects.get(sl=sl)
        except RollCheckingDefect.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)

        for field in [
            'rlno', 'colour', 'dcno', 'defectcode', 'inches', 'counts', 'entrytype',
            'defectname', 'subname', 'points', 'tpoints', 'tcounts', 'holes'
        ]:
            if field in data:
                setattr(obj, field, data[field])

        try:
            obj.save()
            return JsonResponse({'message': 'Updated'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    if request.method == 'DELETE':
        sl = data.get('sl') or request.GET.get('sl')

        if not sl:
            return JsonResponse({'error': 'sl is required'}, status=400)

        deleted, _ = RollCheckingDefect.objects.filter(sl=sl).delete()

        if not deleted:
            return JsonResponse({'error': 'Record not found'}, status=404)

        return JsonResponse({'message': 'Deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def MasterMistakesList(request):
    type = request.GET.get('type')
    queryset = MasterMistakes.objects.all()

    if type:
        queryset = queryset.filter(type=type)

    data = list(queryset.values())
    return JsonResponse(data, safe=False)


def read_body(request):
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        return request.POST

    try:
        return json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return {}


def category_dict(obj):
    return {
        'categoryid': obj.categoryid,
        'category_code': obj.category_code,
        'category_name': obj.category_name,
        'date': obj.date.isoformat() if obj.date else None,
        'log': obj.log,
    }


def defect_dict(request, obj):
    return {
        'defectid': obj.defectid,
        'categoryid': obj.categoryid_id,
        'category_name': obj.categoryid.category_name,
        'defect_code': obj.defect_code,
        'defectname': obj.defectname,
        'defectserial': obj.defectserial,
        'defect_subname': obj.defect_subname,
        'defect_type': obj.defect_type,
        'topbottom': obj.topbottom,
        'tamil': obj.tamil,
        'hindi': obj.hindi,
        'image': (
            request.build_absolute_uri(obj.image)
            if obj.image and obj.image.startswith(('http://', 'https://'))
            else obj.image
        ),
        'date': obj.date.isoformat() if obj.date else None,
        'log': obj.log,
    }


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
def Defect_Category(request):
    if request.method == 'GET':
        queryset = DefectCategory.objects.all().order_by('categoryid')
        categoryid = request.GET.get('categoryid')

        if categoryid:
            queryset = queryset.filter(categoryid=categoryid)

        return JsonResponse(
            [category_dict(obj) for obj in queryset],
            safe=False
        )

    body = read_body(request)
    categoryid = body.get('categoryid') or request.GET.get('categoryid')

    if request.method == 'POST':
        code = body.get('category_code')
        name = body.get('category_name')

        if not code or not name:
            return JsonResponse(
                {'error': 'category_code and category_name are required'},
                status=400
            )

        try:
            obj = DefectCategory.objects.create(
                category_code=code,
                category_name=name,
                log=body.get('log')
            )
        except IntegrityError:
            return JsonResponse(
                {'error': 'Category code already exists'},
                status=409
            )

        return JsonResponse(category_dict(obj), status=201)

    if not categoryid:
        return JsonResponse({'error': 'categoryid is required'}, status=400)

    try:
        obj = DefectCategory.objects.get(categoryid=categoryid)
    except DefectCategory.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    if request.method == 'PUT':
        for field in ['category_code', 'category_name', 'log']:
            if field in body:
                setattr(obj, field, body[field])

        try:
            obj.save()
        except IntegrityError:
            return JsonResponse(
                {'error': 'Category code already exists'},
                status=409
            )

        return JsonResponse(category_dict(obj))

    try:
        obj.delete()
    except IntegrityError:
        return JsonResponse(
            {'error': 'Cannot delete category while defects reference it'},
            status=409
        )

    return JsonResponse({'message': 'Category deleted successfully'})


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
def Defect_Master(request):
    if request.method == 'GET':
        queryset = DefectMaster.objects.select_related(
            'categoryid'
        ).all().order_by('defectid')

        for param, field in [
            ('defectid', 'defectid'),
            ('categoryid', 'categoryid_id'),
            ('defect_code', 'defect_code'),
        ]:
            value = request.GET.get(param)
            if value:
                queryset = queryset.filter(**{field: value})

        return JsonResponse(
            [defect_dict(request, obj) for obj in queryset],
            safe=False
        )

    body = read_body(request)

    if request.method == 'POST':
        if not body.get('categoryid') or not body.get('defectname'):
            return JsonResponse(
                {'error': 'categoryid and defectname are required'},
                status=400
            )

        try:
            with transaction.atomic():
                category = DefectCategory.objects.get(
                    categoryid=body['categoryid']
                )

                # Empty dropdown = automatically generate next defect code.
                selected_code = (body.get('defect_code') or '').strip()

                if selected_code:
                    # Reuse an existing code belonging to this category.
                    code_exists = DefectMaster.objects.filter(
                        categoryid=category,
                        defect_code=selected_code
                    ).exists()

                    if not code_exists:
                        return JsonResponse(
                            {
                                'error': (
                                    'Selected defect code does not exist '
                                    'in this category'
                                )
                            },
                            status=400
                        )

                    defect_code = selected_code

                else:
                    # Find the highest numeric code for this category.
                    prefix = f'{category.category_code}.'
                    existing_codes = (
                        DefectMaster.objects
                        .filter(categoryid=category)
                        .values_list('defect_code', flat=True)
                        .distinct()
                    )

                    highest_number = 0

                    for code in existing_codes:
                        match = re.fullmatch(
                            re.escape(prefix) + r'(\d+)',
                            code or ''
                        )

                        if match:
                            highest_number = max(
                                highest_number,
                                int(match.group(1))
                            )

                    defect_code = (
                        f'{category.category_code}.{highest_number + 1:02d}'
                    )

                # Find the first unused serial for this code.
                used_serials = set(
                    DefectMaster.objects
                    .filter(defect_code=defect_code)
                    .values_list('defectserial', flat=True)
                )

                defectserial = next(
                    (
                        letter for letter in 'abcdefghijklmnopqrstuvwxyz'
                        if letter not in used_serials
                    ),
                    None
                )

                if defectserial is None:
                    return JsonResponse(
                        {'error': 'All serials a-z are already used'},
                        status=400
                    )

                obj = DefectMaster.objects.create(
                    categoryid=category,
                    defect_code=defect_code,
                    defectname=body['defectname'].strip(),
                    defectserial=defectserial,
                    defect_subname=body.get('defect_subname') or None,
                    defect_type=body.get('defect_type') or None,
                    topbottom=body.get('topbottom') or None,
                    tamil=body.get('tamil') or None,
                    hindi=body.get('hindi') or None,
                    log=body.get('log') or None,
                )

        except DefectCategory.DoesNotExist:
            return JsonResponse(
                {'error': 'Category not found'},
                status=404
            )

        except IntegrityError:
            return JsonResponse(
                {
                    'error': (
                        'Defect code and serial already exist. '
                        'Please retry.'
                    )
                },
                status=409
            )

        return JsonResponse(defect_dict(request, obj), status=201)

    if request.method == 'PUT':
        for field in [
            'defect_code', 'defectname', 'defectserial',
            'defect_subname', 'defect_type', 'topbottom',
            'tamil', 'hindi', 'log'
        ]:
            if field in body:
                setattr(obj, field, body[field])

        if 'categoryid' in body:
            try:
                obj.categoryid = DefectCategory.objects.get(
                    categoryid=body['categoryid']
                )
            except DefectCategory.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        try:
            obj.save()
        except IntegrityError:
            return JsonResponse(
                {'error': 'Defect code and serial already exist'},
                status=409
            )

        return JsonResponse(defect_dict(request, obj))

    obj.delete()
    return JsonResponse({'message': 'Defect deleted successfully'})


@csrf_exempt
@require_POST
def Defect_ImageUpload(request):
    defectid = request.POST.get('defectid')
    image = request.FILES.get('image')

    if not defectid or not image:
        return JsonResponse(
            {'error': 'defectid and image are required'},
            status=400
        )

    try:
        obj = DefectMaster.objects.get(defectid=defectid)
    except DefectMaster.DoesNotExist:
        return JsonResponse({'error': 'Defect not found'}, status=404)

    # Basic image-type validation
    if image.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
        return JsonResponse(
            {'error': 'Only JPEG, PNG, and WEBP images are allowed'},
            status=400
        )

    os.makedirs(settings.DEFECT_IMAGES_ROOT, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{os.path.basename(image.name)}"
    filepath = os.path.join(settings.DEFECT_IMAGES_ROOT, filename)

    try:
        with open(filepath, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
    except OSError:
        return JsonResponse(
            {'error': 'Unable to save image to server folder'},
            status=500
        )

    obj.image = f"{settings.DEFECT_IMAGES_URL}{filename}"
    obj.save(update_fields=['image'])

    return JsonResponse({
        'message': 'Image uploaded successfully',
        'defectid': obj.defectid,
        'image': obj.image
    })