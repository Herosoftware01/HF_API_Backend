from django.shortcuts import render
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ValidationError
from imp_reports.models import UnitBundlereport
from bundle_tracking.models import TrsMcutstickerprod,MasUnit,MasTopbottom
from qcapp.models import Unit,Line,machine_details,emp_allocate,Empwisesal
from .models import Assembly_data,ViewFabricfoldingRibdetails,ViewCuttingQtyDetailsLotUnit,ViewUnitFoldDeliveryDetails,ViewElasticCons,ViewCuttingQtyDetailsUnit,ViewOrdersummaryUnit,ViewCuttingQtyDetails,ViewOrdersummary,ViewAccessoryorderqtyElastic,elastic_cons,bundle_transfer,end_line_data, unit_input,ViewOrderdetails,sub_bundle_unit_transfer, Msizes,dependency,dependency_data,PreporatoryEntry,ViewRibdelPreparatory,RibdelEntry,VueCutPlnStat,Elastic_cutting_qty,Elastic_cutting_qty_details,ElasticDelivery,ElasticDeliveryDetails
from django.utils.dateparse import parse_date, parse_datetime
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
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.views import View
from .models import user_unit_permission
from herofashion.models import User
from qcapp.models import Unit
from django.db.models import Sum, IntegerField, Value
from django.db.models.functions import Cast, Coalesce
import json
from django.db import connection, transaction
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .models import (
    folding_data,
    folding_data_details,
    Rope_cutting_data,
    Rope_cutting_data_details,
)


# @require_GET
# def live_scan_data(request):
   
#     trs_data = TrsMcutstickerprod.objects.using("demo").filter(
#         scan="1",
#         livescan__isnull=True
#     ).order_by('jobno','tbid','comboclr','lotno','sizid','bdl')

#     tbid_list = {row.tbid for row in trs_data if row.tbid}
#     tob_bottom_map = {
#         str(item.topbottom_id): item.topbottom_des 
#         for item in MasTopbottom.objects.using("main").filter(topbottom_id__in=tbid_list)
#     }
#     sizeid_list = {row.sizid for row in trs_data if row.sizid}
#     size_map = {
#         str(item.id): item.name
#         for item in Msizes.objects.using("test").filter(id__in=sizeid_list)
#     }


#     mbud_list = [str(row.mbud) for row in trs_data]
   
#     reports = UnitBundlereport.objects.using("app").filter(
#         mbundle_id__in=mbud_list
#     )
    
#     report_map = {str(r.mbundle_id): r for r in reports}
    
#     unit_ids = {int(r.unit_id) for r in trs_data if r.unit_id}
#     unit_name_map = {
#         str(u.unitcode): u.unitname 
#         for u in MasUnit.objects.using("main").filter(unitcode__in=unit_ids)
#     }
    
#     final_data = {}
    
#     for row in trs_data:
#         report = report_map.get(str(row.mbud))
        
#         uid = str(report.unit_id) if report else "0"
#         u_name = unit_name_map.get(uid, "Unknown Unit")
        
#         if uid not in final_data:
#             final_data[uid] = {
#                 "unit_id": uid,
#                 "unit_name": u_name,
#                 "total_records": 0,
#                 "data": []
#             }
            
#         final_data[uid]["total_records"] += 1
        
#         final_data[uid]["data"].append({
#             "dt": row.dt,
#             "empid": row.empid,
#             "mbud": row.mbud,
#             "bundid": row.bundid,
#             "jobno": row.jobno,
#             "tbid": row.tbid,
#             "tbid_name": tob_bottom_map.get(str(row.tbid), "N/A"),
#             "bdl": row.bdl,
#             "comboclr": row.comboclr,
#             "sizid": row.sizid,
#             "sizid_name": size_map.get(str(row.sizid), "N/A"),
#             "pc": row.pc,
#             "total_bundles": report.total_bundles if report else 0,
#             "pcs_count": report.pcs_count if report else 0,
#             "lot": row.lotno,
#         })

#     return JsonResponse({
#         "status": True,
#         "unit_count": len(final_data),
#         "all_unit_data_count": sum(unit["total_records"] for unit in final_data.values()), # இது 6305 ஆக இருக்கும்
#         "data": list(final_data.values())
#     })


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
    
    # 1. TrsMcutstickerprod-la iruka unit_id-a base panni unit_ids edukrom
    unit_ids = {int(row.unit_id) for row in trs_data if row.unit_id is not None}
    unit_name_map = {
        str(u.unitcode): u.unitname 
        for u in MasUnit.objects.using("main").filter(unitcode__in=unit_ids)
    }
    
    final_data = {}
    
    for row in trs_data:
        report = report_map.get(str(row.mbud))
        
        # 2. Report-ku bathila TrsMcutstickerprod table-oda unit_id-a uid-ah use panrom
        uid = str(row.unit_id) if row.unit_id is not None else "0"
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
        "all_unit_data_count": sum(unit["total_records"] for unit in final_data.values()),
        "data": list(final_data.values())
    })


