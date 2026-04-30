from django.db import models

class VueHoldwage(models.Model):
    rownum = models.BigIntegerField(db_column='RowNum', primary_key=True)   # Field name made lowercase.
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    period = models.CharField(db_column='Period', max_length=50)  # Field name made lowercase.
    holdamount = models.DecimalField(db_column='HoldAmount', max_digits=18, decimal_places=2)  # Field name made lowercase.
    chold = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tot = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_holdwage'

class Holdwagepaid(models.Model):
    entry_no = models.IntegerField(primary_key=True)
    dt = models.DateField()
    aadhar_no = models.CharField(max_length=20)
    code = models.IntegerField()
    emp_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    t_period = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    paid_amt = models.DecimalField(max_digits=18, decimal_places=0)
    remarks = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trs_holdwagepaid'




class Empwisesal(models.Model):
    dept = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    salary = models.DecimalField(
        db_column='Salary',
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    ) # Field name made lowercase.
    sl = models.IntegerField(blank=True, null=True)
    wrkunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    photo = models.CharField(max_length=400, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monthlysalary = models.CharField(db_column='MonthlySalary', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    
    designation = models.CharField(
        db_column='mcategory',
        max_length=50,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
  
   
    class Meta:
        managed = False
        db_table = 'Empwisesal'


class Employeeworking(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    workunit = models.CharField(db_column='WorkUnit', max_length=70, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=70, blank=True, null=True)
    type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'EmployeeWorking'     



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
    unit_id = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    total_bundles = models.IntegerField()
    pcs_count = models.IntegerField()
    r_date = models.DateField(db_column='r_Date', blank=True, null=True)  # Field name made lowercase.
    scan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'unit_bundlereport'

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


class AttUnt(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo',primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(blank=True, null=True)
    dept = models.CharField(db_column='DEPT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    onroll = models.IntegerField(blank=True, null=True)
    tail_onr = models.IntegerField(blank=True, null=True)
    ntail_onr = models.IntegerField(blank=True, null=True)
    present = models.IntegerField(blank=True, null=True)
    tailor = models.IntegerField(blank=True, null=True)
    n_tailor = models.IntegerField(blank=True, null=True)
    absent = models.IntegerField(blank=True, null=True)
    tabsent = models.IntegerField(blank=True, null=True)
    ntabsent = models.IntegerField(blank=True, null=True)
    le = models.IntegerField(blank=True, null=True)
    tlv = models.IntegerField(blank=True, null=True)
    ntlv = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_att_unt'

class Holiday(models.Model):
    dt = models.DateTimeField(blank=True, null=True)
    descr = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ty = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Holiday'
    

class EmbAbsetnt(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    photo = models.CharField(max_length=400, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    s = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vue_emb_absetnt'

class LabAtt(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    code_emb_attendance_fact = models.IntegerField(db_column='code emb attendance fact', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    intime = models.DateTimeField(blank=True, null=True)
    outtime = models.DateTimeField(blank=True, null=True)
    emppic = models.CharField(db_column='Emppic', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    img = models.CharField(max_length=53, blank=True, null=True)
    con_code_name_in_out = models.CharField(db_column='Con_Code_name_in_out', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    rel_code_name = models.CharField(db_column='Rel_code_name', max_length=112, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lab_att'

class RptCutting(models.Model):
    planno = models.IntegerField(db_column='PLANNO',primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT')  # Field name made lowercase.
    jobno = models.CharField(db_column='JOBNO', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sample_descr = models.CharField(db_column='SAMPLE_DESCR', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    per = models.DecimalField(db_column='PER', max_digits=18, decimal_places=2)  # Field name made lowercase.
    lot = models.CharField(db_column='LOT', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tply = models.IntegerField(db_column='TPLY')  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    topbottom_id = models.IntegerField(db_column='TopBottom_id')  # Field name made lowercase.
    mtr = models.DecimalField(db_column='MTR', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rls = models.IntegerField(db_column='RLS', blank=True, null=True)  # Field name made lowercase.
    fdeldt = models.DateTimeField(db_column='FDELDT', blank=True, null=True)  # Field name made lowercase.
    plan_mtr = models.DecimalField(db_column='PLAN_MTR', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    plan_kg = models.DecimalField(db_column='PLAN_KG', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    cutdt = models.DateTimeField(blank=True, null=True)
    aply = models.IntegerField(blank=True, null=True)
    ratio_stick_dt = models.DateTimeField(blank=True, null=True)
    bitcheck_dt = models.DateTimeField(blank=True, null=True)
    mas_bud_dt = models.DateTimeField(blank=True, null=True)
    unitdel_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RPT_CUTTING01'

class VueOrdersinhand(models.Model):
    orderno = models.CharField(db_column='OrderNo', max_length=50 ,primary_key=True)  # Field name made lowercase.
      

    class Meta:
        managed = False
        db_table = 'vue_Ordersinhand'
