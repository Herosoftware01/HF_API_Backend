# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TrsHoldwagepaid(models.Model):
    entry_no = models.IntegerField(primary_key=True)
    dt = models.DateField()
    aadhar_no = models.IntegerField()
    code = models.IntegerField()
    emp_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    t_period = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    paid_amt = models.DecimalField(max_digits=18, decimal_places=0)
    remarks = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trs_holdwagepaid'
