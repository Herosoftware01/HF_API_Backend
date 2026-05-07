from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GridSettingViewSet, get_pdf,token_api,reports_list_api, export_report_api, upload_pdf, list_pdfs
from.views import diwasg_list, diwasg_detail
router = DefaultRouter()
router.register(r'grid-settings', GridSettingViewSet, basename='grid-settings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', token_api),
    path('reports/', reports_list_api),
    path("export/", export_report_api),
    path("diwasg/", diwasg_list),
    path("diwasg/<str:id>/", diwasg_detail),
    path("upload-pdf/", upload_pdf),
    path("get-pdf/<str:file_name>/", get_pdf),
    path("list-pdfs/", list_pdfs), 
]
