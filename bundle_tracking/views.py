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
    """
    Resolves raw input ("UNIT-2", "2", 53) to (MasUnit instance, unitcode_int, unit_str).
    """
    if raw_value is None:
        raise ValueError("Unit ID is required")

    val_str = str(raw_value).strip()
    if not val_str:
        raise ValueError("Unit ID is required")

    # 1. Direct lookup by Unit Name (e.g. "UNIT-2")
    unit = MasUnit.objects.using("main").filter(unitname__iexact=val_str).first()

    # 2. Lookup by Unitcode directly if numeric
    if not unit and val_str.isdigit():
        unit = MasUnit.objects.using("main").filter(unitcode=int(val_str)).first()

    # 3. Lookup by stripping "UNIT-" prefix (e.g. "UNIT-53" -> 53)
    if not unit:
        num_part = re.sub(r"[^\d]", "", val_str)
        if num_part:
            unit = MasUnit.objects.using("main").filter(unitcode=int(num_part)).first()

    if not unit:
        # Fallback if MasUnit row isn't in DB but code is numeric
        if val_str.isdigit():
            return None, int(val_str), val_str
        raise ValueError(f"Unit could not be resolved from identifier: {raw_value}")

    return unit, unit.unitcode, unit.unitname


def _get_completed_mbud_set(mbund_ids):
    """
    Checks TrsMcutstickerprod to see which master bundles have 100% of their child
    stickers scanned. Handles mapping between mbundid and TrsCdelPcs21.id.
    """
    if not mbund_ids:
        return set()

    clean_ids = [str(x).strip() for x in mbund_ids if str(x).strip()]

    # Fetch mapping for pcs21: id <-> mbundid
    pcs21_rows = list(
        TrsCdelPcs21.objects.using("demo")
        .filter(mbundid__in=clean_ids)
        .values("id", "mbundid")
    )
    pcs21_id_to_mbund = {r["id"]: str(r["mbundid"]).strip() for r in pcs21_rows}
    all_query_ids = list(pcs21_id_to_mbund.keys()) + [int(x) for x in clean_ids if x.isdigit()]

    child_stats = (
        TrsMcutstickerprod.objects.using("demo")
        .filter(mbud__in=all_query_ids)
        .values("mbud")
        .annotate(
            total=Count("bundid"),
            scanned=Count("bundid", filter=Q(scan__in=[1, "1", True])),
        )
    )

    completed_mbund_ids = set()
    for row in child_stats:
        if row["total"] > 0 and row["total"] == row["scanned"]:
            # If mbud was pcs21.id, map back to mbundid
            if row["mbud"] in pcs21_id_to_mbund:
                completed_mbund_ids.add(pcs21_id_to_mbund[row["mbud"]])
            completed_mbund_ids.add(str(row["mbud"]).strip())

    return completed_mbund_ids


# ==============================================================================
# Views
# ==============================================================================

