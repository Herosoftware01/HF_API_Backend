from django.http import JsonResponse
from .models import (ViewCuttingDelPrint,
ViewKnitDelivery,ViewCutsecFabricdelivery,
VueAccInhTransfer,VueAccProdDel,
TrsGatemodule, CuttingPrintembdel,
ViewYarnProcessDelivery,VueAccProcDel,
ViewAccinwardVerification,ViewFabricDeliveryProcess,
ViewMistakeqtyPrint,ViewUnitPcdelivery,VueRibDeliveryDetails,ViewGdwnFabricDeliveryPlan,
TrsApidtls,ViewFabricDeliveryRepl,HerofashionUser,Holiday,RoleModulePermission,
Dc_Incharge_Verify,Dc_Reciver_Verify,ViewGeneralDeiveryType1,ViewGenStockIssue,ModuleMaster)
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError, transaction
from django.db import transaction
from django.http.multipartparser import MultiPartParser, MultiPartParserError
from django.utils import timezone
from datetime import date
from django.views.decorators.http import require_http_methods
import re



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
    dcno = request.GET.get("dcno")  
    queryset = ViewKnitDelivery.objects.using('test').all()

    if dcno:
        # FIX: Changed from dc=dcno to dcno=dcno
        queryset = queryset.filter(dcno=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def acc_prod_del_print(request):
    no = request.GET.get("no")  

    queryset = VueAccProdDel.objects.using('test').all()

    if no:
        # FIX: Changed from n=no to no=no
        queryset = queryset.filter(no=no)

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
    dcno = request.GET.get("dc")  

    queryset = VueRibDeliveryDetails.objects.using('demo').all()

    if dcno:
        # FIX: Changed from dcno=dcno to dc=dcno
        queryset = queryset.filter(dc=dcno)

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
    dcno = request.GET.get("dcno")

    queryset = ViewFabricDeliveryRepl.objects.using("demo")

    if dcno:
        queryset = queryset.filter(dcno=dcno)
    else:
        return JsonResponse({
            "status": False,
            "message": "dcno is required",
            "count": 0,
            "data": []
        })

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def general_delivery_type1(request):
    dcno = request.GET.get("dcno")

    today = date.today()

    # Current financial year: April 1 → March 31
    if today.month >= 4:
        fy_start = date(today.year, 4, 1)
        fy_end = date(today.year + 1, 3, 31)
    else:
        fy_start = date(today.year - 1, 4, 1)
        fy_end = date(today.year, 3, 31)

    queryset = ViewGeneralDeiveryType1.objects.using('test').all()

    # Current account/financial year
    queryset = queryset.filter(
        date__gte=fy_start,
        date__lte=fy_end
    )

    # DC number filter
    if dcno:
        queryset = queryset.filter(no=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })

def gen_stock_issue(request):
    dcno = request.GET.get("no")

    queryset = ViewGenStockIssue.objects.using("test").filter(
        date__year=timezone.now().year
    )

    if dcno:
        queryset = queryset.filter(no=dcno)

    data = list(queryset.values())

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })



# --- VIEW ---
csrf_exempt
def gate_module_api(request, pk=None):
    # ---------------- GET ----------------
    if request.method == "GET":

        # 1. Single Record by Primary Key
        if pk:
            try:
                obj = TrsGatemodule.objects.using('demo').get(pk=pk)
                data = model_to_dict(obj)
                if obj.date:
                    data["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")
                return JsonResponse({"status": True, "data": data})
            except TrsGatemodule.DoesNotExist:
                return JsonResponse({"status": False, "message": "Record not found"}, status=404)

        # Base Queryset
        queryset = TrsGatemodule.objects.using('demo').all().order_by("-date")

        # 2. Extract Filters from Frontend Request
        dc_no = request.GET.get("no")
        filter_date = request.GET.get("date")  # <--- Capture the single date parameter

        # Apply Filters Dynamically
        if dc_no:
            queryset = queryset.filter(no=dc_no)
        
        if filter_date:
            # __date extracts the YYYY-MM-DD part from the database's DateTimeField
            queryset = queryset.filter(date__date=filter_date)

        # Optional: If no filters are applied, limit to 50 to prevent crashing/slowdown
        if not dc_no and not filter_date:
            queryset = queryset[:50] 

        # Format Response
        data = []
        for obj in queryset:
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




