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
from .models import Assembly_data,end_line_data, unit_input, Msizes,dependency,dependency_data
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connections
from django.db.models import Q
from rest_framework.decorators import api_view


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




@require_GET
def end_live_scan_data(request):
    unit = request.GET.get('unit')
    line = request.GET.get('line')

    verified_dependencies = dependency.objects.filter(verify=True).values(
        'job_no', 'tb_name', 'process_des'
    )

    dependency_map = {}
    for item in verified_dependencies:
        job_no = str(item.get('job_no') or '').strip()
        tb_name = str(item.get('tb_name') or '').strip()
        process_des = str(item.get('process_des') or '').strip().casefold()
        if not job_no or not tb_name or not process_des:
            continue
        key = (job_no.casefold(), tb_name.casefold())
        dependency_map.setdefault(key, set()).add(process_des)

    if not dependency_map:
        return JsonResponse({
            "status": True,
            "message": "No verified endline dependency configuration found.",
            "data": []
        })

    filters = Q()
    for job_no, tb_name in dependency_map.keys():
        filters |= Q(job_no__iexact=job_no) & Q(tb_name__iexact=tb_name)

    assembly_rows = Assembly_data.objects.filter(filters)
    if unit is not None:
        assembly_rows = assembly_rows.filter(unit=unit)
    if line is not None:
        assembly_rows = assembly_rows.filter(line=line)

    unit_ids = {str(row.unit).strip() for row in assembly_rows if row.unit is not None}
    unit_name_map = {
        str(u.unitcode): u.unitname
        for u in MasUnit.objects.using("main").filter(unitcode__in=unit_ids)
    }

    bundle_info = {}
    for row in assembly_rows:
        bundle_id = str(row.bundle_id or '').strip()
        job_no_key = str(row.job_no or '').strip().casefold()
        tb_name_key = str(row.tb_name or '').strip().casefold()
        seq_value = str(row.seq or '').strip().casefold()
        if not bundle_id or not seq_value:
            continue

        bundle_key = (bundle_id, job_no_key, tb_name_key)
        bundle_info.setdefault(bundle_key, {
            'bundle_id': bundle_id,
            'job_no': row.job_no,
            'tb_id': row.tb_id,
            'tb_name': row.tb_name,
            'unit': row.unit,
            'line': row.line,
            'bdl_no': row.bdl_no,
            'mbud': row.mbud,
            'size': row.size,
            'size_id': row.size_id,
            'color': row.color,
            'pc': row.pc,
            'entry_date': row.entry_date,
            'lot': row.lot,
            'has_scanned_row': False,
            'completed_sequences': set(),
        })
        if row.scan:
            bundle_info[bundle_key]['has_scanned_row'] = True
        bundle_info[bundle_key]['completed_sequences'].add(seq_value)

    eligible_units = {}
    for (bundle_id, job_no_key, tb_name_key), info in bundle_info.items():
        if info['has_scanned_row']:
            continue
        required_sequences = dependency_map.get((job_no_key, tb_name_key))
        if required_sequences and required_sequences.issubset(info['completed_sequences']):
            unit_id = str(info['unit'])
            unit_data = eligible_units.setdefault(unit_id, {
                'unit_id': unit_id,
                'unit_name': unit_name_map.get(unit_id, 'Unknown Unit'),
                'total_records': 0,
                'data': []
            })
            unit_data['total_records'] += 1
            unit_data['data'].append({
                'bundid': info['bundle_id'],
                'jobno': info['job_no'],
                'tbid': info['tb_id'],
                'tbid_name': info['tb_name'],
                'bdl': info['bdl_no'],
                'comboclr': info['color'],
                'sizid': info['size_id'],
                'sizid_name': info['size'],
                'mbud': info['mbud'],
                'pc': info['pc'],
                'lot': info['lot'],
                'entry_date': info['entry_date'],
            })

    return JsonResponse({
        "status": True,
        "message": "End Line Live Scan Data API is working",
        "data": list(eligible_units.values())
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




class EndUnitInputAPIView(APIView):
    def post(self, request):
        data_list = request.data.get("data", [])

        try:
            with transaction.atomic():

                # USE_TZ=False என்பதால் localtime வேண்டாம்
                now_ist = timezone.now()

                end_inputs = []

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

                    end_inputs.append(
                        end_line_data(
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

                if end_inputs:
                    end_line_data.objects.bulk_create(end_inputs)

                bundle_ids = [
                    item.get("bundle_id")
                    for item in data_list
                    if item.get("bundle_id")
                ]

                if bundle_ids:
                    Assembly_data.objects.filter(
                        bundle_id__in=bundle_ids
                    ).update(scan=True)

                print("--- Bulk Create & Assembly_data Scan Update Success ---")

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


def get_eligible_assembly_bundle_ids(job_no, process_des, top_bottom=None):
    dependency_query = dependency.objects.filter(
        job_no__iexact=job_no,
        process_des__iexact=process_des,
    )
    if top_bottom:
        top_bottom_filter = Q(tb_name__iexact=top_bottom)
        if str(top_bottom).strip().isdigit():
            top_bottom_filter |= Q(tb_id=int(str(top_bottom).strip()))
        dependency_query = dependency_query.filter(top_bottom_filter)
    process_dependency = dependency_query.order_by('-id').first()

    if not process_dependency or not process_dependency.verify:
        return False, None, "This process dependency is not verified."

    if not process_dependency.and_or:
        return True, None, None

    required_descriptions = list(
        process_dependency.data_entries.values_list('descriptions', flat=True)
    )
    if not required_descriptions:
        return False, None, "Previous process dependency is not configured."

    required_sequences = {
        str(description).strip().casefold()
        for description in required_descriptions
        if str(description or '').strip()
    }
    if not required_sequences:
        return False, None, "Previous process dependency is not configured."

    completed_by_bundle = {}
    completed_query = Assembly_data.objects.filter(job_no__iexact=job_no)
    if top_bottom:
        completed_query = completed_query.filter(tb_name__iexact=top_bottom)
    completed_rows = completed_query.values_list('bundle_id', 'seq')
    for bundle_id, sequence in completed_rows:
        normalized_sequence = str(sequence or '').strip().casefold()
        if normalized_sequence:
            completed_by_bundle.setdefault(str(bundle_id), set()).add(normalized_sequence)

    eligible_bundle_ids = {
        bundle_id
        for bundle_id, completed_sequences in completed_by_bundle.items()
        if required_sequences.issubset(completed_sequences)
    }
    if not eligible_bundle_ids:
        required_process_names = [
            str(description).strip()
            for description in required_descriptions
            if str(description or '').strip()
        ]
        return (
            False,
            set(),
            "Previous process is not complete for any bundle. Required processes: "
            + ", ".join(required_process_names),
        )

    return True, eligible_bundle_ids, None


class GetUnitDataAPIView(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        job_no = request.query_params.get('job_no')
        process_des = request.query_params.get('process_des')
        top_bottom = str(request.query_params.get('top_bottom', '') or '').strip()
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago).order_by('-entry_date')

        if job_no is not None:
            job_no = job_no.strip()
            if not job_no:
                return Response(
                    {"error": "job_no is required to load assembly bundles"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if process_des is not None:
                process_des = process_des.strip()
                if not top_bottom:
                    return Response(
                        {"error": "top_bottom is required to load assembly bundles"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids(
                    job_no, process_des, top_bottom
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = Assembly_data.objects.filter(
                    job_no__iexact=job_no,
                    seq__iexact=process_des,
                ).values_list('bundle_id', flat=True)
                data = data.filter(job_no__iexact=job_no)
                if top_bottom:
                    data = data.filter(tb_name__iexact=top_bottom)
                data = data.exclude(bundle_id__in=already_scanned_ids)
                if eligible_bundle_ids is not None:
                    data = data.filter(bundle_id__in=eligible_bundle_ids)
            else:
                verified_tb_ids = dependency.objects.filter(
                    job_no__iexact=job_no,
                    verify=True
                ).values_list('tb_id', flat=True)
                data = data.filter(
                    job_no__iexact=job_no,
                    tb_id__in=verified_tb_ids,
                    scan=False,
                )

        # JSON response
        results = list(data.values('bundle_id','mbud', 'job_no','color','bdl_no','size','tb_name', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})
    



class EndUnitDataAPIView(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        job_no = request.query_params.get('job_no')
        process_des = request.query_params.get('process_des')
        top_bottom = str(request.query_params.get('top_bottom', '') or '').strip()
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = end_line_data.objects.filter(unit=unit, line=line, entry_date__date=date_obj)
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = end_line_data.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago)

        if job_no is not None:
            job_no = job_no.strip()
            if not job_no:
                return Response(
                    {"error": "job_no is required to load assembly bundles"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if process_des is not None:
                process_des = process_des.strip()
                if not top_bottom:
                    return Response(
                        {"error": "top_bottom is required to load assembly bundles"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids(
                    job_no, process_des, top_bottom
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = Assembly_data.objects.filter(
                    job_no__iexact=job_no,
                    seq__iexact=process_des,
                ).values_list('bundle_id', flat=True)
                data = data.filter(job_no__iexact=job_no)
                if top_bottom:
                    data = data.filter(tb_name__iexact=top_bottom)
                data = data.exclude(bundle_id__in=already_scanned_ids)
                if eligible_bundle_ids is not None:
                    data = data.filter(bundle_id__in=eligible_bundle_ids)
            else:
                verified_tb_ids = dependency.objects.filter(
                    job_no__iexact=job_no,
                    verify=True
                ).values_list('tb_id', flat=True)
                data = data.filter(
                    job_no__iexact=job_no,
                    tb_id__in=verified_tb_ids,
                    scan=False,
                )

        # JSON response
        results = list(data.values('bundle_id','bdl_no','mbud', 'job_no','color','bdl_no','size','tb_name', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})
    



class GetUnitAssemply(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = Assembly_data.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = Assembly_data.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago).order_by('-entry_date')

        # JSON response
        results = list(data.values('bundle_id','bdl_no', 'job_no','seq', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})
    

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
        line=line_obj.id,
        status=1
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
        job_no = str(request.data.get('job_no', '')).strip()
        selected_seq = str(request.data.get('seq', '') or '').strip()
        selected_top_bottom = str(request.data.get('top_bottom', '') or '').strip()
        unit = request.data.get('unit')
        line = request.data.get('line')
        bundle_ids = request.data.get('bundle_ids', [])
        raw_date = request.data.get('date')

        if not emp_code or not machine_id or not job_no or not selected_seq or not selected_top_bottom or not unit or not line or not bundle_ids:
            return Response(
                {"error": "employee, machine, job no, sequence, top/bottom, unit, line and bundles are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        selected_date = parse_datetime(raw_date) if raw_date else timezone.now()
        allocation_date = selected_date.date() if selected_date else timezone.now().date()
        unit_obj = Unit.objects.filter(name__iexact=f"unit-{unit}").first()
        line_obj = Line.objects.filter(unit=unit_obj, line_number=line).first() if unit_obj else None
        allocation_query = emp_allocate.objects.none()
        if unit_obj and line_obj:
            allocation_query = emp_allocate.objects.select_related('machine').filter(
                date__date=allocation_date,
                unit=unit_obj.id,
                line=line_obj.id,
                emp_code=emp_code,
                machine_id=machine_id,
                jobno__iexact=job_no
            )
            if 'seq' in request.data:
                allocation_query = allocation_query.filter(seq=selected_seq)
            if 'top_bottom' in request.data:
                allocation_query = allocation_query.filter(top_bottom__iexact=selected_top_bottom)
        allocation = allocation_query.first()

        if not allocation:
            return Response(
                {"error": "The selected employee is not allocated to this machine and job no."},
                status=status.HTTP_400_BAD_REQUEST
            )

        process_des = str(allocation.seq or '').strip()

        allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids(
            job_no, process_des, selected_top_bottom
        )
        if not allowed:
            return Response(
                {"error": error_message},
                status=status.HTTP_409_CONFLICT
            )

        unique_ids = list(dict.fromkeys(str(value).strip() for value in bundle_ids if str(value).strip()))
        if eligible_bundle_ids is not None:
            ineligible_ids = [value for value in unique_ids if value not in eligible_bundle_ids]
            if ineligible_ids:
                return Response(
                    {"error": "Previous process is not complete for some bundles.", "bundle_ids": ineligible_ids},
                    status=status.HTTP_409_CONFLICT
                )

        with transaction.atomic():
            already_scanned_ids = Assembly_data.objects.filter(
                job_no__iexact=job_no,
                seq__iexact=process_des,
            ).values_list('bundle_id', flat=True)
            bundle_queryset = unit_input.objects.select_for_update().filter(
                unit=unit,
                line=line,
                job_no__iexact=job_no,
                bundle_id__in=unique_ids,
            )
            if selected_top_bottom:
                bundle_queryset = bundle_queryset.filter(tb_name__iexact=selected_top_bottom)
            bundle_queryset = bundle_queryset.exclude(bundle_id__in=already_scanned_ids)
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
                    seq=process_des,
                    # process_des=process_des,
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
                    lot=bundle.lot,
                    emp_id=emp_code
                )
                for bundle in bundles
            ])
            updated = bundle_queryset.update(scan=True)

        return Response({"status": "success", "updated": updated}, status=status.HTTP_200_OK)


save_assembly = SaveAssemblyAPIView.as_view()




# @api_view(['POST'])
# def get_process_details(request):
#     jobno = request.data.get('jobno')
#     topbottom = request.data.get('topbottom')

#     if not jobno or not topbottom:
#         return JsonResponse(
#             {"error": "Jobno and TopBottom required"},
#             status=400
#         )

#     saved_filter = Q(job_no=jobno) & Q(tb_name__iexact=str(topbottom).strip())
#     if str(topbottom).strip().isdigit():
#         saved_filter |= Q(job_no=jobno, tb_id=int(topbottom))

#     saved_dependencies = dependency.objects.filter(saved_filter).prefetch_related(
#         'data_entries'
#     ).order_by('-id')
#     latest_by_process = {}
#     for dep in saved_dependencies:
#         latest_by_process.setdefault(dep.process_id, dep)

#     if latest_by_process:
#         saved_result = []
#         for index, dep in enumerate(reversed(list(latest_by_process.values())), start=1):
#             saved_result.append({
#                 'Jobno': dep.job_no,
#                 'TopBottdes': dep.tb_name,
#                 'TbID': dep.tb_id,
#                 'sl': index,
#                 'Process_des': dep.process_des,
#                 'mc': dep.mc,
#                 'thrd': dep.thrd,
#                 'Wsec': dep.wsec,
#                 'Process_ID': dep.process_id,
#                 'saved_and_or': 1 if dep.and_or else 0,
#                 'saved_verify': bool(dep.verify),
#                 'saved_selected_processes': [
#                     child.descriptions
#                     for child in dep.data_entries.all().order_by('desc_ord_no', 'id')
#                 ],
#             })
#         return JsonResponse(saved_result, safe=False)

#     # 1. Stored Procedure moolam data eduthu varuthu
#     # with connections['demo'].cursor() as cursor:
#     #     cursor.execute(
#     #         "EXEC sp_GetProcessDetails %s, %s",
#     #         [jobno, topbottom]
#     #     )
#     #     columns = [col[0] for col in cursor.description]
#     #     rows = cursor.fetchall()
#     #     result = []
#     #     for row in rows:
#     #         result.append(dict(zip(columns, row)))

#     with connections['demo'].cursor() as cursor:
#         cursor.execute(
#             "EXEC sp_GetProcessDetails %s, %s",
#             [jobno, topbottom]
#         )

#         columns = [col[0] for col in cursor.description]
#         rows = cursor.fetchall()

#         result = []

#         for row in rows:
#             item = dict(zip(columns, row))

#             # Trn = A / R மட்டும்
#             trn = str(
#                 item.get('Trn', '') or ''
#             ).strip().upper()

#             if trn in ('A', 'R'):
#                 result.append(item)

#     # 2. Munbe save aanatha nu check panni results-oda serkkurathu
#     for item in result:
#         process_id = item.get('Process_ID')
#         job_no = item.get('Jobno')
#         tb_id = item.get('TbID')

#         try:
#             # Table-la antha job_no, tb_id, process_id irukha nu paarkurathu
#             existing_dep = dependency.objects.filter(
#                 job_no=job_no,
#                 tb_id=tb_id,
#                 process_id=process_id
#             ).order_by('-id').first()

#             if existing_dep:
#                 # and_or boolean-ah irunthal 1/0 aah mathi anuppurathu
#                 item['saved_and_or'] = 1 if existing_dep.and_or else 0
#                 item['saved_verify'] = bool(existing_dep.verify)
                
#                 # related_name='data_entries' vechu dependency_data-la irukka descriptions-ah edukkurathu
#                 saved_children = existing_dep.data_entries.all().order_by('desc_ord_no', 'id')
#                 item['saved_selected_processes'] = [child.descriptions for child in saved_children]
#             else:
#                 item['saved_and_or'] = 0
#                 item['saved_verify'] = False
#                 item['saved_selected_processes'] = []
                
#         except Exception as e:
#             item['saved_and_or'] = 0
#             item['saved_verify'] = False
#             item['saved_selected_processes'] = []

#     return JsonResponse(result, safe=False)


@api_view(['POST'])
def get_process_details(request):
    jobno = request.data.get('jobno')
    topbottom = request.data.get('topbottom')

    if not jobno or not topbottom:
        return JsonResponse(
            {"error": "Jobno and TopBottom required"},
            status=400
        )

    # =========================================================
    # 1. Stored Procedure-la irunthu data edukkum
    #    Trn also stored procedure-la irunthu varum
    # =========================================================
    with connections['demo'].cursor() as cursor:
        cursor.execute(
            "EXEC sp_GetProcessDetails %s, %s",
            [jobno, topbottom]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        result = []

        for row in rows:
            item = dict(zip(columns, row))

            # Trn = A / R mattum
            trn = str(
                item.get('Trn', '') or ''
            ).strip().upper()

            if trn in ('A'):
                item['Trn'] = trn
                result.append(item)

    # =========================================================
    # 2. Process_ID -> Trn mapping
    # =========================================================
    trn_map = {}

    for item in result:
        process_id = item.get('Process_ID')
        trn = item.get('Trn')

        if process_id is not None:
            trn_map[process_id] = trn

    # =========================================================
    # 3. Saved dependency data check
    # =========================================================
    saved_filter = (
        Q(job_no=jobno) &
        Q(tb_name__iexact=str(topbottom).strip())
    )

    if str(topbottom).strip().isdigit():
        saved_filter |= Q(
            job_no=jobno,
            tb_id=int(topbottom)
        )

    saved_dependencies = (
        dependency.objects
        .filter(saved_filter)
        .prefetch_related('data_entries')
        .order_by('-id')
    )

    latest_by_process = {}

    for dep in saved_dependencies:
        latest_by_process.setdefault(
            dep.process_id,
            dep
        )

    # =========================================================
    # 4. Saved data iruntha
    # =========================================================
    if latest_by_process:

        saved_result = []

        for index, dep in enumerate(
            reversed(list(latest_by_process.values())),
            start=1
        ):
            saved_result.append({
                'Jobno': dep.job_no,
                'TopBottdes': dep.tb_name,
                'TbID': dep.tb_id,
                'sl': index,
                'Process_des': dep.process_des,
                'mc': dep.mc,
                'thrd': dep.thrd,

                # Stored Procedure-la irunthu Trn
                'Trn': trn_map.get(
                    dep.process_id,
                    ''
                ),

                'Wsec': dep.wsec,
                'Process_ID': dep.process_id,

                'saved_and_or': (
                    1 if dep.and_or else 0
                ),

                'saved_verify': bool(
                    dep.verify
                ),

                'saved_selected_processes': [
                    child.descriptions
                    for child in dep.data_entries.all().order_by(
                        'desc_ord_no',
                        'id'
                    )
                ],
            })

        return JsonResponse(
            saved_result,
            safe=False
        )

    # =========================================================
    # 5. Saved data illana
    #    Stored Procedure result direct-ah return pannum
    # =========================================================
    for item in result:

        process_id = item.get('Process_ID')
        job_no = item.get('Jobno')
        tb_id = item.get('TbID')

        try:
            existing_dep = (
                dependency.objects
                .filter(
                    job_no=job_no,
                    tb_id=tb_id,
                    process_id=process_id
                )
                .order_by('-id')
                .first()
            )

            if existing_dep:

                item['saved_and_or'] = (
                    1 if existing_dep.and_or else 0
                )

                item['saved_verify'] = bool(
                    existing_dep.verify
                )

                saved_children = (
                    existing_dep.data_entries
                    .all()
                    .order_by(
                        'desc_ord_no',
                        'id'
                    )
                )

                item['saved_selected_processes'] = [
                    child.descriptions
                    for child in saved_children
                ]

            else:
                item['saved_and_or'] = 0
                item['saved_verify'] = False
                item['saved_selected_processes'] = []

        except Exception:
            item['saved_and_or'] = 0
            item['saved_verify'] = False
            item['saved_selected_processes'] = []

    return JsonResponse(
        result,
        safe=False
    )

@require_GET
def get_job_top_bottom(request):
    """Return the valid Job No / Top-Bottom pairs used by dependency filters."""
    with connections['demo'].cursor() as cursor:
        cursor.execute("EXEC sp_GetJobTopBottom")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

    return JsonResponse(
        [dict(zip(columns, row)) for row in rows],
        safe=False,
    )

@csrf_exempt
def save_process_dependency(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            def safe_integer(value, default=0):
                try:
                    return int(float(value))
                except (TypeError, ValueError):
                    return default

            if not isinstance(data, list):
                data = [data]
            saved_count = 0
            with transaction.atomic():
                first_row = data[0] if data else {}
                existing_group = dependency.objects.select_for_update().filter(
                    job_no=first_row.get('job_no'),
                    tb_id=first_row.get('tb_id'),
                )
                if existing_group.filter(verify=True).exists():
                    return JsonResponse(
                        {"error": "Verified dependency cannot be changed"},
                        status=409
                    )
                group_already_exists = existing_group.exists()

                for row in data:
                    lookup = {
                        'job_no': row.get('job_no'),
                        'tb_id': row.get('tb_id'),
                        'process_id': row.get('process_id'),
                    }

                    # Reuse the latest saved row so repeated saves do not create
                    # another dependency record for the same process.
                    dep = dependency.objects.filter(**lookup).order_by('-id').first()
                    if dep is None:
                        # Once a Job No + Top/Bottom configuration exists, Save
                        # may update it only; it must not append new parent rows.
                        if group_already_exists:
                            continue
                        dep = dependency(**lookup)

                    dep.tb_name = row.get('tb_name')
                    dep.process_des = row.get('process_des')
                    dep.mc = row.get('mc')
                    # The procedure can return values such as "NIL", while the
                    # model stores Thread as an integer. Treat non-numeric
                    # thread values as zero instead of failing the whole save.
                    dep.thrd = safe_integer(row.get('thrd'))
                    dep.wsec = row.get('wsec')
                    dep.and_or = bool(row.get('and_or', 0))
                    dep.verify = False
                    dep.date = timezone.now()
                    dep.save()

                    # The submitted selection is the complete current selection.
                    dep.data_entries.all().delete()
                    selected_processes = row.get('selected_processes') or []
                    dependency_data.objects.bulk_create([
                        dependency_data(
                            dep_id=dep,
                            tb_id=dep.tb_id,
                            process_id=safe_integer(
                                selected.get('process_id')
                                if isinstance(selected, dict)
                                else dep.process_id
                            ),
                            desc_ord_no=index,
                            descriptions=(
                                selected.get('description', '')
                                if isinstance(selected, dict)
                                else selected
                            ),
                            date=timezone.now()
                        )
                        for index, selected in enumerate(selected_processes, start=1)
                    ])
                    saved_count += 1
            return JsonResponse(
                {
                    "message":
                    "Data saved successfully",
                    "count":
                    saved_count
                },
                status=201
            )
        except Exception as e:
            return JsonResponse(
                {
                    "error":str(e)
                },
                status=400
            )
    return JsonResponse(
        {
            "error":
            "Invalid request method"
        },
        status=405
    )


@csrf_exempt
def verify_process_dependency(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        if username != 'admin' or password != 'admin':
            return JsonResponse({"error": "Invalid admin credentials"}, status=403)

        job_no = data.get('job_no')
        tb_id = data.get('tb_id')
        with transaction.atomic():
            dependencies = dependency.objects.select_for_update().filter(
                job_no=job_no,
                tb_id=tb_id
            )
            if not dependencies.exists():
                return JsonResponse(
                    {"error": "Save the dependency before verifying"},
                    status=404
                )
            updated = dependencies.update(verify=True)

        return JsonResponse({"message": "Verified successfully", "count": updated})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_process_dependency(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        with transaction.atomic():
            dependencies = dependency.objects.select_for_update().filter(
                job_no=data.get('job_no'),
                tb_id=data.get('tb_id'),
                verify=True
            )
            if not dependencies.exists():
                return JsonResponse(
                    {"error": "Verified dependency not found"},
                    status=404
                )
            deleted_count, _ = dependencies.delete()

        return JsonResponse({
            "message": "Dependency deleted successfully",
            "count": deleted_count
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