@csrf_exempt
def bundle_home(request):
    """
    Dashboard landing page:
    1. Reads all units from MasUnit.
    2. Counts pending Master Bundles (TrsCdelPcs21 where mbappr=0).
    3. Counts pending Child Bundles (TrsMcutstickerprod where scan=0).
    """
    # 1. Fetch unapproved master bundles
    unapproved_pcs21 = list(
        TrsCdelPcs21.objects.using("demo")
        .filter(mbappr=0)
        .values("id", "mbundid")
    )
    dc_ids = list({p["id"] for p in unapproved_pcs21})

    # 2. Get DC header to resolve unit id
    pcs1_qs = list(
        TrsCdelPcs1.objects.using("demo")
        .filter(id__in=dc_ids, dt__gte=SYSTEM_START_DATE)
        .values("id", "unitid")
    )
    pcs1_map = {row["id"]: row["unitid"] for row in pcs1_qs}

    # 3. Resolve unit names
    all_units = list(MasUnit.objects.using("main").values("unitcode", "unitname"))
    unit_map = {u["unitcode"]: u["unitname"] for u in all_units}

    # 4. Count pending master bundles per unit
    master_counter = Counter()
    for p21 in unapproved_pcs21:
        unitcode = pcs1_map.get(p21["id"])
        unitname = unit_map.get(unitcode)
        if unitname:
            master_counter[unitname] += 1

    # 5. Count pending child bundles per unit
    pending_counter = Counter()
    pending_reports = Bundlereport.objects.using("app").filter(
        scan=0, 
        s_date__gte=SYSTEM_START_DATE
    ).values("mbundle_id", "unit_id")

    for report in pending_reports:
        mbund_id = report["mbundle_id"]
        unit_key = report["unit_id"]

        # Resolve unit name
        try:
            target_unit_name = unit_map.get(int(unit_key), str(unit_key))
        except (ValueError, TypeError):
            target_unit_name = str(unit_key)

        # Get pcs21 id for this bundle
        pcs21_row = TrsCdelPcs21.objects.using("demo").filter(mbundid=mbund_id).first()
        search_mbud = pcs21_row.id if pcs21_row else mbund_id

        child_pending = (
            TrsMcutstickerprod.objects.using("demo")
            .filter(Q(mbud=search_mbud) | Q(mbud=mbund_id), scan__in=[0, "0", None])
            .count()
        )
        if child_pending > 0:
            pending_counter[target_unit_name] += child_pending

    all_unit_names = sorted(list(set(unit_map.values())))
    response_data = []
    for uname in all_unit_names:
        m_count = master_counter.get(uname, 0)
        p_count = pending_counter.get(uname, 0)
        # Only show units with activity or include all units
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
    """
    Shows master bundles waiting to be approved for a specific unit.
    Returns unitid (numeric) and pending DC records.
    """
    raw_unit = unitname or request.GET.get("unit_name")
    try:
        unit, unit_code, unit_name = resolve_unit(raw_unit)
    except ValueError as e:
        return JsonResponse({"status": False, "message": str(e)}, status=400)

    # 1. Fetch unapproved bundle records
    pcs21_qs = TrsCdelPcs21.objects.using("demo").filter(mbappr=0)
    mbundid_filter = request.GET.get("mbundid")
    if mbundid_filter:
        pcs21_qs = pcs21_qs.filter(mbundid=mbundid_filter)

    pcs21_rows = list(pcs21_qs.values("id", "mbundid", "mbappr"))
    dc_ids = [p["id"] for p in pcs21_rows]

    # 2. Filter DCs strictly belonging to this unitcode
    pcs1_rows = list(
        TrsCdelPcs1.objects.using("demo")
        .filter(id__in=dc_ids, unitid=unit_code, dt__gte=SYSTEM_START_DATE)
        .values("id", "dt", "unitid", "jobno", "tbid", "totbdl", "totpcs", "del_remarks")
    )
    pcs1_map = {row["id"]: row for row in pcs1_rows}

    # 3. Topbottom descriptions
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
    3. Creates Bundlereport entry with scan = 0.
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

    # 1. Fetch bundle from pcs21
    try:
        pcs21 = TrsCdelPcs21.objects.using("demo").get(mbundid=mbundid)
    except TrsCdelPcs21.DoesNotExist:
        return JsonResponse({"status": "error", "message": f"Bundle {mbundid} not found"}, status=404)

    # 2. Match with DC header
    try:
        pcs1 = TrsCdelPcs1.objects.using("demo").get(id=pcs21.id)
    except TrsCdelPcs1.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Matching DC record not found in PCS1"}, status=404)

    # 3. Unit validation check
    if pcs1.unitid != current_unit_code:
        expected_unit = MasUnit.objects.using("main").filter(unitcode=pcs1.unitid).first()
        expected_name = expected_unit.unitname if expected_unit else str(pcs1.unitid)
        return JsonResponse({
            "status": "error",
            "message": f"Bundle {mbundid} belongs to {expected_name}, not this unit."
        }, status=400)

    # 4. Check already approved
    if pcs21.mbappr == 1:
        return JsonResponse({
            "status": "warning",
            "message": f"Bundle {mbundid} is already approved"
        }, status=200)

    pcs21.mbappr = 1
    pcs21.save(using="demo")

    # 5. Create tracking row in Bundlereport
    Bundlereport.objects.using("app").create(
        s_date=timezone.now(),
        job_no=pcs1.jobno,
        unit_id=str(pcs1.unitid),
        mbundle_id=str(pcs21.mbundid),
        tb_name=str(pcs1.tbid),
        total_bundles=pcs1.totbdl,
        pcs_count=pcs1.totpcs,
        r_date=None,
        scan=0  # Pending sub-bundle scan
    )

    return JsonResponse({"status": "success", "message": f"Bundle {mbundid} approved successfully"})