MODULE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

LEGACY_MODULE_IDS = {
    "general": "general_transaction_delivery",
    "general_delivery": "general_transaction_delivery",
    "general_delivery_type1": "general_transaction_delivery",
}


def error_response(message, status=400, **extra):
    response = {
        "status": False,
        "message": message,
    }
    response.update(extra)
    return JsonResponse(response, status=status)


def read_json(request, allow_empty=False):
    if not request.body:
        if allow_empty:
            return {}, None
        return None, error_response("Request body is required")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, error_response("Invalid JSON format")

    if not isinstance(data, dict):
        return None, error_response("JSON body must be an object")

    return data, None


def normalize_module_id(module_id):
    if not isinstance(module_id, str):
        return None

    module_id = module_id.strip()

    if not module_id:
        return None

    return LEGACY_MODULE_IDS.get(module_id, module_id)


def serialize_module(module):
    return {
        "module_id": module.module_id,
        "module_name": module.module_name,
        "description": module.description,
        "path": module.path,
        "display_order": module.display_order,
        "is_active": module.is_active,
    }


def validate_module_payload(data, partial=False):
    values = {}
    errors = {}

    if not partial or "module_name" in data:
        module_name = data.get("module_name")

        if not isinstance(module_name, str) or not module_name.strip():
            errors["module_name"] = "Module name is required"
        elif len(module_name.strip()) > 255:
            errors["module_name"] = "Maximum length is 255"
        else:
            values["module_name"] = module_name.strip()

    if not partial or "description" in data:
        description = data.get("description", "")

        if not isinstance(description, str):
            errors["description"] = "Description must be a string"
        else:
            values["description"] = description.strip()

    if not partial or "path" in data:
        path = data.get("path", "")

        if not isinstance(path, str):
            errors["path"] = "Path must be a string"
        elif len(path.strip()) > 255:
            errors["path"] = "Maximum length is 255"
        else:
            values["path"] = path.strip()

    if not partial or "display_order" in data:
        display_order = data.get("display_order", 0)

        if (
            isinstance(display_order, bool)
            or not isinstance(display_order, int)
            or display_order < 0
        ):
            errors["display_order"] = (
                "Display order must be a non-negative integer"
            )
        else:
            values["display_order"] = display_order

    if not partial or "is_active" in data:
        is_active = data.get("is_active", True)

        if not isinstance(is_active, bool):
            errors["is_active"] = "is_active must be true or false"
        else:
            values["is_active"] = is_active

    return values, errors


