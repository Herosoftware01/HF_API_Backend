from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services.process_fashionr import process_fashionr
from django.http import JsonResponse
from .models import FrCutplanMas, FrCutplanSizeandQuantityList, FrCutplanTotalMarkerList, FrCutplanTotalmarkerlistdet, FrCutplanTotalmarkerlistimages, FashionrResult


@csrf_exempt
def process_fashionr_view(request):
    return process_fashionr(request)


@csrf_exempt
def cutplan_list(request):
    result = []
    masters = FrCutplanMas.objects.using("demo1").all()
    for master in masters:

        size_list = list(
            FrCutplanSizeandQuantityList.objects.using("demo1")
            .filter(cutplanid=master.cutplanid)
            .values("sizename", "qty")
        )

        marker_summary = (
            FrCutplanTotalMarkerList.objects.using("demo1")
            .filter(cutplanid=master.cutplanid)
            .values()
            .first()
        )
        
        if marker_summary:
            marker_summary["cutplanid"] = marker_summary.pop("cutplanid_id", None)

        marker_details = []

        details = FrCutplanTotalmarkerlistdet.objects.using("demo1").filter(
            cutplanid=master.cutplanid
        )

        for detail in details:

            image = (
                FrCutplanTotalmarkerlistimages.objects.using("demo1")
                .filter(markerid=detail.markerid)
                .values()
                .first() or {}
            )
            if image:
                image["cutplanid"] = image.pop("cutplanid_id", None)

            marker_details.append({
                **detail.__dict__,
                **image
            })

            # Remove Django internal state if present
            marker_details[-1].pop("_state", None)

        result.append({
            "cutplanid": master.cutplanid,
            "orderno": master.orderno,
            "customer": master.customer,
            "fabrictype": master.fabrictype,
            "projectname": master.projectname,
            "date": master.date,
            "time": master.time,
            "username": master.username,
            "classification": master.classification,
            "SizeAndQuantityList": size_list,
            "TotalMarkerList": marker_summary,
            "TotalMarkerListDet": marker_details,
        })

    return JsonResponse(result, safe=False)


@csrf_exempt
def fashionr_results(request):

    if request.method == "GET":
        data = list(
            FashionrResult.objects.using('demo1').values(
                "slno",
                "title",
                "result",
                "created_datetime",
                "jobno"
            ).order_by("-slno")
        )
        return JsonResponse(data, safe=False)