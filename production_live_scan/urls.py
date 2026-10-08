from django.urls import path
from . import views
from .views import UnitInputAPIView,EndUnitDataAPIView,EndUnitInputAPIView,GetUnitDataAPIView,GetUnitAssemply,GetUnitDataAPIViewsss,GetJobsView,GetColorsView,GetSizesView, GetTbNamesView, GetSequencesView, SaveAssemblySelectionView


from .views import (
    UserListView,
    UnitListView,
    UserUnitPermissionView,
    UserUnitPermissionListView
)

urlpatterns = [
    
    path('live_scan_data/', views.live_scan_data, name='live_scan_data'),
    path('end-live_scan_data/', views.end_live_scan_data, name='end-live_scan_data'),
    path('assembly_emp/', views.assembly_emp, name='assembly_emp'),
    path('save-assembly/', views.save_assembly, name='save-assembly'),
    path('save-bundles/', UnitInputAPIView.as_view(), name='save-bundles'),
    path('end-save-bundles/', EndUnitInputAPIView.as_view(), name='end-save-bundles'),
    path('get_input_scan_bundles/', GetUnitDataAPIView.as_view(), name='get_input_scan_bundles'),
    path('bundle-last-process/', views.get_bundle_last_process, name='bundle_last_process'),
    path('get_input_scan_bundlessss/', GetUnitDataAPIViewsss.as_view(), name='get_input_scan_bundlessss'),
    path('get_end_scan_bundles/', EndUnitDataAPIView.as_view(), name='get_end_scan_bundles'),
    path('get_assembly_bundles/', GetUnitAssemply.as_view(), name='get_assembly_bundles'),
    path("process-details/",views.get_process_details,name="get_process_details"),
    path("preporatory-entry-details/",views.preporatory_entry_details,name="preporatory_entry_details"),
    path("job-top-bottom/", views.get_job_top_bottom, name="get_job_top_bottom"),
    path("save_process_dependency/",views.save_process_dependency,name="save_process_dependency"),
    path("verify_process_dependency/", views.verify_process_dependency, name="verify_process_dependency"),
    path("delete_process_dependency/", views.delete_process_dependency, name="delete_process_dependency"),
    path("save_preporatory_dependency/", views.save_preporatory_dependency, name="save_preporatory_dependency"),
    path("delete_preporatory_dependency/", views.delete_preporatory_dependency, name="delete_preporatory_dependency"),

    path(
        "users/",
        UserListView.as_view(),
        name="user-list"
    ),

    path(
        "units/",
        UnitListView.as_view(),
        name="unit-list"
    ),

    path(
        "user-unit-permission/",
        UserUnitPermissionView.as_view(),
        name="user-unit-permission"
    ),
    path('user-unit-permission-list/', UserUnitPermissionListView.as_view(), name='user-unit-permission-list'),
    path('api/units/', views.get_units, name='get_units'),
    path('api/jobnos-unit/', views.get_jobnos_by_unit, name='get_jobnos_by_unit'),
    path('api/topbottom-unit-job/', views.get_topbottom_by_unit_job, name='get_topbottom_by_unit_job'),
    path('api/table-data/', views.get_table_data, name='get_table_data'),
    path('api/save-table-entry/', views.save_table_entry, name='save_table_entry'),
    
    path('api/jobs/', GetJobsView.as_view(), name='get-jobs'),
    path('api/tb-names/', GetTbNamesView.as_view(), name='get-tb-names'),
    path('api/colors/', GetColorsView.as_view(), name='get-colors'),
    path('api/sizes/', GetSizesView.as_view(), name='get-sizes'),
    path('api/sequences/', GetSequencesView.as_view(), name='get-sequences'),
    path('api/assembly/save/', SaveAssemblySelectionView.as_view(), name='save-assembly'),
]  
