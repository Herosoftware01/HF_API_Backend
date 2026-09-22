from django.http import JsonResponse
from .models import ViewCuttingDelPrint,ViewKnitDelivery,ViewCutsecFabricdelivery,VueAccInhTransfer,VueAccProdDel,TrsGatemodule, CuttingPrintembdel, ViewYarnProcessDelivery,VueAccProcDel,ViewAccinwardVerification,ViewFabricDeliveryProcess,ViewMistakeqtyPrint,ViewUnitPcdelivery,VueRibDeliveryDetails,ViewGdwnFabricDeliveryPlan,TrsApidtls,ViewFabricDeliveryRepl,HerofashionUser,Holiday,RoleModulePermission,Dc_Verify_Incharge,Dc_Reciver_Verify
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.db import transaction



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

        # 1. Single Record by Primary Key (if URL is like /api/1774/)
        if pk:
            try:
                obj = TrsGatemodule.objects.using('demo').get(pk=pk)
                data = model_to_dict(obj)
                if obj.date:
                    data["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")
                return JsonResponse({"status": True, "data": data})
            except TrsGatemodule.DoesNotExist:
                return JsonResponse({"status": False, "message": "Record not found"}, status=404)

        # 2. Filter by DC Number (if URL is like /api/?no=5107)
        dc_no = request.GET.get("no")
        queryset = TrsGatemodule.objects.using('demo').all().order_by("-date")

        if dc_no:
            queryset = queryset.filter(no=dc_no)
        else:
            # Optional: Limit to 50 records if no search is provided to prevent crashing
            queryset = queryset[:50] 

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



def _validate_and_extract_payload(data, is_update=False):
    """
    Validates types, required fields, and converts data types.
    Returns: (cleaned_dict, error_string)
    """
    cleaned = {}

    # Required fields on creation
    required_fields = ["id", "date", "DCNo", "jobno", "trstype", "username"]
    if not is_update:
        missing = [f for f in required_fields if f not in data or data[f] is None or str(data[f]).strip() == ""]
        if missing:
            return None, f"Missing required fields: {', '.join(missing)}"

    # slno (Primary Key)
    if "id" in data:
        try:
            cleaned["id"] = int(data["id"])
        except (ValueError, TypeError):
            return None, "'slno' must be an integer."

    # DCNo
    if "DCNo" in data:
        try:
            cleaned["DCNo"] = int(data["DCNo"])
        except (ValueError, TypeError):
            return None, "'DCNo' must be an integer."

    # username
    if "username" in data:
        try:
            cleaned["username"] = int(data["username"])
        except (ValueError, TypeError):
            return None, "'username' must be an integer."

    # date (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)
    if "date" in data and data["date"]:
        parsed_date = parse_datetime(str(data["date"]))
        if not parsed_date:
            return None, "'date' must be in ISO format (e.g., '2026-09-20T10:30:00')."
        cleaned["date"] = parsed_date

    # jobno & trstype (CharFields with max_length=50)
    for char_field in ["jobno", "trstype"]:
        if char_field in data:
            val = str(data[char_field]).strip()
            if len(val) > 50:
                return None, f"'{char_field}' cannot exceed 50 characters."
            cleaned[char_field] = val

    # wgt (DecimalField max_digits=18, decimal_places=3)
    if "wgt" in data:
        if data["wgt"] is not None and str(data["wgt"]).strip() != "":
            try:
                cleaned["wgt"] = Decimal(str(data["wgt"]))
            except InvalidOperation:
                return None, "'wgt' must be a valid decimal number."
        else:
            cleaned["wgt"] = None

    # mtr (DecimalField max_digits=18, decimal_places=2)
    if "mtr" in data:
        if data["mtr"] is not None and str(data["mtr"]).strip() != "":
            try:
                cleaned["mtr"] = Decimal(str(data["mtr"]))
            except InvalidOperation:
                return None, "'mtr' must be a valid decimal number."
        else:
            cleaned["mtr"] = None

    # rolls (IntegerField, optional)
    if "rolls" in data:
        if data["rolls"] is not None and str(data["rolls"]).strip() != "":
            try:
                cleaned["rolls"] = int(data["rolls"])
            except (ValueError, TypeError):
                return None, "'rolls' must be an integer."
        else:
            cleaned["rolls"] = None

    # bags (CharField, optional, max_length=50)
    if "bags" in data:
        if data["bags"] is not None:
            val = str(data["bags"]).strip()
            if len(val) > 50:
                return None, "'bags' cannot exceed 50 characters."
            cleaned["bags"] = val
        else:
            cleaned["bags"] = None

    return cleaned, None


