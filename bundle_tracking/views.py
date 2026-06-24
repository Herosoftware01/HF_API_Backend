from collections import Counter
from datetime import datetime
from django.http import JsonResponse
from .models import TrsCdelPcs21,TrsCdelPcs1,MasUnit,Bundlereport,TrsMcutstickerprod,Unituser,MasTopbottom
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect


@csrf_exempt
def bundle_home(request):

    pcs21 = list(
        TrsCdelPcs21.objects.using('demo')
        .values('id', 'mbundid', 'mbappr')
    )

    ids = list(set(p["id"] for p in pcs21))

    start_dt = datetime(2026, 6, 8, 0, 0, 0)

    pcs11_qs = TrsCdelPcs1.objects.using('demo').filter(
        id__in=ids,
        dt__gte=start_dt
    ).values(
        'id',
        'unitid'
    )

    pcs11_map = {row["id"]: row for row in pcs11_qs}

    unitids = list(
        set(
            row['unitid']
            for row in pcs11_qs
            if row['unitid'] is not None
        )
    )

    units_qs = MasUnit.objects.using('main').filter(
        unitcode__in=unitids
    ).values(
        'unitcode',
        'unitname'
    )

    units_map = {
        u['unitcode']: u['unitname']
        for u in units_qs
    }

    master_counter = Counter()

    for p21 in pcs21:

        p11 = pcs11_map.get(p21["id"])

        if not p11:
            continue

        unitid = p11.get("unitid")
        unitname = units_map.get(unitid)

        if unitname and p21["mbappr"] == 0:
            master_counter[unitname] += 1

    pending_counter = Counter()

    bundle_reports = Bundlereport.objects.using('app').filter(
        scan=0,
        s_date__gte=start_dt
    ).values(
        'mbundle_id',
        'unit_id'
    )

    mbundid_to_unit = {
        int(br["mbundle_id"]): br["unit_id"]
        for br in bundle_reports
        if str(br["mbundle_id"]).isdigit()
    }

    pcs21_map = {
        p["mbundid"]: p["id"]
        for p in TrsCdelPcs21.objects.using('demo').values(
            'mbundid',
            'id'
        )
    }

    for mbundid, unit_id in mbundid_to_unit.items():

        pcs21_id = pcs21_map.get(mbundid)

        if not pcs21_id:
            continue

        pending_child_count = (
            TrsMcutstickerprod.objects.using('demo')
            .filter(
                mbud=pcs21_id,
                scan=0
            )
            .count()
        )

        if pending_child_count > 0:

            unit_name = units_map.get(int(unit_id))

            if unit_name:
                pending_counter[unit_name] += pending_child_count

    all_units = sorted(
        set(master_counter.keys()) |
        set(pending_counter.keys())
    )

    response_data = []

    for unit in all_units:

        response_data.append({
            "unit_name": unit,
            "master_bundle_count": master_counter.get(unit, 0),
            "pending_child_bundle_count": pending_counter.get(unit, 0),
            "detail_url": f"/bundle_tracking/allocate_unit/{unit}/"
        })

    return JsonResponse({
        "status": True,
        "count": len(response_data),
        "data": response_data
    })

@csrf_exempt
def unit_login_api(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "POST required"
        }, status=405)

    try:
        data = json.loads(request.body)

        unit = data.get("unit")
        user_id = data.get("user_id")
        password = data.get("password")

        user = Unituser.objects.using("app").filter(
            unit_name=unit,
            user_id=user_id,
            password=password
        ).first()

        if user:
            return JsonResponse({
                "status": "success",
                "message": "Login successful"
            })

        return JsonResponse({
            "status": "failed",
            "message": "Invalid credentials"
        })

    except Exception as e:
        print("ERROR:", str(e))

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


@csrf_exempt
def allocate_unit(request, unitname):

    mbundid_filter = request.GET.get("mbundid")

    pcs21_qs = TrsCdelPcs21.objects.using('demo').filter(
        mbappr=0
    )

    if mbundid_filter:
        pcs21_qs = pcs21_qs.filter(
            mbundid=mbundid_filter
        )

    pcs21_qs = pcs21_qs.values(
        'id',
        'mbundid',
        'mbappr'
    )

    ids = [p['id'] for p in pcs21_qs]

    start_dt = datetime(2026, 6, 8, 0, 0, 0)

    pcs11_qs = TrsCdelPcs1.objects.using('demo').filter(
        id__in=ids,
        dt__gte=start_dt
    ).values(
        'id',
        'dt',
        'unitid',
        'jobno',
        'tbid',
        'totbdl',
        'totpcs',
        'del_remarks'
    )

    pcs11_map = {
        row['id']: row
        for row in pcs11_qs
    }

    unitids = set(
        row['unitid']
        for row in pcs11_qs
        if row['unitid'] is not None
    )

    units_qs = MasUnit.objects.using('main').filter(
        unitcode__in=unitids
    ).values(
        'unitcode',
        'unitname'
    )

    units_map = {
        u['unitcode']: u['unitname']
        for u in units_qs
    }

    current_unit_id = None

    for uid, uname in units_map.items():

        if uname.upper() == unitname.upper():
            current_unit_id = uid
            break

    tbids = set(
        row['tbid']
        for row in pcs11_qs
        if row['tbid'] is not None
    )

    topbottom_map = dict(
        MasTopbottom.objects.using('main')
        .filter(
            topbottom_id__in=tbids
        )
        .values_list(
            'topbottom_id',
            'topbottom_des'
        )
    )

    records = []

    for p21 in pcs21_qs:

        p11 = pcs11_map.get(
            p21['id'],
            {}
        )

        unitid_row = p11.get('unitid')

        unitname_db = units_map.get(
            unitid_row,
            ""
        )

        if unitname_db.upper() != unitname.upper():
            continue

        records.append({
            "id": p21["id"],
            "mbundid": p21["mbundid"],
            "mbappr": p21["mbappr"],
            "dt": p11.get("dt"),
            "unitid": unitid_row,
            "jobno": p11.get("jobno"),
            "tbid": topbottom_map.get(
                p11.get('tbid')
            ),
            "totbdl": p11.get("totbdl"),
            "totpcs": p11.get("totpcs"),
            "del_remarks": p11.get("del_remarks"),
        })

    dc_counts = Counter(
        record['id']
        for record in records
    )

    return JsonResponse({
        "status": True,
        "unitname": unitname,
        "unitid": current_unit_id,
        "count": len(records),
        "records": records,
        "dc_counts": dict(dc_counts)
    })
