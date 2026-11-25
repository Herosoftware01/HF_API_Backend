from django.shortcuts import render
from django.http import JsonResponse
from . models import ViewFabricInwardSummary,ViewCuttingOcr,MaunualStock
from django.db import connections
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


#Fabric Summary API

def get_fabric_summary(request):
    # Model field names (change here if your view/table uses different ones)
    JOB, COLOR, FABRIC = 'jobno', 'clr_name', 'fab_name'

    def clean(value, default_label):
        value = (value or '').strip()
        return None if value in ('', default_label) else value

    # Accept both the new and old parameter names from the frontend
    selected = {
        JOB: clean(request.GET.get('jobno'), 'All Jobs'),
        COLOR: clean(request.GET.get('clr_name') or request.GET.get('color'), 'All Colors'),
        FABRIC: clean(request.GET.get('fab_name') or request.GET.get('fabric'), 'All Fabrics'),
    }
    filters = {k: v for k, v in selected.items() if v}

    try:
        base = ViewFabricInwardSummary.objects.using('demo').all()

        def apply(qs, skip=None):
            for field, value in filters.items():
                if field != skip:
                    qs = qs.filter(**{f'{field}__iexact': value})
            return qs

        # Each dropdown is filtered by the OTHER two selections
        def distinct(field):
            values = (apply(base, skip=field)
                      .exclude(**{f'{field}__isnull': True})
                      .values_list(field, flat=True)
                      .distinct().order_by(field))
            return [str(v) for v in values if v]

        rows = []
        if filters:
            rows = list(apply(base).order_by(JOB, COLOR, FABRIC).values())

        return JsonResponse({
            "status": "success",
            "jobs": distinct(JOB),
            "colors": distinct(COLOR),
            "fabrics": distinct(FABRIC),
            "data": rows,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_fabric_ocr(request):

    if request.method != 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'Only GET method is allowed.'
        }, status=405)

    # Get parameters
    job_no = (request.GET.get('Jobno') or '').strip()
    lotwise = (request.GET.get('Lotwise') or 'N').strip().upper()
    diawise = (request.GET.get('Diawise') or 'N').strip().upper()

    # Validate required parameter
    if not job_no:
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno parameter is required.'
        }, status=400)

    # Validate optional parameters
    if lotwise not in ['Y', 'N']:
        return JsonResponse({
            'status': 'error',
            'message': 'Lotwise must be Y or N.'
        }, status=400)

    if diawise not in ['Y', 'N']:
        return JsonResponse({
            'status': 'error',
            'message': 'Diawise must be Y or N.'
        }, status=400)

    try:
        with connections['demo'].cursor() as cursor:

            cursor.execute(
                """
                SET NOCOUNT ON;
                EXEC dbo.sp_GetFabricOCRSummary
                    @JobNo = %s,
                    @Lotwise = %s,
                    @Diawise = %s
                """,
                [job_no, lotwise, diawise]
            )

            # Skip result sets without columns
            while cursor.description is None:
                if not cursor.nextset():
                    break

            data = dictfetchall(cursor) if cursor.description else []

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'parameters': {
                'Jobno': job_no,
                'Lotwise': lotwise,
                'Diawise': diawise
            },
            'data': data
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



#Cutting Summary API

def get_cutting_summary(request):
    # Model field names (change here if your view/table uses different ones)
    JOB, COLOR, FABRIC = 'jobno', 'clr_name', 'fab_name'

    def clean(value, default_label):
        value = (value or '').strip()
        return None if value in ('', default_label) else value

    # Accept both the new and old parameter names from the frontend
    selected = {
        JOB: clean(request.GET.get('jobno'), 'All Jobs'),
        COLOR: clean(request.GET.get('clr_name') or request.GET.get('color'), 'All Colors'),
        FABRIC: clean(request.GET.get('fab_name') or request.GET.get('fabric'), 'All Fabrics'),
    }
    filters = {k: v for k, v in selected.items() if v}

    try:
        base = ViewCuttingOcr.objects.using('demo').all()

        def apply(qs, skip=None):
            for field, value in filters.items():
                if field != skip:
                    qs = qs.filter(**{f'{field}__iexact': value})
            return qs

        # Each dropdown is filtered by the OTHER two selections
        def distinct(field):
            values = (apply(base, skip=field)
                      .exclude(**{f'{field}__isnull': True})
                      .values_list(field, flat=True)
                      .distinct().order_by(field))
            return [str(v) for v in values if v]

        rows = []
        if filters:
            rows = list(apply(base).order_by(JOB, COLOR, FABRIC).values())

        return JsonResponse({
            "status": "success",
            "jobs": distinct(JOB),
            "colors": distinct(COLOR),
            "fabrics": distinct(FABRIC),
            "data": rows,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_cutting_ocr(request):

    if request.method != 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'Only GET method is allowed.'
        }, status=405)

    # Get parameters
    job_no = (request.GET.get('Jobno') or '').strip()
    lotwise = (request.GET.get('Lotwise') or 'N').strip().upper()
    diawise = (request.GET.get('Diawise') or 'N').strip().upper()

    # Validate required parameter
    if not job_no:
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno parameter is required.'
        }, status=400)

    # Validate optional parameters
    if lotwise not in ['Y', 'N']:
        return JsonResponse({
            'status': 'error',
            'message': 'Lotwise must be Y or N.'
        }, status=400)

    if diawise not in ['Y', 'N']:
        return JsonResponse({
            'status': 'error',
            'message': 'Diawise must be Y or N.'
        }, status=400)

    try:
        with connections['demo'].cursor() as cursor:

            cursor.execute(
                """
                SET NOCOUNT ON;
                EXEC dbo.sp_GetCuttingOCRSummary
                    @JobNo = %s,
                    @Lotwise = %s,
                    @Diawise = %s
                """,
                [job_no, lotwise, diawise]
            )

            # Skip result sets without columns
            while cursor.description is None:
                if not cursor.nextset():
                    break

            data = dictfetchall(cursor) if cursor.description else []

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'parameters': {
                'Jobno': job_no,
                'Lotwise': lotwise,
                'Diawise': diawise
            },
            'data': data
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)




def _execute_popup_sp(request, sp_name):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed.'}, status=405)

    job_no = (request.GET.get('Jobno') or '').strip()
    colour = (request.GET.get('Colour') or '').strip()
    fabric = (request.GET.get('Fabric') or '').strip()
    lot_no = (request.GET.get('Lotno') or '').strip() or None
    dia = (request.GET.get('Dia') or '').strip() or None

    if not all([job_no, colour, fabric]):
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno, Colour, and Fabric parameters are required.'
        }, status=400)

    try:
        with connections['demo'].cursor() as cursor:
            cursor.execute(
                    f"SET NOCOUNT ON; EXEC {sp_name} %s, %s, %s, %s, %s",
                    [job_no, colour, fabric, dia, lot_no]  # ⚑ dia before lot_no
                )

            while cursor.description is None and cursor.nextset():
                pass

            data = dictfetchall(cursor) if cursor.description else []

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# Fabric Popup Modal APIs
def get_fabric_inward_summary(request):
    return _execute_popup_sp(request, 'sp_getFabricInwardSummary')


def get_fabric_delivery_summary(request):
    return _execute_popup_sp(request, 'sp_getFabricdeliverySummary')


def get_Fabric_return_summary(request):
    return _execute_popup_sp(request, 'sp_GetCuttingReturnSummary')


# Cutting Popup Modal APIs
def get_fabric_received(request):
    return _execute_popup_sp(request, 'sp_Get_Fabric_Delivery_Cut')


def get_cutting_consumption(request):
    return _execute_popup_sp(request, 'sp_Get_Cutting_Consumption')


def get_cutting_return(request):
    return _execute_popup_sp(request, 'sp_Get_Cutting_Return')


def get_replace_details(request):
    return _execute_popup_sp(request, 'sp_Get_Replace_Details')


def get_cutting_stock_roll(request):
    return _execute_popup_sp(request, 'sp_Get_Cutting_Stock_Roll')



def serialize_stock(obj):
    return {
        "sno": obj.sno,
        "jobno": obj.jobno,
        "colour": obj.colour,
        "lotno": obj.lotno,
        "fabdescr": obj.fabdescr,
        "diaid": obj.diaid,
        "rls": obj.rls,
        "kgs": str(obj.kgs),
        "mtr": str(obj.mtr),
        "clr_name": obj.clr_name,
        "fab_name": obj.fab_name,
        "dia_name": obj.dia_name,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def manual_stock_list_create(request):
    # READ ALL
    if request.method == "GET":
        stocks = MaunualStock.objects.using('default').all()
        data = [serialize_stock(stock) for stock in stocks]
        return JsonResponse(data, safe=False, status=200)

    # CREATE
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            stock = MaunualStock.objects.using('default').create(
                sno=body["sno"],  # Remove this line if SNo is auto-increment in DB
                jobno=body["jobno"],
                colour=body["colour"],
                lotno=body.get("lotno"),
                fabdescr=body["fabdescr"],
                diaid=body["diaid"],
                rls=body["rls"],
                kgs=body["kgs"],
                mtr=body["mtr"],
                clr_name=body.get("clr_name"),
                fab_name=body.get("fab_name"),
                dia_name=body.get("dia_name"),
            )
            return JsonResponse(serialize_stock(stock), status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing required field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def manual_stock_detail(request, sno):
    try:
        stock = MaunualStock.objects.using('default').get(sno=sno)
    except MaunualStock.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)

    # READ SINGLE
    if request.method == "GET":
        return JsonResponse(serialize_stock(stock), status=200)

    # UPDATE
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            updatable_fields = [
                "jobno", "colour", "lotno", "fabdescr", "diaid",
                "rls", "kgs", "mtr", "clr_name", "fab_name", "dia_name"
            ]
            for field in updatable_fields:
                if field in body:
                    setattr(stock, field, body[field])
            stock.save()
            return JsonResponse(serialize_stock(stock), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # DELETE
    if request.method == "DELETE":
        stock.delete()
        return JsonResponse({"message": f"Record {sno} deleted successfully"}, status=200)