# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TmpPrdprn(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(max_length=50)
    unit = models.CharField(db_column='Unit', max_length=50)  # Field name made lowercase.
    jobno = models.CharField(db_column='Jobno', max_length=50)  # Field name made lowercase.
    tb = models.CharField(db_column='Tb', max_length=50)  # Field name made lowercase.
    clr = models.CharField(max_length=50)
    bc = models.IntegerField()
    sew = models.IntegerField()
    che = models.IntegerField()
    irn = models.IntegerField()
    pack = models.IntegerField()
    oth = models.IntegerField()
    mist = models.IntegerField()
    trstype = models.CharField(max_length=80, blank=True, null=True)
    ordqty = models.IntegerField(blank=True, null=True)
    fc = models.IntegerField(blank=True, null=True)
    allotqty = models.IntegerField(blank=True, null=True)
    cutqtyqty = models.IntegerField(blank=True, null=True)
    rejqty = models.IntegerField(blank=True, null=True)
    singer = models.IntegerField(blank=True, null=True)
    o_finaldelvdate = models.DateTimeField(db_column='o_FinalDelvdate', blank=True, null=True)  # Field name made lowercase.
    o_merch = models.CharField(max_length=35, blank=True, null=True)
    o_styledesc = models.CharField(max_length=50, blank=True, null=True)
    buyer = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=450, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_tmp_prdprn'
