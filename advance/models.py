from django.db import models


class IncdebUsers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    screen_per = models.CharField(db_column='Screen_per', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    app_n = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IncDeb_Users'

class Adreq(models.Model):
    entryno = models.IntegerField(db_column='Entryno')  # Field name made lowercase.
    dt = models.DateTimeField()
    empid = models.IntegerField(db_column='Empid')  # Field name made lowercase.
    amt = models.DecimalField(db_column='Amt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    remarks = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')
    smon = models.CharField(max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    syear = models.IntegerField(blank=True, null=True)
    elig = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sl = models.AutoField(db_column='SL',primary_key=True)
    status = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status_dt = models.DateTimeField(blank=True, null=True)
    comments = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mail_sent = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ladvreq'


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


    
class RptCut002(models.Model):
    sl = models.AutoField(primary_key=True)
    dept = models.CharField(db_column='Dept', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    trn = models.IntegerField(db_column='Trn', blank=True, null=True)  # Field name made lowercase.
    trn1 = models.CharField(db_column='Trn1', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(blank=True, null=True)
    nos = models.IntegerField(db_column='Nos', blank=True, null=True)  # Field name made lowercase.
    pc = models.IntegerField(db_column='Pc', blank=True, null=True)  # Field name made lowercase.
    wgt = models.DecimalField(db_column='Wgt', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    mtr = models.DecimalField(db_column='Mtr', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rpt_Cut002'

class HrWrkdtlsnew(models.Model):
    monthlysalary = models.CharField(db_column='MonthlySalary', max_length=1, blank=True, null=True)  # Field name made lowercase.
    esino = models.CharField(max_length=50, blank=True, null=True)
    pfno = models.CharField(max_length=50, blank=True, null=True)
    photo_url = models.CharField(max_length=65, blank=True, null=True)
    status1 = models.CharField(db_column='Status1', max_length=13, blank=True, null=True)  # Field name made lowercase.
    dept_category_unit_pcategory = models.CharField(db_column='Dept_Category_Unit_Pcategory', max_length=214, blank=True, null=True)  # Field name made lowercase.
    con_sc_astaff = models.CharField(max_length=6, blank=True, null=True)
    picpen = models.CharField(db_column='Picpen', max_length=9)  # Field name made lowercase.
    tasstaff = models.CharField(max_length=3, blank=True, null=True)
    photo = models.CharField(max_length=400, blank=True, null=True)
    mcategory = models.CharField(max_length=50, blank=True, null=True)
    con_name_mcate = models.CharField(db_column='Con_name_mcate', max_length=151, blank=True, null=True)  # Field name made lowercase.
    empty = models.CharField(db_column='Empty', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prab = models.CharField(max_length=7)
    filnam = models.CharField(db_column='FILNAM', max_length=44, blank=True, null=True)  # Field name made lowercase.
    emppic = models.CharField(db_column='Emppic', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    prate = models.IntegerField(db_column='Prate')  # Field name made lowercase.
    trn = models.CharField(db_column='Trn', max_length=1)  # Field name made lowercase.
    sl = models.IntegerField(blank=True, null=True)
    sc = models.CharField(max_length=2)
    dept = models.CharField(max_length=70, blank=True, null=True)
    prs = models.CharField(db_column='PRS', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField(primary_key=True)
    category = models.CharField(db_column='Category', max_length=70, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    intercom = models.CharField(max_length=50, blank=True, null=True)
    hostel = models.CharField(db_column='Hostel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    roomdtls = models.CharField(db_column='Roomdtls', max_length=50, blank=True, null=True)  # Field name made lowercase.
    orissa = models.CharField(max_length=3, blank=True, null=True)
    bank = models.CharField(db_column='Bank', max_length=200, blank=True, null=True)  # Field name made lowercase.
    accountdetails = models.CharField(db_column='Accountdetails', max_length=200, blank=True, null=True)  # Field name made lowercase.
    grp2 = models.IntegerField(blank=True, null=True)
    qualification = models.CharField(db_column='Qualification', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pftype = models.CharField(max_length=10, blank=True, null=True)
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    attach = models.CharField(max_length=1550, blank=True, null=True)
    contract_des = models.CharField(max_length=50)
    curwrkunit = models.CharField(db_column='CurWrkUnit', max_length=70, blank=True, null=True)  # Field name made lowercase.
    inch = models.CharField(max_length=3)
    sex = models.CharField(max_length=1, blank=True, null=True)
    nattgrp = models.CharField(max_length=20, blank=True, null=True)
    salary = models.DecimalField(db_column='Salary', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inspection = models.CharField(db_column='INSPECTION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empprs = models.CharField(db_column='Empprs', max_length=80)  # Field name made lowercase.
    skilled = models.CharField(max_length=10)
    aempwatch = models.CharField(max_length=3)
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    tc = models.CharField(max_length=20, blank=True, null=True)
    createdby = models.DateTimeField(blank=True, null=True)
    modifiedby = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HR_WrkDtlsNew'