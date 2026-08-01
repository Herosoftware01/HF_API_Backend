from collections import Counter
from datetime import datetime,date
from django.http import JsonResponse
from .models import TrsCdelPcs21,TrsCdelPcs1,MasUnit,Bundlereport,TrsMcutstickerprod,Unituser,MasTopbottom
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.shortcuts import redirect
from django.db.models import Q



def resolve_unit_code(raw_value, unit_lookup=None):
    if raw_value is None:
        raise ValueError("unitid is required")

    value = str(raw_value).strip()
    if not value:
        raise ValueError("unitid is required")

    try:
        return int(value)
    except ValueError:
        if unit_lookup is not None:
            resolved = unit_lookup(value)
            if resolved is not None:
                return int(resolved)

        raise ValueError(f"Unsupported unit id: {raw_value}")


@csrf_exempt
def bundle_home(request):

    pcs21 = list(
        TrsCdelPcs21.objects.using('demo')
        .values('id', 'mbundid', 'mbappr')
    )

    ids = list(set(p["id"] for p in pcs21))

    start_dt = datetime(2026, 7, 13, 0, 0, 0)

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
def allocate_unit(request, unitname=None):

    unitname = unitname or request.GET.get("unit_name")

    if not unitname:
        return JsonResponse({
            "status": False,
            "message": "unit_name is required"
        }, status=400)

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

    start_dt = datetime(2026, 7, 13, 0, 0, 0)

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

@csrf_exempt
def approve_bundle(request):
    if request.method == "POST":
        mbundid = request.POST.get("mbundid")
        raw_unitid = request.POST.get("unitid")

        try:
            current_unitid = resolve_unit_code(
                raw_unitid,
                unit_lookup=lambda unit_name: MasUnit.objects.using("main")
                .filter(unitname__iexact=unit_name)
                .values_list("unitcode", flat=True)
                .first()
            )
        except ValueError as exc:
            return JsonResponse({"status": "error", "message": str(exc)}, status=400)

        print("bundle and unit id is ", mbundid, current_unitid)

        try:
            # Step 1: Get pcs21 record
            pcs21 = TrsCdelPcs21.objects.using('demo').get(mbundid=mbundid)
        except TrsCdelPcs21.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Bundle {mbundid} not found"}, status=404)

        # Step 2: Get corresponding pcs1 record and related data
        try:
            pcs1 = TrsCdelPcs1.objects.using('demo').get(id=pcs21.id)
            unit = MasUnit.objects.using('main').get(unitcode=pcs1.unitid)
            unit_name = unit.unitname
            topbottom = MasTopbottom.objects.using('main').get(topbottom_id=pcs1.tbid)
        except TrsCdelPcs1.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Matching record not found in pcs1"}, status=404)
        except MasUnit.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Unit with code {pcs1.unitid} not found"}, status=404)
        except MasTopbottom.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Top/Bottom description for id {pcs1.tbid} not found"}, status=404)

        # Step 3: Check unitid
        if pcs1.unitid != current_unitid:
            return JsonResponse({"status": "error", "message": f"This bundle {mbundid} belongs to another unit: {unit_name}"}, status=400)

        # Step 4: Approve or show already approved
        if pcs21.mbappr == 1:
            return JsonResponse({
                "status": "warning",
                "message": f"This bundle {mbundid} already approved"
            }, status=200)

        pcs21.mbappr = 1
        pcs21.save(using='demo')

        Bundlereport.objects.using('app').create(
            s_date=datetime.now(),
            job_no=pcs1.jobno,
            unit_id=current_unitid,
            mbundle_id=pcs21.mbundid,
            tb_name=topbottom.topbottom_des,
            total_bundles=pcs1.totbdl,  # safer from pcs1
            pcs_count=pcs1.totpcs,
            r_date=None,
            scan=0                      # scanned successfully
        )

        return JsonResponse({"status": "success", "message": f"Bundle {mbundid} approved successfully"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def sub_bundle_report(request, unit_id):
    start_dt = datetime(2026, 7, 13, 0, 0, 0)

    unit, unit_code, unit_number = _resolve_unit_for_value(unit_id)

    bundles = Bundlereport.objects.using("app").filter(
        Q(unit_id=unit_code) | Q(unit_id=unit_number),
        scan=0,
        s_date__gte=start_dt
    ).order_by("-s_date")

    bundle_data = []
    for bundle in bundles:
        bundle_data.append({
            "id": bundle.id,
            "unit_id": bundle.unit_id,
            "mbundle_id": bundle.mbundle_id,
            "bundle_no": getattr(bundle, "bundle_no", None),
            "job_no": getattr(bundle, "job_no", None),
            "tb_name": getattr(bundle, "tb_name", None),
            "total_bundles": getattr(bundle, "total_bundles", None),
            "pcs_count": getattr(bundle, "pcs_count", None),
            "scan": int(bundle.scan or 0),
            "S_date": bundle.s_date.strftime("%Y-%m-%d %H:%M:%S") if bundle.s_date else None,
        })

    if not bundle_data and unit:
        pending_data = _pending_master_bundles_for_unit(unit, start_dt)
        bundle_data = pending_data

    return JsonResponse({
        "status": True,
        "unit_id": unit_id,
        "unit_name": unit.unitname if unit else unit_id,
        "count": len(bundle_data),
        "bundles": bundle_data
    })


def _resolve_unit_for_value(unit_id):
    unit_code = str(unit_id).strip()
    unit_number = unit_code.upper().replace("UNIT-", "")

    unit_lookup = Q(unitname__iexact=unit_code)
    if unit_number.isdigit():
        unit_lookup |= Q(unitcode=int(unit_number))

    unit = MasUnit.objects.using("main").filter(unit_lookup).first()
    return unit, unit_code, unit_number


def _pending_master_bundles_for_unit(unit, start_dt):
    pcs21_qs = TrsCdelPcs21.objects.using("demo").filter(
        mbappr=0
    ).values(
        "id",
        "mbundid",
        "mbappr"
    )

    pcs21_by_id = {
        row["id"]: row
        for row in pcs21_qs
    }

    pcs1_qs = TrsCdelPcs1.objects.using("demo").filter(
        id__in=pcs21_by_id.keys(),
        unitid=unit.unitcode,
        dt__gte=start_dt
    ).values(
        "id",
        "dt",
        "unitid",
        "jobno",
        "tbid",
        "totbdl",
        "totpcs"
    ).order_by("-dt")

    tbids = {
        row["tbid"]
        for row in pcs1_qs
        if row["tbid"] is not None
    }

    topbottom_map = dict(
        MasTopbottom.objects.using("main")
        .filter(topbottom_id__in=tbids)
        .values_list("topbottom_id", "topbottom_des")
    )

    bundle_data = []
    for pcs1 in pcs1_qs:
        pcs21 = pcs21_by_id.get(pcs1["id"])
        if not pcs21:
            continue

        bundle_data.append({
            "id": pcs21["id"],
            "unit_id": str(pcs1["unitid"]),
            "mbundle_id": str(pcs21["mbundid"]),
            "bundle_no": None,
            "job_no": pcs1["jobno"],
            "tb_name": topbottom_map.get(pcs1["tbid"], pcs1["tbid"]),
            "total_bundles": pcs1["totbdl"],
            "pcs_count": pcs1["totpcs"],
            "scan": int(pcs21["mbappr"] or 0),
            "S_date": pcs1["dt"].strftime("%Y-%m-%d %H:%M:%S") if pcs1["dt"] else None,
        })

    return bundle_data


@csrf_exempt
def fetch_bundle_details(request):
    if request.method == "POST":
        mbundid = request.POST.get("mbundid")
        unit_id = request.POST.get("unit_id")
        start_dt = datetime(2026, 7, 13, 0, 0, 0)
      

        print("mbundid, unit_id", mbundid, unit_id)

        unit, unit_code, unit_number = _resolve_unit_for_value(unit_id)

        # 1️⃣ CHECK BundleReport FIRST
        exists = Bundlereport.objects.using("app").filter(
            mbundle_id=mbundid,
            scan=0
        ).filter(
            Q(unit_id=unit_code) | Q(unit_id=unit_number)
        ).exists()

        # 2️⃣ GET PCS21
        try:
            pcs21 = TrsCdelPcs21.objects.using("demo").get(mbundid=mbundid)
        except TrsCdelPcs21.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Bundle not found in PCS21"
            })

        # 3️⃣ GET PCS3 ROWS
        pcs3_qs = TrsMcutstickerprod.objects.using("demo").filter(mbud=pcs21.mbundid)
       

        if not pcs3_qs.exists():
            return JsonResponse({
                "status": "error",
                "message": "No PCS3 data found"
            })

        data = list(pcs3_qs.values(
            "bund_id",
            "sizid",
            "lotno",
            "bdl",
            "pc",
            "comboclr",
            "bundid",
            "scan"
        ))

        return JsonResponse({
            "status": "success",
            "mbundid": mbundid,
            "rows": data
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})


