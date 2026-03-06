from django.shortcuts import render



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import QcAdminMistake,Line
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