from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import  Stickemp,VueMistakePartDetails, bit_checking_updates, BitcheckingPlyDetails, TrsCutstickerprodNew, bit_start_end_time
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from django.utils import timezone


def qr_api(request):

    sl = request.GET.get('qr_id')

    data = (
        TrsCutstickerprodNew.objects.using('demo')
        .filter(qrid=sl)
        .values('qrid', 'pc', 'planno','tbid')
        .first()
    )

    if not data:
        return JsonResponse({
            "status": False,
            "message": "Data not found"
        })

    desc = list(
        VueMistakePartDetails.objects.using('demo')
        .filter(planno=data['planno'], topbottom_id=data['tbid'])
        .values_list('det_part', flat=True)
    )

    # ✅ START/END TABLE CHECK
    start_entry = bit_start_end_time.objects.filter(
        qrid=data['qrid']
    ).first()

    saved_data = bit_checking_updates.objects.filter(
        scaner_id=data['qrid']
    )


    if start_entry or saved_data.exists():

        first = saved_data.first() if saved_data.exists() else None

        checked_data = {}

        saved_desc = []

        for item in saved_data:

            saved_desc.append(item.descriptions)

            checked_data[item.descriptions] = [
                int(x)
                for x in item.mistake_pcs.split(',')
                if x.strip()
            ]

        return JsonResponse({
            "status": True,
            "already_saved": True,

            "sl": data['qrid'],
            "plan_no": data['planno'],
            "pc": data['pc'],

            "employee": {
                "code": first.emp_id if first else start_entry.empid
            },


            "descriptions": desc,

            "checked_data": checked_data
        })

    return JsonResponse({
        "status": True,
        "already_saved": False,

        "sl": data['qrid'],
        "plan_no": data['planno'],
        "pc": data['pc'],
        "descriptions": desc
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

    queryset = Stickemp.objects.using('main').values()

    data = []

    for obj in queryset:

        if obj['code'] in pending_emp_ids:
            continue

        raw_path = obj.get('photo')

        if raw_path:
            filename = raw_path.split('\\')[-1]
            obj['photo'] = f"http://10.1.21.153:7003/staff_images/{filename}"
        else:
            obj['photo'] = ""

        data.append(obj)

    return JsonResponse(data, safe=False)



@api_view(['POST'])
def save_checking(request):

    data = request.data

    plan_no = data.get('plan_no')
    desc = data.get('descriptions')

    # prevent duplicate save
    exists = bit_checking_updates.objects.filter(
        plan_no=plan_no,
        descriptions=desc
    ).exists()

    if exists:
        return Response({
            "status": False,
            "message": "Already saved"
        })

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
        total_select_pcs=data.get('total_select_pcs') or 0
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

        details = payload.get("details", [])

        if not details:
            return Response(
                {
                    "status": False,
                    "message": "No details found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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
                }
            )

            # UPDATE END TIME
            bit_start_end_time.objects.filter(
                qrid=scanner_id,
                end__isnull=True
            ).update(
                end=timezone.now()
            )

        return Response(
            {
                "status": True,
                "message": "Saved Successfully"
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
        plan_no = request.GET.get("plan_no")

        if not plan_no:
            return JsonResponse({
                "status": False,
                "message": "plan_no required"
            })

        update_records = bit_checking_updates.objects.filter(
            plan_no=plan_no
        )

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

        BitcheckingPlyDetails.objects.using('demo').filter(
            qr_id__in=scanner_ids
        ).delete()

        bit_start_end_time.objects.filter(qrid__in=scanner_ids).delete()

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

    
        final_exists = BitcheckingPlyDetails.objects.using('demo').filter(
            qr_id=scaner_id
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
            scaner_id=scaner_id
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
        qrid__in=existing_qr_ids
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

        already_exists = bit_start_end_time.objects.filter(
            qrid=qrid
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

            if not qrid:
                return JsonResponse({
                    "status": False,
                    "message": "QR ID missing"
                })

            deleted_count, _ = bit_start_end_time.objects.filter(
                qrid=qrid
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