# Keep csrf_exempt only when this endpoint is protected using token/JWT
# authentication. With Django session authentication, use CSRF protection.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def module_collection(request):
    """
    GET  /dcapp/dc_modules/
    POST /dcapp/dc_modules/
    """

    if request.method == "GET":
        include_inactive = (
            request.GET.get("include_inactive", "false").lower()
            in {"true", "1", "yes"}
        )

        modules = ModuleMaster.objects.all()

        if not include_inactive:
            modules = modules.filter(is_active=True)

        modules = modules.order_by("display_order", "module_name")

        return JsonResponse(
            [serialize_module(module) for module in modules],
            safe=False,
        )

    data, error = read_json(request)

    if error:
        return error

    module_id = data.get("module_id")

    if not isinstance(module_id, str):
        return error_response("module_id is required")

    module_id = module_id.strip()

    if not MODULE_ID_PATTERN.fullmatch(module_id):
        return error_response(
            "module_id must start with a lowercase letter and contain "
            "only lowercase letters, numbers, and underscores"
        )

    if module_id in LEGACY_MODULE_IDS:
        return error_response(
            "This module_id is a legacy alias",
            canonical_module_id=LEGACY_MODULE_IDS[module_id],
        )

    values, validation_errors = validate_module_payload(data)

    if validation_errors:
        return error_response(
            "Validation failed",
            errors=validation_errors,
        )

    try:
        module = ModuleMaster(module_id=module_id, **values)
        module.full_clean()
        module.save(force_insert=True)
    except ValidationError as exception:
        return error_response(
            "Validation failed",
            errors=getattr(
                exception,
                "message_dict",
                {"non_field_errors": exception.messages},
            ),
        )
    except IntegrityError:
        return error_response(
            "A module with this module_id already exists",
            status=409,
        )

    return JsonResponse(
        {
            "status": True,
            "message": "Module created successfully",
            "module": serialize_module(module),
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["GET", "PATCH", "DELETE"])
def module_detail(request, module_id):
    """
    GET    /dcapp/dc_modules/<module_id>/
    PATCH  /dcapp/dc_modules/<module_id>/
    DELETE /dcapp/dc_modules/<module_id>/
    """

    try:
        module = ModuleMaster.objects.get(module_id=module_id)
    except ModuleMaster.DoesNotExist:
        return error_response("Module not found", status=404)

    if request.method == "GET":
        return JsonResponse(serialize_module(module))

    if request.method == "DELETE":
        module.is_active = False
        module.save(update_fields=("is_active", "updated_at"))

        return JsonResponse({
            "status": True,
            "message": "Module deactivated successfully",
            "module": serialize_module(module),
        })

    data, error = read_json(request)

    if error:
        return error

    if "module_id" in data and data["module_id"] != module.module_id:
        return error_response("module_id cannot be changed")

    values, validation_errors = validate_module_payload(
        data,
        partial=True,
    )

    if validation_errors:
        return error_response(
            "Validation failed",
            errors=validation_errors,
        )

    try:
        with transaction.atomic():
            module = ModuleMaster.objects.select_for_update().get(
                module_id=module_id
            )

            for field, value in values.items():
                setattr(module, field, value)

            module.full_clean()
            module.save()
    except ValidationError as exception:
        return error_response(
            "Validation failed",
            errors=getattr(
                exception,
                "message_dict",
                {"non_field_errors": exception.messages},
            ),
        )

    return JsonResponse({
        "status": True,
        "message": "Module updated successfully",
        "module": serialize_module(module),
    })


@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def manage_role_permissions(request, role_param=None):
    """
    GET    /dcapp/dc_permissions/<role>/
    POST   /dcapp/dc_permissions/save/
    DELETE /dcapp/dc_permissions/<role>/
    """

    if request.method == "GET":
        role = role_param or request.GET.get("role")

        if not isinstance(role, str) or not role.strip():
            return error_response("Role is required")

        role = role.strip()

        modules = list(
            ModuleMaster.objects.filter(is_active=True).order_by(
                "display_order",
                "module_name",
            )
        )

        stored_permissions = dict(
            RoleModulePermission.objects.filter(role=role).values_list(
                "module_id",
                "is_enabled",
            )
        )

        response = []

        for module in modules:
            module_data = serialize_module(module)
            module_data["is_enabled"] = stored_permissions.get(
                module.module_id,
                False,
            )
            response.append(module_data)

        return JsonResponse(response, safe=False)

    if request.method == "POST":
        data, error = read_json(request)

        if error:
            return error

        role = data.get("role")

        if not isinstance(role, str) or not role.strip():
            return error_response("Role is required")

        role = role.strip()
        permissions = data.get("permissions", [])

        if not isinstance(permissions, list):
            return error_response("permissions must be an array")

        normalized_permissions = {}
        invalid_items = []

        for index, permission in enumerate(permissions):
            if not isinstance(permission, dict):
                invalid_items.append({
                    "index": index,
                    "message": "Permission must be an object",
                })
                continue

            requested_id = permission.get("module_id")
            module_id = normalize_module_id(requested_id)
            is_enabled = permission.get("is_enabled", False)

            if not module_id:
                invalid_items.append({
                    "index": index,
                    "message": "module_id is required",
                })
                continue

            if not isinstance(is_enabled, bool):
                invalid_items.append({
                    "index": index,
                    "module_id": requested_id,
                    "message": "is_enabled must be true or false",
                })
                continue

            if module_id in normalized_permissions:
                invalid_items.append({
                    "index": index,
                    "module_id": requested_id,
                    "message": "Duplicate module_id",
                })
                continue

            normalized_permissions[module_id] = is_enabled

        if invalid_items:
            return error_response(
                "Invalid permissions",
                errors=invalid_items,
            )

        module_ids = set(normalized_permissions)

        modules = ModuleMaster.objects.in_bulk(module_ids)

        unknown_module_ids = sorted(module_ids - set(modules))

        if unknown_module_ids:
            return error_response(
                "Unknown module_id",
                module_ids=unknown_module_ids,
            )

        inactive_module_ids = sorted(
            module_id
            for module_id, module in modules.items()
            if not module.is_active
        )

        if inactive_module_ids:
            return error_response(
                "Inactive modules cannot receive permissions",
                module_ids=inactive_module_ids,
            )

        try:
            with transaction.atomic():
                for module_id, is_enabled in normalized_permissions.items():
                    RoleModulePermission.objects.update_or_create(
                        role=role,
                        module_id=module_id,
                        defaults={
                            "is_enabled": is_enabled,
                        },
                    )
        except IntegrityError:
            return error_response(
                "Permissions could not be saved because of a conflict",
                status=409,
            )

        return JsonResponse({
            "status": True,
            "message": "Permissions saved successfully",
            "saved_count": len(normalized_permissions),
        })

    # DELETE
    body = {}

    if request.body:
        body, error = read_json(request, allow_empty=True)

        if error:
            return error

    role = role_param or body.get("role") or request.GET.get("role")

    if not isinstance(role, str) or not role.strip():
        return error_response("Role is required")

    role = role.strip()

    deleted_count, _ = RoleModulePermission.objects.filter(
        role=role
    ).delete()

    return JsonResponse({
        "status": True,
        "message": f"Permissions for {role} reset successfully",
        "deleted_count": deleted_count,
    })



@csrf_exempt
def dc_verify_incharge_crud(request):
    """
    All-in-one CRUD API endpoint using standard Django JsonResponse:
      - GET:    Filter by ?id=... or ?dcno=... or fetch all.
      - POST:   Create a new record (JSON body).
      - PUT:    Update an existing record via ?id=... or JSON body id.
      - DELETE: Delete record via ?id=... or JSON body id.
    """
    method = request.method

    # ----------------------------------------------------
    # READ (GET)
    # ----------------------------------------------------
    if method == "GET":
        record_id = request.GET.get("id") or request.GET.get("slno")
        dcno = request.GET.get("dcno") or request.GET.get("DCNo")

        queryset = Dc_Incharge_Verify.objects.all()

        if record_id:
            queryset = queryset.filter(id=record_id)
        if dcno:
            queryset = queryset.filter(DCNo=dcno)

        data = list(queryset.values())
        return JsonResponse({
            "status": True,
            "message": "Records fetched successfully.",
            "count": len(data),
            "data": data
        }, status=200)

    # ----------------------------------------------------
    # Parse JSON body for mutation requests (POST, PUT, DELETE)
    # ----------------------------------------------------
    body = {}
    if method in ["POST", "PUT", "DELETE"]:
        if request.body:
            try:
                body = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse({"status": False, "message": "Invalid JSON payload."}, status=400)

    # Helper to extract valid model fields from payload
    def get_cleaned_data(payload):
        valid_fields = ['date', 'DCNo', 'jobno', 'trstype', 'wgt', 'mtr', 'rolls', 'bags', 'username', 'status']
        return {k: v for k, v in payload.items() if k in valid_fields}

    # ----------------------------------------------------
    # CREATE (POST)
    # ----------------------------------------------------
    if method == "POST":
        cleaned_data = get_cleaned_data(body)
        if not cleaned_data:
            return JsonResponse({"status": False, "message": "No valid fields provided."}, status=400)

        # Default to verified unless explicitly stated otherwise
        cleaned_data.setdefault("status", True)

        # Block re-verifying a DC that already has a verified row for this trstype
        existing = Dc_Incharge_Verify.objects.filter(
            DCNo=cleaned_data.get("DCNo"),
            trstype=cleaned_data.get("trstype"),
            status=True,
        ).first()

        if existing:
            return JsonResponse({
                "status": False,
                "message": "This DC has already been verified for this transaction type!",
                "data": list(Dc_Incharge_Verify.objects.filter(id=existing.id).values())[0],
            }, status=409)

        try:
            instance = Dc_Incharge_Verify.objects.create(**cleaned_data)
            return JsonResponse({
                "status": True,
                "message": "Record created successfully.",
                "data": list(Dc_Incharge_Verify.objects.filter(id=instance.id).values())[0]
            }, status=201)
        except ValidationError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # ----------------------------------------------------
    # UPDATE (PUT)
    # ----------------------------------------------------
    elif method == "PUT":
        record_id = request.GET.get("id") or request.GET.get("slno") or body.get("id")
        
        if not record_id:
            return JsonResponse({"status": False, "message": "'id' parameter is required for updating."}, status=400)

        cleaned_data = get_cleaned_data(body)
        if not cleaned_data:
            return JsonResponse({"status": False, "message": "No valid fields provided to update."}, status=400)

        try:
            instance = Dc_Incharge_Verify.objects.get(id=record_id)
            for key, value in cleaned_data.items():
                setattr(instance, key, value)
            instance.save()

            return JsonResponse({
                "status": True,
                "message": "Record updated successfully.",
                "data": list(Dc_Incharge_Verify.objects.filter(id=instance.id).values())[0]
            }, status=200)
        except Dc_Incharge_Verify.DoesNotExist:
            return JsonResponse({"status": False, "message": f"Record with id '{record_id}' not found."}, status=404)
        except ValidationError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # ----------------------------------------------------
    # DELETE (DELETE)
    # ----------------------------------------------------
    elif method == "DELETE":
        record_id = request.GET.get("id") or request.GET.get("slno") or body.get("id")

        if not record_id:
            return JsonResponse({"status": False, "message": "'id' parameter is required for deletion."}, status=400)

        try:
            instance = Dc_Incharge_Verify.objects.get(id=record_id)
            instance.delete()
            return JsonResponse({
                "status": True,
                "message": f"Record with id '{record_id}' deleted successfully."
            }, status=200)
        except Dc_Incharge_Verify.DoesNotExist:
            return JsonResponse({"status": False, "message": f"Record with id '{record_id}' not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # ----------------------------------------------------
    # Unsupported HTTP Methods
    # ----------------------------------------------------
    return JsonResponse({"status": False, "message": f"Method {method} not allowed."}, status=405)


def _serialize_record(obj, request=None):
    """Helper to convert a model instance to a JSON-serializable dictionary."""
    image_url = None
    if obj.receiver_image:
        image_url = request.build_absolute_uri(obj.receiver_image.url) if request else obj.receiver_image.url

    return {
        'id': obj.id,
        'date': obj.date.isoformat() if obj.date else None,
        'DCNo': obj.DCNo,
        'jobno': obj.jobno,
        'trstype': obj.trstype,
        'wgt': str(obj.wgt) if obj.wgt is not None else None,
        'mtr': str(obj.mtr) if obj.mtr is not None else None,
        'rolls': obj.rolls,
        'qty'  : obj.qty,
        'bags': obj.bags,
        'username': obj.username,
        'latitude': str(obj.latitude) if obj.latitude is not None else None,
        'longitude': str(obj.longitude) if obj.longitude is not None else None,
        'concat_location' : str(obj.concat_location) if obj.concat_location is not None else None,
        'location': obj.location,
        'receiver_image': image_url,
        'received_at': obj.received_at.isoformat() if obj.received_at else None,
        'status': obj.status,
    }


def _extract_and_validate(data, files, is_update=False):
    """
    Validates types, required fields, and constraints.
    Returns (cleaned_data, errors).
    """
    errors = {}
    cleaned = {}

    # 1. Date (Required)
    if 'date' in data:
        parsed_date = parse_datetime(str(data['date']))
        if not parsed_date:
            errors['date'] = 'Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS).'
        else:
            cleaned['date'] = parsed_date
    elif not is_update:
        errors['date'] = 'Field "date" is required.'

    # 2. DCNo (Required, Integer)
    if 'DCNo' in data:
        try:
            cleaned['DCNo'] = int(data['DCNo'])
        except (ValueError, TypeError):
            errors['DCNo'] = 'Must be a valid integer.'
    elif not is_update:
        errors['DCNo'] = 'Field "DCNo" is required.'

    # 3. jobno (Required, max_length=50)
    if 'jobno' in data:
        val = str(data['jobno']).strip()
        if not val:
            errors['jobno'] = 'Field "jobno" cannot be blank.'
        elif len(val) > 50:
            errors['jobno'] = 'Maximum length is 50 characters.'
        else:
            cleaned['jobno'] = val
    elif not is_update:
        errors['jobno'] = 'Field "jobno" is required.'

    # 4. trstype (Required, max_length=50)
    if 'trstype' in data:
        val = str(data['trstype']).strip()
        if not val:
            errors['trstype'] = 'Field "trstype" cannot be blank.'
        elif len(val) > 50:
            errors['trstype'] = 'Maximum length is 50 characters.'
        else:
            cleaned['trstype'] = val
    elif not is_update:
        errors['trstype'] = 'Field "trstype" is required.'

    # 5. username (Required, Integer)
    if 'username' in data:
        try:
            cleaned['username'] = int(data['username'])
        except (ValueError, TypeError):
            errors['username'] = 'Must be a valid integer.'
    elif not is_update:
        errors['username'] = 'Field "username" is required.'

    # 6. wgt (Optional, Decimal max_digits=18, decimal_places=3)
    if 'wgt' in data:
        val = data['wgt']
        if val in [None, '']:
            cleaned['wgt'] = None
        else:
            try:
                dec = Decimal(str(val))
                cleaned['wgt'] = dec
            except (InvalidOperation, TypeError):
                errors['wgt'] = 'Must be a valid decimal number.'

    # 7. mtr (Optional, Decimal max_digits=18, decimal_places=2)
    if 'mtr' in data:
        val = data['mtr']
        if val in [None, '']:
            cleaned['mtr'] = None
        else:
            try:
                dec = Decimal(str(val))
                cleaned['mtr'] = dec
            except (InvalidOperation, TypeError):
                errors['mtr'] = 'Must be a valid decimal number.'

    # 8. rolls (Optional, Integer)
    if 'rolls' in data:
        val = data['rolls']
        if val in [None, '']:
            cleaned['rolls'] = None
        else:
            try:
                cleaned['rolls'] = int(val)
            except (ValueError, TypeError):
                errors['rolls'] = 'Must be a valid integer.'

    if 'qty' in data:
            val = data['qty']
            if val in [None, '']:
                cleaned['qty'] = None
            else:
                try:
                    cleaned['qty'] = float(val)
                except (ValueError, TypeError):
                    errors['qty'] = 'Must be a valid Float.'

    # 9. bags (Optional, max_length=50)
    if 'bags' in data:
        val = str(data['bags']).strip() if data['bags'] is not None else None
        if val and len(val) > 50:
            errors['bags'] = 'Maximum length is 50 characters.'
        else:
            cleaned['bags'] = val if val else None

    # 10. latitude & longitude (Optional Decimals)
    for coord in ['latitude', 'longitude']:
        if coord in data:
            val = data[coord]
            if val in [None, '']:
                cleaned[coord] = None
            else:
                try:
                    dec = Decimal(str(val))
                    cleaned[coord] = dec
                except (InvalidOperation, TypeError):
                    errors[coord] = f'Must be a valid decimal for {coord}.'

    # 11. Concatenated location and location text (Optional)
    for field, max_length in [('concat_location', 100), ('location', 500)]:
        if field in data:
            val = str(data[field]).strip() if data[field] is not None else None
            if val and len(val) > max_length:
                errors[field] = f'Maximum length is {max_length} characters.'
            else:
                cleaned[field] = val if val else None

    # 12. File upload: receiver_image
    if 'receiver_image' in files:
        uploaded_file = files['receiver_image']
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        if not any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
            errors['receiver_image'] = 'Only image files (.jpg, .jpeg, .png, .webp) are allowed.'
        elif uploaded_file.size > 5 * 1024 * 1024:  # 5MB cap
            errors['receiver_image'] = 'File size must not exceed 5MB.'
        else:
            cleaned['receiver_image'] = uploaded_file

    # 13. status (Optional, Boolean)
    if 'status' in data:
        val = data['status']
        if isinstance(val, bool):
            cleaned['status'] = val
        elif isinstance(val, str):
            if val.lower() in ['true', '1']:
                cleaned['status'] = True
            elif val.lower() in ['false', '0']:
                cleaned['status'] = False
            else:
                errors['status'] = 'Must be a boolean value (true/false).'
        else:
            errors['status'] = 'Must be a boolean value (true/false).'

    return cleaned, errors


def _get_request_data_and_files(request):
    """Return form data and uploaded files for POST, PUT, and PATCH requests."""
    if request.content_type and 'application/json' in request.content_type:
        try:
            return json.loads(request.body), {}
        except json.JSONDecodeError:
            raise ValueError('Invalid JSON body.')

    if request.method in ['PUT', 'PATCH'] and request.content_type and request.content_type.startswith('multipart/'):
        try:
            data, files = MultiPartParser(
                request.META,
                request,
                request.upload_handlers,
                request.encoding,
            ).parse()
            return data.dict(), files
        except MultiPartParserError as exc:
            raise ValueError(f'Invalid multipart body: {exc}')

    return request.POST.dict(), request.FILES


@csrf_exempt
def dc_receiver_crud_api(request, record_id=None):
    """
    Single function handling CRUD:
    - GET /api/dc-receiver/           -> List all records
    - GET /api/dc-receiver/<id>/      -> Retrieve single record
    - POST /api/dc-receiver/          -> Create a record (supports multipart and application/json)
    - PUT/POST /api/dc-receiver/<id>/ -> Update a record
    - DELETE /api/dc-receiver/<id>/   -> Delete a record
    """
    # -------------------------------------------------------------
    # 1. READ / RETRIEVE (GET)
    # -------------------------------------------------------------
    if request.method == 'GET':
        rec_id = record_id or request.GET.get('id')
        if rec_id:
            try:
                record = Dc_Reciver_Verify.objects.get(id=rec_id)
                return JsonResponse({'status': 'success', 'data': _serialize_record(record, request)}, status=200)
            except Dc_Reciver_Verify.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Record not found.'}, status=404)

        # Optional query filters
        queryset = Dc_Reciver_Verify.objects.all().order_by('-received_at')
        dc_no = request.GET.get('DCNo')
        job_no = request.GET.get('jobno')
        if dc_no:
            queryset = queryset.filter(DCNo=dc_no)
        if job_no:
            queryset = queryset.filter(jobno__icontains=job_no)

        records_data = [_serialize_record(rec, request) for rec in queryset]
        return JsonResponse({'status': 'success', 'count': len(records_data), 'data': records_data}, status=200)

    # -------------------------------------------------------------
    # 2. CREATE (POST)
    # -------------------------------------------------------------
    elif request.method == 'POST' and not record_id:
        try:
            payload, files = _get_request_data_and_files(request)
        except ValueError as exc:
            return JsonResponse({'status': 'error', 'message': str(exc)}, status=400)

        cleaned_data, errors = _extract_and_validate(payload, files, is_update=False)
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # A DC number may be reused for a different module/type, but not for
        # another receiver record in the same module/type.
        if Dc_Reciver_Verify.objects.filter(
            DCNo=cleaned_data['DCNo'],
            trstype=cleaned_data['trstype'],
        ).exists():
            return JsonResponse({
                'status': 'error',
                'errors': {'DCNo': 'This DC number already exists for this module.'},
            }, status=400)

        try:
            with transaction.atomic():
                instance = Dc_Reciver_Verify(**cleaned_data)
                instance.full_clean()
                instance.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Record created successfully.',
                'data': _serialize_record(instance, request)
            }, status=201)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # -------------------------------------------------------------
    # 3. UPDATE (PUT or POST with record_id)
    # -------------------------------------------------------------
    elif request.method in ['PUT', 'PATCH'] or (request.method == 'POST' and record_id):
        rec_id = record_id or request.GET.get('id')
        if not rec_id:
            return JsonResponse({'status': 'error', 'message': 'Missing record ID for update.'}, status=400)

        try:
            record = Dc_Reciver_Verify.objects.get(id=rec_id)
        except Dc_Reciver_Verify.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Record not found.'}, status=404)

        try:
            payload, files = _get_request_data_and_files(request)
        except ValueError as exc:
            return JsonResponse({'status': 'error', 'message': str(exc)}, status=400)

        cleaned_data, errors = _extract_and_validate(payload, files, is_update=True)
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        duplicate_query = Dc_Reciver_Verify.objects.filter(
            DCNo=cleaned_data.get('DCNo', record.DCNo),
            trstype=cleaned_data.get('trstype', record.trstype),
        ).exclude(pk=record.pk)
        if duplicate_query.exists():
            return JsonResponse({
                'status': 'error',
                'errors': {'DCNo': 'This DC number already exists for this module.'},
            }, status=400)

        try:
            with transaction.atomic():
                for field, value in cleaned_data.items():
                    setattr(record, field, value)
                record.full_clean()
                record.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Record updated successfully.',
                'data': _serialize_record(record, request)
            }, status=200)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # -------------------------------------------------------------
    # 4. DELETE (DELETE)
    # -------------------------------------------------------------
    elif request.method == 'DELETE':
        rec_id = record_id or request.GET.get('id')
        if not rec_id:
            # Handle ID in JSON body if not in path/params
            if request.body:
                try:
                    payload = json.loads(request.body)
                    rec_id = payload.get('id')
                except json.JSONDecodeError:
                    pass

        if not rec_id:
            return JsonResponse({'status': 'error', 'message': 'Record ID is required for deletion.'}, status=400)

        try:
            record = Dc_Reciver_Verify.objects.get(id=rec_id)
            record.delete()
            return JsonResponse({'status': 'success', 'message': f'Record {rec_id} deleted successfully.'}, status=200)
        except Dc_Reciver_Verify.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Record not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': f'Method {request.method} not allowed.'}, status=405)
