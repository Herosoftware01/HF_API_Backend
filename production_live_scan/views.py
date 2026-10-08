from django.shortcuts import render
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from imp_reports.models import UnitBundlereport
from bundle_tracking.models import TrsMcutstickerprod,MasUnit,MasTopbottom
from qcapp.models import Unit,Line,machine_details,emp_allocate,Empwisesal
from .models import Assembly_data,bundle_transfer,end_line_data, unit_input, Msizes,dependency,dependency_data,PreporatoryEntry,ViewRibdelPreparatory,RibdelEntry
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connections
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Sum

from django.views import View
from .models import user_unit_permission
from herofashion.models import User
from qcapp.models import Unit

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
                end_line_inputs = []

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
                            # scan=item.get('scan', False),
                            scan=1 if item.get("allow_end_line") is True else item.get("scan", False),
                            size=item.get('size'),
                            size_id=item.get('size_id'),
                            pc=item.get('pc'),
                            lot=item.get('lot'),
                            date=final_date
                        )
                    )

                
                    # --------------------------------
                    # END LINE
                    # --------------------------------
                    if item.get("allow_end_line") is True:

                        end_line_inputs.append(
                            end_line_data(
                                unit=item.get("unit"),
                                line=item.get("line"),
                                job_no=item.get("job_no"),
                                tb_id=item.get("tb_id"),
                                tb_name=item.get("tb_name"),
                                machine=item.get("machine", ""),
                                date=final_date,
                                bundle_id=item.get("bundle_id"),
                                bdl_no=item.get("bdl_no"),
                                mbud=item.get("mbud"),
                                size=item.get("size"),
                                size_id=item.get("size_id"),
                                color=item.get("color"),
                                pc=item.get("pc"),
                                entry_date=now_ist,
                                scan=item.get("scan", False),
                                lot=item.get("lot") or "0",
                            )
                        )

                # Save normal unit input
                if unit_inputs:
                    unit_input.objects.bulk_create(unit_inputs)

                # Save end line data only when checkbox is enabled
                if end_line_inputs:
                    end_line_data.objects.bulk_create(end_line_inputs)

                # unit_input.objects.bulk_create(unit_inputs)

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

    if not process_dependency.and_or and not process_dependency.or_only:
        return True, None, None

    dependency_entries = list(
        process_dependency.data_entries.values_list(
            'descriptions', 'and_data', 'or_data'
        )
    )
    has_explicit_modes = any(and_data or or_data for _, and_data, or_data in dependency_entries)

    if process_dependency.and_or:
        and_descriptions = [
            description
            for description, and_data, _ in dependency_entries
            if and_data or not has_explicit_modes
        ]
    else:
        and_descriptions = []

    if process_dependency.or_only:
        or_descriptions = [
            description
            for description, _, or_data in dependency_entries
            if or_data or not has_explicit_modes
        ]
    else:
        or_descriptions = []

    and_sequences = {
        str(description).strip().casefold()
        for description in and_descriptions
        if str(description or '').strip()
    }
    or_sequences = {
        str(description).strip().casefold()
        for description in or_descriptions
        if str(description or '').strip()
    }
    if (process_dependency.and_or and not and_sequences) or (
        process_dependency.or_only and not or_sequences
    ):
        return False, None, "Previous process dependency is not configured."

    completed_by_bundle = {}
    completed_query = Assembly_data.objects.filter(job_no__iexact=job_no)
    if top_bottom:
        completed_query = completed_query.filter(tb_name__iexact=top_bottom)
    completed_rows = completed_query.values_list('bundle_id', 'seq')
    for bundle_id, sequence in completed_rows:
        for completed_sequence in split_process_descriptions(sequence):
            normalized_sequence = completed_sequence.casefold()
            completed_by_bundle.setdefault(str(bundle_id), set()).add(normalized_sequence)

    eligible_bundle_ids = {
        bundle_id
        for bundle_id, completed_sequences in completed_by_bundle.items()
        if assembly_dependencies_satisfied(
            completed_sequences,
            and_sequences,
            or_sequences,
        )
    }
    if not eligible_bundle_ids:
        required_process_names = [str(description).strip() for description in and_descriptions]
        or_process_names = [str(description).strip() for description in or_descriptions]
        requirement_details = []
        if required_process_names and not or_process_names:
            requirement_details.append("all AND processes: " + ", ".join(required_process_names))
        if or_process_names:
            requirement_details.append("at least one OR process: " + ", ".join(or_process_names))
        return (
            False,
            set(),
            "Previous process requirements are not complete for any bundle. "
            + "; ".join(requirement_details),
        )

    return True, eligible_bundle_ids, None


