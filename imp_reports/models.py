from django.db import models

class LaySp(models.Model):
    date = models.DateField()
    timer = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    plan_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True,unique=True)
    job_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    roll_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    f_dia = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    plan_ply = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    scl_wgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    plan_obwgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    req_wgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    actual_dia = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    actual_ply = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    actual_obwgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    end_bit = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    bal_wgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    debit_kg = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    roll_time = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    remarks = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    bit_wgt = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lay_spreading_roll_data_update'
class FinalPlans(models.Model):
    plan_no = models.ForeignKey(
        LaySp,
        to_field='plan_no',          # 🔥 VERY IMPORTANT
        on_delete=models.DO_NOTHING,
        db_column='plan_no',
        blank=True,
        null=True,
        related_name='final_plans'
    )
    job_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    empid = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    marker_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    lot_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    fabric_color = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    date = models.DateField()
    timer = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    pcs = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    table_id = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'final_plans'

class LaySpreadingLayemployee(models.Model):
    id = models.BigAutoField(primary_key=True)
    emp1 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    emp2 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    emp3 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    emp4 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    emp5 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    emp6 = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    table = models.IntegerField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'lay_spreading_layemployee'


class MasterFinalMistake(models.Model):
    id = models.BigAutoField(primary_key=True)
    roll_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    machine_id = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    job_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    dc_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    lot_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    field_id = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI')
    color = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    types = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    timer = models.TimeField(blank=True, null=True)
    m1 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m2 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m3 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m4 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m5 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m6 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m7 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m8 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m9 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m10 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m11 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    m12 = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    finish_dia = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    total_meters = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    act_gsm = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    remarks = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    date = models.DateField()
    emp_id1 = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    emp_id2 = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    weight = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    mm1 = models.IntegerField(db_column='MM1', blank=True, null=True)  # Field name made lowercase.
    mm10 = models.IntegerField(db_column='MM10', blank=True, null=True)  # Field name made lowercase.
    mm11 = models.IntegerField(db_column='MM11', blank=True, null=True)  # Field name made lowercase.
    mm12 = models.IntegerField(db_column='MM12', blank=True, null=True)  # Field name made lowercase.
    mm2 = models.IntegerField(db_column='MM2', blank=True, null=True)  # Field name made lowercase.
    mm3 = models.IntegerField(db_column='MM3', blank=True, null=True)  # Field name made lowercase.
    mm4 = models.IntegerField(db_column='MM4', blank=True, null=True)  # Field name made lowercase.
    mm5 = models.IntegerField(db_column='MM5', blank=True, null=True)  # Field name made lowercase.
    mm6 = models.IntegerField(db_column='MM6', blank=True, null=True)  # Field name made lowercase.
    mm7 = models.IntegerField(db_column='MM7', blank=True, null=True)  # Field name made lowercase.
    mm8 = models.IntegerField(db_column='MM8', blank=True, null=True)  # Field name made lowercase.
    mm9 = models.IntegerField(db_column='MM9', blank=True, null=True)  # Field name made lowercase.
    time1 = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    time2 = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_final_mistake'


class UnitBundlereport(models.Model):
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
        db_table = 'unit_bundlereport'
 
