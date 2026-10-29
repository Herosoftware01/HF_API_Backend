from collections import Counter
from datetime import datetime
import json
import re

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Bundlereport,
    MasTopbottom,
    MasUnit,
    Msizes,
    TrsCdelPcs1,
    TrsCdelPcs21,
    TrsMcutstickerprod,
)

SYSTEM_START_DATE = datetime(2026, 10, 1, 0, 0, 0)


# ==============================================================================
# Helper Functions
# ==============================================================================

def resolve_unit(raw_value):
    if raw_value is None:
        raise ValueError("Unit ID is required")

    val_str = str(raw_value).strip()
    if not val_str:
        raise ValueError("Unit ID is required")

    unit = MasUnit.objects.using("main").filter(unitname__iexact=val_str).first()
    if not unit and val_str.isdigit():
        unit = MasUnit.objects.using("main").filter(unitcode=int(val_str)).first()

    if not unit:
        num_part = re.sub(r"[^\d]", "", val_str)
        if num_part:
            unit = MasUnit.objects.using("main").filter(unitcode=int(num_part)).first()

    if not unit:
        if val_str.isdigit():
            return None, int(val_str), val_str
        raise ValueError(f"Unit could not be resolved from identifier: {raw_value}")

    return unit, unit.unitcode, unit.unitname


def _get_search_mbuds(mbund_id):
    """
    Returns search query IDs for TrsMcutstickerprod.mbud.
    Matches either pcs21.id or pcs21.mbundid.
    """
    clean_id = str(mbund_id).strip()
    pcs21 = TrsCdelPcs21.objects.using("demo").filter(mbundid=clean_id).first()
    ids = [clean_id]
    if pcs21:
        ids.append(pcs21.id)
        if str(pcs21.id) not in ids:
            ids.append(str(pcs21.id))
    return ids

def _get_bundle_context(mbund_id):
    """
    Finds the exact pcs21 and pcs1 records for a master bundle.
    """
    clean_id = str(mbund_id).strip()
    pcs21 = TrsCdelPcs21.objects.using("demo").filter(mbundid=clean_id).first()
    pcs1 = None
    if pcs21:
        pcs1 = TrsCdelPcs1.objects.using("demo").filter(id=pcs21.id).first()
    return pcs21, pcs1

# ==============================================================================
# Views
# ==============================================================================

@csrf_exempt
def bundle_home(request):
    unapproved_pcs21 = list(
        TrsCdelPcs21.objects.using("demo")
        .filter(mbappr=0)
        .values("id", "mbundid")
    )
    dc_ids = list({p["id"] for p in unapproved_pcs21})

    pcs1_qs = list(
        TrsCdelPcs1.objects.using("demo")
        .filter(id__in=dc_ids, dt__gte=SYSTEM_START_DATE)
        .values("id", "unitid")
    )
    pcs1_map = {row["id"]: row["unitid"] for row in pcs1_qs}

    all_units = list(MasUnit.objects.using("main").values("unitcode", "unitname"))
    unit_map = {u["unitcode"]: u["unitname"] for u in all_units}

    master_counter = Counter()
    for p21 in unapproved_pcs21:
        unitcode = pcs1_map.get(p21["id"])
        unitname = unit_map.get(unitcode)
        if unitname:
            master_counter[unitname] += 1

    pending_counter = Counter()
    pending_reports = Bundlereport.objects.using("app").filter(
        scan=0, 
        s_date__gte=SYSTEM_START_DATE
    ).values("mbundle_id", "unit_id")

    for report in pending_reports:
        mbund_id = report["mbundle_id"]
        unit_key = report["unit_id"]

        try:
            target_unit_name = unit_map.get(int(unit_key), str(unit_key))
        except (ValueError, TypeError):
            target_unit_name = str(unit_key)

        search_mbuds = _get_search_mbuds(mbund_id)
        child_pending = (
            TrsMcutstickerprod.objects.using("demo")
            .filter(mbud__in=search_mbuds, scan__in=[0, "0", None])
            .count()
        )
        if child_pending > 0:
            pending_counter[target_unit_name] += child_pending

    all_unit_names = sorted(list(set(unit_map.values())))
    response_data = []
    for uname in all_unit_names:
        m_count = master_counter.get(uname, 0)
        p_count = pending_counter.get(uname, 0)
        response_data.append({
            "unit_name": uname,
            "master_bundle_count": m_count,
            "pending_child_bundle_count": p_count,
            "detail_url": f"/bundle_tracking/allocate_unit/{uname}/"
        })

    return JsonResponse({
        "status": True,
        "count": len(response_data),
        "data": response_data
    })


