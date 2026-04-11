from django.db import models

class VueHoldwage(models.Model):
    rownum = models.BigIntegerField(db_column='RowNum', primary_key=True)   # Field name made lowercase.
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    period = models.CharField(db_column='Period', max_length=50)  # Field name made lowercase.
    holdamount = models.DecimalField(db_column='HoldAmount', max_digits=18, decimal_places=2)  # Field name made lowercase.
    chold = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tot = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_holdwage'

class Holdwagepaid(models.Model):
    entry_no = models.IntegerField(primary_key=True)
    dt = models.DateField()
    aadhar_no = models.CharField(max_length=20)
    code = models.IntegerField()
    emp_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    t_period = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    paid_amt = models.DecimalField(max_digits=18, decimal_places=0)
    remarks = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trs_holdwagepaid'




class Empwisesal(models.Model):
    dept = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    salary = models.DecimalField(
        db_column='Salary',
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    ) # Field name made lowercase.
    sl = models.IntegerField(blank=True, null=True)
    wrkunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    photo = models.CharField(max_length=400, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monthlysalary = models.CharField(db_column='MonthlySalary', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    
    designation = models.CharField(
        db_column='mcategory',
        max_length=50,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
  
   
    class Meta:
        managed = False
        db_table = 'Empwisesal'


class Employeeworking(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    workunit = models.CharField(db_column='WorkUnit', max_length=70, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=70, blank=True, null=True)
    type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'EmployeeWorking'     



