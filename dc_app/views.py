from django.http import JsonResponse
from .models import ViewCuttingDelPrint, CuttingPrintembdel, ViewYarnProcessDelivery, ViewUnitPcdelivery, ViewCutsecFabricdelivery
from .models import ViewCuttingDelPrint,ViewKnitDelivery,VueAccInhTransfer,VueAccProdDel,TrsGatemodule, CuttingPrintembdel, ViewYarnProcessDelivery,VueAccProcDel,ViewAccinwardVerification,ViewFabricDeliveryProcess,ViewMistakeqtyPrint,ViewUnitPcdelivery,VueRibDeliveryDetails,ViewGdwnFabricDeliveryPlan,TrsApidtls,ViewFabricDeliveryRepl,HerofashionUser,Holiday,RoleModulePermission
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.db import transaction
from django.contrib.auth import get_user_model


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

def CuttingSecFabric(request, dcno):
    queryset = ViewCutsecFabricdelivery.objects.using('demo').filter(dcno=dcno)
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


def fabric_delivery_repl(request):
    dcno = request.GET.get("dcno")  # Example: ?id=101

    queryset = ViewFabricDeliveryRepl.objects.using('demo').all()

    if dcno:
        queryset = queryset.filter(dcno=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })



# --- VIEW ---
@csrf_exempt
def gate_module_api(request, pk=None):
    # ---------------- GET ----------------
    if request.method == "GET":

        # Single Record
        if pk:
            try:
                obj = TrsGatemodule.objects.using('demo').get(pk=pk)
                data = model_to_dict(obj)

                if obj.date:
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
            if obj.date:
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
                    "status": False,
                    "message": "DcNo Already Saved"
                }, status=409)

            # Safely parse dates if they exist in the payload
            date_val = body.get("date")
            print_date_val = body.get("print_delivery_date")
            gate_date_val = body.get("gate_delivery_date")

            obj = TrsGatemodule.objects.using("demo").create(
                module=module,
                qr_code_dtls=qr_code_dtls,
                companyid=body.get("companyid"),
                year=body.get("year"),
                no=body.get("no"),
                date=parse_datetime(date_val) if date_val else None,
                jobno=body.get("jobno"),
                suppliername=body.get("suppliername"),
                descr=body.get("descr"),
                rls_bdls=body.get("rls_bdls"),
                kg=body.get("kg"),
                mtrs=body.get("mtrs"),
                verify=body.get("verify"),
                print_delivery_date=parse_datetime(print_date_val) if print_date_val else None,
                gate_delivery_date=parse_datetime(gate_date_val) if gate_date_val else None,
                prepered=body.get("prepered"),
                fhero=body.get("fhero")
            )

            return JsonResponse({
                "status": True,
                "message": "Dc Created Successfully",
            }, status=201)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    # ---------------- PUT (Handles React Verification Updates) ----------------
    elif request.method == "PUT":
        if not pk:
            return JsonResponse({
                "status": False, 
                "message": "Record ID is required for updates"
            }, status=400)
            
        try:
            body = json.loads(request.body)
            obj = TrsGatemodule.objects.using('demo').get(pk=pk)
            
            # If 'verify' is in the request payload, update the field
            if "verify" in body:
                obj.verify = body["verify"]

            # 2. Update the 'gate_delivery_date' (THIS WAS MISSING)
            if "gate_delivery_date" in body:
                date_str = body["gate_delivery_date"]
                obj.gate_delivery_date = parse_datetime(date_str) if date_str else None
                
            # Save the updated record
            obj.save(using='demo')
            
            return JsonResponse({
                "status": True,
                "message": "Verification saved successfully"
            }, status=200)

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

    # ---------------- METHOD NOT ALLOWED ----------------
    return JsonResponse({
        "status": False,
        "message": "Method not allowed"
    }, status=405)


def gate_module_api_details(request):

    data = TrsApidtls.objects.using('demo').all()

    data1 = list(data.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data1),
        "data": data1
    })


def get_user_by_username(request):
    
    data = HerofashionUser.objects.all()

    data1 = list(data.values('id', 'username', 'role__name'))

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data1),
        "data": data1
    })



