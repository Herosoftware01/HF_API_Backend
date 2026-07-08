from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import  Stickemp,VueMistakePartDetails,TrsCutstickerprodNew1, bit_checking_updates, BitcheckingPlyDetails, TrsCutstickerprodNew, bit_start_end_time
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db import connections



# def get_previous_entry_mode(qrid):
#     with connections['demo'].cursor() as cursor:
#         cursor.execute(
#             "EXEC sp_GetPreviousEntryMode @QR_ID=%s",
#             [qrid]
#         )

#         row = cursor.fetchone()

#         if row:
#             return row[0]
#         return None

from django.db import connections, DatabaseError

def get_previous_entry_mode(qrid):
    try:
        with connections['demo'].cursor() as cursor:
            cursor.execute(
                "EXEC sp_GetPreviousEntryMode @QR_ID=%s",
                [qrid]
            )
            row = cursor.fetchone()

            if not row:
                return None, None

            entry_mode = row[0]
            message = row[1] if len(row) > 1 else None

            return entry_mode, message

    except Exception as e:
        return None, str(e)


@api_view(["GET"])
def qr_api(request):

    sl = request.GET.get('qr_id')
    print("sl",sl)
    # previous_entry_mode = get_previous_entry_mode(sl)
    previous_entry_mode, prev_error = get_previous_entry_mode(sl)

    if prev_error:
        return JsonResponse({
            "status": False,
            "message": prev_error,   # show SQL error
        })
   

    data = (
        TrsCutstickerprodNew1.objects.using('demo')
        .filter(qrid=sl)
        .values('qrid', 'pc', 'planno', 'topbott_id','t')
        .first()
    )

    # print("qrid", data['qrid'])

    if not data:
        return JsonResponse({
            "status": False,
            "message": "Data not found"
        })

    desc = list(
        VueMistakePartDetails.objects.using('demo')
        .filter(qrid=sl)
        .values_list('det_part', flat=True)
    )

    # START / END CHECK
    start_entry = bit_start_end_time.objects.filter(
        qrid=data['qrid'],
        types=data['t']
    ).first()

    saved_data = bit_checking_updates.objects.filter(
        scaner_id=sl,
        types=data['t']
    )
    # =========================
    # ALREADY SAVED CASE
    # =========================
    if start_entry or saved_data.exists():

        first = saved_data.first() if saved_data.exists() else None

        checked_data = {}
        count_data = {}
        saved_desc = []

        entry_mode = None

        for item in saved_data:

            saved_desc.append(item.descriptions)

            # checked pcs
            checked_data[item.descriptions] = [
                int(x)
                for x in str(item.mistake_pcs).split(',')
                if x.strip().isdigit() and int(x) > 0
            ]

            # count restore (for + / - mode)
            count_data[item.descriptions] = item.out_pcs_count or 0

            # entry mode (same for all rows)
            if not entry_mode:
                entry_mode = item.entry_mood

        return JsonResponse({
            "status": True,
            "already_saved": True,

            "sl": data['qrid'],
            "plan_no": data['planno'],
            "pc": data['pc'],
            "t": data['t'],

            "employee": {
                "code": first.emp_id if first else start_entry.empid
            },
            "descriptions": desc,
            "checked_data": checked_data,
            "count_data": count_data,
            "entry_mood": entry_mode,
            "previous_entry_mode": previous_entry_mode,
             "previous_entry_error": prev_error, 
        })

    # =========================
    # FRESH SCAN CASE
    # =========================
    return JsonResponse({
        "status": True,
        "already_saved": False,
          "previous_entry_error": prev_error, 
        "sl": data['qrid'],
        "plan_no": data['planno'],
        "pc": data['pc'],
        "t": data['t'],
        "descriptions": desc,
        "previous_entry_mode": previous_entry_mode,
        "checked_data": {},
        "count_data": {},
        "entry_mood": None
    })


def emp_stick(request):

    from_date = parse_datetime("2026-05-18 08:28:55.931995")
    existing_qr_ids = set(
        BitcheckingPlyDetails.objects.using('demo')
        .values_list('qr_id', flat=True)
    )

    pending_emp_ids = set(
        bit_checking_updates.objects.filter(
            date__gte=from_date
        ).exclude(
            scaner_id__in=existing_qr_ids   
        ).values_list(
            'emp_id',
            flat=True
        )
    )

    queryset = Stickemp.objects.using("main").values()

    data = []

    for obj in queryset:
        raw_path = obj.get("photo")

        if raw_path:
            filename = raw_path.split("\\")[-1]
            obj["photo"] = f"https://hfapi.herofashion.com/staff_images/{filename}"
        else:
            obj["photo"] = ""

        data.append(obj)

    return JsonResponse(data, safe=False)



