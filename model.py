# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VueOrdersinhand(models.Model):
    uom = models.CharField(max_length=5, blank=True, null=True)
    fdeldt = models.CharField(max_length=30, blank=True, null=True)
    img = models.CharField(max_length=82, blank=True, null=True)
    director = models.CharField(max_length=35)
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    con = models.CharField(db_column='Con', max_length=193, blank=True, null=True)  # Field name made lowercase.
    o_filnam = models.CharField(max_length=8000, blank=True, null=True)
    o_styledesc = models.CharField(db_column='o_StyleDesc', max_length=35, blank=True, null=True)  # Field name made lowercase.
    o_week = models.CharField(max_length=750)
    o_wk = models.CharField(max_length=1)
    o_01_prn = models.CharField(max_length=750)
    o_03_emb = models.CharField(db_column='o_03_Emb', max_length=750)  # Field name made lowercase.
    o_ordtype = models.CharField(db_column='o_OrdType', max_length=6)  # Field name made lowercase.
    o_orderno = models.CharField(db_column='o_Orderno', max_length=50)  # Field name made lowercase.
    o_finaldelvdate = models.DateField(db_column='o_FinalDelvdate', blank=True, null=True)  # Field name made lowercase.
    o_buyer = models.CharField(db_column='o_Buyer', max_length=40, blank=True, null=True)  # Field name made lowercase.
    o_merch = models.CharField(max_length=35, blank=True, null=True)
    o_ordqty = models.IntegerField(blank=True, null=True)
    o_productionunit = models.CharField(db_column='o_ProductionUnit', max_length=35)  # Field name made lowercase.
    o_prodtype = models.CharField(db_column='o_ProdType', max_length=7)  # Field name made lowercase.
    o_buy = models.CharField(db_column='o_Buy', max_length=5, blank=True, null=True)  # Field name made lowercase.
    o_45_cut = models.CharField(max_length=750)
    o_17_sam = models.CharField(max_length=750)
    o_19_erun = models.CharField(db_column='o_19_Erun', max_length=750)  # Field name made lowercase.
    o_21_prun = models.CharField(db_column='o_21_Prun', max_length=750)  # Field name made lowercase.
    o_08_frun = models.CharField(db_column='o_08_Frun', max_length=750)  # Field name made lowercase.
    o_50_run = models.CharField(db_column='o_50_Run', max_length=750)  # Field name made lowercase.
    o_149 = models.CharField(max_length=750)
    o_07 = models.CharField(max_length=750)
    o_37 = models.CharField(max_length=750)
    o_36 = models.CharField(max_length=750)
    o_46 = models.CharField(max_length=750)
    o_10 = models.CharField(max_length=750)
    o_qname = models.CharField(max_length=35, blank=True, null=True)
    o_ordvalue = models.DecimalField(db_column='o_ordValue', max_digits=38, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    stylename = models.CharField(db_column='StyleName', max_length=50)  # Field name made lowercase.
    o_cur = models.CharField(max_length=35, blank=True, null=True)
    o_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    inchargename = models.CharField(db_column='Inchargename', max_length=83)  # Field name made lowercase.
    price_ind = models.DecimalField(db_column='Price_Ind', max_digits=38, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    exrate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    o_customerid = models.IntegerField(db_column='o_Customerid', blank=True, null=True)  # Field name made lowercase.
    filnam = models.CharField(max_length=82, blank=True, null=True)
    actdate = models.CharField(db_column='ActDate', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50)  # Field name made lowercase.
    o_45141 = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'vue_Ordersinhand'
