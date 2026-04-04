from django.shortcuts import render
from django.db import connections
from rest_framework.decorators import api_view
import pandas as pd
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import QcAdminMistake,Unit,Line,roving_qc_mistake,qc_piece_final, MachineAllocation, machine_details, emp_allocate, Empwisesal, VueProcessSequence
from .serializers import QcAdminMistakeSerializer,UnitSerializer,MachineTrasnsferSerializer,MachineSerializer,LineSerializer, MachineAllocationSerializer, VueProcessSequenceSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from collections import defaultdict

from datetime import date
from django.utils.timezone import now
from django.conf import settings



# class QcAdminMistakeAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     # GET (List)
#     def get(self, request):
#         mistakes = QcAdminMistake.objects.all()
#         serializer = QcAdminMistakeSerializer(mistakes, many=True)
#         return Response(serializer.data)

#     # POST (Create)
#     def post(self, request):
#         serializer = QcAdminMistakeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class QcAdminMistakeDetailAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)

#     def get_object(self, pk):
#         try:
#             return QcAdminMistake.objects.get(pk=pk)
#         except QcAdminMistake.DoesNotExist:
#             return None

#     # GET single
#     def get(self, request, pk):
#         mistake = self.get_object(pk)
#         if not mistake:
#             return Response({"error": "Not found"}, status=404)

#         serializer = QcAdminMistakeSerializer(mistake)
#         return Response(serializer.data)

#     # PUT update
#     def put(self, request, pk):
#         mistake = self.get_object(pk)
#         if not mistake:
#             return Response({"error": "Not found"}, status=404)

#         serializer = QcAdminMistakeSerializer(mistake, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)

#     # PATCH (partial update)
#     def patch(self, request, pk):
#         mistake = self.get_object(pk)
#         if not mistake:
#             return Response({"error": "Not found"}, status=404)

#         serializer = QcAdminMistakeSerializer(
#             mistake,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)

#     # DELETE
#     def delete(self, request, pk):
#         mistake = self.get_object(pk)
#         if not mistake:
#             return Response({"error": "Not found"}, status=404)

#         mistake.delete()
#         return Response({"message": "Deleted successfully"}, status=204)
    



class QcAdminMistakeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mistakes = QcAdminMistake.objects.all()
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
        


# @api_view(['GET'])
# def get_bundle_data(request):
#     bundle_id = request.GET.get('bundle_id')

#     if not bundle_id:
#         return Response({"error": "bundle_id is required"}, status=400)

#     with connections['demo'].cursor() as cursor:
#         cursor.execute(
#             "EXEC dbo.GetOrderBundleList_ByBundID @BundID=%s",
#             [bundle_id]
#         )

#         columns = [col[0] for col in cursor.description]
#         results = [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]

