# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    code = models.IntegerField()
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
class VueNewprod02(models.Model):
    t = models.CharField(max_length=2)
    recno = models.IntegerField()
    prdhour = models.IntegerField()
    recdt = models.DateTimeField()
    unit = models.CharField(max_length=50)
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scp = models.CharField(max_length=1, blank=True, null=True)
    empid = models.IntegerField()
    contract_des = models.CharField(max_length=50, blank=True, null=True)
    trstype = models.CharField(max_length=50)
    clr = models.CharField(max_length=50)
    siz = models.CharField(max_length=50)
    qty = models.IntegerField(blank=True, null=True)
    bdl = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'vue_NewProd02'
