# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VueAccProcDel(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    auom = models.CharField(max_length=25)
    auomscale = models.IntegerField()
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    uom = models.CharField(max_length=25, blank=True, null=True)
    uomscale = models.IntegerField(blank=True, null=True)
    siz = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    acc_grp = models.CharField(max_length=35)
    acc_name = models.CharField(max_length=35)
    incharge = models.CharField(max_length=1)
    frmdpt = models.CharField(max_length=35)
    todept = models.CharField(max_length=1)
    supplier = models.CharField(max_length=35)
    supadd1 = models.CharField(max_length=50)
    supadd2 = models.CharField(max_length=50)
    supadd3 = models.CharField(max_length=50)
    supgst = models.CharField(max_length=66)
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    no = models.IntegerField()
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(max_length=12)
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(max_length=66, blank=True, null=True)
    regno = models.CharField(db_column='RegNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dye_clr = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
      managed = False
        db_table = 'vue_acc_proc_del'
  