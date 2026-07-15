from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from imp_reports.models import UnitBundlereport
from bundle_tracking.models import TrsMcutstickerprod,MasUnit


@require_GET
def live_scan_data(request):

    start_date = datetime(2026, 7, 15, 0, 0, 0)

    # Unit bundle report
    reports = UnitBundlereport.objects.using("app").filter(
        s_date__gte=start_date,
        scan=1
    )


    # mbundle_id mapping
    report_map = {}

    unit_ids = set()

    for r in reports:
        report_map[str(r.mbundle_id)] = r
        unit_ids.add(int(r.unit_id))


    # Unit master
    units = MasUnit.objects.using("main").filter(
        unitcode__in=unit_ids
    )


    unit_name = {
        str(u.unitcode): u.unitname
        for u in units
    }


    # Trs data
    trs_data = TrsMcutstickerprod.objects.using("demo").filter(
        mbud__in=report_map.keys(),
        dt__gte=start_date,
        scan="1",
        livescan__isnull=True
    )


    # Group by unit
    final_data = {}


    for row in trs_data:

        report = report_map.get(
            str(row.mbud)
        )

        if not report:
            continue


        uid = str(report.unit_id)


        if uid not in final_data:
            final_data[uid] = {
                "unit_id": uid,
                "unit_name": unit_name.get(uid),
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
            "comboclr": row.comboclr,
            "sizid": row.sizid,
            "bdl": row.bdl,
            "pc": row.pc,
            "weight": row.weight,
            "bund_id": row.bund_id,
            "lotno": row.lotno,
            "frmbc": row.frmbc,
            "scan": row.scan,
            "livescan": row.livescan,

            "total_bundles": report.total_bundles,
            "pcs_count": report.pcs_count
        })


    return JsonResponse({

        "status": True,
        "unit_count": len(final_data),
        # All units total records count
        "all_unit_data_count": sum(
            unit["total_records"]
            for unit in final_data.values()
        ),
        "data": list(final_data.values())

    })