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
    path("get_stock_data/", views.get_stock_data_python, name="get_stock_data"),
    path("get_stock_summary/", views.get_stock_summary_python, name="get_stock_summary"),
    path('api/bundle-detail/', views.bundle_detail_api, name='bundle-detail'),
    path("api/bundle/transfer/",views.transfer_bundles,name="transfer_bundles",),
    path('api/bundle/<str:bundid>/', views.get_bundle_detail, name='get_bundle_detail'),
    path('order_details_api/', views.order_details_api, name='order_details_api'),

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
    path('get-dependency-pc/',views.get_dependency_pc,name='get_dependency_pc'),
    path('elastic/orders/',
         views.elastic_order_list),

    path('elastic/topbottom/',views.elastic_topbottom_list),

    path('elastic/colours/', views.elastic_colour_list),

    path('elastic/sizes/',
         views.elastic_size_details),

    path('elastic/cons/save/',
         views.save_elastic_cons),

    path('elastic/save/',
         views.save_elastic_cutting_entry),

    path('elastic/previous/',
         views.elastic_previous_cutting),

    path('elastic/description/',
         views.elastic_description),
    path('elastic/accessory_qty/', views.elastic_accessory_qty),
    path('api/job-nos/', views.get_job_nos, name='get_job_nos'),
    path('api/top-bottoms/', views.get_top_bottoms, name='get_top_bottoms'),
    path('api/elastic/colors/', views.get_colors, name='get_colors'),
    path('api/elastic-units/', views.get_elastic_units, name='get_elastic_units'),
    path('api/bundle-details/', views.get_bundle_details, name='get_bundle_details'),
    path('api/delivery/save/', views.save_elastic_delivery, name='save_elastic_delivery'),
    path('api/delivery/print/', views.get_elastic_delivery_print, name='get_elastic_delivery_print'),
    path('api/winding/units/', views.get_winding_units, name='winding_units'),
    path('api/winding/jobs/', views.get_winding_jobs, name='winding_jobs'),
    path('api/winding/topbottom/', views.get_winding_topbottom, name='winding_topbottom'),
    path('api/winding/colours/', views.get_winding_colours, name='winding_colours'),
    path('api/winding/lots/', views.get_winding_lots, name='winding_lots'),
    path('api/winding/folding-parts/', views.get_winding_folding_parts, name='winding_folding_parts'),
    path('api/winding/sizes/', views.get_winding_cutting_sizes, name='winding_cutting_sizes'),
    path('api/winding/summary/', views.get_winding_summary_details, name='winding_summary'),
    path('api/winding/available-rolls/', views.get_available_rolls, name='winding_available_rolls'),
    path('api/winding/folding-rolls/', views.get_rope_cutting_available_rolls, name='rope_cutting_available_rolls'),
    path('api/winding/rope-cutting/save/', views.save_rope_cutting_entry, name='save_rope_cutting_entry'),
    path('api/winding/save/', views.save_winding_entry, name='save_winding_entry'),
]  
