from django.urls import path
from .views import *
from .import views
from django.conf.urls.static import static
from django.conf import settings

from .views import QcAdminMistakeAPIView, QcAdminMistakeDetailAPIView

urlpatterns = [
    path('qcadmin_mistakes/', QcAdminMistakeAPIView.as_view(), name='qcadmin_mistakes'),
    path('qcadmin_mistakes/<int:pk>/', QcAdminMistakeDetailAPIView.as_view(), name='qcadmin_mistake_detail'),
    path('lines/', LineAPIView.as_view()),
    path('lines/<int:pk>/', LineAPIView.as_view()),
    path('get_bundle_data/', views.get_bundle_data, name='get_bundle_data'),
    path('save_piece/', views.save_piece, name='save_piece'),
    path("save_final_piece/", views.save_final_piece),
    path("check_bundle_entry_status/", views.check_bundle_entry_status),
    path("get_last_bundle/", views.get_last_bundle),
    # path("import_machine_details_from_excel/", views.import_machine_details_from_excel),
    path('machine-status/', machine_status_api),
    path('api/needle_details/', needle_details_api),

    path('api/machines/', MachineListAPIView.as_view(), name='machines-list'),
    path('api/units/', UnitListAPIView.as_view(), name='units-list'),
    path('api/lines/', LineListAPIView.as_view(), name='lines-list'),
    path('api/allocations/', MachineAllocationAPIView.as_view(), name='allocations-list-create'),
    path('api/allocations/<int:pk>/', MachineAllocationDetailAPIView.as_view(), name='allocations-detail'),
    path('api/employees/', EmployeeAPIView.as_view(), name='employees'),
    path('api/employees_and_staff/', Employee_and_staffAPIView.as_view(), name='employees_and_staff'),

    # Allocate employee to machine
    path('api/emp_allocate/', EmpAllocateAPIView.as_view(), name='emp-allocate'),
    path('api/process-sequence/', views.get_process_sequence, name='process-sequence'),
    path('api/machine/<path:identity>/', views.get_machine_employee),


    path('api/machine-transfer/', MachineTransferListCreateAPIView.as_view(), name='machine-transfer-list-create'),
    path('api/machine-transfer/<int:pk>/', MachineTransferDetailAPIView.as_view(), name='machine-transfer-detail'),

    path('get_order_measurements',views.get_order_measurements,name='get_order_measurements'),
    path("save-measurement/", views.save_measurement),
    path("final-save-measurement/", views.final_save_measurement),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STAFF_IMAGES_URL, document_root=settings.STAFF_IMAGES_ROOT)
