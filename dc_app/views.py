from django.http import JsonResponse
from .models import ViewCuttingDelPrint
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
