from django.shortcuts import render
from django.http import JsonResponse
from . models import ViewFabricInwardSummary
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections,DatabaseError

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
        base = ViewFabricInwardSummary.objects.using('demo')

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
    """Return all rows from a cursor as a list of dicts."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_fabric_inward_summary(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed.'}, status=405)

    # Fetch query parameters
    job_no = request.GET.get('Jobno')
    colour = request.GET.get('Colour')
    fabric = request.GET.get('Fabric')

    # Validation: Ensure all three parameters are supplied
    if not all([job_no, colour, fabric]):
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno, Colour, and Fabric parameters are required.'
        }, status=400)

    try:
        # Use connection mapped to the 'demo' database
        with connections['demo'].cursor() as cursor:
            # For MySQL / MariaDB syntax:
            cursor.callproc('sp_getFabricInwardSummary', [job_no, colour, fabric])
            
            # Note for SQL Server (MSSQL):
            # cursor.execute("EXEC sp_getFabricInwardSummary %s, %s, %s", [job_no, colour, fabric])
            
            data = dictfetchall(cursor)

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def get_fabric_delivery_summary(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed.'}, status=405)

    # Fetch query parameters
    job_no = request.GET.get('Jobno')
    colour = request.GET.get('Colour')
    fabric = request.GET.get('Fabric')

    # Validation: Ensure all three parameters are supplied
    if not all([job_no, colour, fabric]):
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno, Colour, and Fabric parameters are required.'
        }, status=400)

    try:
        # Connect to the 'demo' database
        with connections['demo'].cursor() as cursor:
            # For MySQL / MariaDB:
            cursor.callproc('sp_getFabricdeliverySummary', [job_no, colour, fabric])
            
            # If using SQL Server (MSSQL), use:
            # cursor.execute("EXEC sp_getFabricdeliverySummary %s, %s, %s", [job_no, colour, fabric])
            
            data = dictfetchall(cursor)

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def get_cutting_return_summary(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed.'}, status=405)

    # Fetch query parameters
    job_no = request.GET.get('Jobno')
    colour = request.GET.get('Colour')
    fabric = request.GET.get('Fabric')

    # Validation: Ensure all three parameters are supplied
    if not all([job_no, colour, fabric]):
        return JsonResponse({
            'status': 'error',
            'message': 'Jobno, Colour, and Fabric parameters are required.'
        }, status=400)

    try:
        # Connect to the 'demo' database
        with connections['demo'].cursor() as cursor:
            # For MySQL / MariaDB:
            cursor.callproc('sp_getcuttingretrunSummary', [job_no, colour, fabric])
            
            # If using SQL Server (MSSQL):
            # cursor.execute("EXEC sp_getcuttingretrunSummary %s, %s, %s", [job_no, colour, fabric])
            
            data = dictfetchall(cursor)

        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)