@csrf_exempt
def dc_verify_incharge_crud(request):
    """
    All-in-one CRUD API endpoint using standard Django JsonResponse:
      - GET:    Filter by ?slno=... or ?dcno=... or fetch all.
      - POST:   Create a new record (JSON body).
      - PUT:    Update an existing record via ?slno=... (JSON body).
      - DELETE: Delete record via ?slno=...
    """
    method = request.method

    # ----------------------------------------------------
    # READ (GET)
    # ----------------------------------------------------
    if method == "GET":
        slno = request.GET.get("id")
        dcno = request.GET.get("dcno") or request.GET.get("DCNo")

        queryset = Dc_Verify_Incharge.objects.all()

        if id:
            queryset = queryset.filter(id=id)
        if dcno:
            queryset = queryset.filter(DCNo=dcno)

        data = list(queryset.values())
        return JsonResponse({
            "status": True,
            "message": "Records fetched successfully.",
            "count": len(data),
            "data": data
        }, status=200)

    # Parse JSON body for mutation requests
    if method in ["POST", "PUT"]:
        try:
            body = json.loads(request.body.decode("utf-8")) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON payload."
            }, status=400)

    # ----------------------------------------------------
    # CREATE (POST)
    # ----------------------------------------------------
    if method == "POST":
        cleaned_data, error = _validate_and_extract_payload(body, is_update=False)
        if error:
            return JsonResponse({"status": False, "message": error}, status=400)

        # Check primary key collision since 'slno' is user-supplied
        if Dc_Verify_Incharge.objects.filter(id=cleaned_data["id"]).exists():
            return JsonResponse({
                "status": False,
                "message": f"Record with id '{cleaned_data['id']}' already exists."
            }, status=409)

        try:
            instance = Dc_Verify_Incharge.objects.create(**cleaned_data)
            return JsonResponse({
                "status": True,
                "message": "Record created successfully.",
                "data": list(Dc_Verify_Incharge.objects.filter(slno=instance.slno).values())[0]
            }, status=201)
        except ValidationError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # ----------------------------------------------------
    # UPDATE (PUT)
    # ----------------------------------------------------
    elif method == "PUT":
        slno = request.GET.get("id") or body.get("id")
        if not slno:
            return JsonResponse({
                "status": False,
                "message": "'slno' parameter is required for update (in query params or body)."
            }, status=400)

        try:
            instance = Dc_Verify_Incharge.objects.get(slno=slno)
        except Dc_Verify_Incharge.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": f"Record with slno '{id}' not found."
            }, status=404)

        cleaned_data, error = _validate_and_extract_payload(body, is_update=True)
        if error:
            return JsonResponse({"status": False, "message": error}, status=400)

        # Apply updates
        for field, value in cleaned_data.items():
            if field != "id":  # Avoid mutating primary key
                setattr(instance, field, value)

        try:
            instance.save()
            return JsonResponse({
                "status": True,
                "message": "Record updated successfully.",
                "data": list(Dc_Verify_Incharge.objects.filter(id=instance.id).values())[0]
            }, status=200)
        except ValidationError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # ----------------------------------------------------
    # DELETE (DELETE)
    # ----------------------------------------------------
    elif method == "DELETE":
        id = request.GET.get("id")
        if not id:
            # Fallback check inside JSON body
            try:
                body = json.loads(request.body.decode("utf-8")) if request.body else {}
                id = body.get("id")
            except json.JSONDecodeError:
                pass

        if not id:
            return JsonResponse({
                "status": False,
                "message": "'id' parameter is required for deletion."
            }, status=400)

        try:
            instance = Dc_Verify_Incharge.objects.get(slno=id)
            instance.delete()
            return JsonResponse({
                "status": True,
                "message": f"Record with slno '{id}' deleted successfully."
            }, status=200)
        except Dc_Verify_Incharge.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": f"Record with slno '{id}' not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({"status": False, "message": f"Database error: {str(e)}"}, status=500)

    # Unsupported HTTP Methods
    return JsonResponse({
        "status": False,
        "message": f"Method {method} not allowed."
    }, status=405)


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
        'bags': obj.bags,
        'username': obj.username,
        'latitude': str(obj.latitude) if obj.latitude is not None else None,
        'longitude': str(obj.longitude) if obj.longitude is not None else None,
        'location': obj.location,
        'receiver_image': image_url,
        'received_at': obj.received_at.isoformat() if obj.received_at else None,
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

    # 9. bags (Optional, max_length=50)
    if 'bags' in data:
        val = str(data['bags']).strip() if data['bags'] is not None else None
        if val and len(val) > 50:
            errors['bags'] = 'Maximum length is 50 characters.'
        else:
            cleaned['bags'] = val if val else None

    # 10. latitude & longitude (Optional Decimals)
    for coord, max_d, dec_p in [('latitude', 10, 7), ('longitude', 10, 7)]:
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

    # 11. location (Optional, max_length=500)
    if 'location' in data:
        val = str(data['location']).strip() if data['location'] is not None else None
        if val and len(val) > 500:
            errors['location'] = 'Maximum length is 500 characters.'
        else:
            cleaned['location'] = val if val else None

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

    return cleaned, errors


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
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON body.'}, status=400)
            files = {}
        else:
            payload = request.POST.dict()
            files = request.FILES

        cleaned_data, errors = _extract_and_validate(payload, files, is_update=False)
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

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

        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON body.'}, status=400)
            files = {}
        else:
            payload = request.POST.dict()
            files = request.FILES

        cleaned_data, errors = _extract_and_validate(payload, files, is_update=True)
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

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