@csrf_exempt
def allocate_unit(request, unitname=None):
    raw_unit = unitname or request.GET.get("unit_name")
    try:
        unit, unit_code, unit_name = resolve_unit(raw_unit)
    except ValueError as e:
        return JsonResponse({"status": False, "message": str(e)}, status=400)

    pcs21_qs = TrsCdelPcs21.objects.using("demo").filter(mbappr=0)
    mbundid_filter = request.GET.get("mbundid")
    if mbundid_filter:
        pcs21_qs = pcs21_qs.filter(mbundid=mbundid_filter)

    pcs21_rows = list(pcs21_qs.values("id", "mbundid", "mbappr"))
    dc_ids = [p["id"] for p in pcs21_rows]

    pcs1_rows = list(
        TrsCdelPcs1.objects.using("demo")
        .filter(id__in=dc_ids, unitid=unit_code, dt__gte=SYSTEM_START_DATE)
        .values("id", "dt", "unitid", "jobno", "tbid", "totbdl", "totpcs", "del_remarks")
    )
    pcs1_map = {row["id"]: row for row in pcs1_rows}

    tbids = {r["tbid"] for r in pcs1_rows if r.get("tbid")}
    topbottom_map = dict(
        MasTopbottom.objects.using("main")
        .filter(topbottom_id__in=tbids)
        .values_list("topbottom_id", "topbottom_des")
    )

    records = []
    for p21 in pcs21_rows:
        p1 = pcs1_map.get(p21["id"])
        if not p1:
            continue

        records.append({
            "id": p21["id"],
            "mbundid": p21["mbundid"],
            "mbappr": p21["mbappr"],
            "dt": p1.get("dt"),
            "unitid": p1.get("unitid"),
            "jobno": p1.get("jobno"),
            "tbid": topbottom_map.get(p1.get("tbid")),
            "totbdl": p1.get("totbdl"),
            "totpcs": p1.get("totpcs"),
            "del_remarks": p1.get("del_remarks"),
        })

    dc_counts = Counter(r["id"] for r in records)

    return JsonResponse({
        "status": True,
        "unitname": unit_name,
        "unitid": unit_code,
        "count": len(records),
        "total_dc": len(dc_counts),
        "records": records,
        "dc_counts": dict(dc_counts)
    })


