# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TrsMcutstickerprod(models.Model):
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    mbud = models.IntegerField(db_column='Mbud')  # Field name made lowercase.
    bundid = models.CharField(db_column='BundID', primary_key=True, max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tbid = models.IntegerField(db_column='TBID')  # Field name made lowercase.
    comboclr = models.CharField(db_column='Comboclr', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sizid = models.IntegerField(db_column='SIZID')  # Field name made lowercase.
    bdl = models.IntegerField(db_column='Bdl')  # Field name made lowercase.
    pc = models.IntegerField(db_column='Pc')  # Field name made lowercase.
    porid = models.IntegerField(db_column='PorID')  # Field name made lowercase.
    weight = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    bund_id = models.IntegerField(blank=True, null=True)
    lotno = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    hempid = models.IntegerField(blank=True, null=True)
    frmbc = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    scan = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    livescan = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    old = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    assembly_complected = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    unit_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trs_MCutStickerProd'
