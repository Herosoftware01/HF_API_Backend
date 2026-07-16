from django.db import models

# Create your models here.

class TrsCdelPcs1(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    unitid = models.IntegerField(db_column='UnitID')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tbid = models.IntegerField(db_column='TBID')  # Field name made lowercase.
    lcid = models.IntegerField(db_column='LcID')  # Field name made lowercase.
    totmastbdl = models.IntegerField(db_column='TotMastBdl')  # Field name made lowercase.
    totweight = models.DecimalField(db_column='Totweight', max_digits=18, decimal_places=3)  # Field name made lowercase.
    totbdl = models.IntegerField(db_column='Totbdl')  # Field name made lowercase.
    totpcs = models.IntegerField(db_column='Totpcs')  # Field name made lowercase.
    del_remarks = models.CharField(db_column='Del_Remarks', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    vechno = models.CharField(db_column='Vechno', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ordsamid = models.IntegerField(db_column='OrdSamID')  # Field name made lowercase.
    cut_old = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trs_cdel_pcs1'



class MasUnit(models.Model):
    unitcode = models.IntegerField(db_column='Unitcode', primary_key=True)  
    unitname = models.CharField(db_column='UnitName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(db_column='Place', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tinno = models.CharField(db_column='Tinno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cstno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    shortname = models.CharField(db_column='ShortName', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    login = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)
    faxno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    essunit = models.CharField(db_column='Essunit', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    outsideunit = models.CharField(db_column='OUTSIDEUNIT', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    port = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ty = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    short = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dispid = models.IntegerField(blank=True, null=True)
    pe = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fabgdwn = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    div = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    staff = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mas_Unit'
        
class MasTopbottom(models.Model):
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    topbottom_id = models.IntegerField(db_column='TopBottom_id', primary_key=True)  # Field name made lowercase.
    act = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sl = models.IntegerField(blank=True, null=True)
    ty = models.CharField(db_column='TY', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_TopBottom'


class TrsCdelPcs21(models.Model):
    # pk = models.CompositePrimaryKey('ID', 'MBundID')
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    mbundid = models.IntegerField(db_column='MBundID')  # Field name made lowercase.
    mbappr = models.IntegerField(blank=True, null=True)
    sl = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'trs_cdel_pcs2'

class TrsCdelPcs3(models.Model):
    sl = models.AutoField(primary_key=True)  # Django-side PK

    id = models.IntegerField(db_column='ID')
    bdlid = models.CharField(
        db_column='BdlID',
        max_length=200,
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )
    sizid = models.IntegerField(db_column='SizID')
    lotno = models.CharField(
        db_column='LotNo',
        max_length=10,
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )
    bdl = models.IntegerField(db_column='Bdl')
    noofpcs = models.IntegerField(db_column='Noofpcs')
    comboclr = models.CharField(
        max_length=50,
        db_collation='SQL_Latin1_General_CP1_CI_AS',
        blank=True,
        null=True
    )
    bundid = models.IntegerField(blank=True, null=True)
    scan = models.CharField(
        max_length=1,
        db_collation='SQL_Latin1_General_CP1_CI_AS',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'trs_cdel_Pcs3'



class Bundlereport(models.Model):
    id = models.BigAutoField(primary_key=True)
    s_date = models.DateTimeField(db_column='S_date')  # Field name made lowercase.
    job_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    mbundle_id = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    tb_name = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    unit_id = models.CharField(max_length=100)
    total_bundles = models.IntegerField()
    pcs_count = models.IntegerField()
    r_date = models.DateField(db_column='r_Date', blank=True, null=True)  # Field name made lowercase.
    scan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Unit_BundleReport'

    def __str__(self):
        return f"{self.job_no} - {self.mbundle_id}"


class Unituser(models.Model):

    UNIT_CHOICES = [
        ("Unit-1", "Unit-1"),
        ("Unit-2", "Unit-2"),
        ("Unit-3", "Unit-3"),
        ("Unit-4", "Unit-4"),
        ("Unit-5", "Unit-5"),
    ]

    unit_name = models.CharField(max_length=20, choices=UNIT_CHOICES)
    user_id = models.CharField(max_length=10)
    password = models.CharField(max_length=10)


    class Meta:
        managed = False
        db_table = 'unit_unituser'


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

    class Meta:
        managed = False
        db_table = 'Trs_MCutStickerProd'

