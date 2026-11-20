from django.db import models

class ViewFabricInwardSummary(models.Model):
    sno = models.BigIntegerField(db_column='SNo', primary_key=True)  # Field name made lowercase.
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


class ViewCuttingOcr(models.Model):
    sno = models.BigIntegerField(db_column='SNo', primary_key=True)  # Field name made lowercase.
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


class MaunualStock(models.Model):
    sno = models.BigIntegerField(db_column='SNo', primary_key=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    colour = models.IntegerField(db_column='Colour')  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fabdescr = models.IntegerField(db_column='Fabdescr')  # Field name made lowercase.
    diaid = models.IntegerField(db_column='DiaID')  # Field name made lowercase.
    rls = models.IntegerField()
    kgs = models.DecimalField(max_digits=38, decimal_places=3)
    mtr = models.DecimalField(max_digits=38, decimal_places=2)
    clr_name = models.CharField(max_length=50, blank=True, null=True)
    fab_name = models.CharField(max_length=35, blank=True, null=True)
    dia_name = models.CharField(max_length=35, blank=True, null=True)

    class Meta:

        db_table = 'ocr_maunual_stock'