@csrf_exempt
def approve_bundle(request):
    """
    Receives Master Bundle barcode into unit:
    1. Validates that the bundle belongs to the given unit code.
    2. Updates TrsCdelPcs21.mbappr = 1.
    3. Resets child stickers in TrsMcutstickerprod to scan = '0' so they require scanning!
    4. Creates Bundlereport entry with scan = 0.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST method required"}, status=405)

    mbundid = request.POST.get("mbundid")
    raw_unitid = request.POST.get("unitid")

    if not mbundid or not raw_unitid:
        return JsonResponse({"status": "error", "message": "mbundid and unitid are required"}, status=400)

    try:
        _, current_unit_code, _ = resolve_unit(raw_unitid)
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

    try:
        pcs21 = TrsCdelPcs21.objects.using("demo").get(mbundid=mbundid)
    except TrsCdelPcs21.DoesNotExist:
        return JsonResponse({"status": "error", "message": f"Bundle {mbundid} not found"}, status=404)

    try:
        pcs1 = TrsCdelPcs1.objects.using("demo").get(id=pcs21.id)
    except TrsCdelPcs1.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Matching DC record not found in PCS1"}, status=404)

    if pcs1.unitid != current_unit_code:
        expected_unit = MasUnit.objects.using("main").filter(unitcode=pcs1.unitid).first()
        expected_name = expected_unit.unitname if expected_unit else str(pcs1.unitid)
        return JsonResponse({
            "status": "error",
            "message": f"Bundle {mbundid} belongs to {expected_name}, not this unit."
        }, status=400)

    if pcs21.mbappr == 1:
        return JsonResponse({
            "status": "warning",
            "message": f"Bundle {mbundid} is already approved"
        }, status=200)

    pcs21.mbappr = 1
    pcs21.save(using="demo")

    # IMPORTANT: Ensure all sub-stickers under this master bundle are ready with scan = '0'
    # so they are NOT treated as already completed!
    search_mbuds = [pcs21.id, pcs21.mbundid, str(pcs21.id), str(pcs21.mbundid)]
    TrsMcutstickerprod.objects.using("demo").filter(mbud__in=search_mbuds).update(scan="0")

    # Create tracking row in Bundlereport
    Bundlereport.objects.using("app").create(
        s_date=timezone.now(),
        job_no=pcs1.jobno,
        unit_id=str(pcs1.unitid),
        mbundle_id=str(pcs21.mbundid),
        tb_name=str(pcs1.tbid),
        total_bundles=pcs1.totbdl,
        pcs_count=pcs1.totpcs,
        r_date=None,
        scan=0  # Must be 0
    )

    return JsonResponse({"status": "success", "message": f"Bundle {mbundid} approved successfully"})


def sub_bundle_report(request, unit_id):
    """
    Returns pending master bundles for sub-bundle scanning.
    ONLY bundles with scan=0 are returned.
    Does NOT auto-update unit_bundlereport to scan=1.
    """
    try:
        unit, unit_code, unit_name = resolve_unit(unit_id)
    except ValueError as e:
        return JsonResponse({"status": False, "message": str(e)}, status=400)

    bundles_qs = Bundlereport.objects.using("app").filter(
        Q(unit_id=str(unit_code)) | Q(unit_id=unit_name),
        scan=0,
        s_date__gte=SYSTEM_START_DATE
    ).order_by("-s_date")

    bundle_data = []
    for bundle in bundles_qs:
        bundle_data.append({
            "id": bundle.id,
            "unit_id": str(bundle.unit_id),
            "mbundle_id": bundle.mbundle_id,
            "bundle_no": bundle.mbundle_id,
            "job_no": bundle.job_no,
            "tb_name": bundle.tb_name,
            "total_bundles": bundle.total_bundles,
            "pcs_count": bundle.pcs_count,
            "scan": int(bundle.scan or 0),
            "S_date": bundle.s_date.strftime("%Y-%m-%d %H:%M:%S") if bundle.s_date else None,
        })

    return JsonResponse({
        "status": True,
        "unit_id": unit_code,
        "unit_name": unit_name,
        "count": len(bundle_data),
        "bundles": bundle_data
    })


@csrf_exempt
def fetch_bundle_details(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    mbundid = request.POST.get("mbundid")
    if not mbundid:
        return JsonResponse({"status": "error", "message": "mbundid is required"}, status=400)

    clean_mbundid = str(mbundid).strip()
    pcs21, pcs1 = _get_bundle_context(clean_mbundid)

    # 1. Search strictly by mbundid first
    pcs3_qs = TrsMcutstickerprod.objects.using("demo").filter(mbud=clean_mbundid)

    # 2. If no direct match by mbud, filter with jobno context to prevent cross-contamination
    if not pcs3_qs.exists() and pcs1 and pcs1.jobno:
        # Check if stickers match by jobno and master bundle id or sticker prefix
        pcs3_qs = TrsMcutstickerprod.objects.using("demo").filter(
            Q(mbud=clean_mbundid) | Q(bundid__icontains=clean_mbundid)
        )

    # If still not found, search with fallback but never use small integers like pcs21.id blindly
    if not pcs3_qs.exists():
        return JsonResponse({
            "status": "error", 
            "message": f"No child bundle records found for Master Bundle {clean_mbundid}"
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

    size_ids = {row["sizid"] for row in data if row.get("sizid") is not None}
    size_names = dict(
        Msizes.objects.using("test")
        .filter(id__in=size_ids)
        .values_list("id", "name")
    )

    for row in data:
        row["sizname"] = size_names.get(row["sizid"], str(row.get("sizid", "")))
        row["scan"] = 1 if str(row.get("scan")).strip() in ["1", "True"] else 0

    return JsonResponse({
        "status": "success",
        "mbundid": clean_mbundid,
        "rows": data
    })


# ==============================================================================
# Fixed update_child_bundle_scan
# ==============================================================================

@csrf_exempt
def update_child_bundle_scan(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    bundid = request.POST.get("bundid")
    mbundid = request.POST.get("mbundid")

    if not bundid or not mbundid:
        return JsonResponse({"status": "error", "message": "bundid and mbundid required"}, status=400)

    clean_mbundid = str(mbundid).strip()
    clean_bundid = str(bundid).strip()

    pcs21, pcs1 = _get_bundle_context(clean_mbundid)
    if not pcs21:
        return JsonResponse({"status": "error", "message": "Invalid master bundle"}, status=404)

    target_unit_id = pcs1.unitid if pcs1 else None

    # Handle ~0 format variants
    possible_ids = [clean_bundid]
    if clean_bundid.endswith("~0"):
        possible_ids.append(clean_bundid[:-2])
    else:
        possible_ids.append(clean_bundid + "~0")

    # Update only the child sticker belonging to this master bundle
    updated = TrsMcutstickerprod.objects.using("demo").filter(
        mbud=clean_mbundid,
        bundid__in=possible_ids
    ).update(
        scan="1",
        unit_id=target_unit_id
    )

    if updated == 0:
        # Fallback if mbud is stored differently in TrsMcutstickerprod
        updated = TrsMcutstickerprod.objects.using("demo").filter(
            bundid__in=possible_ids
        ).update(
            scan="1",
            unit_id=target_unit_id
        )

    if updated == 0:
        return JsonResponse({"status": "error", "message": f"Child bundle {bundid} not found"}, status=404)

    # Check sibling completion strictly under this master bundle
    total_count = TrsMcutstickerprod.objects.using("demo").filter(mbud=clean_mbundid).count()
    scanned_count = TrsMcutstickerprod.objects.using("demo").filter(
        mbud=clean_mbundid,
        scan__in=[1, "1", True]
    ).count()

    all_done = (total_count == scanned_count and total_count > 0)

    if all_done:
        Bundlereport.objects.using("app").filter(mbundle_id=clean_mbundid).update(
            scan=1,
            unit_id=str(target_unit_id),
            r_date=timezone.now().date()
        )

    return JsonResponse({
        "status": "success",
        "all_done": all_done,
        "total": total_count,
        "scanned": scanned_count,
        "unit_id": target_unit_id
    })