# def emp_stick(request):

#     from_date = parse_datetime("2026-05-18 08:28:55.931995")

#     # Existing QR + Type combinations
#     existing_qr_type = set(
#         BitcheckingPlyDetails.objects.using('demo')
#         .values_list('qr_id', 'typ')
#     )

#     # Get updates after date
#     updates = (
#         bit_checking_updates.objects
#         .filter(date__gte=from_date)
#         .values('scaner_id', 'types', 'emp_id')
#     )

#     pending_emp_ids = set()

#     for item in updates:

#         qr_type = (
#             item['scaner_id'],
#             item['types']
#         )

#         # QR + Type already exists -> skip
#         if qr_type in existing_qr_type:
#             continue

#         pending_emp_ids.add(item['emp_id'])


#     queryset = (
#         Stickemp.objects.using('main')
#         .exclude(code__in=pending_emp_ids)
#         .values()
#     )

#     data = []

#     for obj in queryset.iterator(chunk_size=1000):

#         raw_path = obj.get('photo')

#         if raw_path:
#             filename = raw_path.split('\\')[-1]
#             obj['photo'] = (
#                 f"https://hfapi.herofashion.com/staff_images/{filename}"
#             )
#         else:
#             obj['photo'] = ""

#         data.append(obj)

#     return JsonResponse(data, safe=False)



@api_view(['POST'])
def save_checking(request):

    data = request.data

    plan_no = data.get('plan_no')
    desc = data.get('descriptions')

    # prevent duplicate save
    exists = bit_checking_updates.objects.filter(
        plan_no=plan_no,
        descriptions=desc,
        scaner_id=data.get('scaner_id')
    ).exists()

    if exists:
        return Response({
            "status": False,
            "message": "Already saved"
        })
    
    entry_mode = str(data.get("entry_mood") or "").strip()

    if entry_mode.lower() in ["", "null", "undefined", "none"]:
        entry_mode = "empty"

    bit_checking_updates.objects.create(
        scaner_id=data.get('scaner_id'),
        emp_id=data.get('emp_id'),
        descriptions=desc,
        out_pcs=data.get('out_pcs') or 0,
        mistake_pcs=data.get('mistake_pcs') or 0,
        out_pcs_count=data.get('mistake_count') or 0,
        ok_pcs=data.get('ok_pcs') or 0,
        total_qty=data.get('total_qty') or 0,
        plan_no=plan_no,
        total_select_pcs=data.get('total_select_pcs') or 0,
        entry_mood=entry_mode,
        types=data.get('types', '')
    )

    return Response({
        "status": True,
        "message": "Saved successfully"
    })


@api_view(['GET'])
def get_saved_plans(request):

    data = bit_checking_updates.objects.values(
        'plan_no',
        'descriptions'
    )

    return Response(list(data))



