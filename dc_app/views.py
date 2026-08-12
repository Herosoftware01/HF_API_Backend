from django.http import JsonResponse
from .models import ViewCuttingDelPrint,ViewKnitDelivery,VueAccInhTransfer,VueAccProdDel,TrsGatemodule, CuttingPrintembdel, ViewYarnProcessDelivery,VueAccProcDel,ViewAccinwardVerification,ViewFabricDeliveryProcess,ViewMistakeqtyPrint,ViewUnitPcdelivery,VueRibDeliveryDetails,ViewGdwnFabricDeliveryPlan
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime

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
    dcno = request.GET.get("dcno")  # Example: ?id=101

    queryset = ViewKnitDelivery.objects.using('test').all()

    if dcno:
        queryset = queryset.filter(dc=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def acc_prod_del_print(request):
    no = request.GET.get("no")  # Example: ?id=101

    queryset = VueAccProdDel.objects.using('test').all()

    if no:
        queryset = queryset.filter(n=no)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def acc_proc_del_print(request):
    no = request.GET.get("no")  # Example: ?id=101

    queryset = VueAccProcDel.objects.using('test').all()

    if no:
        queryset = queryset.filter(no=no)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })


def acc_inhouse_transfer(request):
    no = request.GET.get("no")  # Example: ?id=101

    queryset = VueAccInhTransfer.objects.using('test').all()

    if no:
        queryset = queryset.filter(no=no)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def acc_inward_verification(request):
    jobno = request.GET.get("jobno") 
    supplier = request.GET.get("supplierdcno") 
    pono = request.GET.get("pono") # Example: ?jobno=101 
    billno = request.GET.get("billno")

    queryset = ViewAccinwardVerification.objects.using('test').all()

    if jobno:
        queryset = queryset.filter(jobno=jobno)

    if supplier:
        queryset = queryset.filter(supplierdcno=supplier)

    if pono:
        queryset = queryset.filter(pono=pono)

    if billno:
        queryset = queryset.filter(billno=billno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })


def fabric_process_delivery(request):
    no = request.GET.get("dcno")  # Example: ?dcno=101

    queryset = ViewFabricDeliveryProcess.objects.using('test').all()

    if no:
        queryset = queryset.filter(dcno=no)

    data = list(queryset.values())
    return JsonResponse(data, safe=False)

def mistake_qty_print(request):
    dcno = request.GET.get("dcno")  # Example: ?id=101

    queryset = ViewMistakeqtyPrint.objects.using('demo').all()

    if dcno:
        queryset = queryset.filter(dcno=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def unit_pc_delivery(request, dcno):
    queryset = ViewUnitPcdelivery.objects.using('test').filter(dcno=dcno)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)

def rib_delivery_print(request):
    dcno = request.GET.get("dc")  # Example: ?id=101

    queryset = VueRibDeliveryDetails.objects.using('demo').all()

    if dcno:
        queryset = queryset.filter(dcno=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })


def godown_fabric_delivery_plan(request):
    dcno = request.GET.get("dcno")  # Example: ?id=101

    queryset = ViewGdwnFabricDeliveryPlan.objects.using('demo').all()

    if dcno:
        queryset = queryset.filter(dcno=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })



@csrf_exempt
def gate_module_api(request, pk=None):
    # ---------------- GET ----------------
    if request.method == "GET":

        # Single Record
        if pk:
            try:
                obj = TrsGatemodule.objects.using('demo').get(pk=pk)
                data = model_to_dict(obj)

                data["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")

                return JsonResponse({
                    "status": True,
                    "data": data
                })

            except TrsGatemodule.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "Record not found"
                }, status=404)

        # All Records
        objs = TrsGatemodule.objects.using('demo').all().order_by("-date")

        data = []

        for obj in objs:
            item = model_to_dict(obj)
            item["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")
            data.append(item)

        return JsonResponse({
            "status": True,
            "count": len(data),
            "data": data
        })


    # ---------------- POST ----------------
    elif request.method == "POST":
        try:
            body = json.loads(request.body)

            module = body.get("module")
            qr_code_dtls = body.get("qr_code_dtls")

            # Duplicate check
            if TrsGatemodule.objects.using("demo").filter(
                module=module,
                qr_code_dtls=qr_code_dtls
            ).exists():
                return JsonResponse({
                    "status": True,
                    "message": "DcNo Already Saved"
                }, status=201)

            obj = TrsGatemodule.objects.using("demo").create(
                module=module,
                qr_code_dtls=qr_code_dtls,
                companyid=body.get("companyid"),
                year=body.get("year"),
                no=body.get("no"),
                date=parse_datetime(body.get("date")),
                jobno=body.get("jobno"),
                suppliername=body.get("suppliername"),
                descr=body.get("descr"),
                rls_bdls=body.get("rls_bdls"),
                kg=body.get("kg"),
                mtrs=body.get("mtrs"),
                verify=body.get("verify"),
                print_delivery_date=body.get("print_delivery_date"),
                gate_delivery_date=body.get("gate_delivery_date"),

            )

            return JsonResponse({
                "status": True,
                "message": "Dc Created Successfully",
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)


    # ---------------- PUT (UPDATE) ----------------
    elif request.method == "PUT":

        if not pk:
            return JsonResponse({
                "status": False,
                "message": "ID required"
            }, status=400)

        try:
            obj = TrsGatemodule.objects.using('demo').get(pk=pk)

            body = json.loads(request.body)

            obj.module = body.get("module", obj.module)
            obj.qr_code_dtls = body.get("qr_code_dtls", obj.qr_code_dtls)
            obj.companyid = body.get("companyid", obj.companyid)
            obj.year = body.get("year", obj.year)
            obj.no = body.get("no", obj.no)

            if body.get("date"):
                obj.date = parse_datetime(body.get("date"))

            obj.jobno = body.get("jobno", obj.jobno)
            obj.suppliername = body.get("suppliername", obj.suppliername)
            obj.descr = body.get("descr", obj.descr)
            obj.rls_bdls = body.get("rls_bdls", obj.rls_bdls)
            obj.kg = body.get("kg", obj.kg)
            obj.mtrs = body.get("mtrs", obj.mtrs)

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Updated Successfully"
            })

        except TrsGatemodule.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Record not found"
            }, status=404)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": False,
        "message": "Method not allowed"
    }, status=405)
