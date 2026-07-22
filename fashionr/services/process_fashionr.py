import json
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from ..models import FashionrResult
from .cutplan import save_cutplan

# Future Imports
# from .billofmaterials import save_billofmaterials
# from .costingreport import save_costingreport
# from .operations import save_operations
# from .fabricconsumption import save_fabricconsumption
# from .threadconsumption import save_threadconsumption
# from .deltas import save_deltas


# Register all report handlers here
REPORT_HANDLERS = {
    "cutplan": save_cutplan,
    # "billofmaterials": save_billofmaterials,
    # "costingreport": save_costingreport,
    # "operations": save_operations,
    # "fabricconsumption": save_fabricconsumption,
    # "threadconsumption": save_threadconsumption,
    # "deltas": save_deltas,
}

# Main Entry
@transaction.atomic(using="demo1")
def process_fashionr(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Only POST method allowed."
            },
            status=405
        )

    try:
        body = json.loads(request.body) 
        title = body.get("title")
        jobno = body.get("jobno")
        result = body.get("result")

        # Get FashionR Master Record
        fashion = FashionrResult.objects.using("demo1").filter(
            title=title,
            jobno=jobno
        ).exists()

        if not fashion:
            fashion = FashionrResult.objects.using('demo1').create(
                title=title,
                result= result,   # Store JSON as string
                created_datetime=timezone.now(),
                jobno=jobno
            )

        report_name = title.rsplit(".", 1)[-1].lower()

        # Find Registered Service
        handler = REPORT_HANDLERS.get(report_name)

        if handler is None:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"{report_name} service not implemented."
                },
                status=400
            )

        # Execute Service
        return handler(fashion)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e) }, status=400 )