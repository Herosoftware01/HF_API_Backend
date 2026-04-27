from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import GridSetting
from .serializers import GridSettingSerializer
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
    """
    GET /api/token/
    """
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
    """
    GET /api/reports/
    """
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
    """
    POST /api/export/
    Body:
    {
        "report_id": "uuid",
        "server_path": "",
        "export_type": "PDF",
        "filter_parameters": "{'ReportParameter1':['true'],'StartDate':['1/1/2003'],'SalesOrderNumber':['SO50750','SO50751']}"
    }

    Ex:{
            "report_id": "b24c7b18-1a40-4716-b194-876d6b26e845",
            "server_path": "",
            "export_type": "PDF",
            "filter_parameters": "{'SalesOrderNumber':['SO50751']}"
        }
    """

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