from django.db import models

class TxNotification(models.Model):
    emp_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    wunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cat = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    punch_time = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    sl = models.AutoField(primary_key=True)
    processed = models.BooleanField(blank=True, null=True)
    pic = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    late = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tx_notification'

class TmpPrdprn(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)
    ip = models.CharField(max_length=50)
    unit = models.CharField(db_column='Unit', max_length=50)  # Field name made lowercase.
    jobno = models.CharField(db_column='Jobno', max_length=50,primary_key=True)  # Field name made lowercase.
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
    o_finaldelvdate = models.DateField(db_column='o_FinalDelvdate', blank=True, null=True)  # Field name made lowercase.
    o_merch = models.CharField(max_length=35, blank=True, null=True)
    o_styledesc = models.CharField(max_length=50, blank=True, null=True)
    buyer = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=450, blank=True, null=True)
    tbpic = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_tmp_prdprn'
