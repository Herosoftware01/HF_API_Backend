from django.urls import path
from . import views

urlpatterns = [

    #Employee Module

    path('emp_shift_summary/', views.get_emp_shift_summary, name='get_emp_shift_summary'),
    path('attendance/', views.attendance, name='attendance'),
    path('emp_overall/', views.emp_overall, name="emp_overall"),
    path('absent_details/', views.abs_details, name='absent_details'),
    path('present_details/', views.present_details, name='present_details'),
    path('resign_report/', views.resign_report, name='resign_report'),
    path('resign_join_report/', views.resign_join_report, name='resign_join_report'),
    path('emp_payslip/', views.emp_payslip, name='emp_salary_details'),
    path('emp_timecard/', views.emp_timecard, name='emp_timecard'),
    path('emp_monthly_att/', views.get_employee_attendance, name='get_employee_attendance'),
    path('hr_resignation_details/', views.hr_resignation_details, name='hr_resignation_details'),
    path('join_data/', views.join_data, name='join_data'),
    path('emp_one/', views.oneday_api, name='oneday_api'), 
    path('security_list/', views.security_list, name='security_list'),
    path('work_report/', views.workforce_trends_api, name='workforce_trends_api'),
    path('work_report1/', views.workforce_unit_trends_api, name='workforce_unit_trends_api'), 
    path('empleave/', views.empatlev, name='empleave'), 

    #Staff Module

    path('staff_overview/', views.staff_overview, name='staff_overview'),
    path('staff_pre/', views.staff_pre, name='staff_pre'),
    path('staff_abe/', views.staff_abe, name='staff_abe'),
    path('staff_one/', views.staff_report_api, name='staff_report_api'), 
    path('absent_list/', views.Absent_list, name='Absent_list'),
    path('staff_absent_list/', views.Staff_Absent_list, name='Staff_Absent_list'),
    path('staff_latemins/', views.Staff_Month_Latemins, name='Staff_Month_Latemins'),
    path('staff_ot_amount/', views.Staff_OT_Amount, name='Staff_OT_Amount'),
]
