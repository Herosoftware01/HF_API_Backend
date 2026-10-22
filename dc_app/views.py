from django.http import JsonResponse
from .models import (ViewCuttingDelPrint,
ViewKnitDelivery,ViewCutsecFabricdelivery,
VueAccInhTransfer,VueAccProdDel,
TrsGatemodule, CuttingPrintembdel,
ViewYarnProcessDelivery,VueAccProcDel,
ViewAccinwardVerification,ViewFabricDeliveryProcess,
ViewMistakeqtyPrint,ViewUnitPcdelivery,VueRibDeliveryDetails,ViewGdwnFabricDeliveryPlan,
TrsApidtls,ViewFabricDeliveryRepl,HerofashionUser,Holiday,RoleModulePermission,
Dc_Reciver_Verify,ViewGeneralDeiveryType1,ViewGenStockIssue,ModuleMaster)
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.dateparse import  parse_datetime
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError, transaction
from django.db import transaction
from django.http.multipartparser import MultiPartParser, MultiPartParserError
from django.utils import timezone
from datetime import date, datetime
from django.views.decorators.http import require_http_methods
import re
from django.db.models import Max


def cutting_del_print(request, id=None):
    selected_id = id if id is not None else request.GET.get("id")
    queryset = ViewCuttingDelPrint.objects.using('demo').all()

    if selected_id not in (None, ""):
        try:
            selected_id = int(selected_id)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "id must be an integer.",
            }, status=400)

        data = list(queryset.filter(id=selected_id).values())
    else:
        # Note: Add additional display fields from ViewCuttingDelPrint (e.g., 'orderno', 'supplier') as needed
        options = (
            queryset.values("id")
            .distinct()
            .order_by("id")
        )
        data = [
            {
                "id": option["id"],
            }
            for option in options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })

def cutting_bit_print(request, id):
    
    queryset = CuttingPrintembdel.objects.using('demo').filter(id=id)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)

def yarn_process_delivery(request, dcno):
    queryset = ViewYarnProcessDelivery.objects.using('test').filter(dcno=dcno)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)


def knitting_del_print(request, dcno=None):
    selected_dcno = dcno if dcno is not None else request.GET.get("dcno")
    queryset = ViewKnitDelivery.objects.using('test').all()

    if selected_dcno not in (None, ""):
        try:
            selected_dcno = int(selected_dcno)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dcno must be an integer.",
            }, status=400)

        data = list(queryset.filter(dcno=selected_dcno).values())
    else:
        dc_options = queryset.values("dcno", "knit_name").distinct().order_by("dcno")
        data = [
            {"dcno": option["dcno"], "supplier": option["knit_name"]}
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data
    })


def acc_prod_del_print(request, no=None):
    selected_no = no if no is not None else request.GET.get("no")
    queryset = VueAccProdDel.objects.using('test').all()

    if selected_no not in (None, ""):
        try:
            selected_no = int(selected_no)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "no must be an integer.",
            }, status=400)

        data = list(queryset.filter(no=selected_no).values())
    else:
        prod_options = (
            queryset.values("no", "supplier", "orderno")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "no": option["no"],
                "supplier": option["supplier"],
                "orderno": option["orderno"],
            }
            for option in prod_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })
def acc_proc_del_print(request, no=None):
    selected_no = no if no is not None else request.GET.get("no")
    queryset = VueAccProcDel.objects.using('test').all()

    if selected_no not in (None, ""):
        try:
            selected_no = int(selected_no)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "no must be an integer.",
            }, status=400)

        data = list(queryset.filter(no=selected_no).values())
    else:
        proc_options = (
            queryset.values("no", "supplier", "orderno")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "no": option["no"],
                "supplier": option["supplier"],
                "orderno": option["orderno"],
            }
            for option in proc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })



def acc_inhouse_transfer(request, no=None):
    selected_no = no if no is not None else request.GET.get("no")
    queryset = VueAccInhTransfer.objects.using('test').all()

    if selected_no not in (None, ""):
        try:
            selected_no = int(selected_no)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "no must be an integer.",
            }, status=400)

        data = list(queryset.filter(no=selected_no).values())
    else:
        transfer_options = (
            queryset.values("no", "orderno", "frmdpt", "todept")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "no": option["no"],
                "orderno": option["orderno"],
                "from_department": option["frmdpt"],
                "to_department": option["todept"],
            }
            for option in transfer_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
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


