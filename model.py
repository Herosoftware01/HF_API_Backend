# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VueCuttingPrintembdel(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    frm = models.CharField(max_length=750, blank=True, null=True)
    toad = models.CharField(max_length=750, blank=True, null=True)
    id = models.IntegerField()
    dt = models.DateTimeField()
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)  # Field name made lowercase.
    qrid = models.IntegerField(db_column='QRID')  # Field name made lowercase.
    comboclr = models.CharField(max_length=50)
    lotno = models.CharField(max_length=50)
    portion_des = models.CharField(db_column='Portion_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    noofpcs = models.IntegerField()
    username = models.CharField(db_column='Username', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_cutting_printembdel'
