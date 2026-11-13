# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewFabricInwardSummary(models.Model):
    sno = models.BigIntegerField(db_column='SNo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    colour = models.IntegerField(db_column='Colour', blank=True, null=True)  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fabdescr = models.IntegerField(db_column='Fabdescr', blank=True, null=True)  # Field name made lowercase.
    diaid = models.IntegerField(db_column='DiaID')  # Field name made lowercase.
    rls = models.IntegerField(blank=True, null=True)
    kg = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    mt = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    del_rls = models.IntegerField()
    del_kgs = models.DecimalField(max_digits=38, decimal_places=3)
    del_mtr = models.DecimalField(max_digits=38, decimal_places=2)
    crls = models.IntegerField()
    ckgs = models.DecimalField(max_digits=38, decimal_places=3)
    cmtr = models.DecimalField(max_digits=38, decimal_places=2)
    srls = models.IntegerField()
    skgs = models.DecimalField(max_digits=38, decimal_places=4)
    smtr = models.DecimalField(max_digits=38, decimal_places=2)
    clr_name = models.CharField(max_length=50, blank=True, null=True)
    fab_name = models.CharField(max_length=35, blank=True, null=True)
    dia_name = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_fabric_inward_summary'
