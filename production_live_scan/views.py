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
from .models import unit_input,Msizes
from django.utils.dateparse import parse_datetime
from django.utils import timezone

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
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__date=date_obj)
        else:
            four_days_ago = datetime.now() - timedelta(days=4)
            data = unit_input.objects.filter(unit=unit, line=line, entry_date__gte=four_days_ago)

        # JSON response
        results = list(data.values('bundle_id', 'job_no', 'pc', 'color', 'entry_date'))
        return Response({"status": True, "data": results})


