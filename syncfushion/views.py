from django.shortcuts import render
# from django.db import connections
from rest_framework import status
# from django.http import JsonResponse
from rest_framework import viewsets
from .models import GridSetting,TrsMaildtls
from .serializers import GridSettingSerializer,TrsMaildtlsSerializer
from rest_framework.permissions import IsAuthenticated  # optional

class GridSettingViewSet(viewsets.ModelViewSet):
    queryset = GridSetting.objects.all()
    serializer_class = GridSettingSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .services.boldreports_service import (
    generate_auth_token,
    get_reports_list,
    export_report
)


@api_view(['GET'])
def token_api(request):
   
    try:
        reports = generate_auth_token()
        return Response({
            "success": True,
            "data": reports
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)

@api_view(['GET'])
def reports_list_api(request):
    try:
        reports = get_reports_list()
        return Response({
            "success": True,
            "data": reports
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


@api_view(["POST"])
def export_report_api(request):
   
    try:
        data = request.data

        report_id = data.get("report_id")
        export_type = data.get("export_type", "PDF")
        server_path = data.get("server_path", "/")
        filter_parameters = data.get("filter_parameters", "")

        if not report_id:
            return Response(
                {"success": False, "error": "report_id is required"},
                status=400,
            )

        result = export_report(
            report_id=report_id,
            server_path=server_path,
            export_type=export_type,
            filter_parameters=filter_parameters,
        )

        return Response({
            "success": True,
            "data": result
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
    


#############################################

@api_view(['GET'])
def get_mails(request):
    mails = TrsMaildtls.objects.all()
    serializer = TrsMaildtlsSerializer(mails, many=True)
    return Response(serializer.data)

# ADD API
@api_view(['POST'])
def add_mail(request):
    serializer = TrsMaildtlsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Mail details added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE API
@api_view(['PUT'])
def update_mail(request, pk):
    try:
        mail = TrsMaildtls.objects.get(pk=pk)
    except TrsMaildtls.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TrsMaildtlsSerializer(mail, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Mail details updated successfully",
                "data": serializer.data
            }
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE API
@api_view(['DELETE'])
def delete_mail(request, pk):
    try:
        mail = TrsMaildtls.objects.get(pk=pk)
    except TrsMaildtls.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    mail.delete()

    return Response(
        {"message": "Mail details deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )


