# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewActshift(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='Unitname', max_length=50)  # Field name made lowercase.
    id = models.IntegerField()
    actshift = models.DecimalField(db_column='Actshift', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    mno = models.IntegerField(blank=True, null=True)
    yr = models.IntegerField(blank=True, null=True)
    monthname = models.CharField(db_column='MonthName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_actshift'


class ViewActshiftDay(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='Unitname', max_length=50)  # Field name made lowercase.
    id = models.IntegerField()
    dt = models.DateTimeField()
    actshift = models.DecimalField(db_column='Actshift', max_digits=18, decimal_places=2)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_actshift_day'