def fabric_process_delivery(request, no=None):
    # Accept from URL param or either query param ('no' or 'dcno')
    selected_no = (
        no
        if no is not None
        else (request.GET.get("no") or request.GET.get("dcno"))
    )
    queryset = ViewFabricDeliveryProcess.objects.using('test').all()

    if selected_no not in (None, ""):
        try:
            selected_no = int(selected_no)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "no must be an integer.",
            }, status=400)

        # Filter by 'no' (matching the primary key on ViewFabricDeliveryProcess)
        data = list(queryset.filter(no=selected_no).values())
    else:
        delivery_options = (
            queryset.values("no", "su_name", "orderno", "del_unit")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "no": option["no"],
                "supplier": option["su_name"],
                "orderno": option["orderno"],
                "delivery_unit": option["del_unit"],
            }
            for option in delivery_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })

def mistake_qty_print(request, dcno=None):
    selected_dcno = dcno if dcno is not None else request.GET.get("dcno")
    queryset = ViewMistakeqtyPrint.objects.using('demo').all()

    if selected_dcno not in (None, ""):
        try:
            selected_dcno = int(selected_dcno)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dcno must be an integer.",
            }, status=400)

        data = list(queryset.filter(dcno=selected_dcno).values())
    else:
        dc_options = (
            queryset.values("dcno", "jobno", "toad", "frm")
            .distinct()
            .order_by("dcno")
        )
        data = [
            {
                "dcno": option["dcno"],
                "jobno": option["jobno"],
                "to_party": option["toad"],
                "from_party": option["frm"],
            }
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })

def unit_pc_delivery(request, dcno):
    queryset = ViewUnitPcdelivery.objects.using('test').filter(dcno=dcno)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)

def CuttingSecFabric(request, dcno):
    queryset = ViewCutsecFabricdelivery.objects.using('demo').filter(dcno=dcno)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)


def rib_delivery_print(request, dc=None):
    # Accepts from URL param or query params ('dc' or 'dcno')
    selected_dc = (
        dc
        if dc is not None
        else (request.GET.get("dc") or request.GET.get("dcno"))
    )
    queryset = VueRibDeliveryDetails.objects.using('demo').all()

    if selected_dc not in (None, ""):
        try:
            selected_dc = int(selected_dc)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dc must be an integer.",
            }, status=400)

        data = list(queryset.filter(dc=selected_dc).values())
    else:
        dc_options = (
            queryset.values("dc", "jobno", "deladd", "topbottom_des")
            .distinct()
            .order_by("dc")
        )
        data = [
            {
                "dc": option["dc"],
                "jobno": option["jobno"],
                "delivery_address": option["deladd"],
                "description": option["topbottom_des"],
            }
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })


def godown_fabric_delivery_plan(request, dcno=None):
    selected_dcno = dcno if dcno is not None else request.GET.get("dcno")
    queryset = ViewGdwnFabricDeliveryPlan.objects.using('demo').all()

    if selected_dcno not in (None, ""):
        try:
            selected_dcno = int(selected_dcno)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dcno must be an integer.",
            }, status=400)

        data = list(queryset.filter(dcno=selected_dcno).values())
    else:
        dc_options = (
            queryset.values("dcno", "jobno", "frm", "todept")
            .distinct()
            .order_by("dcno")
        )
        data = [
            {
                "dcno": option["dcno"],
                "jobno": option["jobno"],
                "from_dept": option["frm"],
                "to_dept": option["todept"],
            }
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })


def fabric_delivery_repl(request, dcno=None):
    selected_dcno = dcno if dcno is not None else request.GET.get("dcno")
    queryset = ViewFabricDeliveryRepl.objects.using("demo").all()

    if selected_dcno not in (None, ""):
        try:
            selected_dcno = int(selected_dcno)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dcno must be an integer.",
            }, status=400)

        data = list(queryset.filter(dcno=selected_dcno).values())
    else:
        dc_options = (
            queryset.values("dcno", "jobno", "frm", "todept")
            .distinct()
            .order_by("dcno")
        )
        data = [
            {
                "dcno": option["dcno"],
                "jobno": option["jobno"],
                "from_dept": option["frm"],
                "to_dept": option["todept"],
            }
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })

def general_delivery_type1(request, dcno=None):
    selected_dcno = (
        dcno
        if dcno is not None
        else (request.GET.get("dcno") or request.GET.get("no"))
    )

    today = date.today()

    # Current financial year: April 1 → March 31
    if today.month >= 4:
        fy_start = date(today.year, 4, 1)
        fy_end = date(today.year + 1, 3, 31)
    else:
        fy_start = date(today.year - 1, 4, 1)
        fy_end = date(today.year, 3, 31)

    queryset = (
        ViewGeneralDeiveryType1.objects.using('test')
        .filter(date__gte=fy_start, date__lte=fy_end)
    )

    if selected_dcno not in (None, ""):
        try:
            selected_dcno = int(selected_dcno)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "dcno must be an integer.",
            }, status=400)

        data = list(queryset.filter(no=selected_dcno).values())
    else:
        dc_options = (
            queryset.values("no", "suppliername", "department","ty")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "dcno": option["no"],
                "supplier": option["suppliername"],
                "department": option["department"],
                "type" : option["ty"]
            }
            for option in dc_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })

def gen_stock_issue(request, no=None):
    selected_no = (
        no
        if no is not None
        else (request.GET.get("no") or request.GET.get("dcno"))
    )

    queryset = ViewGenStockIssue.objects.using("test").filter(
        date__year=timezone.now().year
    )

    if selected_no not in (None, ""):
        try:
            selected_no = int(selected_no)
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "no must be an integer.",
            }, status=400)

        data = list(queryset.filter(no=selected_no).values())
    else:
        issue_options = (
            queryset.values("no", "frm_dept", "to_dept", "reqno")
            .distinct()
            .order_by("no")
        )
        data = [
            {
                "no": option["no"],
                "from_dept": option["frm_dept"],
                "to_dept": option["to_dept"],
                "reqno": option["reqno"],
            }
            for option in issue_options
        ]

    return JsonResponse({
        "status": True,
        "message": "Success",
        "count": len(data),
        "data": data,
    })