@api_view(["POST"])
def bitchecking_final_data(request):

    try:

        payload = request.data

        emp_id = payload.get("emp_id")
        scanner_id = payload.get("scaner_id")
        total_qty = payload.get("total_qty")
        types = payload.get("types", "")

        details = payload.get("details", [])

        if not details:
            return Response(
                {
                    "status": False,
                    "message": "No details found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        raw_mode = payload.get("entry_mood")

        # normalize
        if raw_mode is not None:
            raw_mode = str(raw_mode).strip().lower()

        # treat invalid values
        invalid_values = ["", "null", "undefined", "none"]

        if not raw_mode or raw_mode in invalid_values:
            existing_mode = (
                BitcheckingPlyDetails.objects.using('demo')
                .filter(qr_id=scanner_id)
                .values_list('entry_mode', flat=True)
                .first()
            )

            entry_mode = existing_mode if existing_mode else "empty"
        else:
            entry_mode = raw_mode 

        # STORED PROCEDURE CALL
        sticker_data = [] 

        for item in details:

            description = item.get("descriptions")

            BitcheckingPlyDetails.objects.using('demo').update_or_create(

                # already exists check
                qr_id=scanner_id,
                category=description,

                defaults={
                    "emp_id": emp_id,
                    "total_pcs": total_qty,

                    "ok_pcs": item.get("ok_pcs") or 0,
                    "mistake_pcs": item.get("mistake_count") or 0,
                    "mistake_ply": item.get("mistake_pcs") or 0,

                    "result": item.get("total_select_pcs") or 0,
                    "final_tpcs": item.get("final_tpcs") or 0,
                    "out_ply": item.get("out_pcs") or 0,
                    "typ": item.get("types") or 0,
                    "entry_mode": entry_mode
                }
            )
            print("data save success ===",scanner_id)

            # UPDATE END TIME

        bit_start_end_time.objects.filter(
            qrid=scanner_id,
            types= types,
            end__isnull=True
        ).update(
            end=timezone.now()
        )

    

        with connections["demo"].cursor() as cursor:
            cursor.execute(
                "EXEC sp_GetStickerDetails @sl=%s",
                [scanner_id]
            )

            columns = [col[0] for col in cursor.description]

            rows = cursor.fetchall()

            for row in rows:
                sticker_data.append(dict(zip(columns, row)))
        
        with connections["demo"].cursor() as cursor:
            cursor.execute("EXEC sp_GenerateBitCheckProduction")

        # data  r_p=True
        if sticker_data:
            BitcheckingPlyDetails.objects.using('demo').filter(
                qr_id=scanner_id,
                typ=types
            ).update(r_p=True)
        else:
            BitcheckingPlyDetails.objects.using('demo').filter(
                qr_id=scanner_id,
                typ=types
            ).update(r_p=False)

        return Response(
            {
                "status": True,
                "message": "Saved Successfully",
                "data": sticker_data,
                "r_p": bool(sticker_data)
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:

        return Response(
            {
                "status": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(["GET"])
def check_final_saved(request):

    scanner_id = request.GET.get("scanner_id")

    exists = BitcheckingPlyDetails.objects.using('demo').filter(
        qr_id=scanner_id
    ).exists()

    return Response({
        "status": True,
        "final_saved": exists
    })



@csrf_exempt
def delete_checking(request):

    if request.method != "DELETE":
        return JsonResponse({
            "status": False,
            "message": "Invalid Request"
        })

    try:
        # plan_no = request.GET.get("plan_no")
        qrid = request.GET.get("qrid")
        types = request.GET.get("types")

        if not qrid:
            return JsonResponse({
                "status": False,
                "message": "plan_no required"
            })

        update_records = bit_checking_updates.objects.filter(scaner_id=qrid, types=types)

        if not update_records.exists():
            return JsonResponse({
                "status": False,
                "message": "No records found"
            })

        scanner_ids = list(
            update_records.values_list(
                "scaner_id",
                flat=True
            )
        )

        with connections['demo'].cursor() as cursor:
            for qr in scanner_ids:
                print("Qr id :", qr)
                cursor.execute(
                    "EXEC sp_Delete_BitcheckProd @qr_id = %s",
                    (qr,)
                )

        BitcheckingPlyDetails.objects.using('demo').filter(
            qr_id__in=scanner_ids,
            typ=types
        ).delete()

        bit_start_end_time.objects.filter(qrid__in=scanner_ids, types=types).delete()

        update_records.delete()

        return JsonResponse({
            "status": True,
            "message": "Deleted Successfully"
        })

    except Exception as e:

        return JsonResponse({
            "status": False,
            "message": str(e)
        })
    

@csrf_exempt
def delete_single_checking(request):

    if request.method != "POST":
        return JsonResponse({
            "status": False
        })

    try:

        body = json.loads(request.body)

        plan_no = body.get("plan_no")
        descriptions = body.get("descriptions")
        scaner_id = body.get("scaner_id")
        types = body.get("types")

    
        final_exists = BitcheckingPlyDetails.objects.using('demo').filter(
            qr_id=scaner_id,
            typ=types
        ).exists()

        if final_exists:

            return JsonResponse({
                "status": False,
                "message":
                "Final data already saved. Use main DELETE button."
            })

   
        bit_checking_updates.objects.filter(
            plan_no=plan_no,
            descriptions=descriptions,
            scaner_id=scaner_id,
            types=types
        ).delete()

        return JsonResponse({
            "status": True,
            "message": "Deleted Successfully"
        })

    except Exception as e:

        return JsonResponse({
            "status": False,
            "message": str(e)
        })
    


def pending_scaner_ids(request):

    from_date = parse_datetime("2026-05-18 06:13:27.396456")

    existing_qr_ids = list(
        BitcheckingPlyDetails.objects.using('demo').values_list(
            'qr_id',
            flat=True
        )
    )

    queryset = bit_start_end_time.objects.filter(
        start__gte=from_date
    ).exclude(
        qrid__in=existing_qr_ids,
    ).order_by('qrid', 'start')

    seen = set()
    unique_data = []

    for row in queryset:
        if row.qrid not in seen:
            seen.add(row.qrid)
            has_update = bit_checking_updates.objects.filter(
                scaner_id=row.qrid
            ).exists()
            unique_data.append({
                "scaner_id": row.qrid,
                "emp_id": row.empid,
                "date": row.start,
                "has_update": has_update
            })

    return JsonResponse({
        "status": "success",
        "count": len(unique_data),
        "data": unique_data
    })


from django.utils import timezone

@csrf_exempt
def qc_start(request):

    if request.method == "POST":

        data = json.loads(request.body)

        qrid = data.get("qrid")
        empid = data.get("empid")
        types = data.get("types")
        print("Received Data:", qrid, empid, types)

        already_exists = bit_start_end_time.objects.filter(
            qrid=qrid,
            types=types
        ).exists()

        if already_exists:

            return JsonResponse({
                "status": False,
                "message": "QRID already exists"
            })

        ist_time = timezone.now()

        obj = bit_start_end_time.objects.create(
            qrid=qrid,
            empid=empid,
            types=types,
            start=ist_time
        )

        return JsonResponse({
            "status": True,
            "id": obj.id
        })

    return JsonResponse({
        "status": False
    })


@csrf_exempt
def delete_pending_scanner(request):

    if request.method == "POST":

        try:

            body = json.loads(request.body)

            qrid = body.get("qrid")
            types = body.get("types")

            if not qrid:
                return JsonResponse({
                    "status": False,
                    "message": "QR ID missing"
                })

            deleted_count, _ = bit_start_end_time.objects.filter(
                qrid=qrid,
                types=types
            ).delete()

            if deleted_count > 0:

                return JsonResponse({
                    "status": True,
                    "message": "Deleted Successfully"
                })

            return JsonResponse({
                "status": False,
                "message": "No matching record found"
            })

        except Exception as e:

            return JsonResponse({
                "status": False,
                "message": str(e)
            })

    return JsonResponse({
        "status": False,
        "message": "Invalid Request"
    })



@csrf_exempt
def print_bit_checking_sticker(request):
    if request.method == "POST":
        data = json.loads(request.body)

        sl = data["sl"]
        print_cut = data["print_cut_sticker"]
        print_mistake = data["print_mistake_sticker"]

        print("Printing Sticker for SL:", sl)
        print("Print Cut Sticker:", print_cut)
        print("Print Mistake Sticker:", print_mistake)

        with connections['demo'].cursor() as cursor:
            cursor.execute("""
                EXEC sp_PrintBitCheckingSticker
                    @SL=%s,
                    @PrintCutSticker=%s,
                    @PrintMistakeSticker=%s
            """, [
                sl,
                int(print_cut),
                int(print_mistake)
            ])

        return JsonResponse({
            "status": "success"
        })
    



from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def merge_images(request):
    image1 = request.FILES.get("image1")
    image2 = request.FILES.get("image2")

    if not image1 or not image2:
        return HttpResponse("Both images are required.", status=400)

    # Open images
    bg = Image.open(image1).convert("RGBA")
    overlay = Image.open(image2).convert("RGBA")

    # Resize overlay (25% of background width)
    overlay_width = int(bg.width * 0.25)
    ratio = overlay_width / overlay.width
    overlay_height = int(overlay.height * ratio)

    overlay = overlay.resize((overlay_width, overlay_height))

    # Position (Bottom Right)
    x = 20
    y = 20

    bg.paste(overlay, (x, y), overlay)

    output = BytesIO()
    bg.save(output, format="PNG")
    output.seek(0)

    return HttpResponse(output.getvalue(), content_type="image/png")

