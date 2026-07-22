from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from imp_reports.models import UnitBundlereport
from bundle_tracking.models import TrsMcutstickerprod,MasUnit,MasTopbottom
from qcapp.models import Unit,Line,machine_details,emp_allocate,Empwisesal
from .models import Assembly_data, unit_input, Msizes,dependency,dependency_data
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


@require_GET
def live_scan_data(request):
   
    trs_data = TrsMcutstickerprod.objects.using("demo").filter(
        scan="1",
        livescan__isnull=True
    ).order_by('jobno','tbid','comboclr','lotno','sizid','bdl')

    tbid_list = {row.tbid for row in trs_data if row.tbid}
    tob_bottom_map = {
        str(item.topbottom_id): item.topbottom_des 
        for item in MasTopbottom.objects.using("main").filter(topbottom_id__in=tbid_list)
    }
    sizeid_list = {row.sizid for row in trs_data if row.sizid}
    size_map = {
        str(item.id): item.name
        for item in Msizes.objects.using("test").filter(id__in=sizeid_list)
    }


    mbud_list = [str(row.mbud) for row in trs_data]
   
    reports = UnitBundlereport.objects.using("app").filter(
        mbundle_id__in=mbud_list
    )
    
    report_map = {str(r.mbundle_id): r for r in reports}
    
    unit_ids = {int(r.unit_id) for r in reports if r.unit_id}
    unit_name_map = {
        str(u.unitcode): u.unitname 
        for u in MasUnit.objects.using("main").filter(unitcode__in=unit_ids)
    }
    
    final_data = {}
    
    for row in trs_data:
        report = report_map.get(str(row.mbud))
        
        uid = str(report.unit_id) if report else "0"
        u_name = unit_name_map.get(uid, "Unknown Unit")
        
        if uid not in final_data:
            final_data[uid] = {
                "unit_id": uid,
                "unit_name": u_name,
                "total_records": 0,
                "data": []
            }
            
        final_data[uid]["total_records"] += 1
        
        final_data[uid]["data"].append({
            "dt": row.dt,
            "empid": row.empid,
            "mbud": row.mbud,
            "bundid": row.bundid,
            "jobno": row.jobno,
            "tbid": row.tbid,
            "tbid_name": tob_bottom_map.get(str(row.tbid), "N/A"),
            "bdl": row.bdl,
            "comboclr": row.comboclr,
            "sizid": row.sizid,
            "sizid_name": size_map.get(str(row.sizid), "N/A"),
            "pc": row.pc,
            "total_bundles": report.total_bundles if report else 0,
            "pcs_count": report.pcs_count if report else 0,
            "lot": row.lotno,
        })

    return JsonResponse({
        "status": True,
        "unit_count": len(final_data),
        "all_unit_data_count": sum(unit["total_records"] for unit in final_data.values()), # இது 6305 ஆக இருக்கும்
        "data": list(final_data.values())
    })


