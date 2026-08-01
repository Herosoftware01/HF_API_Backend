# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class QcappQcHourlyApproval(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit = models.IntegerField()
    line = models.IntegerField()
    approval_hour = models.IntegerField()
    date = models.DateField()
    unit_incharge_user = models.IntegerField(blank=True, null=True)
    unit_incharge_sign = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    unit_incharge_time = models.DateTimeField(blank=True, null=True)
    oa_user = models.IntegerField(blank=True, null=True)
    oa_sign = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    oa_time = models.DateTimeField(blank=True, null=True)
    fm_user = models.IntegerField(blank=True, null=True)
    fm_sign = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    fm_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'qcapp_qc_hourly_approval'
