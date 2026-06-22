# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


<<<<<<< HEAD
class UnitUnituser(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    user_id = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI')
    password = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'unit_unituser'
=======
class TxNotification(models.Model):
    emp_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    wunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cat = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    punch_time = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    sl = models.AutoField(primary_key=True)
    processed = models.BooleanField(blank=True, null=True)
    pic = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    late = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tx_notification'
>>>>>>> 203fc034225e175ae9a5f208e177c49a5b0bd0af
