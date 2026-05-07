# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VueNewprod02(models.Model):
    t = models.CharField(max_length=2)
    recno = models.IntegerField()
    prdhour = models.IntegerField()
    recdt = models.DateTimeField()
    unit = models.CharField(max_length=50)
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)  # Field name made lowercase.
    scp = models.CharField(max_length=1, blank=True, null=True)
    empid = models.IntegerField()
    contract_des = models.CharField(max_length=50, blank=True, null=True)
    trstype = models.CharField(max_length=50)
    clr = models.CharField(max_length=50)
    siz = models.CharField(max_length=50)
    qty = models.IntegerField(blank=True, null=True)
    bdl = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'vue_NewProd02'
