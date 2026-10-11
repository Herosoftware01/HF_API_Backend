# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewGenStockIssue(models.Model):
    qrdetails = models.CharField(db_column='QRDetails', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(max_length=12)
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(max_length=66, blank=True, null=True)
    regno = models.CharField(db_column='RegNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ph = models.CharField(max_length=17)
    to_dept = models.CharField(max_length=35)
    no = models.IntegerField(db_column='No')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    frm_dept = models.CharField(max_length=35)
    itemgrp = models.CharField(max_length=35)
    itemname = models.CharField(max_length=35)
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=25)  # Field name made lowercase.
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    altuom = models.CharField(max_length=25, blank=True, null=True)
    companyid = models.SmallIntegerField(db_column='CompanyID')  # Field name made lowercase.
    year = models.SmallIntegerField(db_column='Year')  # Field name made lowercase.
    reqno = models.IntegerField(db_column='reqNo', blank=True, null=True)  # Field name made lowercase.
    reqdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_gen_stock_Issue'
