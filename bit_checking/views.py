from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import  Stickemp,VueMistakePartDetails, bit_checking_updates, BitcheckingPlyDetails, TrsCutstickerprodNew
from django.views.decorators.csrf import csrf_exempt


def qr_api(request):

    sl = request.GET.get('qr_id')

    data = (
        TrsCutstickerprodNew.objects.using('demo')
        .filter(qrid=sl)
        .values('qrid', 'pc', 'planno')
        .first()
    )

    if not data:
        return JsonResponse({
            "status": False,
            "message": "Data not found"
        })

    desc = list(
        VueMistakePartDetails.objects.using('demo')
        .filter(planno=data['planno'])
        .values_list('det_part', flat=True)
    )

    saved_data = bit_checking_updates.objects.filter(
        scaner_id=data['qrid']
    )


    if saved_data.exists():

        first = saved_data.first()

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
                "code": first.emp_id
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
    queryset = Stickemp.objects.using('main').values()
    # Modify image paths
    for obj in queryset:
        raw_path = obj['photo'] if obj.get('photo') else None
        if raw_path:
            filename = raw_path.split('\\')[-1]
            obj['photo'] = f"http://10.1.21.153:7003/staff_images/{filename}"
        else:
            obj['photo'] = ""

    data = list(queryset)
    
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

                    "ok_pcs": item.get("ok_pcs"),
                    "mistake_pcs": item.get("mistake_count"),
                    "mistake_ply": item.get("mistake_pcs"),

                    "result": item.get("total_select_pcs"),
                    "final_tpcs": item.get("final_tpcs"),
                    "out_ply": item.get("out_pcs"),
                }
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