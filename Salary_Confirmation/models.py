from django.db import models

class MasProcess(models.Model):
    process_id = models.IntegerField(db_column='Process_ID', primary_key=True)
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)
    mc = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Mas_Process'


class Salcon_Operation_Category(models.Model):
    id = models.AutoField(primary_key=True)
    slno = models.ForeignKey('Salcon_Employee_Details', on_delete=models.PROTECT)
    process_id = models.ForeignKey(MasProcess, on_delete=models.PROTECT)
    emp_id = models.IntegerField()
    oper_category = models.CharField(max_length=20)
    sam_time = models.TimeField()
    cycle_time1 = models.TimeField()
    cycle_time2 = models.TimeField()
    cycle_time3 = models.TimeField()
    cycle_time4 = models.TimeField()
    cycle_time5 = models.TimeField()
    avg_with_alw = models.TimeField()
    given = models.IntegerField()
    achved = models.IntegerField()    
    efficiency = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_type} - {self.operations}"

class Salcon_Employee_Details(models.Model):
    id = models.AutoField(primary_key=True)
    slno = models.IntegerField(unique=True)
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=50)
    prev_salary = models.DecimalField(max_digits=10, decimal_places=2)
    prev_company = models.CharField(max_length=50)
    prev_category = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    current_category = models.CharField(max_length=50)
    current_grade = models.CharField(max_length=50)
    evaluation_date = models.DateField()
    unit = models.CharField(max_length=30)
    salary_recommendation = models.DecimalField(max_digits=10, decimal_places=2)
    salary_type = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.emp_name} - {self.experience}"

class Salcon_Approval(models.Model):
    id = models.AutoField(primary_key=True)
    slno = models.ForeignKey('Salcon_Employee_Details', on_delete=models.PROTECT)
    emp_id = models.IntegerField()
    salary_approved = models.IntegerField()
    approve_fm = models.IntegerField()
    approve_fm_date = models.DateTimeField()
    approve_hr = models.IntegerField()
    approve_hr_date = models.DateTimeField()
    approve_md = models.IntegerField()
    approve_md_date = models.DateTimeField()