def get_holidays(request):
    current_year = timezone.now().year

    data = Holiday.objects.using('main').filter(
        dt__year=current_year
    )

    data1 = list(data.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data1),
        "data": data1
    })


# Hardcoded single source of truth for all modules
AVAILABLE_MODULES = [
    {"module_id": "cut_to_unit", "module_name": "Cut to Unit Delivery"},
    {"module_id": "cutting_sec_fabric", "module_name": "Cutting Section Fabric"},
    {"module_id": "knitting_delivery", "module_name": "Knitting Delivery"},
    {"module_id": "bit_delivery", "module_name": "Bit Delivery Challan"},
    {"module_id": "yarn_process", "module_name": "Yarn Process Challan"},
    {"module_id": "acc_production", "module_name": "Accessory Production"},
    {"module_id": "acc_process", "module_name": "Accessory Process"},
    {"module_id": "acc_inhouse", "module_name": "Accessory Inhouse Delivery"},
    {"module_id": "fabric_process", "module_name": "Fabric Process Delivery"},
    {"module_id": "mistake_cut", "module_name": "Mistake Cut Delivery"},
    {"module_id": "rib_cut", "module_name": "Rib Cut Delivery"},
    {"module_id": "godown_fabric", "module_name": "Godown Fabric Delivery"},
    {"module_id": "replacement_del", "module_name": "Replacement Delivery"},
    {"module_id": "unit_pcs", "module_name": "Unit Pcs Delivery"},
]


@csrf_exempt
def manage_role_permissions(request, role_param=None):
    """
    Single function handling CRUD for Role Permissions.
    GET: Reads permissions for a role.
    POST: Creates or Updates permissions.
    DELETE: Deletes/Resets permissions for a role.
    """
    
    # ------------------ READ (GET) ------------------
    if request.method == 'GET':
        # Depending on url routing, role might come from URL param or query string
        role = role_param or request.GET.get('role')
        
        if not role:
            return JsonResponse({"error": "Role is required"}, status=400)
            
        # Fetch existing DB permissions for this role
        db_permissions = RoleModulePermission.objects.filter(role=role)
        db_perm_dict = {p.module_id: p.is_enabled for p in db_permissions}
        
        # Build response based on single source of truth (AVAILABLE_MODULES)
        response_data = []
        for mod in AVAILABLE_MODULES:
            response_data.append({
                "module_id": mod["module_id"],
                "module_name": mod["module_name"],
                # Default to False if not found in DB
                "is_enabled": db_perm_dict.get(mod["module_id"], False) 
            })
            
        # Returning array directly to match your React component's expected data format
        return JsonResponse(response_data, safe=False)


    # ------------------ CREATE / UPDATE (POST) ------------------
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data.get('role')
            permissions = data.get('permissions', [])
            
            if not role:
                return JsonResponse({"status": False, "message": "Role is required"}, status=400)
                
            # Iterate and save using update_or_create to handle both Create and Update
            for perm in permissions:
                module_id = perm.get('module_id')
                is_enabled = perm.get('is_enabled', False)
                
                # Fetch module_name securely from the constant to prevent arbitrary data injection
                module_name = next((m['module_name'] for m in AVAILABLE_MODULES if m['module_id'] == module_id), None)
                
                if module_name:
                    RoleModulePermission.objects.update_or_create(
                        role=role,
                        module_id=module_id,
                        defaults={
                            'module_name': module_name,
                            'is_enabled': is_enabled
                        }
                    )
                    
            return JsonResponse({"status": True, "message": "Permissions saved successfully"})
            
        except json.JSONDecodeError:
            return JsonResponse({"status": False, "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=500)


    # ------------------ DELETE (DELETE) ------------------
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            role = data.get('role')
            
            if not role:
                return JsonResponse({"status": False, "message": "Role is required for deletion"}, status=400)
                
            # Deletes all custom permissions for this role, effectively resetting them to default (OFF)
            RoleModulePermission.objects.filter(role=role).delete()
            return JsonResponse({"status": True, "message": f"Permissions for {role} reset successfully"})
            
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=500)

    else:
        return JsonResponse({"status": False, "message": "Method not allowed"}, status=405)