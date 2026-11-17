# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewCuttingOcr(models.Model):
    sno = models.BigIntegerField(db_column='SNo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    colour = models.IntegerField(db_column='Colour')  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fabdescr = models.IntegerField(db_column='Fabdescr')  # Field name made lowercase.
    diaid = models.IntegerField(db_column='DiaID')  # Field name made lowercase.
    rec_rls = models.IntegerField()
    rec_kg = models.DecimalField(max_digits=38, decimal_places=3)
    rec_mt = models.DecimalField(max_digits=38, decimal_places=2)
    crt_crls = models.IntegerField()
    crt_kgs = models.DecimalField(max_digits=38, decimal_places=3)
    crt_mtr = models.DecimalField(max_digits=38, decimal_places=2)
    stk_rls = models.IntegerField()
    stk_kgs = models.DecimalField(max_digits=38, decimal_places=3)
    stk_mtr = models.DecimalField(max_digits=38, decimal_places=2)
    cns_rls = models.IntegerField()
    cns_kgs = models.DecimalField(max_digits=38, decimal_places=3)
    cns_mtr = models.DecimalField(max_digits=38, decimal_places=2)
    ebit = models.DecimalField(max_digits=38, decimal_places=2)
    rep_rls = models.IntegerField()
    rep_kgs = models.DecimalField(max_digits=38, decimal_places=2)
    rep_mtr = models.DecimalField(max_digits=38, decimal_places=2)
    bigbitkg = models.DecimalField(max_digits=38, decimal_places=2)
    clr_name = models.CharField(max_length=50, blank=True, null=True)
    fab_name = models.CharField(max_length=35, blank=True, null=True)
    dia_name = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_cutting_ocr'
