# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VueResignDtls(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    photo = models.CharField(max_length=400, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    resigndt = models.DateTimeField(db_column='resignDt', blank=True, null=True)  # Field name made lowercase.
    days_worked = models.IntegerField(db_column='Days_Worked', blank=True, null=True)  # Field name made lowercase.
    unitcode = models.IntegerField(db_column='Unitcode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_resign_Dtls'