def get_bundle_detail(request, bundid):
    try:
        # 1. Muthalil antha bundid database-la irukka nu check panrom (filters illamal)
        bundle = TrsMcutstickerprod.objects.using('demo').filter(bundid=bundid).first()

        if not bundle:
            return JsonResponse({'error': 'Bundle ID not found!'}, status=404)

        # 2. Condition check: livescan = 1 iruntha already unit input complete
        if bundle.livescan == '1' or bundle.livescan == 1:  # String or Integer handling
            return JsonResponse({'error': 'Bundle already unit input completed!'}, status=400)

        # 3. Condition check: scan = 0 iruntha bundle not scanned by unit
        if bundle.scan == '0' or bundle.scan == 0:
            return JsonResponse({'error': 'Bundle not scanned by unit!'}, status=400)

        # 4. Ellam correct-ah iruntha details-a return panrom
        data = {
            'bundid': bundle.bundid,
            'jobno': bundle.jobno,
            'comboclr': bundle.comboclr,
            'sizid': bundle.sizid,
            'bdl': bundle.bdl,
            'pc': bundle.pc,
            'unit_id': bundle.unit_id,
            'weight': float(bundle.weight) if bundle.weight else None,
            'lotno': bundle.lotno,
        }
        return JsonResponse(data, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def transfer_bundles(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    try:
        data = json.loads(request.body)

        bundids = data.get("bundids", [])
        unit_name_or_code = data.get("unit_id") # React-il irunthu varura Unit Name or Code

        print(f"bundle ids {bundids} and target unit input {unit_name_or_code}")

        if not bundids or not unit_name_or_code:
            return JsonResponse(
                {"error": "Invalid data provided"},
                status=400
            )

        # 1. MasUnit table-la target unitcode-a find panrom
        unit_obj = MasUnit.objects.using("main").filter(
            unitname=unit_name_or_code
        ).first()

        if not unit_obj:
            unit_obj = MasUnit.objects.using("main").filter(
                unitcode=unit_name_or_code
            ).first()

        if not unit_obj:
            return JsonResponse({"error": "Selected unit not found in database!"}, status=404)

        target_unit_code = unit_obj.unitcode  # New To Unit Code

        updated_count = 0
        current_time = datetime.now()

        # 2. Ovvoru bundle-kum loop panrom
        for bundid in bundids:
            bundle = TrsMcutstickerprod.objects.using("demo").filter(bundid=bundid).first()
            
            if bundle:
                old_unit_id = bundle.unit_id  # Current unit_id becomes from_unit
                
                # TrsMcutstickerprod table update: unit_id and unit_trs = 1
                bundle.unit_id = target_unit_code
                bundle.unit_trs = 1  # True / 1
                bundle.save(using="demo")
                
                # sub_bundle_unit_transfer table-la ONLY CREATE (No update, logs every transfer)
                sub_bundle_unit_transfer.objects.create(
                    bundle_id=bundid,
                    from_unit=old_unit_id if old_unit_id is not None else 0,
                    to_unit=target_unit_code,
                    date=current_time
                )
                updated_count += 1

        return JsonResponse({
            "message": "Transferred successfully and history logged",
            "updated_count": updated_count,
            "assigned_unitcode": target_unit_code
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    

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
                    parsed_date_only = parse_date(raw_date) if not parsed_date else None

                    if parsed_date:
                        # Frontend date already IST (13:34)
                        if timezone.is_aware(parsed_date):
                            final_date = parsed_date.replace(tzinfo=None)
                        else:
                            final_date = parsed_date
                    elif parsed_date_only:
                        final_date = datetime.combine(parsed_date_only, datetime.min.time())
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
                            date=final_date,
                            emp_id=item.get('emp_id', ''),
                            reject_pcs=item.get('reject_pc'),
                            rework_pcs=item.get('rework_pc'),
                            ok_pcs=item.get('ok_pc'),
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


def get_transfer_unit_and_line(unit, line=None):
    unit_obj = Unit.objects.filter(name__iexact=f"unit-{unit}").only('id').first()
    if not unit_obj:
        return None, None
    if line is None:
        return unit_obj.id, None
    line_id = Line.objects.filter(
        unit_id=unit_obj.id,
        line_number=line,
    ).values_list('id', flat=True).first()
    return unit_obj.id, line_id


def get_eligible_assembly_bundle_ids(job_no, process_des, top_bottom=None, unit=None):
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
        return True, set(), None

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
    completed_query = Assembly_data.objects.filter(
        job_no__iexact=job_no,
        unit_transfer=False,
    )
    transfer_unit_id = None
    if unit is not None:
        completed_query = completed_query.filter(unit=unit)
        transfer_unit_id, _ = get_transfer_unit_and_line(unit)
    if top_bottom:
        completed_query = completed_query.filter(tb_name__iexact=top_bottom)
    completed_rows = list(completed_query.values_list('bundle_id', 'seq'))
    transferred_query = bundle_transfer.objects.filter(job_no__iexact=job_no)
    if unit is None or transfer_unit_id is None:
        transferred_query = transferred_query.none()
    else:
        transferred_query = transferred_query.filter(unit=transfer_unit_id)
    if top_bottom:
        transferred_query = transferred_query.filter(tb_name__iexact=top_bottom)
    completed_rows.extend(transferred_query.values_list('bundle_id', 'seq'))
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
            "Bundle not available for the current process.\n" 
            + "; ".join(requirement_details),
        )
        # return (
        #     False,
        #     set(),
        #     "Previous process requirements are not complete for any bundle. "
        #     + "; ".join(requirement_details),
        # )

    return True, eligible_bundle_ids, None


def assembly_dependencies_satisfied(completed_sequences, and_sequences, or_sequences):
    and_requirements_met = and_sequences.issubset(completed_sequences)
    or_requirements_met = (
        not or_sequences or not completed_sequences.isdisjoint(or_sequences)
    )
    return and_requirements_met and or_requirements_met


def assembly_process_stock_available(
    completed_sequences,
    process_name,
    and_sequences,
    or_sequences,
):
    process_is_complete = str(process_name or '').strip().casefold() in completed_sequences
    return (
        not process_is_complete
        and assembly_dependencies_satisfied(
            completed_sequences,
            and_sequences,
            or_sequences,
        )
    )


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


def get_already_assembled_bundle_ids(job_no, unit, process_des, top_bottom=None):
    assembly_rows = Assembly_data.objects.filter(
        job_no__iexact=job_no,
        unit=unit,
        unit_transfer=False,
    ).filter(assembly_sequence_filter(process_des))
    if top_bottom:
        assembly_rows = assembly_rows.filter(tb_name__iexact=top_bottom)
    bundle_ids = set(assembly_rows.values_list('bundle_id', flat=True))

    transfer_unit_id, _ = get_transfer_unit_and_line(unit)
    if transfer_unit_id is None:
        return bundle_ids
    transferred_rows = bundle_transfer.objects.filter(
        job_no__iexact=job_no,
        unit=transfer_unit_id,
    ).filter(assembly_sequence_filter(process_des))
    if top_bottom:
        transferred_rows = transferred_rows.filter(tb_name__iexact=top_bottom)
    bundle_ids.update(transferred_rows.values_list('bundle_id', flat=True))
    return bundle_ids


def get_eligible_assembly_bundle_ids_for_processes(
    job_no,
    process_des,
    top_bottom=None,
    unit=None,
):
    process_descriptions = split_process_descriptions(process_des)
    if not process_descriptions:
        return False, None, "Process sequence is required."

    eligible_bundle_ids = set()
    all_bundles_eligible = False
    errors = []
    for description in process_descriptions:
        allowed, bundle_ids, error_message = get_eligible_assembly_bundle_ids(
            job_no, description, top_bottom, unit
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
    if not errors:
        return True, None, None
    return False, set(), " ".join(dict.fromkeys(errors))


def get_assembly_dependency_statuses(job_no, process_des, top_bottom=None):
    statuses = []
    for description in split_process_descriptions(process_des):
        dependency_query = dependency.objects.filter(
            job_no__iexact=job_no,
            process_des__iexact=description,
        )
        if top_bottom:
            top_bottom_filter = Q(tb_name__iexact=top_bottom)
            if str(top_bottom).strip().isdigit():
                top_bottom_filter |= Q(tb_id=int(str(top_bottom).strip()))
            dependency_query = dependency_query.filter(top_bottom_filter)
        process_dependency = dependency_query.order_by('-id').first()
        statuses.append({
            "process": description,
            "verified": bool(process_dependency and process_dependency.verify),
        })
    return statuses


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
            print("date filter applied:", data.query)

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
                dependency_statuses = get_assembly_dependency_statuses(
                    job_no, process_des, top_bottom
                )
                unverified_processes = [
                    item["process"]
                    for item in dependency_statuses
                    if not item["verified"]
                ]
                if unverified_processes:
                    return Response({
                        "status": True,
                        "data": [],
                        "dependency_statuses": dependency_statuses,
                        "message": (
                            "Dependency not verified for: "
                            + ", ".join(unverified_processes)
                        ),
                    })

                allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids_for_processes(
                    job_no, process_des, top_bottom, unit
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = get_already_assembled_bundle_ids(
                    job_no,
                    unit,
                    process_des,
                    top_bottom,
                )
                data = data.filter(job_no__iexact=job_no)
                if top_bottom:
                    data = data.filter(tb_name__iexact=top_bottom)
                data = data.exclude(bundle_id__in=already_scanned_ids)
                if eligible_bundle_ids is not None:
                    data = data.filter(bundle_id__in=eligible_bundle_ids)
                results = list(data.values(
                    'bundle_id', 'mbud', 'job_no', 'color', 'bdl_no', 'size',
                    'tb_name', 'pc', 'entry_date',
                ))

                transfer_unit_id, transfer_line_id = get_transfer_unit_and_line(unit, line)
                if transfer_unit_id is not None and transfer_line_id is not None:
                    transferred = bundle_transfer.objects.filter(
                        unit=transfer_unit_id,
                        line=transfer_line_id,
                        job_no__iexact=job_no,
                    )
                    if top_bottom:
                        transferred = transferred.filter(tb_name__iexact=top_bottom)
                    transferred = transferred.exclude(bundle_id__in=already_scanned_ids)
                    if eligible_bundle_ids is not None:
                        transferred = transferred.filter(bundle_id__in=eligible_bundle_ids)

                    existing_bundle_ids = {row['bundle_id'] for row in results}
                    for row in transferred.values(
                        'bundle_id', 'mbud', 'job_no', 'color', 'bdl_no', 'size',
                        'tb_name', 'pc', 'entry_date',
                    ):
                        if row['bundle_id'] not in existing_bundle_ids:
                            results.append(row)
                            existing_bundle_ids.add(row['bundle_id'])
                return Response({
                    "status": True,
                    "data": results,
                    "dependency_statuses": dependency_statuses,
                })
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
                    job_no, process_des, top_bottom, unit
                )
                if not allowed:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_409_CONFLICT
                    )
                already_scanned_ids = get_already_assembled_bundle_ids(
                    job_no,
                    unit,
                    process_des,
                    top_bottom,
                )
                data = data.filter(job_no__iexact=job_no)
                if top_bottom:
                    data = data.filter(tb_name__iexact=top_bottom)
                data = data.exclude(bundle_id__in=already_scanned_ids)
                if eligible_bundle_ids is not None:
                    data = data.filter(bundle_id__in=eligible_bundle_ids)
                results = list(data.values(
                    'bundle_id', 'mbud', 'job_no', 'color', 'bdl_no', 'size',
                    'tb_name', 'pc', 'entry_date',
                ))
                transfer_unit_id, transfer_line_id = get_transfer_unit_and_line(unit, line)
                if transfer_unit_id is not None and transfer_line_id is not None:
                    transferred = bundle_transfer.objects.filter(
                        unit=transfer_unit_id,
                        # line=transfer_line_id,
                        job_no__iexact=job_no,
                    )
                    if top_bottom:
                        transferred = transferred.filter(tb_name__iexact=top_bottom)
                    transferred = transferred.exclude(bundle_id__in=already_scanned_ids)
                    if eligible_bundle_ids is not None:
                        transferred = transferred.filter(bundle_id__in=eligible_bundle_ids)

                    result_ids = {row['bundle_id'] for row in results}
                    for row in transferred.values(
                        'bundle_id', 'mbud', 'job_no', 'color', 'bdl_no', 'size',
                        'tb_name', 'pc', 'entry_date',
                    ):
                        if row['bundle_id'] not in result_ids:
                            results.append(row)
                            result_ids.add(row['bundle_id'])
                return Response({"status": True, "data": results})
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


# class GetUnitDataAPIViewsss(APIView):
#     def get(self, request):
#         unit = request.query_params.get('unit')
#         line = request.query_params.get('line')
#         job_no = request.query_params.get('job_no')
#         process_des = request.query_params.get('process_des')
#         top_bottom = str(request.query_params.get('top_bottom', '') or '').strip()
#         selected_date = request.query_params.get('date') 

#         if selected_date:
#             date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
#             # data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj).order_by('-entry_date')
#             data = unit_input.objects.filter(unit=unit, entry_date__date=date_obj).order_by('-entry_date')
#         else:
#             # four_days_ago = datetime.now() - timedelta(days=1)
#             today = date.today()
#             print("Today's date:", today)
#             # data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=today).order_by('-entry_date')
#             data = unit_input.objects.filter(unit=unit, entry_date__date=today).order_by('-entry_date')

#         if job_no is not None:
#             job_no = job_no.strip()
#             if not job_no:
#                 return Response(
#                     {"error": "job_no is required to load assembly bundles"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             if process_des is not None:
#                 process_des = process_des.strip()
#                 if not top_bottom:
#                     return Response(
#                         {"error": "top_bottom is required to load assembly bundles"},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#                 allowed, eligible_bundle_ids, error_message = get_eligible_assembly_bundle_ids(
#                     job_no, process_des, top_bottom
#                 )
#                 if not allowed:
#                     return Response(
#                         {"error": error_message},
#                         status=status.HTTP_409_CONFLICT
#                     )
#                 already_scanned_ids = Assembly_data.objects.filter(
#                     job_no__iexact=job_no,
#                     seq__iexact=process_des,
#                 ).values_list('bundle_id', flat=True)
#                 data = data.filter(job_no__iexact=job_no)
#                 if top_bottom:
#                     data = data.filter(tb_name__iexact=top_bottom)
#                 data = data.exclude(bundle_id__in=already_scanned_ids)
#                 if eligible_bundle_ids is not None:
#                     data = data.filter(bundle_id__in=eligible_bundle_ids)
#             else:
#                 verified_tb_ids = dependency.objects.filter(
#                     job_no__iexact=job_no,
#                     verify=True
#                 ).values_list('tb_id', flat=True)
#                 data = data.filter(
#                     job_no__iexact=job_no,
#                     tb_id__in=verified_tb_ids,
#                     scan=False,
#                 )

#         # JSON response
#         results = list(data.values('bundle_id','mbud', 'job_no','color','bdl_no','size','tb_name', 'pc', 'color', 'entry_date'))
#         return Response({"status": True, "data": results})



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
                unit=unit,scan=False
            ).order_by('-date')
        elif selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            data = Assembly_data.objects.filter(
                unit=unit,
                scan=False,
                date__date=date_obj,
            ).order_by('-date')
        else:
            data = Assembly_data.objects.filter(
                unit=unit,
                scan=False,
                date__gte=date.today(),
            ).order_by('-date')

        results = list(data.values(
            'bundle_id', 'bdl_no', 'job_no', 'seq', 'pc', 'color', 'date','tb_name',
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
        'id',
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
        allocate_id = request.data.get('allocate_id')
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
            job_no, process_des, selected_top_bottom, unit
        )
        if not allowed:
            return Response(
                {"error": error_message},
                status=status.HTTP_409_CONFLICT
            )

        unique_ids = list(dict.fromkeys(str(value).strip() for value in bundle_ids if str(value).strip()))
        if not unique_ids:
            return Response(
                {"error": "At least one valid bundle is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if eligible_bundle_ids is not None:
            ineligible_ids = [value for value in unique_ids if value not in eligible_bundle_ids]
            if ineligible_ids:
                return Response(
                    {"error": "Previous process is not complete for some bundles.", "bundle_ids": ineligible_ids},
                    status=status.HTTP_409_CONFLICT
                )

        with transaction.atomic():
            already_scanned_ids = get_already_assembled_bundle_ids(
                job_no,
                unit,
                process_des,
                selected_top_bottom,
            )
            input_queryset = unit_input.objects.select_for_update().filter(
                unit=unit,
                job_no__iexact=job_no,
                bundle_id__in=unique_ids,
            )
            if selected_top_bottom:
                input_queryset = input_queryset.filter(tb_name__iexact=selected_top_bottom)
            input_queryset = input_queryset.exclude(bundle_id__in=already_scanned_ids)
            input_bundles = list(input_queryset)

            transfer_unit_id, transfer_line_id = get_transfer_unit_and_line(unit, line)
            transfer_bundles = []
            if transfer_unit_id is not None and transfer_line_id is not None:
                transfer_queryset = bundle_transfer.objects.select_for_update().filter(
                    unit=transfer_unit_id,
                    # line=transfer_line_id,
                    job_no__iexact=job_no,
                    bundle_id__in=unique_ids,
                ).exclude(bundle_id__in=already_scanned_ids)
                if selected_top_bottom:
                    transfer_queryset = transfer_queryset.filter(tb_name__iexact=selected_top_bottom)
                transfer_bundles = list(transfer_queryset.order_by('-entry_date'))

            bundles_by_id = {bundle.bundle_id: bundle for bundle in transfer_bundles}
            for bundle in input_bundles:
                bundles_by_id.setdefault(bundle.bundle_id, bundle)
            found_ids = set(bundles_by_id)
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
                    entry_mode=entry_mode,
                    allocate_id=allocate_id,
                )
                for bundle, description in bundle_process_pairs(
                    [bundles_by_id[bundle_id] for bundle_id in unique_ids],
                    process_des,
                )
            ])
            # with connections['demo'].cursor() as cursor:
            #     for bundle_id in unique_ids:
            #         cursor.execute(
            #             "EXEC dbo.sp_CheckBundleProcessScan @BDLID = %s",
            #             [str(bundle_id)]
            #         )
            #         print(f"Executed sp_CheckBundleProcessScan for bundle {bundle_id}.")
            input_bundle_ids = {
                bundle.bundle_id
                for bundle in input_bundles
                if bundles_by_id[bundle.bundle_id] is bundle
            }
            updated = input_queryset.filter(bundle_id__in=input_bundle_ids).update(scan=True)

        return Response({"status": "success", "updated": updated}, status=status.HTTP_200_OK)


save_assembly = SaveAssemblyAPIView.as_view()




@api_view(['POST'])
def get_process_details(request):
    jobno = request.data.get('jobno')
    topbottom = request.data.get('topbottom')
    include_saved_raw = request.data.get('include_saved', True)

    if isinstance(include_saved_raw, str):
        include_saved = include_saved_raw.strip().lower() not in {'false', '0', 'no'}
    else:
        include_saved = bool(include_saved_raw)

    if not jobno or not topbottom:
        return JsonResponse(
            {"error": "Jobno and TopBottom required"},
            status=400
        )
    result = []
    has_preparatory = False
        
    with connections['demo'].cursor() as cursor:
        cursor.execute(
            "EXEC sp_GetProcessDetails %s, %s",
            [jobno, topbottom]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        

        for row in rows:
            item = dict(zip(columns, row))

            # Trn = A / R mattum
            trn = str(
                item.get('Trn', '') or ''
            ).strip().upper()

            if trn in ('A', 'R'):
                item['Trn'] = trn
                result.append(item)
                if trn == 'R':
                    has_preparatory = True

        preporatory_data = []
        if has_preparatory:
            cursor.execute(
                "EXEC sp_GetRibDef %s, %s",
                [jobno, topbottom]
            )
            rib_columns = [col[0] for col in cursor.description]
            rib_rows = cursor.fetchall()
            preporatory_data = [dict(zip(rib_columns, row)) for row in rib_rows]

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

    if include_saved and latest_by_process:

        saved_result = []

        for index, dep in enumerate(
            reversed(list(latest_by_process.values())),
            start=1
        ):
            current_trn = trn_map.get(dep.process_id, '')
            saved_result.append({
                'Jobno': dep.job_no,
                'TopBottdes': dep.tb_name,
                'TbID': dep.tb_id,
                'sl': index,
                'Process_des': dep.process_des,
                'mc': dep.mc,
                'Part': dep.part,
                'thrd': dep.thrd,
                'preporatory_data': preporatory_data if current_trn == 'R' else [],

                'Trn': dep.trn or trn_map.get(
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
        item['preporatory_data'] = preporatory_data if item['Trn'] == 'R' else []
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

                        # deleted_assembly_count, _ = impacted_assembly.delete()
                        deleted_assembly_count = impacted_assembly.update(edit_data=1)

                    if affected_bundle_ids:
                        unit_input.objects.filter(
                            job_no__iexact=first_row.get('job_no'),
                            tb_id=first_row.get('tb_id'),
                            bundle_id__in=affected_bundle_ids,
                        ).update(scan=False)

                    existing_group.update(verify=False)
                group_already_exists = existing_group.exists()
                changed_process_keys = {
                    str(process_name or '').strip().casefold()
                    for process_name in changed_processes
                    if str(process_name or '').strip()
                }

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
                        process_key = str(row.get('process_des') or '').strip().casefold()
                        if group_already_exists and (
                            not edit_confirmed or process_key not in changed_process_keys
                        ):
                            continue
                        dep = dependency(**lookup)

                    dep.tb_name = row.get('tb_name')
                    dep.process_des = row.get('process_des')
                    dep.part = row.get('part')
                    dep.trn = row.get('trn')
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

# class GetJobsView(APIView):
#     def get(self, request):
#         jobs = Assembly_data.objects.values_list('job_no',flat=True).distinct().order_by('job_no')
#         return Response(list(jobs))

class GetJobsView(APIView):
    def get(self, request):
        unit = request.GET.get('unit')
        print(f"Received unit parameter: {unit}")  # Debugging line
        queryset = Assembly_data.objects.all()
        if unit:
            queryset = queryset.filter(unit=unit)
            
        jobs = queryset.values_list('job_no', flat=True).distinct().order_by('job_no')
        return Response(list(jobs))

class GetTbNamesView(APIView):
    def get(self, request):
        job_nos = request.GET.get('job_no', '')
        job_list = [j.strip() for j in job_nos.split(',') if j.strip()]
        tb_names = Assembly_data.objects.filter(job_no__in=job_list).values_list('tb_name', flat=True).distinct().order_by('tb_name')
        return Response(list(tb_names))

class GetColorsView(APIView):
    def get(self, request):
        job_nos = request.GET.get('job_no', '')
        tb_names = request.GET.get('tb_name', '')
        
        job_list = [j.strip() for j in job_nos.split(',') if j.strip()]
        tb_list = [t.strip() for t in tb_names.split(',') if t.strip()]
        
        colors = Assembly_data.objects.filter(
            job_no__in=job_list, 
            tb_name__in=tb_list
        ).values_list('color', flat=True).distinct().order_by('color')
        return Response(list(colors))

class GetSizesView(APIView):
    def get(self, request):
        job_nos = request.GET.get('job_no', '')
        tb_names = request.GET.get('tb_name', '')
        colors = request.GET.get('color', '')
        
        job_list = [j.strip() for j in job_nos.split(',') if j.strip()]
        tb_list = [t.strip() for t in tb_names.split(',') if t.strip()]
        color_list = [c.strip() for c in colors.split(',') if c.strip()]
        
        sizes = Assembly_data.objects.filter(
            job_no__in=job_list, 
            tb_name__in=tb_list, 
            color__in=color_list
        ).values_list('size', flat=True).distinct().order_by('size')
        return Response(list(sizes))

class GetSequencesView(APIView):
    def get(self, request):
        job_nos = request.GET.get('job_no', '')
        tb_names = request.GET.get('tb_name', '')
        colors = request.GET.get('color', '')
        sizes = request.GET.get('size', '')
        
        job_list = [j.strip() for j in job_nos.split(',') if j.strip()]
        tb_list = [t.strip() for t in tb_names.split(',') if t.strip()]
        color_list = [c.strip() for c in colors.split(',') if c.strip()]
        size_list = [s.strip() for s in sizes.split(',') if s.strip()]
        
        sequences = Assembly_data.objects.filter(
            job_no__in=job_list, 
            tb_name__in=tb_list,
            color__in=color_list,
            size__in=size_list,
            unit_transfer=False
        ).values('id', 'seq', 'bundle_id', 'bdl_no', 'size', 'color', 'pc', 'scan','job_no','tb_name').order_by('seq')
        
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



@api_view(['POST', 'GET'])
def get_stock_data_python(request):
    jobno = request.data.get('jobno') or request.GET.get('jobno')
    topbottom = request.data.get('topbottom') or request.GET.get('topbottom')
    print(f"Received jobno: {jobno}, topbottom: {topbottom}")  # Debugging line

    if not jobno or not topbottom:
        return JsonResponse(
            {"error": "jobno and topbottom are required parameters"},
            status=400
        )

    # 1. Fetch dependencies based on jobno and topbottom (tb_id or tb_name)
    dep_query = dependency.objects.filter(job_no__iexact=str(jobno).strip())
    if str(topbottom).strip().isdigit():
        dep_query = dep_query.filter(tb_id=int(topbottom))
    else:
        dep_query = dep_query.filter(tb_name__iexact=str(topbottom).strip())
    
    dependencies = list(dep_query)
    if not dependencies:
        return JsonResponse([], safe=False)

    valid_tb_ids = list(set(d.tb_id for d in dependencies))

    # 2. Fetch Tally sticker production records
    prod_records = TrsMcutstickerprod.objects.using('demo').filter(
        jobno__iexact=str(jobno).strip(),
        tbid__in=valid_tb_ids,
        livescan='1',
        scan=1
    )

    # 3. Map size names from mSizes
    size_ids = list(set(p.sizid for p in prod_records if p.sizid))
    sizes_map = {s.id: s.name for s in Msizes.objects.using('test').filter(id__in=size_ids)}

    # 4. Fetch assembly scan records for matching bundles
    assembly_records = Assembly_data.objects.filter(
        job_no__iexact=str(jobno).strip(),
        tb_id__in=valid_tb_ids
    )
    
    # Organize assembly scans into a dictionary: (job_no, tb_id, bundle_id) -> set of scanned seqs
    assembly_map = {}
    for asm in assembly_records:
        key = (asm.job_no.strip().upper(), asm.tb_id, asm.bundle_id.strip())
        if key not in assembly_map:
            assembly_map[key] = set()
        if asm.seq:
            assembly_map[key].add(asm.seq.strip())

    # 5. Fetch dependency data (AND / OR rules) for these dependencies
    dep_ids = [d.id for d in dependencies]
    dep_data_qs = dependency_data.objects.filter(dep_id_id__in=dep_ids)
    
    dep_rules = {}
    for d in dependencies:
        dep_rules[d.id] = {
            'dependency': d,
            'and_descs': [],
            'or_descs': []
        }
    
    for dd in dep_data_qs:
        if dd.dep_id_id in dep_rules:
            if dd.and_data:
                dep_rules[dd.dep_id_id]['and_descs'].append(dd.descriptions.strip())
            if dd.or_data:
                dep_rules[dd.dep_id_id]['or_descs'].append(dd.descriptions.strip())

    # 6. Process each bundle and calculate stock using python logic
    results = []
    for prod in prod_records:
        bundle_key = (prod.jobno.strip().upper(), prod.tbid, prod.bundid.strip())
        scanned_seqs = assembly_map.get(bundle_key, set())
        size_name = sizes_map.get(prod.sizid, str(prod.sizid))

        for dep_id, rules in dep_rules.items():
            dep_obj = rules['dependency']
            and_list = rules['and_descs']
            or_list = rules['or_descs']

            total_and = len(and_list)
            matched_and = sum(1 for desc in and_list if desc in scanned_seqs)

            total_or = len(or_list)
            matched_or = sum(1 for desc in or_list if desc in scanned_seqs)

            # Business Logic: AND must be fully matched, OR must have at least one match (if present)
            is_and_satisfied = (total_and == matched_and)
            is_or_satisfied = (total_or == 0 or matched_or > 0)

            if is_and_satisfied and is_or_satisfied:
                stock = 0
            else:
                stock = prod.pc

            results.append({
                "job_no": prod.jobno,
                "tb_id": prod.tbid,
                "tb_name": dep_obj.tb_name,
                "bundle_id": prod.bundid,
                "color": prod.comboclr,
                "size": size_name,
                "process_des": dep_obj.process_des,
                "stock": stock
            })

    return JsonResponse(results, safe=False, status=200)


@api_view(['POST', 'GET'])
def get_stock_summary_python(request):
    jobno = request.data.get('jobno') or request.GET.get('jobno')
    topbottom = request.data.get('topbottom') or request.GET.get('topbottom')

    if not jobno or not topbottom:
        return JsonResponse(
            {"error": "jobno and topbottom are required parameters"},
            status=400
        )

    # 1. Fetch dependencies based on jobno and topbottom (tb_id or tb_name)
    dep_query = dependency.objects.filter(job_no__iexact=str(jobno).strip())
    if str(topbottom).strip().isdigit():
        dep_query = dep_query.filter(tb_id=int(topbottom))
    else:
        dep_query = dep_query.filter(tb_name__iexact=str(topbottom).strip())
    
    dependencies = list(dep_query)
    if not dependencies:
        return JsonResponse([], safe=False)

    valid_tb_ids = list(set(d.tb_id for d in dependencies))

    # 2. Fetch Tally sticker production records for these TB IDs
    prod_records = list(TrsMcutstickerprod.objects.using('demo').filter(
        jobno__iexact=str(jobno).strip(),
        tbid__in=valid_tb_ids,
        livescan='1',
        scan=1
    ))

    if not prod_records:
        return JsonResponse([], safe=False)

    # 3. Fetch assembly scan records for matching bundles
    assembly_records = Assembly_data.objects.filter(
        job_no__iexact=str(jobno).strip(),
        tb_id__in=valid_tb_ids
    )
    
    assembly_map = {}
    for asm in assembly_records:
        key = (asm.job_no.strip().upper(), asm.tb_id, asm.bundle_id.strip())
        if key not in assembly_map:
            assembly_map[key] = set()
        if asm.seq:
            assembly_map[key].add(asm.seq.strip())

    # 4. Fetch dependency data (AND / OR rules)
    dep_ids = [d.id for d in dependencies]
    dep_data_qs = dependency_data.objects.filter(dep_id_id__in=dep_ids)
    
    dep_rules = {}
    for d in dependencies:
        dep_rules[d.id] = {
            'dependency': d,
            'and_descs': [],
            'or_descs': []
        }
    
    for dd in dep_data_qs:
        if dd.dep_id_id in dep_rules:
            if dd.and_data:
                dep_rules[dd.dep_id_id]['and_descs'].append(dd.descriptions.strip())
            if dd.or_data:
                dep_rules[dd.dep_id_id]['or_descs'].append(dd.descriptions.strip())

    # 5. Initialize summary dictionary per process_des
    process_summary = {}
    for d in dependencies:
        process_summary[d.id] = {
            "job_no": jobno,
            "tb_id": d.tb_id,
            "tb_name": d.tb_name,
            "process_des": d.process_des,
            "total_pieces": 0,
            "total_stock": 0
        }

    # 6. Iterate through all production bundles and accumulate stock per process
    for prod in prod_records:
        bundle_key = (prod.jobno.strip().upper(), prod.tbid, prod.bundid.strip())
        scanned_seqs = assembly_map.get(bundle_key, set())
        pc_val = prod.pc or 0

        for dep_id, rules in dep_rules.items():
            # Match production TBID with dependency TBID
            if prod.tbid != rules['dependency'].tb_id:
                continue

            and_list = rules['and_descs']
            or_list = rules['or_descs']

            total_and = len(and_list)
            matched_and = sum(1 for desc in and_list if desc in scanned_seqs)

            total_or = len(or_list)
            matched_or = sum(1 for desc in or_list if desc in scanned_seqs)

            is_and_satisfied = (total_and == matched_and)
            is_or_satisfied = (total_or == 0 or matched_or > 0)

            # Calculate stock for this bundle under this process
            bundle_stock = 0 if (is_and_satisfied and is_or_satisfied) else pc_val

            # Accumulate totals
            process_summary[dep_id]["total_pieces"] += pc_val
            process_summary[dep_id]["total_stock"] += bundle_stock

    results = list(process_summary.values())
    return JsonResponse(results, safe=False, status=200, json_dumps_params={'ensure_ascii': False})



from django.db.models import Sum, Min, IntegerField, Value
from django.db.models.functions import Coalesce, Cast
from django.http import JsonResponse


def get_cut_data(job_no, tb_name, color):
    cut_data = {}

    with connections['demo'].cursor() as cursor:
        cursor.execute(
            """
            EXEC sp_GetCuttingPcs
                @JobNo = %s,
                @TopBottom_des = %s,
                @comboclr = %s,
                @siz = NULL
            """,
            [job_no, tb_name, color]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        for row in rows:
            data = dict(zip(columns, row))
            size = data['siz']
            cut_data[size] = data['pc'] or 0

    return cut_data

def get_order_qty_data(job_no, tb_name, color):
    order_qty_data = {}

    with connections['demo'].cursor() as cursor:
        cursor.execute(
            """
            EXEC sp_GetOrderAllotment
                @OrdNo = %s,
                @TopBottom_des = %s,
                @UnitName = NULL,
                @Clr = %s,
                @Siz = NULL
            """,
            [job_no, tb_name, color]
        )

        columns = [col[0] for col in cursor.description]

        for row in cursor.fetchall():
            data = dict(zip(columns, row))
            order_qty_data[data['Siz']] = data['qty'] or 0

    return order_qty_data


def get_dependency_pc(request):
    job_no = request.GET.get('job_no')
    tb_name = request.GET.get('tb_name')
    color = request.GET.get('color')

    if not job_no or not tb_name or not color:
        return JsonResponse({
            "error": "job_no, tb_name and color are required"
        }, status=400)
       
    # 1. Fetch distinct processes in correct order using Min(id)
    processes = list(
        dependency.objects.filter(
            job_no=job_no,
            tb_name=tb_name
        )
        .values('process_des')
        .annotate(first_id=Min('id'))
        .order_by('first_id')
        .values_list('process_des', flat=True)
    )

    process_dependencies = {}
    for process_dependency in dependency.objects.filter(
        job_no=job_no,
        tb_name=tb_name
    ).order_by('id'):
        process_dependencies[process_dependency.process_des] = process_dependency

    dependency_ids = [item.id for item in process_dependencies.values()]
    dependency_entries = list(
        dependency_data.objects.filter(dep_id_id__in=dependency_ids).values(
            'dep_id_id', 'descriptions', 'and_data', 'or_data'
        )
    )
    entries_by_dependency = {}
    for entry in dependency_entries:
        entries_by_dependency.setdefault(entry['dep_id_id'], []).append(entry)

    process_rules = {}
    for process_name, process_dependency in process_dependencies.items():
        entries = entries_by_dependency.get(process_dependency.id, [])
        has_explicit_modes = any(entry['and_data'] or entry['or_data'] for entry in entries)
        and_sequences = set()
        or_sequences = set()
        for entry in entries:
            is_and_dependency = (
                entry['and_data'] if has_explicit_modes else process_dependency.and_or
            )
            is_or_dependency = (
                entry['or_data'] if has_explicit_modes else process_dependency.or_only
            )
            descriptions = {
                description.strip().casefold()
                for description in split_process_descriptions(entry['descriptions'])
            }
            if is_and_dependency:
                and_sequences.update(descriptions)
            if is_or_dependency:
                or_sequences.update(descriptions)
        process_rules[(process_dependency.tb_id, process_name)] = (and_sequences, or_sequences)

    # 2. Aggregate production per size and sequence.
    assembly_qs = (
        Assembly_data.objects.filter(
            job_no=job_no,
            tb_name=tb_name,
            color=color
        )
        .values('tb_id', 'size', 'seq')
        .annotate(
            total_pc=Coalesce(
                Sum(Cast('pc', output_field=IntegerField())),
                Value(0),
                output_field=IntegerField()
            )
        )
    )

    size_data = {}
    bundle_data = {}
    tb_ids = set()
    sizes_set = set()

    for row in assembly_qs:
        size = row['size']
        seq = row['seq']
        tb_id = row['tb_id']

        tb_ids.add(tb_id)
        sizes_set.add(size)

        if size not in size_data:
            size_data[size] = {}
        
        # Aggregate totals if multiple rows exist for same size & seq
        size_data[size][seq] = size_data[size].get(seq, 0) + row['total_pc']

    stock_rows = (
        Assembly_data.objects.filter(
            job_no=job_no,
            tb_name=tb_name,
            color=color
        )
        .values('tb_id', 'size', 'bundle_id', 'bdl_no', 'seq')
        .annotate(
            total_pc=Coalesce(
                Sum(Cast('pc', output_field=IntegerField())),
                Value(0),
                output_field=IntegerField()
            )
        )
    )
    for row in stock_rows:
        bundle_key = (row['tb_id'], row['size'], row['bundle_id'])
        bundle = bundle_data.setdefault(bundle_key, {
            'bundle_id': row['bundle_id'],
            'bundle_no': row['bdl_no'],
            'sequences': set(),
            'pc': 0
        })
        bundle['pc'] = max(bundle['pc'], row['total_pc'])
        bundle['sequences'].update(
            description.strip().casefold()
            for description in split_process_descriptions(row['seq'])
        )

    stock_data = {}
    stock_bundles = {}
    for (tb_id, size, _), bundle in bundle_data.items():
        for (dependency_tb_id, process_name), (and_sequences, or_sequences) in process_rules.items():
            if dependency_tb_id != tb_id:
                continue
            if assembly_process_stock_available(
                bundle['sequences'],
                process_name,
                and_sequences,
                or_sequences
            ):
                stock_data.setdefault(size, {})
                stock_data[size][process_name] = (
                    stock_data[size].get(process_name, 0) + bundle['pc']
                )
                stock_bundles.setdefault(size, {}).setdefault(process_name, []).append({
                    'bundle_id': bundle['bundle_id'],
                    'bundle_no': bundle['bundle_no'],
                    'pc': bundle['pc']
                })

    # 3. Optimize Cut Data: Fetch ALL tb_ids in a SINGLE query using `__in` filter
    # Get Cut Qty from Stored Procedure
    cut_data = get_cut_data(job_no, tb_name, color)
    order_qty_data = get_order_qty_data(job_no, tb_name, color)

    # Include sizes from Stored Procedure
    sizes_set.update(cut_data.keys())

    # Convert sizes set to list
    # sizes = list(sizes_set)

    size_order = {
        'XS': 1, 
        'S': 2, 
        'M': 3, 
        'L': 4, 
        'XL': 5, 
        'XXL': 6, '2XL': 6, 
        'XXXL': 7, '3XL': 7,
        'XXXXL': 8, '4XL': 8
    }

    def get_size_rank(size_name):
        cleaned = str(size_name).strip().upper()
        return size_order.get(cleaned, 99) # Unknown sizes-ah kadasiyil kondu vara 99 kodukkirom

    sizes = sorted(list(sizes_set), key=get_size_rank)

    # 4. Build Final Response Efficiently
    result_data = []
    for size in sizes:
        cut_qty = cut_data.get(size, 0)
        order_qty = order_qty_data.get(size, 0)
        seq_data = {}

        for process in processes:
            pc = size_data.get(size, {}).get(process, 0)

            seq_data[process] = {
                "pc": pc,
                "bal": cut_qty - pc,
                "stock": stock_data.get(size, {}).get(process, 0),
                "stock_bundles": stock_bundles.get(size, {}).get(process, [])
            }

        result_data.append({
            "size": size,
            "cut_qty": cut_qty,
            "order_qty": order_qty,
            "seq": seq_data
        })

    return JsonResponse({
        "job_no": job_no,
        "tb_name": tb_name,
        "color": color,
        "data": result_data
    })

@api_view(['GET'])
def bundle_detail_api(request):
    bundle_id = request.GET.get('bundle_id')
    
    if not bundle_id:
        return Response({"error": "bundle_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # bundle_id allathu bdl_no vechu thedalaam
        bundle = Assembly_data.objects.filter(bundle_id=bundle_id).first()
        if not bundle:
            bundle = Assembly_data.objects.filter(bdl_no=bundle_id).first()
            
        if not bundle:
            return Response({"error": "Bundle not found"}, status=status.HTTP_404_NOT_FOUND)
            
        data = {
            "id": bundle.id,
            "unit": bundle.unit,
            "line": bundle.line,
            "job_no": bundle.job_no,
            "tb_id": bundle.tb_id,
            "tb_name": bundle.tb_name,
            "machine": bundle.machine,
            "seq": bundle.seq,
            "date": bundle.date,
            "bundle_id": bundle.bundle_id,
            "bdl_no": bundle.bdl_no,
            "mbud": bundle.mbud,
            "size": bundle.size,
            "size_id": bundle.size_id,
            "color": bundle.color,
            "pc": bundle.pc,
            "entry_date": bundle.entry_date,
            "scan": bundle.scan, # Boolean (True / False) or 1 / 0
            "lot": bundle.lot,
            "emp_id": bundle.emp_id,
            "entry_mode": bundle.entry_mode,
            "unit_transfer": bundle.unit_transfer,
            "edit_data": bundle.edit_data,
            "allocate_id": bundle.allocate_id
        }
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def order_details_api(request):
    order_no = request.GET.get('order_no')

    if not order_no:
        return Response(
            {"error": "order_no parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        detail = ViewOrderdetails.objects.using('demo').filter(
            orderno=order_no
        ).first()

        if not detail:
            return Response(
                {"error": "Order details not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "orderno": detail.orderno,
            "prdsl": detail.prdsl,
            "product": detail.product,
            "clr": detail.clr,
            "sizename": detail.sizename,
            "ordqty": detail.ordqty,
            "merch": detail.merch,
            "buyer": detail.buyer,
            "prdnunit": detail.prdnunit,
            "finaldelvdate": detail.finaldelvdate,
            "style": detail.style,
            "img1": detail.img1
        }

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# 1. Order No Dropdown
@api_view(['GET'])
def elastic_order_list(request):

    data = (
        ViewOrdersummary.objects.using('demo')
        .values_list('ordno', flat=True)
        .distinct()
        .order_by('ordno')
    )

    return Response(list(data))


# 2. Top/Bottom Dropdown
@api_view(['GET'])
def elastic_topbottom_list(request):

    ordno = request.GET.get('ordno')

    data = (
        ViewOrdersummary.objects.using('demo')
        .filter(ordno=ordno)
        .values_list('topbottom_des', flat=True)
        .distinct()
        .order_by('topbottom_des')
    )

    return Response(list(data))


# 3. Colour Dropdown
@api_view(['GET'])
def elastic_colour_list(request):

    ordno = request.GET.get('ordno')
    topbottom = request.GET.get('topbottom')

    data = (
        ViewOrdersummary.objects.using('demo')
        .filter(
            ordno=ordno,
            topbottom_des=topbottom
        )
        .values_list('clr', flat=True)
        .distinct()
        .order_by('clr')
    )

    return Response(list(data))


# 4. Size and Order Qty
@api_view(['GET'])
def elastic_size_details(request):
    ordno = request.GET.get('ordno')
    jobno = request.GET.get('jobno')
    topbottom = request.GET.get('topbottom')
    colour = request.GET.get('colour')

    print(f"DEBUG REQ -> ordno: {ordno}, jobno: {jobno}, topbottom: {topbottom}, colour: {colour}")

    # 1. Get size and order_qty from ViewOrdersummary
    order_data = (
        ViewOrdersummary.objects.using('demo')
        .filter(
            ordno=ordno,
            topbottom_des=topbottom,
            clr=colour
        )
        .values('siz')
        .annotate(qty=Sum('qty'))
        .order_by('siz')
    )

    result = []
    for row in order_data:
        size_name = row['siz']
        order_qty = row['qty'] or 0

        # Prefer editable consumption values, then fall back to the source view.
        saved_cons_query = elastic_cons.objects.filter(
            color__iexact=colour,
            sizedescr__iexact=size_name,
            topbott__iexact=topbottom
        ).order_by('id')
        if jobno:
            saved_cons_query = saved_cons_query.filter(jobno__iexact=jobno)
            cons_obj = saved_cons_query.first()
            if not cons_obj:
                cons_obj = elastic_cons.objects.filter(
                    jobno='',
                    color__iexact=colour,
                    sizedescr__iexact=size_name,
                    topbott__iexact=topbottom
                ).order_by('id').first()
        else:
            cons_obj = saved_cons_query.filter(jobno='').first()
            if not cons_obj:
                cons_obj = saved_cons_query.first()

        cons_source = 'elastic_cons' if cons_obj else 'none'
        if not cons_obj:
            cons_query = ViewElasticCons.objects.using('demo').filter(
                color__iexact=colour,
                sizedescr__iexact=size_name,
                topbott__iexact=topbottom
            ).order_by('sl1')
            if jobno:
                cons_query = cons_query.filter(jobno__iexact=jobno)
            cons_obj = cons_query.first()
            if cons_obj:
                cons_source = 'view_elastic_cons'

        len_cms = str(cons_obj.cons) if cons_obj and cons_obj.cons is not None else ""

        # 3. Get total_pcs_cut (noofpcs) from ViewCuttingQtyDetails matching jobno, topbottom_des, clrcombo, and name
        cutting_query = ViewCuttingQtyDetails.objects.using('demo').filter(
            topbottom_des__iexact=topbottom,
            clrcombo__iexact=colour,
            name__iexact=size_name
        ).order_by('itemno')  # Ensure consistent ordering
        if jobno:
            cutting_query = cutting_query.filter(jobno__iexact=jobno)

        cutting_obj = cutting_query.first()
        total_pcs_cut = cutting_obj.noofpcs if cutting_obj and cutting_obj.noofpcs is not None else ""

        print(f"Size: {size_name} | Found Cons: {len_cms} | Found Cutting Qty: {total_pcs_cut}")

        # Calculate initial balance
        balance = order_qty - (int(total_pcs_cut) if total_pcs_cut != "" else 0)

        result.append({
            'size': size_name,
            'order_qty': order_qty,
            'len_cms': len_cms,
            'cons_source': cons_source,
            'total_pcs_cut': total_pcs_cut,
            'balance': balance,
            'prev_cut_qty': "",
            'current_cut_qty': "",
            'estimate_mtr': ""
        })

    return Response(result)


@api_view(['POST'])
def save_elastic_cons(request):
    jobno = str(request.data.get('jobno') or '').strip()
    topbottom = str(request.data.get('topbottom') or '').strip()
    colour = str(request.data.get('colour') or '').strip()
    sizes = request.data.get('sizes')

    if not topbottom or not colour or not isinstance(sizes, list) or not sizes:
        return Response(
            {'error': 'Top/Bottom, Colour and at least one size are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(jobno) > 50 or len(topbottom) > 50 or len(colour) > 1800:
        return Response(
            {'error': 'One or more selection values exceed the allowed length.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    cons_field = elastic_cons._meta.get_field('cons')
    validated_sizes = []
    seen_sizes = set()
    for row in sizes:
        if not isinstance(row, dict):
            return Response(
                {'error': 'Each size entry must include a size and CMS length.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        size_name = str(row.get('size') or '').strip()
        if not size_name or len(size_name) > 50 or size_name in seen_sizes:
            return Response(
                {'error': 'Size names must be present, unique and no longer than 50 characters.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            consumption = cons_field.clean(row.get('len_cms'), None)
        except ValidationError as error:
            return Response(
                {'error': f'Invalid CMS length for size {size_name}: {error.messages[0]}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_sizes.append((size_name, consumption))
        seen_sizes.add(size_name)

    with transaction.atomic():
        for size_name, consumption in validated_sizes:
            matching_rows = elastic_cons.objects.filter(
                jobno__iexact=jobno,
                sizedescr__iexact=size_name,
                topbott__iexact=topbottom,
                color__iexact=colour
            )
            if matching_rows.exists():
                matching_rows.update(cons=consumption)
                continue

            fallback_rows = elastic_cons.objects.filter(
                jobno='',
                sizedescr__iexact=size_name,
                topbott__iexact=topbottom,
                color__iexact=colour
            ) if jobno else matching_rows

            if fallback_rows.exists():
                fallback_rows.update(cons=consumption)
                continue

            elastic_cons.objects.create(
                jobno=jobno,
                sizedescr=size_name,
                cons=consumption,
                topbott=topbottom,
                color=colour
            )

    return Response(
        {
            'saved_count': len(validated_sizes),
            'saved_sizes': [size_name for size_name, _ in validated_sizes],
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def save_elastic_cutting_entry(request):
    def clean_text(model, field_name, value, required=False):
        text = '' if value is None else str(value).strip()
        if required and not text:
            raise ValueError(f'{field_name} is required.')
        field = model._meta.get_field(field_name)
        if field.max_length and len(text) > field.max_length:
            raise ValueError(f'{field_name} exceeds {field.max_length} characters.')
        return text or None

    def clean_number(model, field_name, value, integer=False, required=False):
        text = clean_text(model, field_name, value)
        if text is None:
            if required:
                raise ValueError(f'{field_name} is required.')
            return Decimal('0'), None
        try:
            number = Decimal(text)
        except InvalidOperation as error:
            raise ValueError(f'{field_name} must be a valid number.') from error
        if not number.is_finite() or number < 0:
            raise ValueError(f'{field_name} must be zero or a positive number.')
        if integer and number != number.to_integral_value():
            raise ValueError(f'{field_name} must be a whole number.')
        normalized = format(number.normalize(), 'f')
        return number, clean_text(model, field_name, normalized)

    payload = request.data
    sizes = payload.get('sizes')
    if not isinstance(sizes, list) or not sizes:
        return Response(
            {'error': 'At least one size row is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order_no = clean_text(Elastic_cutting_qty, 'order_no', payload.get('order_no'), required=True)
        topbottom = clean_text(Elastic_cutting_qty, 'topbottom', payload.get('topbottom'), required=True)
        colour = clean_text(Elastic_cutting_qty, 'color', payload.get('color'), required=True)
        elastic_description = clean_text(
            Elastic_cutting_qty, 'elastic_description', payload.get('elastic_description')
        )
        inward_mtrs = clean_number(Elastic_cutting_qty, 'inward_mtrs', payload.get('inward_mtrs'))[1]
        actual_consumption_value, actual_consumption = clean_number(
            Elastic_cutting_qty, 'actual_consumption', payload.get('actual_consumption'), required=True
        )
        _, wastage = clean_number(
            Elastic_cutting_qty, 'wastage', payload.get('wastage'), required=True
        )

        entry_date = parse_date(str(payload.get('date') or ''))
        if not entry_date:
            raise ValueError('A valid entry date is required.')
        entry_datetime = timezone.make_aware(
            datetime.combine(entry_date, datetime.min.time()),
            timezone.get_current_timezone()
        )

        validated_rows = []
        seen_sizes = set()
        total_cut_qty = Decimal('0')
        total_estimate_mtrs = Decimal('0')

        for row in sizes:
            if not isinstance(row, dict):
                raise ValueError('Each size row must be an object.')

            size_name = clean_text(Elastic_cutting_qty_details, 'size', row.get('size'), required=True)
            if size_name in seen_sizes:
                raise ValueError(f'Duplicate size row: {size_name}.')
            seen_sizes.add(size_name)

            length, length_text = clean_number(
                Elastic_cutting_qty_details, 'len_cm', row.get('len_cm')
            )
            order_qty, order_qty_text = clean_number(
                Elastic_cutting_qty_details, 'order_qty', row.get('order_qty'), integer=True
            )
            pcs_cut, pcs_cut_text = clean_number(
                Elastic_cutting_qty_details, 'pcs_cut', row.get('pcs_cut'), integer=True
            )
            previous_qty, _ = clean_number(
                Elastic_cutting_qty_details, 'elastic_cutting_qty', row.get('prev_cut_qty'), integer=True
            )
            current_qty, _ = clean_number(
                Elastic_cutting_qty_details, 'elastic_cutting_qty',
                row.get('elastic_cutting_qty'), integer=True
            )
            quantity_limit = max(order_qty, pcs_cut)
            if previous_qty + current_qty > quantity_limit:
                raise ValueError(
                    f'Elastic quantities for size {size_name} exceed the order/cut quantity limit ({quantity_limit}).'
                )

            bundles = row.get('bundles') or []
            if not isinstance(bundles, list):
                raise ValueError(f'Bundle rows for size {size_name} must be a list.')
            clean_bundles = []
            bundle_total = Decimal('0')
            for bundle_index, bundle in enumerate(bundles, start=1):
                if not isinstance(bundle, dict):
                    raise ValueError(f'Bundle {bundle_index} for size {size_name} must be an object.')
                bundle_no = clean_text(
                    Elastic_cutting_qty_details, 'bdl_no',
                    bundle.get('bdl_no', bundle_index), required=True
                )
                bundle_qty, bundle_qty_text = clean_number(
                    Elastic_cutting_qty_details, 'bdl_qty', bundle.get('bdl_qty'), integer=True
                )
                if bundle_qty <= 0:
                    raise ValueError(f'Bundle {bundle_index} for size {size_name} must have a positive quantity.')
                clean_bundles.append((bundle_no, bundle_qty, bundle_qty_text))
                bundle_total += bundle_qty

            if current_qty > 0 and bundle_total != current_qty:
                raise ValueError(
                    f'Bundle quantities for size {size_name} must total {current_qty} pcs.'
                )
            if current_qty == 0 and bundle_total:
                raise ValueError(f'Bundle quantities for size {size_name} must total zero.')

            size_estimate = (length * current_qty / Decimal('100')).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            if current_qty > 0:
                detail_rows = []
                for bundle_no, bundle_qty, bundle_qty_text in clean_bundles:
                    bundle_estimate = (
                        length * bundle_qty / Decimal('100')
                    ).quantize(Decimal('0.0001'))
                    detail_rows.append({
                        'size': size_name,
                        'len_cm': length_text,
                        'order_qty': order_qty_text,
                        'pcs_cut': pcs_cut_text,
                        'elastic_cutting_qty': bundle_qty_text,
                        'estimate_mtrs': format(bundle_estimate, 'f'),
                        'bdl_no': bundle_no,
                        'bdl_qty': bundle_qty_text,
                    })
                validated_rows.extend(detail_rows)
            total_cut_qty += current_qty
            total_estimate_mtrs += size_estimate

        if total_cut_qty <= 0:
            raise ValueError('Enter an Elastic Current Cut Qty before saving.')

        lower_bound = max(Decimal('0'), total_estimate_mtrs - Decimal('5'))
        upper_bound = total_estimate_mtrs + Decimal('5')
        if actual_consumption_value < lower_bound or actual_consumption_value > upper_bound:
            raise ValueError(
                f'Actual Consumption must be between {lower_bound} and {upper_bound} Mtrs.'
            )

        total_cut_text = format(total_cut_qty.normalize(), 'f')
        total_estimate_text = format(
            total_estimate_mtrs.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), 'f'
        )
        clean_text(Elastic_cutting_qty, 'total_cutting_qty', total_cut_text)
        clean_text(Elastic_cutting_qty, 'estimate_mtrs', total_estimate_text)
    except (ValueError, InvalidOperation) as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        entry = Elastic_cutting_qty.objects.create(
            order_no=order_no,
            topbottom=topbottom,
            color=colour,
            elastic_description=elastic_description,
            inward_mtrs=inward_mtrs,
            date=entry_datetime,
            actual_consumption=actual_consumption,
            wastage=wastage,
            total_cutting_qty=total_cut_text,
            estimate_mtrs=total_estimate_text,
        )
        Elastic_cutting_qty_details.objects.bulk_create([
            Elastic_cutting_qty_details(entry_no=entry, **row)
            for row in validated_rows
        ])

    return Response(
        {'entry_no': entry.entry_no, 'saved_details': len(validated_rows)},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def elastic_previous_cutting(request):
    order_no = str(request.GET.get('order_no') or '').strip()
    topbottom = str(request.GET.get('topbottom') or '').strip()
    colour = str(request.GET.get('color') or '').strip()
    accessory = str(request.GET.get('elastic_description') or '').strip()
    if not order_no or not topbottom or not colour:
        return Response(
            {'error': 'Order, Top/Bottom and Colour are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    entries_query = Elastic_cutting_qty.objects.filter(
        order_no__iexact=order_no,
        topbottom__iexact=topbottom,
        color__iexact=colour,
    )
    if accessory:
        entries_query = entries_query.filter(elastic_description__iexact=accessory)
    entries = list(entries_query.order_by('entry_no'))

    def saved_decimal(value, field_name):
        try:
            number = Decimal(str(value or '0'))
        except InvalidOperation as error:
            raise ValueError(f'Saved {field_name} data is invalid.') from error
        if not number.is_finite():
            raise ValueError(f'Saved {field_name} data is invalid.')
        return number

    try:
        previous_estimate = sum(
            (saved_decimal(entry.estimate_mtrs, 'estimate Mtrs') for entry in entries),
            Decimal('0')
        )
        previous_wastage = sum(
            (saved_decimal(entry.wastage, 'wastage') for entry in entries),
            Decimal('0')
        )
        previous_qty_by_size = {}
        if entries:
            details = Elastic_cutting_qty_details.objects.filter(
                entry_no__in=[entry.entry_no for entry in entries]
            ).values_list('size', 'elastic_cutting_qty')
            for size_name, qty in details:
                if size_name:
                    size_key = str(size_name).strip().casefold()
                    previous_qty_by_size[size_key] = (
                        previous_qty_by_size.get(size_key, Decimal('0'))
                        + saved_decimal(qty, 'previous cut quantity')
                    )
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'previous_cutting_mtrs': format(previous_estimate.normalize(), 'f'),
        'previous_wastage_mtrs': format(previous_wastage.normalize(), 'f'),
        'prev_cut_qty_by_size': {
            size_name: format(qty.normalize(), 'f')
            for size_name, qty in previous_qty_by_size.items()
        },
    })


@api_view(['GET'])
def elastic_accessory_qty(request):
    ordno = request.GET.get('ordno')
    accessory = request.GET.get('accessory')

    data = (
        ViewAccessoryorderqtyElastic.objects.using('demo')
        .filter(orderno=ordno, accessory=accessory)
        .first()
    )

    qty = data.qty if data else 0
    return Response({'qty': qty})


# 5. Elastic Description
@api_view(['GET'])
def elastic_description(request):

    ordno = request.GET.get('ordno')

    data = (
        ViewAccessoryorderqtyElastic.objects.using('demo')
        .filter(orderno=ordno)
        .values_list('accessory', flat=True)
        .distinct()
    )

    return Response(list(data))


############### Elastic Delivery API ###############

# 1. Get Distinct Order Numbers (JobNos)
def get_job_nos(request):
    job_nos = list(Elastic_cutting_qty.objects.values_list('order_no', flat=True).distinct())
    return JsonResponse(job_nos, safe=False)

def get_top_bottoms(request):
    ordno = request.GET.get('order_no')
    top_bottoms = list(Elastic_cutting_qty.objects.filter(order_no=ordno).values_list('topbottom', flat=True).distinct())
    return JsonResponse(top_bottoms, safe=False)

# 2. Get Colors by OrderNo
def get_colors(request):
    print("DEBUG: Fetching colors for order_no", request.GET.get('order_no'))
    order_no = request.GET.get('order_no')
    print(f"DEBUG: Fetching colors for order_no: {order_no}")
    colors = list(Elastic_cutting_qty.objects.filter(order_no=order_no).values_list('color', flat=True).distinct())
    return JsonResponse(colors, safe=False)

def get_elastic_units(request):
    ordno = request.GET.get('order_no')
    topbottom = request.GET.get('topbottom')
    color = request.GET.get('color')
    
    units = list(
        ViewOrdersummaryUnit.objects.using('demo').filter(
            ordno=ordno, 
            topbottom_des=topbottom, 
            clr=color
        ).values_list('unitname', flat=True).distinct()
    )
    return JsonResponse(units, safe=False)

# 5. Get Bundle Details 
def get_bundle_details(request):
    order_no = request.GET.get('order_no')
    topbottom = request.GET.get('topbottom')
    color = request.GET.get('color')
    unitname = request.GET.get('unitname')
    
    try:
        summary_rows = ViewOrdersummaryUnit.objects.using('demo').filter(
            ordno=order_no,
            topbottom_des=topbottom,
            clr=color,
            unitname=unitname
        ).values('siz', 'qty')

        # 1. 0 உள்ள சைஸ்களைக் கண்டறிந்து ஒரு லிஸ்ட்டில் சேமிக்கிறோம்
        skipped_sizes = []
        preloaded_summary = []
        
        for row in summary_rows:
            size_name = row['siz']
            order_qty_val = row['qty'] or 0

            cut_summary = ViewCuttingQtyDetailsUnit.objects.using('demo').filter(
                jobno=order_no,
                topbottom_des=topbottom,
                comboclr=color,
                unitname=unitname,
                name=size_name
            ).values('noofpcs').first()
            
            pcs_cut_val = cut_summary['noofpcs'] if cut_summary and cut_summary['noofpcs'] is not None else 0

            # Ord Qty மற்றும் Cut Qty இரண்டும் 0 எனில் skip செய்வோம்
            if order_qty_val == 0 and pcs_cut_val == 0:
                skipped_sizes.append(size_name)
                continue

            preloaded_summary.append({
                "size": size_name,
                "order_qty": order_qty_val,
                "pcs_cut": pcs_cut_val,
            })

        previous_deliveries = {
            row["size"]: row["total_qty"] or 0
            for row in ElasticDeliveryDetails.objects.filter(
                delivery_id__job_no=order_no,
                delivery_id__topbottom=topbottom,
                delivery_id__colour=color,
                delivery_id__unit=unitname
            ).values("size").annotate(total_qty=Sum("cur_del_qty"))
        }
        for row in preloaded_summary:
            row["prev_del_qty"] = previous_deliveries.get(row["size"], 0)

        # 2. Elastic cutting details லிருந்து bundles எடுக்கும்போது skipped_sizes-ல் உள்ளவை வரக்கூடாது
        cutting_qty_records = Elastic_cutting_qty.objects.filter(order_no=order_no, topbottom=topbottom, color=color)
        bundles_list = []
        for record in cutting_qty_records:
            details = Elastic_cutting_qty_details.objects.filter(entry_no=record, delivery=False)
            for d in details:
                # 0 உள்ள சைஸ் பண்டில்களை வலது பக்க டேபிளில் காட்டாமல் தவிர்க்கிறோம்
                if d.size in skipped_sizes:
                    continue
                    
                bundles_list.append({
                    "entry_no": record.entry_no,
                    "topbottom": record.topbottom,
                    "bdl_id": d.bdl_id,
                    "size": d.size,
                    "len_cm": d.len_cm,
                    "elastic_cutting_qty": float(d.elastic_cutting_qty or 0),
                    "bdl_no": d.bdl_no,
                    "bdl_qty": d.bdl_qty,
                })
            
        return JsonResponse({
            "preloaded_summary": preloaded_summary,
            "bundles": bundles_list
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def save_elastic_delivery(request):
    job_no = str(request.data.get("job_no") or "").strip()
    topbottom = str(request.data.get("topbottom") or "").strip()
    colour = str(request.data.get("colour") or "").strip()
    unit = str(request.data.get("unit") or "").strip()
    details = request.data.get("details")

    if not job_no or not topbottom or not colour or not unit:
        return Response(
            {"error": "Job number, Top/Bottom, Colour and Unit are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if (
        len(job_no) > 50 or len(topbottom) > 50
        or len(colour) > 50 or len(unit) > 100
    ):
        return Response(
            {"error": "One or more selection values exceed the allowed length."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not isinstance(details, list) or not details:
        return Response(
            {"error": "Scan at least one bundle before saving delivery."},
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_details = []
    seen_bundle_ids = set()
    try:
        for row in details:
            if not isinstance(row, dict):
                raise ValueError("Each delivery detail must be an object.")

            size = str(row.get("size") or "").strip()
            bundle_ids = row.get("bdl_ids")
            unit_ord_qty = int(row.get("unit_ord_qty"))
            unit_cut_qty = int(row.get("unit_cut_qty"))
            cur_del_qty = int(row.get("cur_del_qty"))
            total_bdl = int(row.get("total_bdl"))

            if (
                not size or len(size) > 50
                or not isinstance(bundle_ids, list) or not bundle_ids
                or unit_ord_qty < 0 or unit_cut_qty < 0
                or cur_del_qty <= 0 or total_bdl <= 0
                or total_bdl != len(bundle_ids)
            ):
                raise ValueError(f"Invalid delivery values for size {size or '(blank)'}.")

            normalized_ids = [int(bundle_id) for bundle_id in bundle_ids]
            if any(bundle_id <= 0 for bundle_id in normalized_ids):
                raise ValueError("Bundle IDs must be positive integers.")
            if any(bundle_id in seen_bundle_ids for bundle_id in normalized_ids):
                raise ValueError("A bundle cannot be included more than once.")
            seen_bundle_ids.update(normalized_ids)
            validated_details.append({
                "size": size,
                "bdl_ids": normalized_ids,
                "unit_ord_qty": unit_ord_qty,
                "unit_cut_qty": unit_cut_qty,
                "cur_del_qty": cur_del_qty,
                "total_bdl": total_bdl,
            })
    except (TypeError, ValueError, OverflowError) as error:
        return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        bundle_rows = list(
            Elastic_cutting_qty_details.objects.select_for_update().filter(
                bdl_id__in=seen_bundle_ids,
                delivery=False,
                entry_no__order_no=job_no,
                entry_no__topbottom=topbottom,
                entry_no__color=colour,
            )
        )
        bundles_by_id = {bundle.bdl_id: bundle for bundle in bundle_rows}
        if set(bundles_by_id) != seen_bundle_ids:
            return Response(
                {"error": "One or more scanned bundles are invalid or already delivered."},
                status=status.HTTP_409_CONFLICT
            )

        for row in validated_details:
            matching_bundles = [bundles_by_id[bundle_id] for bundle_id in row["bdl_ids"]]
            if any(str(bundle.size or "").strip().lower() != row["size"].lower() for bundle in matching_bundles):
                return Response(
                    {"error": f"Scanned bundles do not match size {row['size']}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                scanned_qty = sum(Decimal(bundle.elastic_cutting_qty or "0") for bundle in matching_bundles)
            except (InvalidOperation, TypeError):
                return Response(
                    {"error": f"Invalid bundle quantity for size {row['size']}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if scanned_qty != Decimal(row["cur_del_qty"]):
                return Response(
                    {"error": f"Scanned bundle quantity for size {row['size']} does not match delivery quantity."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        delivery = ElasticDelivery.objects.create(
            job_no=job_no,
            topbottom=topbottom,
            colour=colour,
            unit=unit,
        )
        saved_details = []
        for row in validated_details:
            delivery_detail = ElasticDeliveryDetails.objects.create(
                delivery_id=delivery,
                unit_ord_qty=row["unit_ord_qty"],
                unit_cut_qty=row["unit_cut_qty"],
                size=row["size"],
                cur_del_qty=row["cur_del_qty"],
                total_bdl=row["total_bdl"],
            )
            Elastic_cutting_qty_details.objects.filter(
                bdl_id__in=row["bdl_ids"]
            ).update(delivery=True, delivery_id=delivery_detail.id)
            saved_details.append(delivery_detail.id)

    return Response(
        {
            "delivery_id": delivery.id,
            "detail_ids": saved_details,
            "saved_count": len(saved_details),
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_elastic_delivery_print(request):
    job_no = str(request.query_params.get("job_no") or "").strip()
    topbottom = str(request.query_params.get("topbottom") or "").strip()
    colour = str(request.query_params.get("colour") or "").strip()
    unit = str(request.query_params.get("unit") or "").strip()

    if not job_no or not topbottom or not colour or not unit:
        return Response(
            {"error": "Job number, Top/Bottom, Colour and Unit are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    deliveries = ElasticDelivery.objects.filter(
        job_no=job_no,
        topbottom=topbottom,
        colour=colour,
        unit=unit,
    ).order_by("delivery_date", "id")

    result = []
    for delivery in deliveries:
        details = list(
            ElasticDeliveryDetails.objects.filter(delivery_id=delivery).order_by("id")
        )
        detail_ids = [detail.id for detail in details]
        bundles = Elastic_cutting_qty_details.objects.filter(
            delivery=True,
            delivery_id__in=detail_ids,
        ).order_by("bdl_id")

        result.append({
            "delivery_id": delivery.id,
            "job_no": delivery.job_no,
            "topbottom": delivery.topbottom,
            "colour": delivery.colour,
            "unit": delivery.unit,
            "delivery_date": delivery.delivery_date.isoformat(),
            "bundles": [
                {
                    "bdl_id": bundle.bdl_id,
                    "size": bundle.size,
                    "qty": bundle.elastic_cutting_qty,
                    "len_cm": bundle.len_cm,
                }
                for bundle in bundles
            ],
        })

    return Response({"deliveries": result}, status=status.HTTP_200_OK)



############### End of Elastic Delivery API ###############


############## Rip Entry API ##############

@require_GET
def get_winding_units(request):
    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .exclude(unitname__isnull=True)
        .exclude(unitname='')
        .values_list('unitname', flat=True)
        .distinct()
        .order_by('unitname')
    )
    units = [u.strip() for u in qs if u and u.strip()]
    return JsonResponse({'units': list(dict.fromkeys(units))})


@require_GET
def get_winding_jobs(request):
    unit = request.GET.get('unit', '').strip()
    if not unit:
        return JsonResponse({'jobs': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(unitname__iexact=unit)
        .exclude(jobno__isnull=True)
        .exclude(jobno='')
        .values_list('jobno', flat=True)
        .distinct()
        .order_by('jobno')
    )
    jobs = [j.strip() for j in qs if j and j.strip()]
    return JsonResponse({'jobs': list(dict.fromkeys(jobs))})


@require_GET
def get_winding_topbottom(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('jobno', '').strip()
    if not unit or not jobno:
        return JsonResponse({'topbottoms': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(unitname__iexact=unit, jobno__iexact=jobno)
        .exclude(topbottom_des__isnull=True)
        .exclude(topbottom_des='')
        .values_list('topbottom_des', flat=True)
        .distinct()
        .order_by('topbottom_des')
    )
    topbottoms = [tb.strip() for tb in qs if tb and tb.strip()]
    return JsonResponse({'topbottoms': list(dict.fromkeys(topbottoms))})


@require_GET
def get_winding_colours(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('job_no', '').strip()
    topbottom = request.GET.get('top_bottom', '').strip()
    if not (unit and jobno and topbottom):
        return JsonResponse({'colours': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
        )
        .exclude(comboclr__isnull=True)
        .exclude(comboclr='')
        .values_list('comboclr', flat=True)
        .distinct()
        .order_by('comboclr')
    )
    colours = [value.strip() for value in qs if value and value.strip()]
    return JsonResponse({'colours': list(dict.fromkeys(colours))})


@require_GET
def get_winding_lots(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('job_no', '').strip()
    topbottom = request.GET.get('top_bottom', '').strip()
    colour = request.GET.get('colour_combo', '').strip()
    if not (unit and jobno and topbottom and colour):
        return JsonResponse({'lots': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
            comboclr__iexact=colour,
        )
        .exclude(lotno__isnull=True)
        .exclude(lotno='')
        .values_list('lotno', flat=True)
        .distinct()
        .order_by('lotno')
    )
    lots = [value.strip() for value in qs if value and value.strip()]
    return JsonResponse({'lots': list(dict.fromkeys(lots))})


@require_GET
def get_winding_folding_parts(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('job_no', '').strip()
    topbottom = request.GET.get('top_bottom', '').strip()
    colour = request.GET.get('colour_combo', '').strip()
    lotno = request.GET.get('lot_no', '').strip()
    if not (unit and jobno and topbottom and colour and lotno):
        return JsonResponse({'folding_parts': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
            comboclr__iexact=colour,
            lotno__iexact=lotno,
        )
        .exclude(portion_des__isnull=True)
        .exclude(portion_des='')
        .values_list('portion_des', flat=True)
        .distinct()
        .order_by('portion_des')
    )
    folding_parts = [value.strip() for value in qs if value and value.strip()]
    return JsonResponse({'folding_parts': list(dict.fromkeys(folding_parts))})


@require_GET
def get_winding_cutting_sizes(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('job_no', '').strip()
    topbottom = request.GET.get('top_bottom', '').strip()
    colour = request.GET.get('colour_combo', '').strip()
    folding_part = request.GET.get('folding_parts', '').strip()
    lotno = request.GET.get('lot_no', '').strip()
    if not (unit and jobno and topbottom and colour and folding_part and lotno):
        return JsonResponse({'sizes': []})

    items = (
        ViewCuttingQtyDetailsLotUnit.objects.using('demo')
        .filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
            comboclr__iexact=colour,
            lotno__iexact=lotno,
        )
        .values('name', 'noofpcs')
        .order_by('name')
    )

    previous_cuts = (
        Rope_cutting_data.objects.filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom__iexact=topbottom,
            color__iexact=colour,
            folding_part__iexact=folding_part,
            lotno__iexact=lotno,
        )
        .exclude(current_qty__isnull=True)
        .exclude(current_qty='')
        .values('size')
        .annotate(prev_cut=Sum(Cast('current_qty', IntegerField())))
    )
    previous_by_size = {
        (item.get('size') or '').strip().casefold(): item.get('prev_cut') or 0
        for item in previous_cuts
    }

    sizes = [
        {
            'size': item['name'],
            'cut_qty': item['noofpcs'] or 0,
            'prev_cut': previous_by_size.get(item['name'].strip().casefold(), 0),
        }
        for item in items
    ]
    return JsonResponse({'sizes': sizes})


@require_GET
def get_winding_summary_details(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('jobno', '').strip()
    topbottom = request.GET.get('topbottom', '').strip()

    if not (unit and jobno and topbottom):
        return JsonResponse({'rows': []})

    qs = (
        ViewFabricfoldingRibdetails.objects.using('demo')
        .filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
        )
        .values('comboclr', 'portion_des','fabclr', 'lotno', 'siz', 'kg', 'mtr')
        .order_by('comboclr', 'portion_des', 'lotno', 'siz')
    )

    previous_rows = (
        folding_data.objects.filter(
            unitname__iexact=unit,
            jobno__iexact=jobno,
            topbottom_des__iexact=topbottom,
        )
        .values('color', 'folding_part', 'fabclr', 'lotno', 'size')
        .annotate(
            previous_kg=Sum('current_kg'),
            previous_mtr=Sum('current_mtr'),
        )
    )

    def summary_key(color, folding_part, fabclr, lotno, size):
        return tuple(
            (value or '').strip().casefold()
            for value in (color, folding_part, fabclr, lotno, size)
        )

    previous_by_key = {}
    for previous in previous_rows:
        key = summary_key(
            previous.get('color'),
            previous.get('folding_part'),
            previous.get('fabclr'),
            previous.get('lotno'),
            previous.get('size'),
        )
        totals = previous_by_key.setdefault(key, [Decimal('0'), Decimal('0')])
        totals[0] += previous.get('previous_kg') or Decimal('0')
        totals[1] += previous.get('previous_mtr') or Decimal('0')

    rows = []
    for idx, item in enumerate(qs, start=1):
        clr = (item.get('comboclr') or '').strip()
        previous_kg, previous_mtr = previous_by_key.get(
            summary_key(
                item.get('comboclr'),
                item.get('portion_des'),
                item.get('fabclr'),
                item.get('lotno'),
                item.get('siz'),
            ),
            (Decimal('0'), Decimal('0')),
        )
        rows.append({
            'id': idx,
            'clrCombo': clr,
            'foldingParts': (item.get('portion_des') or '').strip(),
            'fabricColour': (item.get('fabclr') or '').strip(),
            'lotNo': (item.get('lotno') or '').strip(),
            'size': (item.get('siz') or '').strip(),
            'reqKg': (item.get('kg') or 0),
            'reqMtr': (item.get('mtr') or 0),
            'prevKg': previous_kg,
            'prevMtr': previous_mtr,
        })

    return JsonResponse({'rows': rows})


@require_GET
def get_available_rolls(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('jobno', '').strip()
    topbottom = request.GET.get('topbottom', '').strip()
    lotno = request.GET.get('lotno', '').strip()
    clr_name = request.GET.get('clr_name', '').strip()

    if not unit or not jobno:
        return JsonResponse({'rolls': []})

    qs = ViewUnitFoldDeliveryDetails.objects.using('demo').filter(
        unitname__iexact=unit,
        jobno__iexact=jobno,
    )

    # Filter by topbottom_des if field exists on ViewUnitFoldDeliveryDetails
    model_fields = [f.name for f in ViewUnitFoldDeliveryDetails._meta.get_fields()]
    if topbottom and 'topbottom_des' in model_fields:
        qs = qs.filter(topbottom_des__iexact=topbottom)

    if lotno:
        qs = qs.filter(lotno__iexact=lotno)

    if clr_name:
        qs = qs.filter(clr_name__iexact=clr_name)

    items = qs.values(
        'rlno',
        'clr_name',
        'lotno',
        'fab',
        'fabid',
        'wgtkgs',
        'mtr',
    ).order_by('rlno')

    rolls = [
        {
            'rollNo': (item.get('rlno') or '').strip(),
            'colour': (item.get('clr_name') or '').strip(),
            'lotNo': (item.get('lotno') or '').strip(),
            'fabric': (item.get('fab') or '').strip(),
            'fabId': item.get('fabid') or 0,
            'dia': '',
            'kgs': float(item.get('wgtkgs') or 0),
            'mtrs': float(item.get('mtr') or 0),
        }
        for item in items
    ]

    return JsonResponse({'rolls': rolls})


@require_GET
def get_rope_cutting_available_rolls(request):
    unit = request.GET.get('unit', '').strip()
    jobno = request.GET.get('job_no', '').strip()
    topbottom = request.GET.get('top_bottom', '').strip()
    colour = request.GET.get('colour_combo', '').strip()
    folding_part = request.GET.get('folding_parts', '').strip()
    lotno = request.GET.get('lot_no', '').strip()
    size = request.GET.get('size', '').strip()

    if not all((unit, jobno, topbottom, colour, folding_part, lotno, size)):
        return JsonResponse({'rolls': []})

    folding_ids = list(
        folding_data.objects.filter(
            topbottom_des__iexact=topbottom,
            jobno__iexact=jobno,
            unitname__iexact=unit,
            color__iexact=colour,
            folding_part__iexact=folding_part,
            lotno__iexact=lotno,
            size__iexact=size,
        ).values_list('id', flat=True)
    )
    if not folding_ids:
        return JsonResponse({'rolls': []})

    details = (
        folding_data_details.objects
        .filter(folding_data_id__in=folding_ids, rope_cutting__isnull=True)
        .values('id', 'roll_no', 'color', 'lotno', 'fabric', 'kgs', 'mtr')
        .order_by('roll_no')
    )
    rolls = [
        {
            'detailId': item['id'],
            'rollNo': (item.get('roll_no') or '').strip(),
            'colour': (item.get('color') or '').strip(),
            'lotNo': (item.get('lotno') or '').strip(),
            'fabric': (item.get('fabric') or '').strip(),
            'siz': size,
            'kgs': float(item.get('kgs') or 0),
            'mtrs': float(item.get('mtr') or 0),
        }
        for item in details
    ]
    return JsonResponse({'rolls': rolls})


@csrf_exempt
def save_rope_cutting_entry(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required.'}, status=405)

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Invalid request payload.'}, status=400)

    def text_value(value, field_name, max_length):
        text = str(value or '').strip()
        if not text:
            raise ValueError(f'{field_name} is required.')
        if len(text) > max_length:
            raise ValueError(f'{field_name} cannot exceed {max_length} characters.')
        return text

    def whole_number(value, field_name, minimum=0):
        if isinstance(value, bool):
            raise ValueError(f'{field_name} must be a whole number.')
        try:
            number = int(str(value).strip())
        except (TypeError, ValueError):
            raise ValueError(f'{field_name} must be a whole number.')
        if number < minimum:
            raise ValueError(f'{field_name} must be at least {minimum}.')
        return number

    try:
        jobno = text_value(payload.get('jobNo'), 'Job No', 50)
        topbottom = text_value(payload.get('topBott'), 'Top/Bottom', 50)
        unitname = text_value(payload.get('unit'), 'Unit', 50)
        colour = text_value(payload.get('colourCombo'), 'Colour/Combo', 100)
        folding_part = text_value(payload.get('foldingParts'), 'Folding Parts', 100)
        lotno = text_value(payload.get('lotNo'), 'Lot No', 10)
        size = text_value(payload.get('size'), 'Size', 35)

        entry_date = parse_date(str(payload.get('date') or ''))
        if not entry_date:
            raise ValueError('A valid entry date is required.')
        entry_datetime = timezone.make_aware(
            datetime.combine(entry_date, datetime.min.time()),
            timezone.get_current_timezone(),
        )

        cutting_qty = whole_number(payload.get('cuttingQty'), 'Cutting Qty', minimum=1)
        current_qty = whole_number(payload.get('currentQty'), 'Current Qty', minimum=1)
        if current_qty > cutting_qty:
            raise ValueError('Current Qty cannot exceed Cutting Qty.')

        detail_ids = payload.get('detailIds')
        if not isinstance(detail_ids, list) or not detail_ids:
            raise ValueError('Scan at least one available roll before saving.')
        detail_ids = [
            whole_number(value, 'Folding detail ID', minimum=1)
            for value in detail_ids
        ]
        if len(set(detail_ids)) != len(detail_ids):
            raise ValueError('A folding detail ID cannot be selected more than once.')

        requested_bundles = payload.get('bundles')
        if not isinstance(requested_bundles, list) or not requested_bundles:
            raise ValueError('At least one bundle quantity is required.')
        bundles = [
            whole_number(
                row.get('qty') if isinstance(row, dict) else None,
                f'Bundle {index} Qty',
                minimum=1,
            )
            for index, row in enumerate(requested_bundles, start=1)
        ]
        if sum(bundles) != current_qty:
            raise ValueError(f'Bundle quantities must total {current_qty} pcs.')

        with transaction.atomic():
            selected_details = list(
                folding_data_details.objects.filter(
                    id__in=detail_ids,
                    rope_cutting__isnull=True,
                    folding_data_id__jobno__iexact=jobno,
                    folding_data_id__topbottom_des__iexact=topbottom,
                    folding_data_id__unitname__iexact=unitname,
                    folding_data_id__color__iexact=colour,
                    folding_data_id__folding_part__iexact=folding_part,
                    folding_data_id__lotno__iexact=lotno,
                    folding_data_id__size__iexact=size,
                ).values('id', 'kgs', 'mtr')
            )
            if {row['id'] for row in selected_details} != set(detail_ids):
                raise ValueError(
                    'One or more selected rolls are unavailable or do not match this entry.'
                )

            total_kgs = sum(
                (row['kgs'] or Decimal('0') for row in selected_details),
                Decimal('0'),
            )
            total_mtrs = sum(
                (row['mtr'] or Decimal('0') for row in selected_details),
                Decimal('0'),
            )
            entry = Rope_cutting_data.objects.create(
                jobno=jobno,
                topbottom=topbottom,
                unitname=unitname,
                date=entry_datetime,
                color=colour,
                folding_part=folding_part,
                lotno=lotno,
                size=size,
                cutting_qty=str(cutting_qty),
                current_qty=str(current_qty),
                total_roll=len(detail_ids),
                kgs=format(total_kgs, 'f'),
                mtrs=format(total_mtrs, 'f'),
            )
            Rope_cutting_data_details.objects.bulk_create(
                [
                    Rope_cutting_data_details(
                        rope_cutting_data_id=entry,
                        bundle_qty=bundle_qty,
                        s_no=index,
                    )
                    for index, bundle_qty in enumerate(bundles, start=1)
                ]
            )
            linked_count = folding_data_details.objects.filter(
                id__in=detail_ids,
                rope_cutting__isnull=True,
            ).update(rope_cutting=entry.id)
            if linked_count != len(detail_ids):
                raise ValueError(
                    'One or more selected rolls were already used by another entry.'
                )
    except ValueError as error:
        return JsonResponse({'error': str(error)}, status=400)

    return JsonResponse(
        {
            'success': True,
            'id': entry.id,
            'detailCount': len(bundles),
            'rollCount': len(detail_ids),
        },
        status=201,
    )


@csrf_exempt
def save_winding_entry(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required.'}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'Invalid request payload.'}, status=400)

    emp_id = str(data.get('emp_id') or '').strip()
    if not emp_id:
        return JsonResponse({'error': 'Employee ID is required to save.'}, status=400)
    if len(emp_id) > 20:
        return JsonResponse({'error': 'Employee ID cannot exceed 20 characters.'}, status=400)

    def text_value(value, field_name, max_length, required=False):
        text = str(value or '').strip()
        if required and not text:
            raise ValueError(f'{field_name} is required.')
        if len(text) > max_length:
            raise ValueError(f'{field_name} cannot exceed {max_length} characters.')
        return text or None

    def decimal_value(value, field_name):
        if value in (None, ''):
            return Decimal('0')
        try:
            number = Decimal(str(value))
            quantized = number.quantize(Decimal('0.0001'))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError(f'{field_name} must be a valid number with up to 4 decimal places.')
        if not number.is_finite() or number < 0 or number != quantized:
            raise ValueError(f'{field_name} must be non-negative with up to 4 decimal places.')
        return number

    try:
        jobno = text_value(data.get('jobNo'), 'Job No', 50, required=True)
        topbottom = text_value(data.get('topBott'), 'Top/Bottom', 50, required=True)
        unitname = text_value(data.get('unit'), 'Unit', 50, required=True)
        color = text_value(data.get('colourCombo'), 'Colour Combo', 100)
        folding_part = text_value(data.get('foldingParts'), 'Folding Part', 100)
        fabclr = text_value(data.get('fabricColour'), 'Fabric Colour', 50)
        lotno = text_value(data.get('lotNo'), 'Lot No', 10, required=True)
        size = text_value(data.get('size'), 'Size', 35, required=True)
        req_kg = decimal_value(data.get('reqKg'), 'Required Kg')
        req_mtr = decimal_value(data.get('reqMtr'), 'Required Mtr')
        prev_kg = decimal_value(data.get('prevKg'), 'Previous Kg')

        scanned_roll = data.get('scannedRoll')
        if not isinstance(scanned_roll, dict):
            raise ValueError('Scan a roll before saving.')
        roll_no = text_value(scanned_roll.get('rollNo'), 'Roll No', 50, required=True)
        roll_color = text_value(scanned_roll.get('colour'), 'Roll Colour', 100)
        roll_lotno = text_value(scanned_roll.get('lot'), 'Roll Lot No', 10)
        fabric = text_value(
            scanned_roll.get('fabricType') or scanned_roll.get('fabric'),
            'Fabric',
            100,
        )
        stock_kg = decimal_value(scanned_roll.get('stockKg'), 'Stock Kg')
        stock_mtr = decimal_value(scanned_roll.get('stockMtr'), 'Stock Mtr')

        requested_rows = data.get('windingDetails')
        if not isinstance(requested_rows, list):
            raise ValueError('Winding details are required.')

        details = []
        total_kg = Decimal('0')
        total_mtr = Decimal('0')
        for row_index, row in enumerate(requested_rows, start=1):
            if not isinstance(row, dict):
                raise ValueError('Each winding detail must be an object.')
            w_id = row.get('w_id', row_index)
            if isinstance(w_id, bool) or not isinstance(w_id, int) or w_id < 1:
                raise ValueError('Winding S.No must be a positive whole number.')
            wgt_kg = decimal_value(row.get('wgtKg'), 'Wgt Kg')
            current_mtr = decimal_value(row.get('mtrs'), 'Mtrs')
            if wgt_kg == 0 and current_mtr == 0:
                continue
            details.append((w_id, wgt_kg, current_mtr))
            total_kg += wgt_kg
            total_mtr += current_mtr

        if not details:
            raise ValueError('Enter at least one winding weight or meter value.')
        if total_kg > max(Decimal('0'), req_kg - prev_kg):
            raise ValueError('Total Wgt Kg cannot exceed the remaining Required Kg.')
        if total_kg > stock_kg:
            raise ValueError('Total Wgt Kg cannot exceed the scanned roll Stock Kg.')
    except ValueError as error:
        return JsonResponse({'error': str(error)}, status=400)

    with transaction.atomic():
        entry = folding_data.objects.create(
            jobno=jobno,
            topbottom_des=topbottom,
            unitname=unitname,
            color=color,
            folding_part=folding_part,
            lotno=lotno,
            size=size,
            req_mtr=req_mtr,
            req_kg=req_kg,
            fabclr=fabclr,
            emp_id=emp_id,
            current_kg=total_kg,
            current_mtr=total_mtr,
        )
        folding_data_details.objects.bulk_create(
            [
                folding_data_details(
                    folding_data_id=entry,
                    roll_no=roll_no,
                    color=roll_color,
                    lotno=roll_lotno,
                    fabric=fabric,
                    kgs=stock_kg,
                    mtr=stock_mtr,
                    wgt_kg=wgt_kg,
                    current_mtr=current_mtr,
                    w_id=w_id,
                )
                for w_id, wgt_kg, current_mtr in details
            ]
        )

    return JsonResponse(
        {'success': True, 'id': entry.id, 'detailCount': len(details)},
        status=201,
    )


############## End of Rip Entry API ##############

