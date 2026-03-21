from django.shortcuts import render
from django.db import connection
from django.db import connections
from rest_framework.decorators import api_view



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import QcAdminMistake,Line,qc_piece_final
from .serializers import QcAdminMistakeSerializer,LineSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from collections import defaultdict



class QcAdminMistakeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET (List)
    def get(self, request):
        mistakes = QcAdminMistake.objects.all()
        serializer = QcAdminMistakeSerializer(mistakes, many=True)
        return Response(serializer.data)

    # POST (Create)
    def post(self, request):
        serializer = QcAdminMistakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QcAdminMistakeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return QcAdminMistake.objects.get(pk=pk)
        except QcAdminMistake.DoesNotExist:
            return None

    # GET single
    def get(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(mistake)
        return Response(serializer.data)

    # PUT update
    def put(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(mistake, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # PATCH (partial update)
    def patch(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        serializer = QcAdminMistakeSerializer(
            mistake,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE
    def delete(self, request, pk):
        mistake = self.get_object(pk)
        if not mistake:
            return Response({"error": "Not found"}, status=404)

        mistake.delete()
        return Response({"message": "Deleted successfully"}, status=204)
    

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
    bundle_id = request.GET.get('bundle_id')

    if not bundle_id:
        return Response({"error": "bundle_id is required"}, status=400)

    with connections['demo'].cursor() as cursor:
        cursor.execute(
            "EXEC dbo.GetOrderBundleList_ByBundID @BundID=%s",
            [bundle_id]
        )

        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return Response(results)
        


from .models import qc_piece_data

@api_view(['POST'])
def save_piece(request):
    data = request.data
    bundle_no = data.get("bundle_no")
    bundle_id = data.get("bundle_id")
    jobno = data.get("jobno")
    product = data.get("product")
    color = data.get("color")
    size = data.get("size")
    unit = data.get("unit")
    line = data.get("line")
    total_pieces = data.get("total_pieces")
    piece_no = data.get("piece_no")
    total_mistake = data.get("total_mistake")
    mistake_percentage = data.get("mistake_percentage")
    defects = data.get("defects", [])

    for defect in defects:
        qc_piece_data.objects.create(
            bundle_no=bundle_no,
            bundle_id=bundle_id,
            jobno=jobno,
            product=product,
            color=color,
            size=size,
            unit=unit,
            line=line,
            total_pieces=total_pieces,
            piece_no=piece_no,
            total_mistake=total_mistake,
            mistake_percentage=mistake_percentage,
            category=defect.get("category", ""),
            mistake_name=defect.get("mistake_name", ""),
            mistake_count=defect.get("mistake_count", 0)
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
            total_pieces=total_pieces,
            checked_piece=checked_piece,
            force_save=force_save,
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

    last = qc_piece_data.objects.filter(unit=unit,line=line).order_by("-id").first()


    if not last:
        return Response({"error": "No bundle found"}, status=404)

    bundle_id = last.bundle_id
    line = last.line
    unit= last.unit
    piece= last.piece_no

    print("unit",unit)
    print("line",line)
    print("bundle_id",bundle_id)
    print("piece",piece)

    # ✅ count checked pieces
    # checked_count = qc_piece_data.objects.filter(bundle_id=bundle_id).count()

    # ✅ check if completed
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


# @api_view(["GET"])
# def get_last_bundle(request):
#     from .models import qc_piece_data, qc_piece_final

#     unit = request.GET.get("unit")
#     line = request.GET.get("line")

#     if not unit or not line:
#         return Response({"error": "unit and line required"}, status=400)

#     #  filter by unit + line
#     last = qc_piece_data.objects.filter(unit=unit, line=line).order_by("-id").first()

#     if not last:
#         return Response({"error": "No bundle found"}, status=404)

#     bundle_id = last.bundle_id

#     # check completion
#     is_completed = qc_piece_final.objects.filter(
#         bundle_id=bundle_id,
#         unit=unit,
#         line=line
#     ).exists()

#     return Response({
#         "bundle_id": bundle_id,
#         "bundle_no": last.bundle_no,
#         "jobno": last.jobno,
#         "product": last.product,
#         "color": last.color,
#         "size": last.size,
#         "total_pieces": last.total_pieces,
#         "piece_no":last.piece_no,
#         "checked_pieces": last.piece_no,
#         "is_completed": is_completed
#     })

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

