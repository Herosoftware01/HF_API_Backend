from django.urls import path
from .views import *
from .import views


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
]