def assembly_dependencies_satisfied(completed_sequences, and_sequences, or_sequences):
    and_requirements_met = and_sequences.issubset(completed_sequences)
    or_requirements_met = (
        not or_sequences or not completed_sequences.isdisjoint(or_sequences)
    )
    return and_requirements_met and or_requirements_met


def split_process_descriptions(process_des):
    return list(dict.fromkeys(
        description.strip()
        for description in str(process_des or '').split(',')
        if description.strip()
    ))


def bundle_process_pairs(bundles, process_des):
    return [
        (bundle, description)
        for bundle in bundles
        for description in split_process_descriptions(process_des)
    ]


def assembly_sequence_filter(process_des):
    sequence_filter = Q(seq__iexact=str(process_des or '').strip())
    for description in split_process_descriptions(process_des):
        sequence_filter |= Q(seq__iexact=description)
    return sequence_filter


def get_eligible_assembly_bundle_ids_for_processes(job_no, process_des, top_bottom=None):
    process_descriptions = split_process_descriptions(process_des)
    if not process_descriptions:
        return False, None, "Process sequence is required."

    eligible_bundle_ids = set()
    all_bundles_eligible = False
    errors = []
    for description in process_descriptions:
        allowed, bundle_ids, error_message = get_eligible_assembly_bundle_ids(
            job_no, description, top_bottom
        )
        if not allowed:
            if bundle_ids is None:
                return False, None, error_message
            errors.append(error_message)
            continue
        if bundle_ids is None:
            all_bundles_eligible = True
        else:
            eligible_bundle_ids.update(bundle_ids)

    if all_bundles_eligible:
        return True, None, None
    if eligible_bundle_ids:
        return True, eligible_bundle_ids, None
    return False, set(), " ".join(dict.fromkeys(errors))


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
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, job_no=job_no).order_by('-entry_date')
        else:
            # four_days_ago = datetime.now() - timedelta(days=1)
            today = date.today()
            print("Today's date:", today)
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=today).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, job_no=job_no).order_by('-entry_date')

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
                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids_for_processes(
                    job_no, process_des, top_bottom
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = Assembly_data.objects.filter(
                    job_no__iexact=job_no,
                ).filter(assembly_sequence_filter(process_des)).values_list('bundle_id', flat=True)
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


@api_view(['GET'])
def get_bundle_last_process(request):
    bundle_id = str(request.query_params.get('bundle_id') or '').strip()
    if not bundle_id:
        return Response(
            {"error": "bundle_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    latest_entry = (
        Assembly_data.objects
        .filter(bundle_id__iexact=bundle_id)
        .order_by('-id')
        .values('seq', 'job_no', 'tb_name')
        .first()
    )
    last_processes = split_process_descriptions(latest_entry['seq']) if latest_entry else []
    if not last_processes:
        return Response({"available": False, "message": "Bundle not available"})

    return Response({
        "available": True,
        "last_process": last_processes[-1],
        "job_no": latest_entry['job_no'],
        "top_bottom": latest_entry['tb_name'],
    })


class GetUnitDataAPIViewsss(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        job_no = request.query_params.get('job_no')
        process_des = request.query_params.get('process_des')
        top_bottom = str(request.query_params.get('top_bottom', '') or '').strip()
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, entry_date__date=date_obj).order_by('-entry_date')
        else:
            # four_days_ago = datetime.now() - timedelta(days=1)
            today = date.today()
            print("Today's date:", today)
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=today).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, entry_date__date=today).order_by('-entry_date')

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
                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids_for_processes(
                    job_no, process_des, top_bottom
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = Assembly_data.objects.filter(
                    job_no__iexact=job_no,
                ).filter(assembly_sequence_filter(process_des)).values_list('bundle_id', flat=True)
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


class GetUnitDataAPIViewsss(APIView):
    def get(self, request):
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        job_no = request.query_params.get('job_no')
        process_des = request.query_params.get('process_des')
        top_bottom = str(request.query_params.get('top_bottom', '') or '').strip()
        selected_date = request.query_params.get('date') 

        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, entry_date__date=date_obj).order_by('-entry_date')
        else:
            # four_days_ago = datetime.now() - timedelta(days=1)
            today = date.today()
            print("Today's date:", today)
            # data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=today).order_by('-entry_date')
            data = unit_input.objects.filter(unit=unit, entry_date__date=today).order_by('-entry_date')

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
            # four_days_ago = datetime.now() - timedelta(days=4)
            four_days_ago = date.today()
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
                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids_for_processes(
                    job_no, process_des, top_bottom
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = Assembly_data.objects.filter(
                    job_no__iexact=job_no,
                ).filter(assembly_sequence_filter(process_des)).values_list('bundle_id', flat=True)
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
        all_dates = request.query_params.get('all_dates', '').lower() == 'true'

        if all_dates:
            data = Assembly_data.objects.filter(
                unit=unit, line=line,
            ).order_by('-entry_date')
        elif selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = Assembly_data.objects.filter(
                unit=unit,
                line=line,
                entry_date__date=date_obj,
            ).order_by('-entry_date')
        else:
            data = Assembly_data.objects.filter(
                unit=unit,
                line=line,
                entry_date__gte=date.today(),
            ).order_by('-entry_date')

        results = list(data.values(
            'bundle_id', 'bdl_no', 'job_no', 'seq', 'pc', 'color', 'entry_date'
        ))
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
        # status=1
    ).values(
        'emp_code',
        'machine',
        'machine__Identity',
        'seq',
        'jobno',
        'top_bottom',
        'status',
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
        entry_mode = str(request.data.get('entry_mode', '')).strip().lower()

        if not emp_code or not machine_id or not job_no or not selected_seq or not selected_top_bottom or not unit or not line or not bundle_ids:
            return Response(
                {"error": "employee, machine, job no, sequence, top/bottom, unit, line and bundles are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if entry_mode not in {'manual', 'scan'}:
            return Response(
                {"error": "entry_mode must be either 'manual' or 'scan'"},
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

        allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids_for_processes(
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
            ).filter(assembly_sequence_filter(process_des)).values_list('bundle_id', flat=True)
            bundle_queryset = unit_input.objects.select_for_update().filter(
                unit=unit,
                # line=line,
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
                print("Some bundles are unavailable or already scanned:", missing_ids)
                return Response(
                    {"error": "Some bundles are unavailable or already scanned.", "bundle_ids": missing_ids},
                    status=status.HTTP_409_CONFLICT
                )

            entry_date = timezone.now()
            Assembly_data.objects.bulk_create([
                Assembly_data(
                    unit=unit,
                    line=line,
                    job_no=bundle.job_no,
                    tb_id=bundle.tb_id,
                    tb_name=bundle.tb_name,
                    machine=allocation.machine.Identity,
                    seq=description,
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
                    emp_id=emp_code,
                    entry_mode=entry_mode
                )
                for bundle, description in bundle_process_pairs(bundles, process_des)
            ])
            updated = bundle_queryset.update(scan=True)

        return Response({"status": "success", "updated": updated}, status=status.HTTP_200_OK)


save_assembly = SaveAssemblyAPIView.as_view()




@api_view(['POST'])
def get_process_details(request):
    jobno = request.data.get('jobno')
    topbottom = request.data.get('topbottom')

    if not jobno or not topbottom:
        return JsonResponse(
            {"error": "Jobno and TopBottom required"},
            status=400
        )
        
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

                'saved_or_only': (
                    1 if dep.or_only else 0
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
                    if child.and_data or not child.or_data
                ],

                'saved_or_selected_processes': [
                    child.descriptions
                    for child in dep.data_entries.all().order_by(
                        'desc_ord_no',
                        'id'
                    )
                    if child.or_data
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

                item['saved_or_only'] = (
                    1 if existing_dep.or_only else 0
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
                    if child.and_data or not child.or_data
                ]

                item['saved_or_selected_processes'] = [
                    child.descriptions
                    for child in saved_children
                    if child.or_data
                ]

            else:
                item['saved_and_or'] = 0
                item['saved_or_only'] = 0
                item['saved_verify'] = False
                item['saved_selected_processes'] = []
                item['saved_or_selected_processes'] = []

        except Exception:
            item['saved_and_or'] = 0
            item['saved_or_only'] = 0
            item['saved_verify'] = False
            item['saved_selected_processes'] = []
            item['saved_or_selected_processes'] = []

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
            if not isinstance(data, dict) or data.get("password") != "12345":
                return JsonResponse({"error": "Invalid password"}, status=403)

            edit_confirmed = False
            changed_processes = []

            edit_confirmed = data.get("edit_confirmed") is True
            changed_processes = data.get("changed_processes") or []
            data = data.get("dependencies") or []

            def safe_integer(value, default=0):
                try:
                    return int(float(value))
                except (TypeError, ValueError):
                    return default

            if not isinstance(data, list):
                data = [data]
            saved_count = 0
            affected_bundle_ids = []
            deleted_assembly_count = 0
            affected_process_names = []
            with transaction.atomic():
                first_row = data[0] if data else {}
                existing_group = dependency.objects.select_for_update().filter(
                    job_no=first_row.get('job_no'),
                    tb_id=first_row.get('tb_id'),
                )
                if existing_group.filter(verify=True).exists():
                    if not edit_confirmed or not changed_processes:
                        return JsonResponse(
                            {"error": "Verified dependency requires confirmed edit"},
                            status=409
                        )

                    changed_process_keys = {
                        str(process_name or '').strip().casefold()
                        for process_name in changed_processes
                        if str(process_name or '').strip()
                    }
                    dependents_by_prerequisite = {}
                    process_names_by_key = {}

                    for saved_dependency in existing_group.prefetch_related('data_entries'):
                        process_name = str(saved_dependency.process_des or '').strip()
                        process_key = process_name.casefold()
                        if not process_key:
                            continue
                        process_names_by_key[process_key] = process_name

                        for entry in saved_dependency.data_entries.all():
                            prerequisite_key = str(entry.descriptions or '').strip().casefold()
                            if prerequisite_key:
                                dependents_by_prerequisite.setdefault(
                                    prerequisite_key, set()
                                ).add(process_key)

                    impacted_process_keys = set(changed_process_keys)
                    pending_process_keys = list(changed_process_keys)
                    while pending_process_keys:
                        prerequisite_key = pending_process_keys.pop()
                        for dependent_key in dependents_by_prerequisite.get(prerequisite_key, set()):
                            if dependent_key not in impacted_process_keys:
                                impacted_process_keys.add(dependent_key)
                                pending_process_keys.append(dependent_key)

                    affected_process_names = [
                        process_names_by_key.get(process_key, process_key)
                        for process_key in impacted_process_keys
                    ]

                    changed_assembly_filter = Q()
                    for process_name in changed_processes:
                        changed_assembly_filter |= Q(seq__iexact=str(process_name).strip())

                    changed_assembly = Assembly_data.objects.filter(
                        job_no__iexact=first_row.get('job_no'),
                        tb_id=first_row.get('tb_id'),
                    ).filter(changed_assembly_filter)
                    affected_bundle_ids = list(
                        changed_assembly.values_list('bundle_id', flat=True).distinct()
                    )

                    if affected_bundle_ids and affected_process_names:
                        impacted_assembly_filter = Q()
                        for process_name in affected_process_names:
                            impacted_assembly_filter |= Q(seq__iexact=process_name)

                        impacted_assembly = Assembly_data.objects.filter(
                            job_no__iexact=first_row.get('job_no'),
                            tb_id=first_row.get('tb_id'),
                            bundle_id__in=affected_bundle_ids,
                        ).filter(impacted_assembly_filter)
                        deleted_assembly_count, _ = impacted_assembly.delete()

                    if affected_bundle_ids:
                        unit_input.objects.filter(
                            job_no__iexact=first_row.get('job_no'),
                            tb_id=first_row.get('tb_id'),
                            bundle_id__in=affected_bundle_ids,
                        ).update(scan=False)

                    existing_group.update(verify=False)
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
                    dep.or_only = bool(row.get('or_only', 0))
                    dep.verify = False
                    dep.verify_user = None
                    dep.verify_date = None
                    dep.date = timezone.now()
                    dep.save()

                    # The submitted selection is the complete current selection.
                    dep.data_entries.all().delete()
                    selected_groups = (
                        (
                            row.get('and_selected_processes')
                            or row.get('selected_processes')
                            or [],
                            True,
                            False,
                        ),
                        (row.get('or_selected_processes') or [], False, True),
                    )
                    entries = []
                    for selected_processes, and_data, or_data in selected_groups:
                        for index, selected in enumerate(selected_processes, start=1):
                            entries.append(dependency_data(
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
                                and_data=and_data,
                                or_data=or_data,
                                date=timezone.now(),
                            ))
                    dependency_data.objects.bulk_create(entries)
                    saved_count += 1
            return JsonResponse(
                {
                    "message":
                    "Data saved successfully",
                    "count":
                    saved_count,
                    "edited": edit_confirmed,
                    "deleted_assembly_rows": deleted_assembly_count,
                    "affected_processes": affected_process_names,
                    "affected_bundle_count": len(affected_bundle_ids),
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_process_dependency(request):
    try:
        data = request.data
        # username = str(data.get('username', '')).strip()
        password = data.get('password', '')
        if password != 'admin':
            return JsonResponse({"error": "Invalid admin credentials"}, status=403)

        job_no = data.get('job_no')
        tb_id = data.get('tb_id')
        verifier_username = request.user.get_username()
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
            updated = dependencies.update(
                verify=True,
                verify_user=verifier_username,
                verify_date=timezone.now(),
            )

        print(f"username {verifier_username} verified {updated} dependencies for job_no {job_no} and tb_id {tb_id}")

        return JsonResponse({
            "message": "Verified successfully",
            "count": updated,
            "verify_user": verifier_username,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_process_dependency(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        if not isinstance(data, dict) or data.get("password") != "12345":
            return JsonResponse({"error": "Invalid password"}, status=403)

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


################################# Preporatory Entry API #################################

@api_view(['POST'])
def preporatory_entry_details(request):
    jobno = request.data.get('jobno')
    topbottom = request.data.get('topbottom')

    if not jobno or not topbottom:
        return Response(
            {"error": "Jobno and TopBottom required"},
            status=400
        )
        
    with connections['demo'].cursor() as cursor:
        # 1. sp_GetProcessDetails (Trn == 'R' filtering)
        cursor.execute(
            "EXEC sp_GetProcessDetails %s, %s",
            [jobno, topbottom]
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        result = []
        for row in rows:
            item = dict(zip(columns, row))
            trn = str(item.get('Trn', '') or '').strip().upper()
            if trn == 'R':
                item['Trn'] = trn
                result.append(item)

        # 2. sp_GetRibDef (preporatory_data)
        cursor.execute(
            "EXEC sp_GetRibDef %s, %s",
            [jobno, topbottom]
        )
        rib_columns = [col[0] for col in cursor.description]
        rib_rows = cursor.fetchall()
        preporatory_data = [dict(zip(rib_columns, row)) for row in rib_rows]

    saved_entries = list(PreporatoryEntry.objects.filter(
        jobno__iexact=jobno,
        topbottom__iexact=topbottom,
    ))
    saved_by_process = {
        entry.process.casefold(): entry
        for entry in saved_entries
    }
    for item in result:
        saved_entry = saved_by_process.get(str(item.get('Process_des') or '').casefold())
        item['saved_selected_processes'] = (
            saved_entry.selected_processes or "" if saved_entry else ""
        )
        item['elastic_status'] = bool(saved_entry.elastic_status) if saved_entry else False

    # Rendu data-vum orae response-la anupprom
    return Response({
        "details": result,
        "preporatory_data": preporatory_data,
        "has_saved_data": bool(saved_entries),
    })

@api_view(["POST"])
def save_preporatory_dependency(request):
  jobno = request.data.get("jobno")
  topbottom = request.data.get("topbottom")
  items = request.data.get("items", [])

  if not jobno or not topbottom:
    return Response(
        {"error": "Job Number and Top/Bottom are required!"},
        status=status.HTTP_400_BAD_REQUEST,
    )

  try:
    for item in items:
      process_name = item.get(
          "process"
      )  # React-lendaru vara process description name
      selected_processes = item.get("selected_processes", "")
      if isinstance(selected_processes, list):
        selected_processes = selected_processes[0] if selected_processes else ""
      if not isinstance(selected_processes, str):
        return Response(
            {"error": "Selected part must be a character value."},
            status=status.HTTP_400_BAD_REQUEST,
        )
      elastic_status = item.get("elastic_status", False)

      if process_name:
        PreporatoryEntry.objects.update_or_create(
            jobno=jobno,
            topbottom=topbottom,
            process=process_name,
            defaults={
                "selected_processes": selected_processes,
                "elastic_status": elastic_status,
            },
        )

    return Response(
        {"message": "Configurations saved successfully!"},
        status=status.HTTP_200_OK,
    )

  except Exception as e:
    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def delete_preporatory_dependency(request):
    jobno = request.data.get("jobno")
    topbottom = request.data.get("topbottom")

    if not jobno or not topbottom:
        return Response(
                {"error": "Job Number and Top/Bottom are required!"},
                status=status.HTTP_400_BAD_REQUEST,
        )

    deleted_count, _ = PreporatoryEntry.objects.filter(
            jobno__iexact=jobno,
            topbottom__iexact=topbottom,
    ).delete()
    return Response({
            "message": "Configuration deleted successfully!",
            "count": deleted_count,
    }, status=status.HTTP_200_OK)





# 1. Get Distinct Unit Names
@api_view(['GET'])
def get_units(request):
    units = ViewRibdelPreparatory.objects.values_list('unitname', flat=True).distinct()
    return Response(list(units))

# 2. Get Job Nos based on UnitName
@api_view(['GET'])
def get_jobnos_by_unit(request):
    unitname = request.GET.get('unitname')
    jobnos = ViewRibdelPreparatory.objects.filter(unitname=unitname).values_list('jobno', flat=True).distinct()
    return Response(list(jobnos))

# 3. Get TopBottom Des based on UnitName & JobNo
@api_view(['GET'])
def get_topbottom_by_unit_job(request):
    unitname = request.GET.get('unitname')
    jobno = request.GET.get('jobno')
    topbottoms = ViewRibdelPreparatory.objects.filter(unitname=unitname, jobno=jobno).values_list('topbottom_des', flat=True).distinct()
    return Response(list(topbottoms))

# 4. Get Table Data based on UnitName, JobNo, TopBottom_des
@api_view(['GET'])
def get_table_data(request):
    unitname = request.GET.get('unitname')
    jobno = request.GET.get('jobno')
    topbottom_des = request.GET.get('topbottom_des')
    
    records = list(ViewRibdelPreparatory.objects.filter(
        unitname=unitname, jobno=jobno, topbottom_des=topbottom_des
    ).values())

    entered_totals = {
        (
            entry["jobno"],
            entry["topbottom_des"],
            entry["clrcomb"],
            entry["siz"],
            entry["lotno"],
        ): entry["entered_total"] or 0
        for entry in RibdelEntry.objects.filter(
            jobno=jobno,
            topbottom_des=topbottom_des,
        ).values(
            "jobno",
            "topbottom_des",
            "clrcomb",
            "siz",
            "lotno",
        ).annotate(entered_total=Sum("entered_qty"))
    }
    for record in records:
        record["total_qty"] = record["delpc"] or 0
        entry_key = (
            record["jobno"],
            record["topbottom_des"],
            record["clrcomb"],
            record["siz"],
            record["lotno"],
        )
        record["available_qty"] = max(
            record["total_qty"] - entered_totals.get(entry_key, 0),
            0,
        )

    return Response(records)

# 5. Save Row Entry
@api_view(['POST'])
def save_table_entry(request):
    data = request.data
    employee_id = str(data.get('employee_id') or '').strip()
    rowno = data.get('rowno')
    try:
        entered_qty = int(data.get('entered_qty', 0))
    except (TypeError, ValueError):
        return Response({'error': 'Entered quantity must be a whole number.'}, status=400)

    if not employee_id:
        return Response({'error': 'Employee is required.'}, status=400)
    
    try:
        row_item = ViewRibdelPreparatory.objects.get(rowno=rowno)
    except ViewRibdelPreparatory.DoesNotExist:
        return Response({'error': 'Record not found!'}, status=404)
        
    total_qty = row_item.delpc or 0
    entry_filter = {
        "jobno": row_item.jobno,
        "topbottom_des": row_item.topbottom_des,
        "clrcomb": row_item.clrcomb,
        "siz": row_item.siz,
        "lotno": row_item.lotno,
    }
    entered_total = RibdelEntry.objects.filter(
        **entry_filter
    ).aggregate(total=Sum('entered_qty'))['total'] or 0
    available_qty = max(total_qty - entered_total, 0)
    
    if entered_qty <= 0:
        return Response({'error': 'Negative or zero entry is not allowed!'}, status=400)
    if entered_qty > available_qty:
        return Response(
            {'error': f'Entered quantity cannot exceed Available Delpc ({available_qty})!'},
            status=400,
        )
        
    RibdelEntry.objects.create(
        employee_id=employee_id,
        jobno=row_item.jobno,
        topbottom_des=row_item.topbottom_des,
        clrcomb=row_item.clrcomb,
        siz=row_item.siz,
        lotno=row_item.lotno,
        total_qty=total_qty,
        entered_qty=entered_qty
    )
    
    return Response({
        'message': f'Successfully saved entry for Row {row_item.rowno}!',
        'total_qty': total_qty,
        'available_qty': available_qty - entered_qty,
    })
    

################################# Unit Permission API #################################


@method_decorator(csrf_exempt, name="dispatch")
class UserUnitPermissionView(View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        app = request.GET.get("app")
        if not user_id:
            return JsonResponse({
                "success": False,
                "message": "User is required"
            }, status=400)
        if not app:
            return JsonResponse({
                "success": False,
                "message": "App is required"
            }, status=400)
        permissions = user_unit_permission.objects.filter(
            user_id=user_id,
            app=app
        ).values_list(
            "unit_id",
            flat=True
        )
        return JsonResponse({
            "success": True,
            "user_id": int(user_id),
            "app": app,
            "unit_ids": list(permissions)
        })
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            app = data.get("app")
            unit_ids = data.get("unit_ids", [])
            if not user_id:
                return JsonResponse({
                    "success": False,
                    "message": "User is required"
                }, status=400)
            if app not in dict(user_unit_permission.APP_CHOICES):
                return JsonResponse({
                    "success": False,
                    "message": "Invalid app"
                }, status=400)
            user = User.objects.filter(
                id=user_id
            ).first()
            if not user:
                return JsonResponse({
                    "success": False,
                    "message": "User not found"
                }, status=404)

            units = Unit.objects.filter(
                id__in=unit_ids
            )
            valid_unit_ids = list(
                units.values_list("id", flat=True)
            )

            with transaction.atomic():
                user_unit_permission.objects.filter(
                    user_id=user_id,
                    app=app
                ).delete()
                permission_data = []

                for unit_id in valid_unit_ids:

                    permission_data.append(
                        user_unit_permission(
                            user_id=user_id,
                            app=app,
                            unit_id=unit_id
                        )
                    )
                user_unit_permission.objects.bulk_create(
                    permission_data
                )
            return JsonResponse({
                "success": True,
                "message": "Permission saved successfully",
                "user_id": user_id,
                "app": app,
                "unit_ids": valid_unit_ids
            })
        except Exception as e:

            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class UserListView(View):

    def get(self, request):

        users = User.objects.filter(
            is_active=True
        ).values(
            "id",
            "username",
            "first_name",
            "last_name"
        )

        return JsonResponse(
            list(users),
            safe=False
        )

@method_decorator(csrf_exempt, name="dispatch")
class UnitListView(View):

    def get(self, request):

        units = Unit.objects.all().values(
            "id",
            "name"
        )

        return JsonResponse(
            list(units),
            safe=False
        )


@method_decorator(csrf_exempt, name="dispatch")
class UserUnitPermissionListView(View):
    def get(self, request):
        try:
            permissions = user_unit_permission.objects.select_related('user').all()
            
            # Grouping or listing raw permissions nicely
            data = []
            # Or group by user and app
            grouped = {}
            for p in permissions:
                key = (p.user_id, p.app)
                if key not in grouped:
                    grouped[key] = {
                        "user_id": p.user_id,
                        "username": p.user.username if p.user else "",
                        "app": p.app,
                        "unit_ids": []
                    }
                grouped[key]["unit_ids"].append(p.unit_id)
                
            return JsonResponse({
                "success": True,
                "results": list(grouped.values())
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)


################################### End of Unit Permission API #################################

##################### Bundle Transfer API ########################

class GetJobsView(APIView):
    def get(self, request):
        jobs = Assembly_data.objects.values_list('job_no',flat=True).distinct().order_by('job_no')
        return Response(list(jobs))

class GetTbNamesView(APIView):
    def get(self, request):
        job_no = request.GET.get('job_no')
        tb_names = Assembly_data.objects.filter(job_no=job_no).values_list('tb_name', flat=True).distinct().order_by('tb_name')
        return Response(list(tb_names))

class GetColorsView(APIView):
    def get(self, request):
        job_no = request.GET.get('job_no')
        tb_name = request.GET.get('tb_name')
        colors = Assembly_data.objects.filter(job_no=job_no, tb_name=tb_name).values_list('color', flat=True).distinct().order_by('color')
        return Response(list(colors))

class GetSizesView(APIView):
    def get(self, request):
        job_no = request.GET.get('job_no')
        tb_name = request.GET.get('tb_name')
        color = request.GET.get('color')
        sizes = Assembly_data.objects.filter(job_no=job_no, tb_name=tb_name, color=color).values_list('size', flat=True).distinct().order_by('size')
        return Response(list(sizes))

class GetSequencesView(APIView):
    def get(self, request):
        job_no = request.GET.get('job_no')
        tb_name = request.GET.get('tb_name')
        color = request.GET.get('color')
        size = request.GET.get('size')
        
        sequences = Assembly_data.objects.filter(
            job_no=job_no, 
            tb_name=tb_name,
            color=color,
            size=size,
            unit_transfer=False
        ).values('id', 'seq', 'bundle_id', 'bdl_no', 'size', 'color', 'pc', 'scan').order_by('seq')
        
        return Response(list(sequences))

class SaveAssemblySelectionView(APIView):
    def post(self, request):
        selected_ids = request.data.get('selected_ids', [])
        unit_id = request.data.get('unit_id')
        line_id = request.data.get('line_id')

        if not isinstance(selected_ids, list) or not selected_ids:
            return Response({'error': 'No bundles selected for saving.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_ids = [int(selected_id) for selected_id in selected_ids]
            unit_id = int(unit_id)
            line_id = int(line_id)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Valid bundle, unit, and line selections are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Unit.objects.filter(pk=unit_id).exists():
            return Response({'error': 'Selected unit was not found.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Line.objects.filter(pk=line_id, unit_id=unit_id).exists():
            return Response(
                {'error': 'Selected line does not belong to the selected unit.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        unique_ids = set(selected_ids)
        with transaction.atomic():
            bundles = Assembly_data.objects.select_for_update().filter(id__in=unique_ids)
            if bundles.count() != len(unique_ids):
                return Response(
                    {'error': 'One or more selected bundles were not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )
            transfer_time = timezone.now()
            bundle_transfer.objects.bulk_create([
                bundle_transfer(
                    unit=unit_id,
                    line=line_id,
                    job_no=bundle.job_no,
                    tb_id=bundle.tb_id,
                    tb_name=bundle.tb_name,
                    machine=bundle.machine,
                    seq=bundle.seq,
                    date=transfer_time,
                    bundle_id=bundle.bundle_id,
                    bdl_no=bundle.bdl_no,
                    mbud=bundle.mbud,
                    size=bundle.size,
                    size_id=bundle.size_id,
                    color=bundle.color,
                    pc=bundle.pc,
                    entry_date=transfer_time,
                    lot=bundle.lot,
                    emp_id=bundle.emp_id,
                )
                for bundle in bundles
            ])
            Assembly_data.objects.filter(id__in=unique_ids).update(unit_transfer=True)

        return Response(
            {'success': True, 'message': 'Bundles transferred successfully!'},
            status=status.HTTP_200_OK,
        )
