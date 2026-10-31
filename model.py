# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Timecard(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='Month', max_length=8, blank=True, null=True)  # Field name made lowercase.
    doj = models.DateTimeField(db_column='DOJ', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=80, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=80, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    morningintime = models.CharField(db_column='MorningInTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    outtime = models.CharField(db_column='OutTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    hrs = models.IntegerField(db_column='Hrs')  # Field name made lowercase.
    otintime = models.CharField(db_column='OTInTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    otouttime = models.CharField(db_column='OTOutTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    otshift = models.DecimalField(db_column='OTShift', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='Des', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'timecard'
