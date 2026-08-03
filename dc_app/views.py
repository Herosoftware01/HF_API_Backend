from django.http import JsonResponse
from .models import ViewCuttingDelPrint, CuttingPrintembdel, ViewYarnProcessDelivery
from .models import ViewCuttingDelPrint,ViewKnitDelivery,VueAccProdDel,TrsGatemodule
import json

def cutting_del_print(request):
    id = request.GET.get("id")  # Example: ?id=101

    queryset = ViewCuttingDelPrint.objects.using('demo').all()

    if id:
        queryset = queryset.filter(id=id)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def cutting_bit_print(request, id):
    
    queryset = CuttingPrintembdel.objects.using('demo').filter(id=id)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)


def yarn_process_delivery(request, dcno):
    queryset = ViewYarnProcessDelivery.objects.using('test').filter(dcno=dcno)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)


def knitting_del_print(request):
    id = request.GET.get("id")  # Example: ?id=101

    queryset = ViewKnitDelivery.objects.using('test').all()

    if id:
        queryset = queryset.filter(dc=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def acc_prod_del_print(request):
    id = request.GET.get("id")  # Example: ?id=101

    queryset = VueAccProdDel.objects.using('test').all()

    if id:
        queryset = queryset.filter(n=n)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })


