from django.shortcuts import render,get_object_or_404
from django.db import connections
from rest_framework.decorators import api_view
# import pandas as pd
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import QcAdminMistake,Cont_employee,cut_sample_data,cut_sample_data_final,VueUser,Unit,Needle_change,Line,roving_qc_mistake,qc_piece_final, MachineAllocation, machine_details, emp_allocate, Empwisesal, VueProcessSequence
from .serializers import QcAdminMistakeSerializer,UnitSerializer,MachineTrasnsferSerializer,MachineSerializer,LineSerializer, MachineAllocationSerializer, VueProcessSequenceSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from collections import defaultdict
from django.shortcuts import get_object_or_404
from datetime import date
from django.utils.timezone import now
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from datetime import datetime
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone


class QcAdminMistakeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request):
    #     mistakes = QcAdminMistake.objects.all()
    #     serializer = QcAdminMistakeSerializer(mistakes, many=True)
    #     return Response(serializer.data)

    def get(self, request):
        priority_order = Case(
            When(name="Needle Holes", then=Value(1)),
            When(name="Skip Stitch", then=Value(2)),
            When(name="Loose Stitch", then=Value(3)),
            When(name="Broken Stitch", then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )

        mistakes = QcAdminMistake.objects.annotate(
            priority=priority_order
        ).order_by('priority', 'id')

        serializer = QcAdminMistakeSerializer(mistakes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QcAdminMistakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QcAdminMistakeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return QcAdminMistake.objects.get(pk=pk)
        except QcAdminMistake.DoesNotExist:
            return None

    def get(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(mistake)
        return Response(serializer.data)

    def put(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(mistake, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(
            mistake, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        mistake.delete()
        return Response(status=204) 





class LineAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        lines = Line.objects.all()

        grouped_data = defaultdict(list)

        for line in lines:
            grouped_data[line.unit_id].append(line.line_number)

        response_data = []

        for unit, line_numbers in grouped_data.items():
            response_data.append({
                "unit": unit,
                "lines": line_numbers
            })

        return Response(response_data)


    # CREATE LINE
    def post(self, request):

        serializer = LineSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE LINE
    def delete(self, request, pk):

        try:
            line = Line.objects.get(pk=pk)
            line.delete()
            return Response({"message":"Line deleted"},status=status.HTTP_204_NO_CONTENT)

        except Line.DoesNotExist:
            return Response({"error":"Line not found"},status=status.HTTP_404_NOT_FOUND)
        



@api_view(['GET'])
def get_bundle_data(request):
    try:
        bundle_id = request.GET.get('bundle_id')
       
        if not bundle_id:
            return Response({"error": "bundle_id is required"}, status=400)

        with connections['demo'].cursor() as cursor:
            cursor.execute(
                "EXEC dbo.GetOrderBundleList_ByBundID @BundID=%s",
                [bundle_id]
            )

            if cursor.description is None:
                return Response({"message": "Bundle Not Found"}, status=404)

            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        if not results:
            return Response({"message": "Bundle Not Found"}, status=404)

     
        bundle_ids_from_api = [
            str(item.get('bundid')) for item in results if item.get('bundid') is not None
        ]

        # checked_bundle_ids = set(
        #     qc_piece_final.objects.filter(
        #         bundle_id__in=bundle_ids_from_api
        #     ).values_list('bundle_id', flat=True)
        # )

        checked_bundle_ids = set(
            qc_piece_final.objects.filter(
                bundle_id__in=bundle_ids_from_api
            ).exclude(qc_type='rowing_qc')   #  ignore rowing_qc
            .values_list('bundle_id', flat=True)
        )

        for item in results:
            bund_id = str(item.get('bundid'))

            if bund_id in checked_bundle_ids:
                return Response({
                    "message": "This bundle is already checked"
                }, status=200)

        return Response(results)

    except Exception as e:
        return Response(
            {"error": "Something went wrong", "details": str(e)},
            status=500
        )

from .models import qc_piece_data


@api_view(['POST'])
def save_piece(request):
    data = request.data
    user_id = data.get("userId")

    if not user_id:
        return Response({"status": "error", "message": "user_id is required"}, status=400)
    
    bundle_no = data.get("bundle_no")
    bundle_id = data.get("bundle_id")
    jobno = data.get("jobno")
    product = data.get("product")
    color = data.get("color")
    size = data.get("size")
    # unit = data.get("unit")
    unit = int(data.get("unit"))
    line = int(data.get("line"))
    seq = data.get("seq")
    machine_id = data.get("machineId")
    qc_type = data.get("qc_type")
    total_pieces = int(data.get("total_pieces") or 0)
    piece_no = int(data.get("piece_no") or 0)
    total_mistake = int(data.get("total_mistake") or 0)
    mistake_percentage = data.get("mistake_percentage")
    defects = data.get("defects", [])
    # emp_id = data.get("operator")
    # machine_id = data.get("machineId", "")
    process = data.get("process", "")
    shade_variation = data.get("shade_variation", False)
    number_sticker = data.get("number_sticker", False)
    remarks = data.get("remarks", "")
    

    # Save defects to qc_piece_data
    saved_pieces = []
    for defect in defects:
        qc_piece = qc_piece_data.objects.create(
            bundle_no=bundle_no,
            bundle_id=bundle_id,
            jobno=jobno,
            product=product,
            color=color,
            size=size,
            unit=unit,
            line=line,
            seq=seq,
            machine_id=machine_id,
            qc_type=qc_type,
            total_pieces=total_pieces,
            piece_no=piece_no,
            total_mistake=total_mistake,
            mistake_percentage=mistake_percentage,
            category=defect.get("category", ""),
            mistake_name=defect.get("mistake_name", ""),
            mistake_count=defect.get("mistake_count", 0),
            user_id=user_id
        )
        saved_pieces.append(qc_piece)

    # If qc_type is 'rowing_qc', save extra info in roving_qc_mistake
    if qc_type == "rowing_qc":
        for qc_piece in saved_pieces:
            roving_qc_mistake.objects.create(
                qc_piece=qc_piece,
                machine_id=machine_id,
                seq=seq,
                operation=process,
                # emb_id=emp_id,  # add if you have embroidery ID
                shade_var=shade_variation,
                num_sticker=number_sticker,
                remark=remarks
            )

    return Response({"status": "success"})



# @api_view(["POST"])
# def save_final_piece(request):
#     try:
#         bundle_no = request.data.get("bundle_no")
#         bundle_id = request.data.get("bundle_id")
#         jobno = request.data.get("jobno")
#         product = request.data.get("product")
#         color = request.data.get("color")
#         size = request.data.get("size")
#         unit = request.data.get("unit")
#         line = request.data.get("line")
#         machine_id = request.data.get("machineId")
#         user_id = request.data.get("userId", None)
#         seq = request.data.get("seq")
#         qc_type = request.data.get("qc_type")
#         total_pieces = int(request.data.get("total_pieces", 0))
#         checked_piece = int(request.data.get("checked_piece", 0))
#         force_save = request.data.get("force_save", False)

#         if not bundle_id:
#             return Response({"error": "bundle_id is required"}, status=400)

#         if total_pieces == 0:
#             return Response({"error": "total_pieces cannot be 0"}, status=400)

#         if checked_piece < total_pieces and not force_save:
#             return Response(
#                 {
#                     "error": "All pieces not checked. Enable force save to continue.",
#                     "checked_piece": checked_piece,
#                     "total_pieces": total_pieces,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         qc_piece_final.objects.create(
#             bundle_no=bundle_no,
#             bundle_id=bundle_id,
#             jobno=jobno,
#             product=product,
#             color=color,
#             size=size,
#             line=line,
#             unit=unit,
#             qc_type=qc_type,
#             total_pieces=total_pieces,
#             checked_piece=checked_piece,
#             force_save=force_save,
#             user_id=user_id,
#             seq=seq,
#             machine_id=machine_id
#         )

#         return Response(
#             {
#                 "message": "Saved successfully",
#                 "checked_piece": checked_piece,
#                 "total_pieces": total_pieces,
#                 "force_save": force_save,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def save_final_piece(request):
    try:
        bundle_no = request.data.get("bundle_no")
        bundle_id = request.data.get("bundle_id")
        jobno = request.data.get("jobno")
        product = request.data.get("product")
        color = request.data.get("color")
        size = request.data.get("size")
        unit = request.data.get("unit")
        line = request.data.get("line")
        machine_id = request.data.get("machineId")
        user_id = request.data.get("userId", None)
        seq = request.data.get("seq")
        qc_type = request.data.get("qc_type")
        total_pieces = int(request.data.get("total_pieces", 0))
        checked_piece = int(request.data.get("checked_piece", 0))
        force_save = request.data.get("force_save", False)

        if not bundle_id:
            return Response(
                {"error": "bundle_id is required"},
                status=400
            )

        if total_pieces == 0:
            return Response(
                {"error": "total_pieces cannot be 0"},
                status=400
            )

        if checked_piece < total_pieces and not force_save:
            return Response(
                {
                    "error": "All pieces not checked. Enable force save to continue.",
                    "checked_piece": checked_piece,
                    "total_pieces": total_pieces,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ UPDATE if exists else CREATE
        obj, created = qc_piece_final.objects.update_or_create(
            bundle_id=bundle_id,
            qc_type=qc_type,
            seq=seq,

            defaults={
                "bundle_no": bundle_no,
                "jobno": jobno,
                "product": product,
                "color": color,
                "size": size,
                "line": line,
                "unit": unit,
                "total_pieces": total_pieces,
                "checked_piece": checked_piece,
                "force_save": force_save,
                "user_id": user_id,
                "machine_id": machine_id,
            }
        )

        return Response(
            {
                "message": "Updated successfully" if not created else "Saved successfully",
                "checked_piece": checked_piece,
                "total_pieces": total_pieces,
                "force_save": force_save,
                "created": created
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def get_last_bundle(request):
    from .models import qc_piece_data, qc_piece_final, roving_qc_mistake

    unit = request.GET.get("unit")
    line = request.GET.get("line")
    qc_type = request.GET.get("qc_type")
    seq = request.GET.get("seq")
    bundle_id = request.GET.get("bundle_id")
    # bundle_id = request.GET.get("bundle_id")

    last = qc_piece_data.objects.filter(
        unit=unit,
        line=line,
        qc_type=qc_type,
        seq__iexact=seq,
        bundle_id=bundle_id
        
    ).order_by("-id").first()

    if not last:
        return Response({"error": "No bundle found"}, status=404)

    bundle_id = last.bundle_id
    piece = last.piece_no

    is_completed = qc_piece_final.objects.filter(bundle_id=bundle_id).exists()

    roving_data = {}

    if qc_type and qc_type.strip().lower() == "rowing_qc":
        mistakes = roving_qc_mistake.objects.filter(qc_piece__bundle_id=last.bundle_id,seq__iexact=seq)
        print("Mistakes count for bundle:", mistakes.count())
        roving_data = {
            "machine_id": mistakes.first().machine_id if mistakes.exists() else None,
            "operation": mistakes.first().operation if mistakes.exists() else None,
            "operator": mistakes.first().emb_id if mistakes.exists() else None,
            "user_id": last.user_id,
            "roving_mistakes": [
                {
                    "machine_id": m.machine_id,
                    "operation": m.operation,
                    "emb_id": m.emb_id,
                    "shade_var": m.shade_var,
                    "num_sticker": m.num_sticker,
                    "remark": m.remark
                }
                for m in mistakes
            ]
        }

        print("roving_data", roving_data)

    return Response({
        "bundle_id": bundle_id,
        "bundle_no": last.bundle_no,
        "jobno": last.jobno,
        "product": last.product,
        "color": last.color,
        "size": last.size,
        "total_pieces": last.total_pieces,
        "piece_no": piece,
        "checked_pieces": piece,
        "is_completed": is_completed,
        #  extra only for roving
        **roving_data
    })



@api_view(["GET"])
def check_bundle_entry_status(request):
    bundle_id = request.GET.get("bundle_id")
   

    if not bundle_id:
        return Response({"error": "bundle_id required"}, status=400)

    in_data = qc_piece_data.objects.filter(bundle_id=bundle_id).exists()
    in_final = qc_piece_final.objects.filter(bundle_id=bundle_id).exists()

    if in_data and in_final:
        return Response({"status": "both"})  # open ProductionDetails

    elif in_data and not in_final:
        return Response({"status": "in_progress"})  # go to Defects directly

    else:
        return Response({"status": "new"})  # normal flow
    


# def import_machine_details_from_excel(request):
#     file_path = 'C:/Users/Murthy/Desktop/Full App/HF_API/machine.xlsx'

#     try:
#         # Read Excel, header is at row 4 (index 3)
#         df = pd.read_excel(file_path, header=3)

#         # Clean column names
#         df.columns = df.columns.str.strip()

#         required_columns = ['Identity', 'Item', 'Description']

#         missing_cols = [col for col in required_columns if col not in df.columns]
#         if missing_cols:
#             return HttpResponse(f"Error: Missing columns {missing_cols}")

#         # Drop rows with empty required fields
#         df = df.dropna(subset=required_columns)

#         count = 0
#         skipped = 0

#         for _, row in df.iterrows():
#             try:
#                 machine_details.objects.create(
#                     Identity=str(row['Identity']).strip(),
#                     Item=str(row['Item']).strip(),
#                     Description=str(row['Description']).strip()
#                 )
#                 count += 1
#             except Exception as e:
#                 # Likely a unique constraint or DB error
#                 skipped += 1
#                 continue

#         return HttpResponse(f"Success: {count} records imported, {skipped} skipped due to DB constraints")

#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")



class MachineListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get IDs of already allocated machines
        allocated_ids = MachineAllocation.objects.values_list('machine_id', flat=True)
        
        # Exclude allocated machines from the queryset
        unallocated_machines = machine_details.objects.exclude(id__in=allocated_ids)
        
        serializer = MachineSerializer(unallocated_machines, many=True)
        return Response(serializer.data)

# ------------------ Units ------------------
class UnitListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

# ------------------ Lines ------------------
class LineListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unit_id = request.GET.get("unit")
        if unit_id:
            lines = Line.objects.filter(unit_id=unit_id)
        else:
            lines = Line.objects.all()
        serializer = LineSerializer(lines, many=True)
        return Response(serializer.data)


from django.db.models import Max

class MachineAllocationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unit_id = request.GET.get("unit")
        line_id = request.GET.get("line")

        # Step 1: Get latest allocation id per machine
        latest_ids = MachineAllocation.objects.values('machine').annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # Step 2: Fetch only those latest allocations
        allocations = MachineAllocation.objects.filter(id__in=latest_ids)

        # Step 3: Apply filters if needed
        if unit_id:
            allocations = allocations.filter(unit=unit_id)
        if line_id:
            allocations = allocations.filter(line=line_id)

        serializer = MachineAllocationSerializer(allocations, many=True)
        return Response(serializer.data)

    def post(self, request):
        machines = request.data.get("machine_id")  # use `machine_id` consistently
        unit_id = request.data.get("unit")
        line_id = request.data.get("line")

        if not machines or not unit_id or not line_id:
            return Response({"error": "machine_id, unit and line are required"}, status=400)

        if not isinstance(machines, list):
            machines = [machines]

        created_allocations = []

        for m_id in machines:
            serializer = MachineAllocationSerializer(data={
                "machine_id": m_id,
                "unit": unit_id,
                "line": line_id
            })
            if serializer.is_valid():
                allocation = serializer.save()
                created_allocations.append(MachineAllocationSerializer(allocation).data)
            else:
                return Response(serializer.errors, status=400)

        return Response(created_allocations, status=201)

class MachineAllocationDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return MachineAllocation.objects.get(pk=pk)
        except MachineAllocation.DoesNotExist:
            return None

    def delete(self, request, pk):
        allocation = self.get_object(pk)
        if not allocation:
            return Response({"error": "Not found"}, status=404)
        allocation.delete()
        return Response({"message": "Deleted successfully"}, status=204)





# class EmployeeAPIView(APIView):
#     def get(self, request):
#         employees = Empwisesal.objects.using('main').filter(status='working').values('code', 'name', 'photo', 'dept')
        
#         staff_url = settings.STAFF_IMAGES_URL.rstrip('/')

#         data = []
#         for emp in employees:
#             photo_url = None
#             if emp.get('photo'):
#                 filename = emp['photo'].split('\\')[-1]
#                 photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"

#             data.append({
#                 "code": emp['code'],
#                 "name": emp['name'],
#                 "dept": emp['dept'],
#                 "photo": photo_url,
#             })

#         return Response(data)


# class EmployeeAPIView(APIView):
#     def get(self, request):
#         employees = Empwisesal.objects.using('main').filter(status='working').values('code', 'name', 'photo', 'dept')
        
#         staff_url = settings.STAFF_IMAGES_URL.rstrip('/')

#         data = []
#         for emp in employees:
#             photo_url = None
#             if emp.get('photo'):
#                 filename = emp['photo'].split('\\')[-1]
#                 photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"

#             data.append({
#                 "code": emp['code'],
#                 "name": emp['name'],
#                 "dept": emp['dept'],
#                 "photo": photo_url,
#             })

#         return Response(data)


class EmployeeAPIView(APIView):
    def get(self, request):

        # 1. Main employees
        employees = Empwisesal.objects.using('main').filter(
            status='working'
        ).values('code', 'name', 'photo', 'dept')

        staff_url = settings.STAFF_IMAGES_URL.rstrip('/')

        data = []

        # Empwisesal data
        for emp in employees:
            photo_url = None
            if emp.get('photo'):
                filename = emp['photo'].split('\\')[-1]
                photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"

            data.append({
                "code": emp['code'],
                "name": emp['name'],
                "dept": emp['dept'],   # already string in this table
                "photo": photo_url,
                "source": "empwisesal"
            })

        # 2. Contractor employees (Cont_employee + Mas_contractor)
        contractors = Cont_employee.objects.select_related('con_id').all()

        for emp in contractors:
            contractor_name = emp.con_id.name if emp.con_id else ""
            data.append({
                "code": emp.code,
                "name": f"{emp.name} ({contractor_name})",
                "dept": emp.con_id.name if emp.con_id else None,  # Mas_contractor name
                "photo": None,
                "source": "contract_employee"
            })

        return Response(data)


class Employee_and_staffAPIView(APIView):
    def get(self, request):
        employees = VueUser.objects.using('main').values('code', 'name', 'photo', 'wunit')
        
        staff_url = settings.STAFF_IMAGES_URL.rstrip('/')

        data = []
        for emp in employees:
            photo_url = None
            if emp.get('photo'):
                filename = emp['photo'].split('\\')[-1]
                photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"

            data.append({
                "code": emp['code'],
                "name": emp['name'],
                "dept": emp['wunit'],
                "photo": photo_url,
            })

        return Response(data)


class EmpAllocateAPIView(APIView):
    def post(self, request):
        emp_code = request.data.get("emp_code")
        machine_id = request.data.get("machine_id")
        unit = request.data.get("unit")
        line = request.data.get("line")
        status = request.data.get("status", 1)  # default online
        sequence = request.data.get("sequence")
        

        if not emp_code or not machine_id or not unit or not line:
            return Response(
                {"error": "emp_code, machine_id, unit and line are required"},
                status=400
            )

        # today = now().date()
        
        jobno = None
        top_bottom = None
        seq = None

        if sequence:

            parts = sequence.split("~")

            if len(parts) >= 3:
                jobno = parts[0]
                top_bottom = parts[1]
                seq = parts[2]

            else:
                seq = sequence
        from django.utils import timezone

        today = datetime.now().date()

        allocation = emp_allocate.objects.filter(
            emp_code=emp_code,
            machine_id=machine_id,
            unit=unit,
            line=line,
            date__date=today  # use correct field
        ).first() # get latest allocation if multiple exist

        
        if allocation: 
            allocation.status = status

            allocation.jobno = jobno
            allocation.top_bottom = top_bottom
            allocation.seq = seq
            allocation.save()
            return Response({"message": "Status and Sequence updated"})
        else:
            emp_allocate.objects.create(
                emp_code=emp_code,
                machine_id=machine_id,
                unit=unit,
                line=line,
                status=status,
                date=timezone.now(),
                jobno=jobno,
                top_bottom=top_bottom,
                seq=seq

            )
            return Response({"message": "Employee allocated"})





@api_view(['GET'])
def get_process_sequence(request):
    jobno = request.query_params.get('jobno')
    topbottom_des = request.query_params.get('topbottom_des')

    if not jobno or not topbottom_des:
        return Response({"error": "jobno and topbottom_des are required"}, status=400)

    queryset = VueProcessSequence.objects.using('demo').filter(jobno=jobno, topbottom_des=topbottom_des).order_by('sl')
    serializer = VueProcessSequenceSerializer(queryset, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def get_machine_employee(request, identity):
    print("identity", identity)

    try:
        unit = request.query_params.get('unit')
        line = request.query_params.get('line')
        jobno = request.query_params.get('jobno')
        topbottom_des = request.query_params.get('topbottom_des')
        bundleNo = request.query_params.get('bundleNo')

        print("unit==", unit, "line==", line)

        identity = identity.rstrip('/')
        # today = now().date()
        today = timezone.now().date()

        #  Step 1: Get line_id from Line table
        line_obj = Line.objects.filter(
            unit_id=unit,
            line_number=line
        ).first()

        if not line_obj:
            return Response({
                "error": "Line not found",
                "has_data": False,
                "processes": []
            }, status=404)

        #  Step 2: Match EVERYTHING in one query
        last_entry = emp_allocate.objects.select_related('machine').filter(
            machine__Identity__iexact=identity,
            date__date=today,
            unit=unit,
            line=line_obj.id   # FK match
        ).order_by('-id').first()

        #  If not match → Machine not found
        if not last_entry:
            return Response({
                "error": "Machine not found",
                "has_data": False,
                "processes": []
            }, status=404)

        machine = last_entry.machine

        # ---------------- EMPLOYEE ----------------
        emp_code = last_entry.emp_code
        emp_name = None
        photo_url = "https://www.example.com/default-profile.png"

        employee = Empwisesal.objects.using('main').filter(
            status='working',
            code=emp_code
        ).first()

        if employee:
            emp_name = employee.name
            if employee.photo:
                filename = employee.photo.split('\\')[-1]
                staff_url = settings.STAFF_IMAGES_URL.rstrip('/')
                photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"

        # ---------------- PROCESSES ----------------
        processes = []

        if jobno and topbottom_des:
            seq_match = list(
                qc_piece_final.objects.filter(
                    jobno=jobno,
                    product=topbottom_des,
                    bundle_no=bundleNo
                ).values_list('seq', flat=True)
            )

            queryset = VueProcessSequence.objects.using('demo').filter(
                jobno=jobno,
                topbottom_des=topbottom_des,
                mc=machine.mcgrp
            ).exclude(
                process_des__in=seq_match
            ).order_by('sl')

            processes = [
                {
                    "sl": p.sl,
                    "sl1": p.sl1,
                    "prsid": p.prsid,
                    "process_des": p.process_des,
                    "mc": p.mc
                }
                for p in queryset
            ]

        # ---------------- RESPONSE ----------------
        return Response({
            "machine_identity": machine.Identity,
            "machine_id": machine.id,
            "mcgrp": machine.mcgrp,
            "emp_code": emp_code,
            "employee_name": emp_name,
            "emp_photo": photo_url,
            "has_data": True,
            "processes": processes
        })

    except Exception as e:
        print("ERROR:", str(e))
        return Response({
            "error": "Internal server error",
            "has_data": False,
            "processes": []
        }, status=500)



from django.db.models import Max

class MachineTransferListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Step 1: Get latest allocation id per machine
        latest_ids = MachineAllocation.objects.values('machine').annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # Step 2: Fetch only those latest allocations
        allocations = MachineAllocation.objects.filter(id__in=latest_ids).select_related('machine', 'unit', 'line')

        serializer = MachineTrasnsferSerializer(allocations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MachineTrasnsferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Allows multiple allocations per day
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachineTransferDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(MachineAllocation, pk=pk)

    def get(self, request, pk):
        allocation = self.get_object(pk)
        serializer = MachineTrasnsferSerializer(allocation)
        return Response(serializer.data)

    def put(self, request, pk):
        allocation = self.get_object(pk)
        serializer = MachineTrasnsferSerializer(allocation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        allocation = self.get_object(pk)
        serializer = MachineTrasnsferSerializer(allocation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        allocation = self.get_object(pk)
        allocation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def machine_status_api(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            identity = data.get("machine_id")
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "GET":
        identity = request.GET.get("Identity")

    else:
        return JsonResponse({"error": "Only GET and POST allowed"}, status=405)

    if not identity:
        return JsonResponse({"error": "Identity is required"}, status=400)

    identity = identity.strip()

    try:
        machine = machine_details.objects.get(Identity__iexact=identity)
    except machine_details.DoesNotExist:
        return JsonResponse({"error": "Machine not found"}, status=404)

    # today = date.today()
    today = timezone.now().date()

    allocation = emp_allocate.objects.filter(
        machine=machine,
        date__date=today
    ).order_by('-id').first()

    if not allocation:
        return JsonResponse({
            "message": "Machine not allocated today"
        })

    if not allocation.status:
        return JsonResponse({
            "message": "Machine is offline"
        })

    return JsonResponse({
        "message": "Machine is online",
        "emp_code": allocation.emp_code,
        "unit": allocation.unit,
        "line": allocation.line
    })


@csrf_exempt
def needle_details_api(request):

    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        machine = data.get("machine_id")
        emp_code = data.get("emp_code")  # optional (frontend add pannala na empty)
        line = data.get("line")
        unit = data.get("unit")
        count = data.get("count", 0)
        needle_changed = data.get("needle_changed", 0)

    except Exception as e:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    #  validation
    if not machine:
        return JsonResponse({"error": "machine_id is required"}, status=400)

    # needle change illa na count = 0
    if not needle_changed:
        count = 0

    #  save
    Needle_change.objects.create(
        machine=machine,
        emp_code=emp_code if emp_code else "",
        line=line,
        unit=unit,
        n_count=count
    )

    return JsonResponse({
        "message": "Needle details saved successfully"
    })



def get_order_measurements(request):
    ordid = request.GET.get('ordid')
    topbottom = request.GET.get('TopBottom_des')
    siz = request.GET.get('siz')

    with connections['demo'].cursor() as cursor:
        cursor.execute(
            """
            EXEC usp_GetOrderMeasurements
                @ordid=%s,
                @TopBottom_des=%s,
                @siz=%s
            """,
            [ordid, topbottom, siz]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    result = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({
        "status": "success",
        "data": result
    })



@csrf_exempt
def save_measurement(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            jobno = data.get("jobNo")
            bundle_no = data.get("bundleNo")
            bundle_id = data.get("bundle_id")
            measurement_dtls = data.get("measurement_dtls")
            bf_ironing = data.get("bf_ironing")
            af_ironing = data.get("af_ironing")

            update_fields = {}

            # only update if NOT null
            if data.get("reading1") is not None:
                update_fields["reading1"] = data.get("reading1")

            if data.get("reading2") is not None:
                update_fields["reading2"] = data.get("reading2")

            if data.get("reading3") is not None:
                update_fields["reading3"] = data.get("reading3")

            if data.get("pcs_no_r1") is not None:
                update_fields["pcs_no_r1"] = data.get("pcs_no_r1")

            if data.get("pcs_no_r2") is not None:
                update_fields["pcs_no_r2"] = data.get("pcs_no_r2")

            if data.get("pcs_no_r3") is not None:
                update_fields["pcs_no_r3"] = data.get("pcs_no_r3")

            obj, created = cut_sample_data.objects.update_or_create(
                jobno=jobno,
                bundle_no=bundle_no,
                bundle_id=bundle_id,
                bf_ironing=bf_ironing,
                af_ironing=af_ironing,
                measurement_dtls=measurement_dtls,
                defaults={
                    "product": data.get("product"),
                    "color": data.get("colour"),
                    "size": data.get("size"),
                    "title": data.get("title"),
                    "measurement": data.get("measurement"),
                    **update_fields
                }
            )

            return JsonResponse({
                "status": "success",
                "created": created,
                "id": obj.id
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
        

@csrf_exempt
def final_save_measurement(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            obj = cut_sample_data_final.objects.create(
                jobno=data.get("jobNo"),
                bundle_no=data.get("bundleNo"),
                bundle_id=data.get("bundle_id"),
                product=data.get("product"),
                color=data.get("colour"),
                size=data.get("size"),

                bf_ironing=data.get("bf_ironing"),
                af_ironing=data.get("af_ironing"),

                # force save = 1 when button clicked
                force_save=True if data.get("force_save") else False
            )

            return JsonResponse({
                "status": "success",
                "id": obj.id
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })


@csrf_exempt
def check_ironing_status(request):
    if request.method == "GET":
        jobno = request.GET.get("jobno")
        bundle_no = request.GET.get("bundle_no")

        try:
            qs = cut_sample_data_final.objects.filter(
                jobno=jobno,
                bundle_no=bundle_no
            )

            #  No record
            if not qs.exists():
                return JsonResponse({
                    "status": "new",
                    "bf_ironing": False,
                    "af_ironing": False
                })

            # CHECK FULL HISTORY
            bf_done = qs.filter(bf_ironing=True).exists()
            af_done = qs.filter(af_ironing=True).exists()

            return JsonResponse({
                "status": "exists",
                "bf_ironing": bf_done,
                "af_ironing": af_done
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
        

@api_view(['GET'])
def get_existing_measurements(request):
    bundle_id = request.GET.get('bundle_id')
    product = request.GET.get('product')
    bf_ironing = request.GET.get('bf_ironing')
    af_ironing = request.GET.get('af_ironing')

    bf_ironing = True if bf_ironing in ["true", "1", True] else False
    af_ironing = True if af_ironing in ["true", "1", True] else False

    data = cut_sample_data.objects.filter(
        bundle_id=bundle_id,
        product=product,
        bf_ironing=bf_ironing,
        af_ironing=af_ironing
    )

    result = []
    for d in data:
        result.append({
            "title": d.title,
            "measurement_dtls": d.measurement_dtls,
            "measurement": d.measurement,
            "pcs_no_r1": d.pcs_no_r1,
            "pcs_no_r2": d.pcs_no_r2,
            "pcs_no_r3": d.pcs_no_r3,
            "reading1": d.reading1,
            "reading2": d.reading2,
            "reading3": d.reading3,
        })

    return Response({"data": result})

########## cutting measurement start ############

def get_cutting_measurements(request):
    sl = request.GET.get('sl')
    
    with connections['demo'].cursor() as cursor:
        cursor.execute(
            """
            EXEC sp_GetStickerDetails_BySL
                @sl=%s
                
            """,
            [sl]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    result = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({
        "status": "success",
        "data": result
    })

def get_allocate_report(request):

    unit_id = request.GET.get("unit")
    line_id = request.GET.get("line")

    s_data = emp_allocate.objects.filter(
        unit=unit_id,
        line=line_id,
        date__date=date.today()
    ).values(
        "emp_code",
        "seq",
        "jobno",
        "top_bottom"
    )

    data = []

    for row in s_data:
        emp = Empwisesal.objects.using('main').filter(
            code=row["emp_code"]
        ).first()

        data.append({
            "emp_code": row["emp_code"],
            "seq": row["seq"],
            "jobno": row["jobno"],
            "top_bottom": row["top_bottom"],
            "name": emp.name if emp else ""
        })

    return JsonResponse(data, safe=False)

def qc_reports(request):

    if request.method == "GET":
        data = qc_piece_data.objects.using('default').all().values()
        data_list = list(data)
        return JsonResponse(data_list, safe=False)


def machine_allocation_api(request):
    # 1. Get the date from the frontend, default to today's date if not provided
    # selected_date = request.GET.get('date', date.today().strftime("%Y-%m-%d %H:%M:%S"))
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = date.today()
    
    result = []

    allocations = MachineAllocation.objects.select_related(
        'machine',
        'unit',
        'line'
    )

    for allocation in allocations:
        # 2. Filter employees by BOTH the machine AND the selected date
        employees = list(
            emp_allocate.objects.filter(
                machine=allocation.machine,
                date__date=selected_date  # <--- THIS IS THE CRITICAL FIX
            ).values(
                'emp_code',
                'date',
                'unit',
                'machine_id',
                'line',
                'status',
                'seq',
                'jobno',
                'top_bottom'
            )
        )

        result.append({
            "machine": {
                "id": allocation.machine.id,
                "identity": allocation.machine.Identity,
                "item": allocation.machine.Item,
                "description": allocation.machine.Description,
                "mcgrp": allocation.machine.mcgrp
            },
            "allocation": {
                "unit_id": allocation.unit.id if allocation.unit else None,
                "unit_name": allocation.unit.name if allocation.unit else None,
                "line_id": allocation.line.id if allocation.line else None,
                "line_number": allocation.line.line_number if allocation.line else None,
                "machine_id": allocation.machine.id,
                "allocated_at": allocation.allocated_at.strftime("%Y-%m-%d %H:%M:%S") if allocation.allocated_at else None
            },
            "employees": employees # Now this ONLY contains today's operators
        })

    return JsonResponse({
        "status": True,
        "count": len(result),
        "data": result
    })