class UnitInputAPIView(APIView):
    def post(self, request):
        data_list = request.data.get("data", [])

        try:
            with transaction.atomic():

                # USE_TZ=False என்பதால் localtime வேண்டாம்
                now_ist = timezone.now()

                unit_inputs = []

                for item in data_list:

                    raw_date = item.get("date")

                    parsed_date = parse_datetime(raw_date)

                    if parsed_date:
                        # Frontend date already IST (13:34)
                        if timezone.is_aware(parsed_date):
                            final_date = parsed_date.replace(tzinfo=None)
                        else:
                            final_date = parsed_date
                    else:
                        final_date = now_ist


                    print("Saving Date:", final_date)

                    unit_inputs.append(
                        unit_input(
                            bundle_id=item.get('bundle_id'),
                            bdl_no=item.get('bdl_no'),
                            mbud=item.get('mbud'),
                            unit=item.get('unit'),
                            line=item.get('line'),
                            entry_date=now_ist,
                            job_no=item.get('job_no'),
                            color=item.get('color'),
                            tb_id=item.get('tb_id'),
                            tb_name=item.get('tb_name'),
                            scan=item.get('scan', False),
                            size=item.get('size'),
                            size_id=item.get('size_id'),
                            pc=item.get('pc'),
                            lot=item.get('lot'),
                            date=final_date
                        )
                    )

                unit_input.objects.bulk_create(unit_inputs)


                bundle_ids = [
                    item.get("bundle_id")
                    for item in data_list
                    if item.get("bundle_id")
                ]

                # Trs_MCutStickerProd update
                if bundle_ids:
                    TrsMcutstickerprod.objects.using('demo').filter(
                        bundid__in=bundle_ids
                    ).update(
                        livescan=1
                    )

                print("--- Bulk Create & LiveScan Update Success ---")

            return Response(
                {"status": "success"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            import traceback
            traceback.print_exc()

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta

class GetUnitDataAPIView(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj, scan=False)
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago, scan=False)

        # JSON response
        results = list(data.values('bundle_id','mbud', 'job_no','color','bdl_no','size','tb_name', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})
    


class GetUnitAssemply(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = Assembly_data.objects.filter(unit=unit, line=line, entry_date__date=date_obj)
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = Assembly_data.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago)

        # JSON response
        results = list(data.values('bundle_id', 'job_no', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})
<<<<<<< HEAD


=======
    

def assembly_emp(request):
    unit = request.GET.get('unit')
    line = request.GET.get('line')
    date = request.GET.get('date')

    if not unit or not line or not date:
        return JsonResponse(
            {"error": "unit, line and date are required"},
            status=400
        )

    filter_date = date.split('T')[0]

    unit_name = f"unit-{unit}"

    unit_obj = Unit.objects.filter(name=unit_name).first()

    if not unit_obj:
        return JsonResponse({"error": "Unit not found"}, status=404)


    line_obj = Line.objects.filter(
        unit=unit_obj,
        line_number=line
    ).first()

    if not line_obj:
        return JsonResponse({"error": "Line not found"}, status=404)


    emp_details = list(emp_allocate.objects.filter(
        date__date=filter_date,
        unit=unit_obj.id,
        line=line_obj.id
    ).values(
        'emp_code',
        'machine',
        'machine__Identity',
        'seq',
        'jobno',
        'top_bottom'
    ))


    # Convert emp_code to integer
    emp_codes = [
        int(emp['emp_code']) 
        for emp in emp_details
        if emp['emp_code'].isdigit()
    ]


    emp_names = Empwisesal.objects.using('main').filter(
        code__in=emp_codes
    ).values(
        'code',
        'name'
    )


    emp_name_dict = {
        str(emp['code']): emp['name']
        for emp in emp_names
    }


    for emp in emp_details:
        emp['emp_name'] = emp_name_dict.get(
            emp['emp_code'],
            ''
        )


    return JsonResponse({
        "unit_id": unit_obj.id,
        "line_id": line_obj.id,
        "line": line,
        "date": filter_date,
        "data": emp_details
    })


class SaveAssemblyAPIView(APIView):
    def post(self, request):
        emp_code = str(request.data.get('emp_code', '')).strip()
        machine_id = request.data.get('machine_id')
        unit = request.data.get('unit')
        line = request.data.get('line')
        bundle_ids = request.data.get('bundle_ids', [])
        raw_date = request.data.get('date')

        if not emp_code or not machine_id or not unit or not line or not bundle_ids:
            return Response(
                {"error": "employee, machine, unit, line and bundles are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        selected_date = parse_datetime(raw_date) if raw_date else timezone.now()
        allocation_date = selected_date.date() if selected_date else timezone.now().date()
        unit_obj = Unit.objects.filter(name__iexact=f"unit-{unit}").first()
        line_obj = Line.objects.filter(unit=unit_obj, line_number=line).first() if unit_obj else None
        allocation = unit_obj and line_obj and emp_allocate.objects.select_related('machine').filter(
            date__date=allocation_date,
            unit=unit_obj.id,
            line=line_obj.id,
            emp_code=emp_code,
            machine_id=machine_id
        ).first()

        if not allocation:
            return Response(
                {"error": "The selected employee is not allocated to this machine."},
                status=status.HTTP_400_BAD_REQUEST
            )

        unique_ids = list(dict.fromkeys(str(value).strip() for value in bundle_ids if str(value).strip()))
        with transaction.atomic():
            bundle_queryset = unit_input.objects.select_for_update().filter(
                unit=unit,
                line=line,
                bundle_id__in=unique_ids,
                scan=False
            )
            bundles = list(bundle_queryset)
            found_ids = {bundle.bundle_id for bundle in bundles}
            missing_ids = [value for value in unique_ids if value not in found_ids]
            if missing_ids:
                return Response(
                    {"error": "Some bundles are unavailable or already scanned.", "bundle_ids": missing_ids},
                    status=status.HTTP_409_CONFLICT
                )

            entry_date = timezone.now()
            Assembly_data.objects.bulk_create([
                Assembly_data(
                    unit=bundle.unit,
                    line=bundle.line,
                    job_no=bundle.job_no,
                    tb_id=bundle.tb_id,
                    tb_name=bundle.tb_name,
                    machine=allocation.machine.Identity,
                    date=selected_date or entry_date,
                    bundle_id=bundle.bundle_id,
                    bdl_no=bundle.bdl_no,
                    mbud=bundle.mbud,
                    size=bundle.size,
                    size_id=bundle.size_id,
                    color=bundle.color,
                    pc=bundle.pc,
                    entry_date=entry_date,
                    scan=False,
                    lot=bundle.lot
                )
                for bundle in bundles
            ])
            updated = bundle_queryset.update(scan=True)

        return Response({"status": "success", "updated": updated}, status=status.HTTP_200_OK)


save_assembly = SaveAssemblyAPIView.as_view()


@csrf_exempt
def save_process_dependency(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            dep = dependency.objects.create(
                job_no=data.get('job_no'),
                tb_id=data.get('tb_id'),
                tb_name=data.get('tb_name'),
                process_des=data.get('process_des'),
                mc=data.get('mc'),
                thrd=data.get('thrd'),
                wsec=data.get('wsec'),
                process_id=data.get('process_id'),
                and_or=data.get('and_or'), # True for AND, False for OR
                date=timezone.now()
            )

            selected_processes = data.get('selected_processes', [])
            for desc in selected_processes:
                dependency_data.objects.create(
                    dep_id=dep,
                    descriptions=desc,
                    date=timezone.now()
                )

            return JsonResponse({'message': 'Data saved successfully!'}, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
>>>>>>> ab16dac5d6f74ee455440a5981571042fc8a86cb
