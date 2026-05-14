from django.http import JsonResponse
from .models import LaySp, MasterFinalMistake, UnitBundlereport, FinalPlans,Corarlck1,CoraRollcheck,BuntrackReport,LaySpreadingLayemployee,VueAdGrid1
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db import connections
from django.db.models import OuterRef, Subquery
from collections import Counter
from datetime import date
from django.utils.dateparse import parse_date

from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_lay_sp_data(request): 
    if request.method == 'GET':
        # 1. Define the FinalPlans Subquery
        # We use .strip() logic conceptually, but in SQL, ensure these match.
        final_plan_qs = FinalPlans.objects.using('mssql').filter(
            plan_no=OuterRef('plan_no'),
            job_no=OuterRef('job_no')
        )

        # 2. Define the Employee/Table Subquery 
        # Joining based on the table_id and date from the FinalPlans 
        # (Since LaySp doesn't have table_id directly)
        emp_qs = LaySpreadingLayemployee.objects.using('app').filter(
            table=OuterRef('final_plans__table_id'),
            date=OuterRef('date')
        )

        data = (
            LaySp.objects.using('mssql')
            .annotate(
                # Fetching fields from FinalPlans
                final_plans__pcs=Subquery(final_plan_qs.values('pcs')[:1]),
                final_plans__empid=Subquery(final_plan_qs.values('empid')[:1]),
                final_plans__marker_no=Subquery(final_plan_qs.values('marker_no')[:1]),
                final_plans__lot_no=Subquery(final_plan_qs.values('lot_no')[:1]),
                final_plans__fabric_color=Subquery(final_plan_qs.values('fabric_color')[:1]),
                final_plans__date_time_fp=Subquery(final_plan_qs.values('date_time')[:1]),
                
                # Fetching Employee Data using the annotated table_id
                emp_name_1=Subquery(emp_qs.values('emp1')[:1]),
                emp_name_2=Subquery(emp_qs.values('emp2')[:1]),
                table_id=Subquery(emp_qs.values('table')[:1]),
            )
            .values(
                'date', 'timer', 'plan_no', 'job_no', 'roll_no', 'f_dia',
                'plan_ply', 'scl_wgt', 'plan_obwgt', 'req_wgt', 'actual_dia',
                'actual_ply', 'actual_obwgt', 'end_bit', 'bal_wgt', 'debit_kg',
                'roll_time', 'remarks', 'bit_wgt', 'date_time',
                'final_plans__pcs', 'final_plans__empid',
                'final_plans__marker_no', 'final_plans__lot_no', 'final_plans__fabric_color',
                'final_plans__date_time_fp', 'emp_name_1', 'emp_name_2', 'table_id'
            )
        )

        return JsonResponse(list(data), safe=False)
    

@csrf_exempt
def lay_sp_sal(request):
    if request.method == 'GET':
        data = VueAdGrid1.objects.using('mssql1').all().filter(dept='cutting').values()
        data_list = list(data)
        return JsonResponse(data_list, safe=False)
    
    
@csrf_exempt
def get_master_final_mistake_data(request):
    if request.method == 'GET':
        data = MasterFinalMistake.objects.using('mssql').all().values()
        data_list = list(data)
        return JsonResponse(data_list, safe=False)
    
@csrf_exempt
def get_unit_bundle_report_data(request):

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    unit = request.GET.get("unit")

    queryset = UnitBundlereport.objects.using("app").all()

    # Default start from 2026-04-20 if no start_date provided
    effective_from = parse_date(start_date) if start_date else date(2026, 4, 20)
    queryset = queryset.filter(s_date__date__gte=effective_from)

    # end_date is optional, only apply if provided
    if end_date:
        queryset = queryset.filter(s_date__date__lte=parse_date(end_date))

    if unit and unit != "all":
        queryset = queryset.filter(tb_name=unit)

    return JsonResponse(list(queryset.values()), safe=False)

def mistake_summary(request):
    try:
        with connections['mssql1'].cursor() as cursor:
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
        roll_data = CoraRollcheck.objects.using('mssql1').filter(
            rlno=OuterRef('roll_id')
        )

        data = Corarlck1.objects.using('mssql1').annotate(
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
    


@csrf_exempt
def unit_bundle(request):
    target_units = ['Unit-1', 'Unit-2', 'Unit-3', 'Unit-4', 'Unit-5']

    unit = request.GET.get('unit')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    queryset = BuntrackReport.objects.using('demo').all()

    # Unit Filter
    if unit:
        queryset = queryset.filter(unitname=unit)
    else:
        queryset = queryset.filter(unitname__in=target_units)

    # Default start from 2026-04-20 if no from_date provided
    effective_from = parse_date(from_date) if from_date else date(2026, 4, 20)
    queryset = queryset.filter(r_dt__date__gte=effective_from)

    # to_date is optional, only apply if provided
    if to_date:
        queryset = queryset.filter(r_dt__date__lte=parse_date(to_date))

    data = list(
        queryset.values(
            'sl', 'unit_id', 'jobno', 'totmastbdl', 'totbdl',
            'ordsamid', 'b_id', 'r_dt', 'mbunid', 'unitname',
            'mbappr', 'pcs_count'
        )
    )

    return JsonResponse(data, safe=False)

