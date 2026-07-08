from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GridSettingViewSet,token_api,reports_list_api, export_report_api

from . import views

from .views import GridSettingViewSet, get_pdf,token_api,reports_list_api, export_report_api, upload_pdf, list_pdfs
from.views import diwasg_list, diwasg_detail
from . import views
router = DefaultRouter()
router.register(r'grid-settings', GridSettingViewSet, basename='grid-settings')
from .views import tasks_create, tasks_list, tasks_single, tasks_update, tasks_delete, upload_image, get_image, gantt_list, gantt_detail, block_list, block_detail

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', token_api),
    path('reports/', reports_list_api),
    path("export/", export_report_api),

    path('mail/add/', views.add_mail, name='add_mail'),
    path('mail/get_mails/', views.get_mails, name='add_mail'),
    path('mail/update/<int:pk>/', views.update_mail, name='update_mail'),
    path('mail/delete/<int:pk>/', views.delete_mail, name='delete_mail'),
    path("diwasg/", diwasg_list),
    path("diwasg/<str:id>/", diwasg_detail),
    path("upload-pdf/", upload_pdf),
    path("get-pdf/<str:file_name>/", get_pdf),
    path("list-pdfs/", list_pdfs), 

    path('mail/add/', views.add_mail, name='add_mail'),
    path('mail/get_mails/', views.get_mails, name='get_mails'),
    path('mail/get_mailss/', views.get_mailss, name='get_mailss'),
    path('mail/update/<int:pk>/', views.update_mail, name='update_mail'),
    path('mail/delete/<int:pk>/', views.delete_mail, name='delete_mail'),

    path('task_create/',tasks_create), # post Method (New task update)
    path('task_list/',tasks_list),  # Get all task
    path('task_single/<int:id>/',tasks_single), # Get single task
    path('task_update/<int:id>/',tasks_update), # put method (update tasks)
    path('task_delete/<int:id>/',tasks_delete), # delete method (delete the tasks)

    path('upload-image/', upload_image),
    path("image/<str:filename>/", get_image),    
    path('gantt/', gantt_list),
    path('gantt/<int:id>/', gantt_detail),
    path('blocks/', block_list),
    path('blocks/<int:id>/<str:name>/', block_detail),
    path('stock_dtls/', views.load_tmpwrk),
    path("upload/", views.upload_to_drive, name="upload_file"),
    path("uploadss/", views.service_to_drive, name="upload_files"),
    path('fashionr_results/', views.fashionr_results, name='fashionr_results'),
]
