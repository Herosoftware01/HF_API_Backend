# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewGdwnFabricDeliveryPlan(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', blank=True, null=True)  # Field name made lowercase.
    frm = models.CharField(max_length=11)
    todept = models.CharField(max_length=12)
    dcno = models.IntegerField()
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    markerno = models.IntegerField(db_column='MarkerNo')  # Field name made lowercase.
    lotno = models.CharField(max_length=50)
    colour = models.CharField(db_column='Colour', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dia = models.CharField(db_column='Dia', max_length=35)  # Field name made lowercase.
    rls = models.IntegerField(blank=True, null=True)
    kg = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    mtr = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    rlno = models.CharField(max_length=8000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_gdwn_fabric_delivery_plan'