# --- VIEW ---
@csrf_exempt
def gate_module_api(request, pk=None):

    # ---------------- CORS PREFLIGHT (OPTIONS) ----------------
    if request.method == "OPTIONS":
        response = JsonResponse({"status": True})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return response

    # ---------------- GET ----------------
    # ---------------- GET ----------------
    if request.method == "GET":
        if pk:
            try:
                obj = TrsGatemodule.objects.using("demo").get(pk=pk)
                data = model_to_dict(obj)
                if obj.date:
                    data["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")
                return JsonResponse({"status": True, "data": data})
            except TrsGatemodule.DoesNotExist:
                return JsonResponse({"status": False, "message": "Record not found"}, status=404)

        queryset = TrsGatemodule.objects.using("demo").all().order_by("-date")

        dc_no = request.GET.get("no")
        filter_date = request.GET.get("date")

        if dc_no:
            queryset = queryset.filter(no=dc_no)
        if filter_date:
            queryset = queryset.filter(date__date=filter_date)

        # Calculate the next available SL for today
        today_date = datetime.now().date()
        max_sl_dict = TrsGatemodule.objects.using("demo").filter(
            gate_delivery_date__date=today_date
        ).aggregate(Max('sl'))
        next_sl = (max_sl_dict.get('sl__max') or 0) + 1

        data = []
        for obj in queryset:
            item = model_to_dict(obj)
            if obj.date:
                item["date"] = obj.date.strftime("%Y-%m-%d %H:%M:%S")
            # Attach next_sl so the frontend can preview it before saving
            item["next_sl"] = next_sl 
            data.append(item)

        return JsonResponse({"status": True, "count": len(data), "data": data, "next_sl": next_sl})

    # ---------------- POST ----------------
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            module = body.get("module")
            qr_code_dtls = body.get("qr_code_dtls")

            if TrsGatemodule.objects.using("demo").filter(
                module=module, qr_code_dtls=qr_code_dtls
            ).exists():
                return JsonResponse({
                    "status": False,
                    "message": "DcNo Already Saved"
                }, status=409)

            date_val = body.get("date")
            print_date_val = body.get("print_delivery_date")
            gate_date_val = body.get("gate_delivery_date")
            inch_verify_date = body.get("inch_verify_date")
            without_iv_date = body.get("without_iv_date")

            parsed_date = parse_datetime(date_val) if date_val else None
            
            # --- Auto-generate daily SL ---
            new_sl = 1
            if parsed_date:
                record_date = parsed_date.date()
                max_sl_dict = TrsGatemodule.objects.using("demo").filter(
                    date__date=record_date
                ).aggregate(Max('sl'))
                
                current_max = max_sl_dict.get('sl__max') or 0
                new_sl = current_max + 1

                if new_sl > 500:
                    return JsonResponse({
                        "status": False, 
                        "message": "Daily limit of 500 records reached."
                    }, status=400)

            TrsGatemodule.objects.using("demo").create(
                module=module,
                qr_code_dtls=qr_code_dtls,
                companyid=body.get("companyid"),
                year=body.get("year"),
                no=body.get("no"),
                date=parsed_date,
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
                fhero=body.get("fhero"),
                inch_verify_date=parse_datetime(inch_verify_date) if inch_verify_date else None,
                inch_verify_status=body.get("inch_verify_status"),
                inch_reject_remakrs=body.get("inch_reject_remakrs"),
                inch_remakrs_date=body.get("inch_remakrs_date"),
                sl=new_sl,
                without_inch_verify=body.get("without_inch_verify", False),
                without_iv_date=body.get("without_iv_date")
            )

            return JsonResponse({"status": True, "message": "Dc Created Successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

    # ---------------- PUT / PATCH ----------------
    # ---------------- PUT / PATCH ----------------
    elif request.method in ["PUT", "PATCH"]:
        if not pk:
            return JsonResponse({
                "status": False,
                "message": "Record ID is required for updates"
            }, status=400)

        try:
            body = json.loads(request.body)
            obj = TrsGatemodule.objects.using("demo").get(pk=pk)

            # Update original fields
            if "verify" in body:
                obj.verify = body["verify"]
            
            if "gate_delivery_date" in body:
                date_str = body["gate_delivery_date"]
                obj.gate_delivery_date = parse_datetime(date_str) if date_str else None

            if "fhero" in body:
                obj.fhero = body["fhero"]
                
            if "inch_verify_date" in body:
                date_str = body["inch_verify_date"]
                obj.inch_verify_date = parse_datetime(date_str) if date_str else None
                
            if "inch_verify_status" in body:
                obj.inch_verify_status = body["inch_verify_status"]

            if "inch_reject_remakrs" in body:
                obj.inch_reject_remakrs = body["inch_reject_remakrs"]

            if "inch_remakrs_date" in body:
                obj.inch_remakrs_date = body["inch_remakrs_date"]
                
            if "without_inch_verify" in body:
                obj.without_inch_verify = body["without_inch_verify"]

            if "without_iv_date" in body:
                obj.without_iv_date = body["without_iv_date"]

            # --- AUTO-GENERATE SL ON GATE VERIFICATION ---
            # Generate SL only if this is a standard verify (not just an inch-bypass logging attempt) 
            # and it doesn't already have an SL.
            if "verify" in body and not obj.sl and body.get("without_inch_verify") is not True:
                # Group by today's date based on gate_delivery_date to reset daily
                record_date = datetime.now().date()
                if obj.gate_delivery_date:
                    record_date = obj.gate_delivery_date.date()

                max_sl_dict = TrsGatemodule.objects.using("demo").filter(
                    gate_delivery_date__date=record_date
                ).aggregate(Max('sl'))
                
                current_max = max_sl_dict.get('sl__max') or 0
                new_sl = current_max + 1

                if new_sl > 500:
                    return JsonResponse({
                        "status": False, 
                        "message": "Daily limit of 500 records reached."
                    }, status=400)
                    
                obj.sl = new_sl

            obj.save(using="demo")

            return JsonResponse({
                "status": True,
                "message": "Verification saved successfully",
                "sl": obj.sl  # Pass the generated SL back to React
            }, status=200)

        except TrsGatemodule.DoesNotExist:
            return JsonResponse({"status": False, "message": "Record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

        
    # ---------------- FALLBACK ----------------
    return JsonResponse({
        "status": False,
        "message": f"Method '{request.method}' not allowed"
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


def get_user_by_username(request, username=None):
    data = HerofashionUser.objects.all()
    if username is not None:
        data = data.filter(username=username)

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
