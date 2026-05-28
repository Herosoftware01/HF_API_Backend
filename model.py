# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HrLabourattendence(models.Model):
    unit = models.CharField(db_column='Unit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='DEPT', max_length=50)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=50)  # Field name made lowercase.
    subcat = models.CharField(db_column='SUBCAT', max_length=50)  # Field name made lowercase.
    shift_contract = models.CharField(db_column='Shift_Contract', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hostel = models.CharField(db_column='Hostel', max_length=10)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    empimage = models.CharField(db_column='EmpImage', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=7)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    intime = models.CharField(db_column='InTime', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    attendence_status = models.CharField(db_column='Attendence Status', max_length=14)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    photo = models.CharField(max_length=400, blank=True, null=True)
    status1 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hr_Labourattendence'
