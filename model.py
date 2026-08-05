# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewFabricDeliveryProcess(models.Model):
    companyid = models.SmallIntegerField(db_column='CompanyID')  # Field name made lowercase.
    year = models.SmallIntegerField(db_column='Year')  # Field name made lowercase.
    no = models.IntegerField(db_column='No')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    lotno = models.SmallIntegerField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    su_name = models.CharField(db_column='su_Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    su_add1 = models.CharField(max_length=50, blank=True, null=True)
    su_add2 = models.CharField(max_length=50, blank=True, null=True)
    su_pin = models.CharField(max_length=15, blank=True, null=True)
    su_gst = models.CharField(max_length=50, blank=True, null=True)
    cmpy_phone1 = models.CharField(max_length=50, blank=True, null=True)
    companyname = models.CharField(max_length=12)
    cmpy_add1 = models.CharField(max_length=50, blank=True, null=True)
    cmpy_add2 = models.CharField(max_length=50, blank=True, null=True)
    cmpy_place = models.CharField(max_length=66, blank=True, null=True)
    cmpy_gst = models.CharField(max_length=20, blank=True, null=True)
    cmpy_state = models.CharField(max_length=34, blank=True, null=True)
    clr_name = models.CharField(max_length=50, blank=True, null=True)
    del_unit = models.CharField(max_length=35, blank=True, null=True)
    itemno1 = models.SmallIntegerField(db_column='ItemNo1')  # Field name made lowercase.
    ty = models.CharField(max_length=35)
    fab = models.CharField(max_length=35)
    gsm = models.SmallIntegerField(db_column='GSM', blank=True, null=True)  # Field name made lowercase.
    dia = models.CharField(max_length=35)
    finaldia = models.CharField(db_column='FinalDia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rolls = models.IntegerField(db_column='Rolls')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4)  # Field name made lowercase.
    yarninfo = models.CharField(db_column='YarnInfo', max_length=971, blank=True, null=True)  # Field name made lowercase.
    style = models.CharField(max_length=35)
    state_name = models.CharField(db_column='state_Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state_code = models.CharField(max_length=2, blank=True, null=True)
    place = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_fabric_delivery_process'