def sub_bundle_report(request, unit_id):
    """
    Returns pending master bundles for sub-bundle scanning.
    Excludes master bundles where all child stickers are already scanned.
    """
    try:
        unit, unit_code, unit_name = resolve_unit(unit_id)
    except ValueError as e:
        return JsonResponse({"status": False, "message": str(e)}, status=400)

    # Filter Bundlereport by unitcode or unitname
    bundles_qs = Bundlereport.objects.using("app").filter(
        Q(unit_id=str(unit_code)) | Q(unit_id=unit_name),
        scan=0,
        s_date__gte=SYSTEM_START_DATE
    ).order_by("-s_date")

    candidate_ids = [b.mbundle_id for b in bundles_qs if b.mbundle_id]
    completed_mbuds = _get_completed_mbud_set(candidate_ids)

    bundle_data = []
    for bundle in bundles_qs:
        clean_mb_id = str(bundle.mbundle_id).strip()

        # If child scan is already 100% complete, auto-close the report row
        if clean_mb_id in completed_mbuds:
            Bundlereport.objects.using("app").filter(id=bundle.id).update(
                scan=1,
                r_date=timezone.now().date()
            )
            continue

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
    """
    Fetches child bundle stickers from TrsMcutstickerprod.
    Queries by both pcs21.id and pcs21.mbundid to handle foreign key variations.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    mbundid = request.POST.get("mbundid")
    if not mbundid:
        return JsonResponse({"status": "error", "message": "mbundid is required"}, status=400)

    pcs21 = TrsCdelPcs21.objects.using("demo").filter(mbundid=mbundid).first()
    search_ids = [mbundid]
    if pcs21:
        search_ids.append(pcs21.id)

    pcs3_qs = TrsMcutstickerprod.objects.using("demo").filter(mbud__in=search_ids)
    if not pcs3_qs.exists():
        return JsonResponse({"status": "error", "message": "No child bundle records found in TrsMcutstickerprod"})

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

    # Fetch size names from Msizes in 'test' DB
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
        "mbundid": mbundid,
        "rows": data
    })


@csrf_exempt
def update_child_bundle_scan(request):
    """
    Scans a single child bundle:
    1. Sets TrsMcutstickerprod: scan = 1, unit_id = pcs1.unitid.
    2. Checks if all child stickers under this master bundle are completed.
    3. If complete, updates Bundlereport: scan = 1, r_date = today.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    bundid = request.POST.get("bundid")
    mbundid = request.POST.get("mbundid")

    if not bundid or not mbundid:
        return JsonResponse({"status": "error", "message": "bundid and mbundid required"}, status=400)

    # 1. Resolve master bundle and unit id from DC
    pcs21 = TrsCdelPcs21.objects.using("demo").filter(mbundid=mbundid).first()
    if not pcs21:
        return JsonResponse({"status": "error", "message": "Invalid master bundle"}, status=404)

    pcs1 = TrsCdelPcs1.objects.using("demo").filter(id=pcs21.id).first()
    target_unit_id = pcs1.unitid if pcs1 else None

    # 2. Update child sticker record
    search_mbuds = [pcs21.id, pcs21.mbundid]
    updated = TrsMcutstickerprod.objects.using("demo").filter(
        mbud__in=search_mbuds,
        bundid=bundid
    ).update(
        scan="1",
        unit_id=target_unit_id
    )

    if updated == 0:
        return JsonResponse({"status": "error", "message": f"Child bundle {bundid} not found"}, status=404)

    # 3. Check if all sibling stickers are scanned
    total_count = TrsMcutstickerprod.objects.using("demo").filter(mbud__in=search_mbuds).count()
    scanned_count = TrsMcutstickerprod.objects.using("demo").filter(
        mbud__in=search_mbuds,
        scan__in=[1, "1", True]
    ).count()

    all_done = (total_count == scanned_count and total_count > 0)

    # 4. If all child bundles are finished, finalize Bundlereport
    if all_done:
        Bundlereport.objects.using("app").filter(mbundle_id=mbundid).update(
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