@csrf_exempt
def update_child_bundle_scan(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    bundid = request.POST.get("bundid")
    mbundid = request.POST.get("mbundid")
    unit_id = request.POST.get("unit_id")

    # 🔐 SAFETY CHECK
    if not bundid or not mbundid or not unit_id:
        return JsonResponse({
            "status": "error",
            "message": "Missing data"
        })

    # 1️⃣ GET PCS21
    try:
        pcs21 = TrsCdelPcs21.objects.using("demo").get(mbundid=mbundid)
    except TrsCdelPcs21.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Invalid master bundle"
        })

    # 2️⃣ UPDATE CHILD BUNDLE (bundid match)
    updated = TrsMcutstickerprod.objects.using("demo").filter(
        mbud=pcs21.mbundid,
        bundid=bundid
    ).update(scan="1")

    if updated == 0:
        return JsonResponse({
            "status": "error",
            "message": "Child bundle not found"
        })

    # 3️⃣ CHECK ALL CHILD BUNDLES
    total_count = TrsMcutstickerprod.objects.using("demo").filter(
        mbud=pcs21.mbundid
    ).count()

    scanned_count = TrsMcutstickerprod.objects.using("demo").filter(
        mbud=pcs21.mbundid,
        scan=1
    ).count()

    all_done = total_count == scanned_count and total_count > 0

    # 4️⃣ UPDATE BundleReport
    if all_done:
        Bundlereport.objects.using("app").filter(
            mbundle_id=mbundid,
            unit_id=unit_id
        ).update(
            scan=1,
            r_date=timezone.now().date()
        )

    return JsonResponse({
        "status": "success",
        "all_done": all_done,
        "total": total_count,
        "scanned": scanned_count
    })
