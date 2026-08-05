# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewAccinwardVerification(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    supplierdcno = models.CharField(db_column='SupplierDCNo', max_length=50)  # Field name made lowercase.
    pono = models.IntegerField(db_column='PONo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    items = models.CharField(db_column='Items', max_length=71, blank=True, null=True)  # Field name made lowercase.
    clr_siz = models.CharField(max_length=101, blank=True, null=True)
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=25)  # Field name made lowercase.
    bill_rate = models.DecimalField(db_column='Bill_Rate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    gst = models.CharField(db_column='GST', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_accinward_verification'