#     return Response(results)



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

        checked_bundle_ids = set(
            qc_piece_final.objects.filter(
                bundle_id__in=bundle_ids_from_api
            ).values_list('bundle_id', flat=True)
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

# @api_view(['POST'])
# def save_piece(request):
#     data = request.data
#     bundle_no = data.get("bundle_no")
#     bundle_id = data.get("bundle_id")
#     jobno = data.get("jobno")
#     product = data.get("product")
#     color = data.get("color")
#     size = data.get("size")
#     unit = data.get("unit")
#     line = data.get("line")
#     qc_type = data.get("qc_type")
#     total_pieces = data.get("total_pieces")
#     piece_no = data.get("piece_no")
#     total_mistake = data.get("total_mistake")
#     mistake_percentage = data.get("mistake_percentage")
#     defects = data.get("defects", [])

#     for defect in defects:
#         qc_piece_data.objects.create(
#             bundle_no=bundle_no,
#             bundle_id=bundle_id,
#             jobno=jobno,
#             product=product,
#             color=color,
#             size=size,
#             unit=unit,
#             line=line,
#             qc_type=qc_type,
#             total_pieces=total_pieces,
#             piece_no=piece_no,
#             total_mistake=total_mistake,
#             mistake_percentage=mistake_percentage,
#             category=defect.get("category", ""),
#             mistake_name=defect.get("mistake_name", ""),
#             mistake_count=defect.get("mistake_count", 0)
#         )

#     return Response({"status": "success"})



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
    unit = data.get("unit")
    line = data.get("line")
    qc_type = data.get("qc_type")
    total_pieces = data.get("total_pieces")
    piece_no = data.get("piece_no")
    total_mistake = data.get("total_mistake")
    mistake_percentage = data.get("mistake_percentage")
    defects = data.get("defects", [])
    emp_id = data.get("operator")
    machine_id = data.get("machineId", "")
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
                operation=process,
                emb_id=emp_id,  # add if you have embroidery ID
                shade_var=shade_variation,
                num_sticker=number_sticker,
                remark=remarks
            )

    return Response({"status": "success"})



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
        user_id = request.data.get("userId", None)
        qc_type = request.data.get("qc_type")
        total_pieces = int(request.data.get("total_pieces", 0))
        checked_piece = int(request.data.get("checked_piece", 0))
        force_save = request.data.get("force_save", False)

        if not bundle_id:
            return Response({"error": "bundle_id is required"}, status=400)

        if total_pieces == 0:
            return Response({"error": "total_pieces cannot be 0"}, status=400)

        if checked_piece < total_pieces and not force_save:
            return Response(
                {
                    "error": "All pieces not checked. Enable force save to continue.",
                    "checked_piece": checked_piece,
                    "total_pieces": total_pieces,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        qc_piece_final.objects.create(
            bundle_no=bundle_no,
            bundle_id=bundle_id,
            jobno=jobno,
            product=product,
            color=color,
            size=size,
            line=line,
            unit=unit,
            qc_type=qc_type,
            total_pieces=total_pieces,
            checked_piece=checked_piece,
            force_save=force_save,
            user_id=user_id
        )

        return Response(
            {
                "message": "Saved successfully",
                "checked_piece": checked_piece,
                "total_pieces": total_pieces,
                "force_save": force_save,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(["GET"])
def get_last_bundle(request):
    from .models import qc_piece_data, qc_piece_final
    unit = request.GET.get("unit")
    line = request.GET.get("line")
    qc_type = request.GET.get("qc_type")

    last = qc_piece_data.objects.filter(unit=unit,line=line,qc_type=qc_type).order_by("-id").first()


    if not last:
        return Response({"error": "No bundle found"}, status=404)

    bundle_id = last.bundle_id
    
    line = last.line
    unit= last.unit
    piece= last.piece_no

    print("bundle_id", bundle_id)
    print("line", line)
    print("unit", unit)
    print("qc_type", qc_type)


    is_completed = qc_piece_final.objects.filter(bundle_id=bundle_id).exists()

    return Response({
        "bundle_id": bundle_id,
        "bundle_no": last.bundle_no,
        "jobno": last.jobno,
        "product": last.product,
        "color": last.color,
        "size": last.size,
        "total_pieces": last.total_pieces,
        "piece_no":piece,
        "checked_pieces": piece,
        "is_completed": is_completed   
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
    


def import_machine_details_from_excel(request):
    file_path = 'C:/Users/Murthy/Desktop/Full App/HF_API/machine.xlsx'

    try:
        # Read Excel, header is at row 4 (index 3)
        df = pd.read_excel(file_path, header=3)

        # Clean column names
        df.columns = df.columns.str.strip()

        required_columns = ['Identity', 'Item', 'Description']

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return HttpResponse(f"Error: Missing columns {missing_cols}")

        # Drop rows with empty required fields
        df = df.dropna(subset=required_columns)

        count = 0
        skipped = 0

        for _, row in df.iterrows():
            try:
                machine_details.objects.create(
                    Identity=str(row['Identity']).strip(),
                    Item=str(row['Item']).strip(),
                    Description=str(row['Description']).strip()
                )
                count += 1
            except Exception as e:
                # Likely a unique constraint or DB error
                skipped += 1
                continue

        return HttpResponse(f"Success: {count} records imported, {skipped} skipped due to DB constraints")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")



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




class EmployeeAPIView(APIView):
    def get(self, request):
        
        employees = Empwisesal.objects.using('main').filter(status='working').values('code', 'name', 'photo')

        data = [
            {
                "code": emp['code'],
                "name": emp['name'],
            }
            for emp in employees
        ]
      
        return Response(data)



class EmpAllocateAPIView(APIView):
    def post(self, request):
        emp_code = request.data.get("emp_code")
        machine_id = request.data.get("machine_id")
        unit = request.data.get("unit")
        line = request.data.get("line")
        status = request.data.get("status", 1)  # default online

        if not emp_code or not machine_id or not unit or not line:
            return Response(
                {"error": "emp_code, machine_id, unit and line are required"},
                status=400
            )

        today = now().date()

        # Check if employee already allocated today
        allocation = emp_allocate.objects.filter(
            emp_code=emp_code,
            machine_id=machine_id,
            unit=unit,
            line=line,
            date=today  # use correct field
        ).first()

        if allocation:
            allocation.status = status
            allocation.save()
            return Response({"message": "Status updated"})
        else:
            emp_allocate.objects.create(
                emp_code=emp_code,
                machine_id=machine_id,
                unit=unit,
                line=line,
                status=status,
                date=today
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



# @api_view(['GET'])
# def get_machine_employee(request, identity):
#     try:
#         identity = identity.rstrip('/')

#         machine = machine_details.objects.get(Identity__iexact=identity)

#         today = now().date()

#         last_entry = emp_allocate.objects.filter(
#             machine=machine,
#             date=today
#         ).order_by('-id').first()

#         # 🔥 default values
#         emp_code = None
#         emp_name = None
#         photo_url = "https://www.example.com/default-profile.png"

#         # ✅ only if allocation exists
#         if last_entry:
#             emp_code = last_entry.emp_code

#             employee = Empwisesal.objects.using('main').filter(
#                 status='working',
#                 code=emp_code
#             ).first()

#             if employee:
#                 emp_name = employee.name

#                 if employee.photo:
#                     filename = employee.photo.split('\\')[-1]
#                     staff_url = settings.STAFF_IMAGES_URL.rstrip('/')
#                     photo_url = f"http://127.0.0.1:8000/{staff_url}/{filename}"

#         return Response({
#             "machine_identity": machine.Identity,
#             "machine_id": machine.id,
#             "emp_code": emp_code,
#             "employee_name": emp_name,
#             "emp_photo": photo_url,
#             "has_data": True if last_entry else False
#         })

#     except machine_details.DoesNotExist:
#         return Response({
#             "error": "Machine not found",
#             "has_data": False
#         }, status=404)



@api_view(['GET'])
def get_machine_employee(request, identity):
    print("identity",identity)
    try:
        identity = identity.rstrip('/')
        machine = machine_details.objects.get(Identity__iexact=identity)

        today = now().date()
        last_entry = emp_allocate.objects.filter(machine=machine, date=today).order_by('-id').first()

        emp_code = None
        emp_name = None
        photo_url = "https://www.example.com/default-profile.png"

        if last_entry:
            emp_code = last_entry.emp_code
            employee = Empwisesal.objects.using('main').filter(status='working', code=emp_code).first()
            if employee:
                emp_name = employee.name
                if employee.photo:
                    filename = employee.photo.split('\\')[-1]
                    staff_url = settings.STAFF_IMAGES_URL.rstrip('/')
                    photo_url = f"http://127.0.0.1:8000/{staff_url}/{filename}"

        # Fetch matching processes from VueProcessSequence
        jobno = request.query_params.get('jobno')
        topbottom_des = request.query_params.get('topbottom_des')

        processes = []
        if jobno and topbottom_des:
            queryset = VueProcessSequence.objects.using('demo').filter(
                jobno=jobno,
                topbottom_des=topbottom_des,
                mc=machine.mcgrp
            ).order_by('sl')
            processes = [
                {
                    "sl": p.sl,
                    "sl1": p.sl1,
                    "prsid": p.prsid,
                    "process_des": p.process_des,
                    "mc": p.mc
                } for p in queryset
            ]

        return Response({
            "machine_identity": machine.Identity,
            "machine_id": machine.id,
            "mcgrp": machine.mcgrp,
            "emp_code": emp_code,
            "employee_name": emp_name,
            "emp_photo": photo_url,
            "has_data": True if last_entry else False,
            "processes": processes
        })

    except machine_details.DoesNotExist:
        return Response({
            "error": "Machine not found",
            "has_data": False,
            "processes": []
        }, status=404)


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