class BuntrackReport(models.Model):
    sl = models.IntegerField(primary_key=True)
    unit_id = models.IntegerField(db_column='Unit_id')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    totmastbdl = models.IntegerField(db_column='TotMastBdl')  # Field name made lowercase.
    totbdl = models.IntegerField(db_column='Totbdl')  # Field name made lowercase.
    ordsamid = models.IntegerField(db_column='OrdSamID')  # Field name made lowercase.
    pcs_count = models.IntegerField(blank=True, null=True)
    b_id = models.IntegerField(db_column='B_id')  # Field name made lowercase.
    r_dt = models.DateTimeField(db_column='R_dt', blank=True, null=True)  # Field name made lowercase.
    mbunid = models.IntegerField(db_column='MBunID', blank=True, null=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='UnitName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mbappr = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_buntrack_report'


class CoraRollcheck(models.Model):
    sl = models.BigIntegerField(db_column='SL', primary_key=True)
    trn = models.CharField(db_column='Trn', max_length=1)
    jobno = models.CharField(db_column='JobNo', max_length=50)
    company = models.CharField(db_column='Company', max_length=11)
    year = models.IntegerField(db_column='Year')
    pono = models.IntegerField(db_column='Pono')
    pdcref = models.CharField(db_column='Pdcref', max_length=50)
    supplier = models.CharField(db_column='Supplier', max_length=35, blank=True, null=True)
    fabricdescription = models.CharField(db_column='FabricDescription', max_length=35, blank=True, null=True)
    colour = models.CharField(db_column='Colour', max_length=50, blank=True, null=True)
    filnam = models.CharField(max_length=82, blank=True, null=True)
    dia = models.CharField(db_column='Dia', max_length=35, blank=True, null=True)
    gsm = models.IntegerField()
    rlno = models.CharField(max_length=50, unique=True)  # 👈 IMPORTANT for FK
    ll = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=3)
    mills = models.CharField(db_column='Mills', max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cora_RollCheck'

    def __str__(self):
        return f"{self.rlno} - {self.jobno}"


class Corarlck1(models.Model):
    sl = models.AutoField(primary_key=True)
    dt = models.DateField()

    # 👇 MAIN LINK (FK using rlno instead of id)
    roll = models.ForeignKey(
        CoraRollcheck,
        to_field='rlno',
        db_column='rlno',
        on_delete=models.DO_NOTHING,
        related_name='coral_entries',
        null=True,
        blank=True
    )

    hole = models.CharField(max_length=50, blank=True, null=True)
    setoff = models.CharField(max_length=50, blank=True, null=True)
    needle_line = models.CharField(max_length=50, blank=True, null=True)
    oil_line = models.CharField(max_length=50, blank=True, null=True)
    oil_drops = models.CharField(db_column='Oil_drops', max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    poovari = models.CharField(max_length=50, blank=True, null=True)
    yarn_mistake = models.CharField(max_length=50, blank=True, null=True)
    lycra_cut = models.CharField(max_length=50, blank=True, null=True)
    yarn_uneven = models.CharField(max_length=50, blank=True, null=True)
    neps = models.CharField(max_length=50, blank=True, null=True)
    empid = models.IntegerField(blank=True, null=True)
    timer = models.CharField(db_column='Timer', max_length=50, blank=True, null=True)
    dia = models.CharField(max_length=50, blank=True, null=True)
    na_holes = models.CharField(max_length=50, blank=True, null=True)
    m12 = models.CharField(max_length=50, blank=True, null=True)
    loop_len = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    submit = models.BooleanField()
    mach_id = models.CharField(max_length=5, blank=True, null=True)
    time1 = models.TimeField(blank=True, null=True)
    time2 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CoraRlck1'

    def __str__(self):
        return f"{self.roll_id} - {self.dt}"



class VueAdGrid1(models.Model):
    rn = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wrkunit = models.CharField(max_length=50, blank=True, null=True)
    sl = models.IntegerField(primary_key=True)
    dt = models.DateTimeField()
    id = models.IntegerField()
    mins = models.DecimalField(max_digits=18, decimal_places=2)
    sv = models.DecimalField(max_digits=18, decimal_places=2)
    m = models.IntegerField(blank=True, null=True)
    pers = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    photo = models.CharField(max_length=400, blank=True, null=True)
    amt = models.DecimalField(max_digits=37, decimal_places=4, blank=True, null=True)
    salary = models.DecimalField(db_column='Salary', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_ad_grid1'


class QcappQcPieceFinal(models.Model):
    id = models.BigAutoField(primary_key=True)
    bundle_no = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    bundle_id = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    jobno = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    product = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    color = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    size = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    total_pieces = models.IntegerField()
    checked_piece = models.IntegerField()
    force_save = models.BooleanField()
    line = models.IntegerField()
    unit = models.IntegerField()
    qc_type = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    date = models.DateTimeField()
    user_id = models.IntegerField()
    seq = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    machine_id = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'qcapp_qc_piece_final'