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

class Leavempabsent(models.Model):
    leav_entno = models.IntegerField(db_column='Leav_EntNo')  # Field name made lowercase.
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    expecdt = models.DateTimeField(db_column='ExpecDt')  # Field name made lowercase.
    leav_applydt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vue_Trs_LeavEmpAbsent'

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


class ResignDtls(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase.
    code = models.IntegerField()
    photo = models.CharField(max_length=400, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    resigndt = models.DateTimeField(db_column='resignDt', blank=True, null=True)  # Field name made lowercase.
    days_worked = models.IntegerField(db_column='Days_Worked', blank=True, null=True)  # Field name made lowercase.
    unitcode = models.IntegerField(db_column='Unitcode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_resign_Dtls'

class TrsHrRsgnDtls(models.Model):
    empid = models.IntegerField(primary_key=True)
    user_nms = models.CharField(max_length=25, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    in_ch_remarks = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    in_ch_date = models.DateTimeField(blank=True, null=True)
    hr_remarks = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    hr_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trs_hr_rsgn_dtls'

class Empjoin(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    photo = models.CharField(max_length=400, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(max_length=50, blank=True, null=True)
    unitcode = models.IntegerField(db_column='Unitcode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_empjoin'


class AttStaff(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(max_length=70, blank=True, null=True)
    onroll = models.IntegerField(blank=True, null=True)
    present = models.IntegerField(blank=True, null=True)
    leave = models.IntegerField(blank=True, null=True)
    absent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_att_staff'

class StaffAbsent(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    photo = models.CharField(max_length=400, blank=True, null=True)
    wunit = models.CharField(max_length=70, blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70)
    s = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_staff_absent'

class StaffAtt(models.Model):
    code_emb_attendance_fact = models.IntegerField(db_column='code emb attendance fact', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    date = models.DateTimeField(blank=True, null=True)
    dept = models.CharField(max_length=70, blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    intime = models.DateTimeField(blank=True, null=True)
    outtime = models.DateTimeField(blank=True, null=True)
    emppic = models.CharField(db_column='Emppic', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    img = models.CharField(max_length=53, blank=True, null=True)
    con_code_name_in_out = models.CharField(db_column='Con_Code_name_in_out', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    rel_code_name = models.CharField(db_column='Rel_code_name', max_length=82, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'staff_att'


class ContractSec(models.Model):
    name = models.CharField(max_length=70)
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField( max_length=70, blank=True, null=True)  # Field name made lowercase.
    intime = models.TimeField(blank=True, null=True)
    outtime = models.TimeField(blank=True, null=True)
    code = models.CharField(max_length=20)
    slno = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contract_sec'


class BillAge(models.Model):
    no = models.IntegerField(db_column='No',primary_key=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate')  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate')  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', max_length=63, blank=True, null=True)  # Field name made lowercase.
    narration = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(db_column='Username', max_length=35, blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(db_column='Module', max_length=50, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ageing = models.IntegerField(db_column='Ageing', blank=True, null=True)  # Field name made lowercase.
    suppliers = models.CharField(db_column='Suppliers', max_length=35, blank=True, null=True)  # Field name made lowercase.
    employees = models.CharField(db_column='Employees', max_length=35, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    billpassed = models.SmallIntegerField(db_column='BillPassed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bill_age'


class BillPass(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate')  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', max_length=63, blank=True, null=True)  # Field name made lowercase.
    billno1 = models.CharField(max_length=50)
    paymentdate = models.DateTimeField(blank=True, null=True)
    daysbetweenbillandpayment = models.IntegerField(db_column='DaysBetweenBillAndPayment', blank=True, null=True)  # Field name made lowercase.
    module1 = models.CharField(db_column='Module1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ageing = models.IntegerField(db_column='Ageing', blank=True, null=True)  # Field name made lowercase.
    daysbetweenbillandedate = models.IntegerField(db_column='DaysBetweenBillAndEDate', blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(db_column='Module', max_length=255, blank=True, null=True)  # Field name made lowercase.
    suppliers = models.CharField(db_column='Suppliers', max_length=35, blank=True, null=True)  # Field name made lowercase.
    employees = models.CharField(db_column='Employees', max_length=35, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    billpassed = models.SmallIntegerField(db_column='BillPassed')  # Field name made lowercase.
    br_ageing = models.IntegerField(db_column='BR Ageing', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    billdate_ageing = models.IntegerField(db_column='BillDate Ageing', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Bill_pass'

class BillMdapprove(models.Model):
    billpaid = models.SmallIntegerField(db_column='BillPaid')  # Field name made lowercase.
    billpassed = models.SmallIntegerField(db_column='BillPassed')  # Field name made lowercase.
    lz_module_name11 = models.CharField(db_column='LZ_Module Name11', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    username = models.CharField(db_column='Username', max_length=35, blank=True, null=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='Company_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billno = models.CharField(max_length=50)
    billno1 = models.CharField(db_column='Billno1', max_length=63, blank=True, null=True)  # Field name made lowercase.
    supplier = models.CharField(db_column='Supplier', max_length=35, blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate')  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate')  # Field name made lowercase.
    lz_module_name1 = models.CharField(db_column='LZ_Module Name1', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_rowdata = models.IntegerField(db_column='_ROWDATA',primary_key=True)  # Field name made lowercase. Field renamed because it started with '_'.
    lz_no = models.IntegerField(db_column='LZ_No', blank=True, null=True)  # Field name made lowercase.
    mdapproval = models.CharField(db_column='MDApproval', max_length=12, blank=True, null=True)  # Field name made lowercase.
    hz_version = models.IntegerField(db_column='HZ_Version', blank=True, null=True)  # Field name made lowercase.
    le_date = models.DateTimeField(db_column='LE_Date', blank=True, null=True)  # Field name made lowercase.
    lz_reference = models.CharField(db_column='LZ_Reference', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lz_beno = models.IntegerField(db_column='LZ_BENo', blank=True, null=True)  # Field name made lowercase.
    le_bedate = models.DateTimeField(db_column='LE_BEDate', blank=True, null=True)  # Field name made lowercase.
    lz_module_name = models.IntegerField(db_column='LZ_Module Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lz_supplier = models.CharField(db_column='LZ_Supplier', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lz_billno = models.CharField(db_column='LZ_BillNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    le_billdate = models.DateTimeField(db_column='LE_BillDate', blank=True, null=True)  # Field name made lowercase.
    ra_assessable_amount = models.DecimalField(db_column='RA_Assessable Amount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ra_taxableocamount = models.DecimalField(db_column='RA_TaxableOCAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    # ra_tax_amount = models.DecimalField(db_column='RA_Tax Amount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ra_nontaxableocamount = models.DecimalField(db_column='RA_NonTaxableOCAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ra_billvalue = models.DecimalField(db_column='RA_BillValue', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    # ra_t_debit = models.DecimalField(db_column='RA_T.Debit', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ra_tds_deducted_amount = models.DecimalField(db_column='RA_TDS Deducted Amount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ra_bill_pass_value = models.DecimalField(db_column='RA_Bill Pass Value', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lz_isauthorized_field = models.CharField(db_column='LZ_isAuthorized?', max_length=13, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    lz_incharge = models.CharField(db_column='LZ_Incharge', max_length=35, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bill_mdapprove'



class HrLabourattendence(models.Model):

    unit = models.CharField(
        db_column='Unit',
        max_length=50,
        blank=True,
        null=True
    )

    code = models.IntegerField(primary_key=True)

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    joindt = models.DateTimeField(
        db_column='JoinDt',
        blank=True,
        null=True
    )

    dept = models.CharField(
        db_column='DEPT',
        max_length=50
    )

    cat = models.CharField(
        db_column='CAT',
        max_length=50
    )

    subcat = models.CharField(
        db_column='SUBCAT',
        max_length=50
    )

    shift_contract = models.CharField(
        db_column='Shift_Contract',
        max_length=1,
        blank=True,
        null=True
    )

    hostel = models.CharField(
        db_column='Hostel',
        max_length=10
    )

    gender = models.CharField(
        db_column='Gender',
        max_length=6
    )

    empimage = models.CharField(
        db_column='EmpImage',
        max_length=8000,
        blank=True,
        null=True
    )

    status = models.CharField(
        db_column='Status',
        max_length=7
    )

    date = models.CharField(
        db_column='Date',
        max_length=4000,
        blank=True,
        null=True
    )

    intime = models.CharField(
        db_column='InTime',
        max_length=4000,
        blank=True,
        null=True
    )

    attendence_status = models.CharField(
        db_column='Attendence Status',
        max_length=14
    )

    mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    photo = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    status1 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hr_Labourattendence'


# =========================
# DATABASE : demo
# TABLE : EmployeeWorking
# =========================

class Employeeworking1(models.Model):

    code = models.IntegerField(primary_key=True)

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    workunit = models.CharField(
        db_column='WorkUnit',
        max_length=70,
        blank=True,
        null=True
    )

    category = models.CharField(
        db_column='Category',
        max_length=70,
        blank=True,
        null=True
    )

    type = models.CharField(
        max_length=6
    )

    class Meta:
        managed = False
        db_table = 'EmployeeWorking'



class BitcheckHour(models.Model):
    dt = models.DateTimeField(blank=True, null=True)
    empid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    s = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True,)
    v_pc = models.IntegerField(blank=True, null=True)
    vi_pc = models.IntegerField(blank=True, null=True)
    i_pc = models.IntegerField(blank=True, null=True)
    ii_pc = models.IntegerField(blank=True, null=True)
    iii_pc = models.IntegerField(blank=True, null=True)
    iv_pc = models.IntegerField(blank=True, null=True)
    v_pan = models.IntegerField(blank=True, null=True)
    vi_pan = models.IntegerField(blank=True, null=True)
    i_pan = models.IntegerField(blank=True, null=True)
    ii_pan = models.IntegerField(blank=True, null=True)
    iii_pan = models.IntegerField(blank=True, null=True)
    iv_pan = models.IntegerField(blank=True, null=True)
    amt = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_bitcheck_hour'



class StickerHour(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    empid = models.IntegerField(primary_key=True)
    dt = models.DateField(blank=True, null=True)
    v_pc = models.IntegerField(blank=True, null=True)
    vi_pc = models.IntegerField(blank=True, null=True)
    i_pc = models.IntegerField(blank=True, null=True)
    ii_pc = models.IntegerField(blank=True, null=True)
    iii_pc = models.IntegerField(blank=True, null=True)
    iv_pc = models.IntegerField(blank=True, null=True)
    v_pan = models.IntegerField(blank=True, null=True)
    vi_pan = models.IntegerField(blank=True, null=True)
    i_pan = models.IntegerField(blank=True, null=True)
    ii_pan = models.IntegerField(blank=True, null=True)
    iii_pan = models.IntegerField(blank=True, null=True)
    iv_pan = models.IntegerField(blank=True, null=True)
    s_hift = models.DecimalField(max_digits=38, decimal_places=2)
    amt = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_sticker_hour'


class VueRepCutPend(models.Model):
    slno = models.BigIntegerField(primary_key=True)
    dt = models.DateTimeField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)
    clrcombo = models.CharField(max_length=50)
    siz = models.CharField(max_length=35)
    lotno = models.CharField(max_length=50)
    panel_description = models.CharField(max_length=8000, blank=True, null=True)
    mistake_pcs = models.IntegerField(db_column='Mistake_Pcs', blank=True, null=True)
    mistake_panel_count = models.IntegerField(db_column='Mistake_Panel_Count', blank=True, null=True)
    merge_pcs = models.IntegerField(db_column='Merge_Pcs')  
    replace_cutting_pcs = models.IntegerField(db_column='Replace_Cutting_Pcs') 
    status = models.CharField(db_column='Status', max_length=7)
    pendpc = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vue_rep_cut_pend'
        
class VueDyeingRatenew(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    prs = models.CharField(max_length=35)
    clr = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    supplier = models.CharField(max_length=35, blank=True, null=True)
    no = models.IntegerField(db_column='No')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fabric = models.CharField(max_length=35)
    rolls = models.IntegerField(blank=True, null=True)
    wgt = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)
    lotno = models.SmallIntegerField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    mdapprovedrate = models.DecimalField(db_column='MDApprovedRate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    red = models.IntegerField(db_column='Red', blank=True, null=True)  # Field name made lowercase.
    green = models.IntegerField(db_column='Green', blank=True, null=True)  # Field name made lowercase.
    blue = models.IntegerField(db_column='Blue', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'vue_dyeing_ratenew'


class Txorderdetstyles(models.Model):
    companyid = models.IntegerField(db_column='CompanyID', blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    no = models.CharField(db_column='No', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    year = models.SmallIntegerField(db_column='Year')  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    ordertype = models.SmallIntegerField(db_column='OrderType', blank=True, null=True)  # Field name made lowercase.
    customerid = models.IntegerField(db_column='CustomerID', blank=True, null=True)  # Field name made lowercase.
    departmentid = models.IntegerField(db_column='DepartmentID', blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=2100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pono = models.CharField(db_column='PONo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    finaldelvdate = models.DateTimeField(db_column='FinalDelvDate', blank=True, null=True)  # Field name made lowercase.
    ourdelvdate = models.DateTimeField(db_column='OurDelvDate', blank=True, null=True)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    quantityactual = models.DecimalField(db_column='QuantityActual', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    quantityextra = models.DecimalField(db_column='QuantityExtra', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    uom = models.SmallIntegerField(db_column='UOM', blank=True, null=True)  # Field name made lowercase.
    pcsperpack = models.DecimalField(db_column='PcsPerPack', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    orderconfyear = models.SmallIntegerField(db_column='OrderConfYear')  # Field name made lowercase.
    orderconfno = models.SmallIntegerField(db_column='OrderConfNo')  # Field name made lowercase.
    styleid = models.IntegerField(db_column='StyleID')  # Field name made lowercase.
    stylename = models.CharField(db_column='StyleName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    styledesc = models.CharField(db_column='StyleDesc', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    packingtype = models.SmallIntegerField(db_column='PackingType')  # Field name made lowercase.
    finalinspby = models.SmallIntegerField(db_column='FinalInspBy')  # Field name made lowercase.
    testagencyid = models.IntegerField(db_column='TestAgencyID')  # Field name made lowercase.
    measurementscale = models.SmallIntegerField(db_column='MeasurementScale')  # Field name made lowercase.
    measurementscalemp = models.SmallIntegerField(db_column='MeasurementScaleMP')  # Field name made lowercase.
    completedmc = models.SmallIntegerField(db_column='CompletedMC')  # Field name made lowercase.
    completedapl = models.SmallIntegerField(db_column='CompletedAPL')  # Field name made lowercase.
    completedacl = models.SmallIntegerField(db_column='CompletedACL')  # Field name made lowercase.
    completedlt = models.SmallIntegerField(db_column='CompletedLT')  # Field name made lowercase.
    completeddes = models.SmallIntegerField(db_column='CompletedDES')  # Field name made lowercase.
    completeddoc = models.SmallIntegerField(db_column='CompletedDOC')  # Field name made lowercase.
    completedsp = models.SmallIntegerField(db_column='CompletedSP')  # Field name made lowercase.
    quality = models.CharField(db_column='Quality', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    stitching = models.CharField(db_column='Stitching', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    packing = models.CharField(db_column='Packing', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='Comments', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isprinted = models.SmallIntegerField(db_column='IsPrinted')  # Field name made lowercase.
    isembroided = models.SmallIntegerField(db_column='IsEmbroided')  # Field name made lowercase.
    isothers = models.SmallIntegerField(db_column='IsOthers')  # Field name made lowercase.
    printinstr = models.CharField(db_column='PrintInstr', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    embroidryinstr = models.CharField(db_column='EmbroidryInstr', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    othersinstr = models.CharField(db_column='OthersInstr', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    workbookno = models.CharField(db_column='WorkBookNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    workbookno_a = models.CharField(db_column='WorkBookNo_A', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    extra = models.DecimalField(db_column='Extra', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    authorized = models.SmallIntegerField(db_column='Authorized')  # Field name made lowercase.
    mpauthorized = models.SmallIntegerField(db_column='MPAuthorized')  # Field name made lowercase.
    acceauthorized = models.SmallIntegerField(db_column='AcceAuthorized')  # Field name made lowercase.
    supplierid = models.IntegerField(db_column='SupplierID')  # Field name made lowercase.
    yarnsupplied = models.SmallIntegerField(db_column='YarnSupplied')  # Field name made lowercase.
    fabricsupplied = models.SmallIntegerField(db_column='FabricSupplied')  # Field name made lowercase.
    productiontype = models.SmallIntegerField(db_column='ProductionType')  # Field name made lowercase.
    productionid = models.IntegerField(db_column='ProductionID')  # Field name made lowercase.
    merchandiserid = models.IntegerField(db_column='MerchandiserID')  # Field name made lowercase.
    qltycontrollerid = models.IntegerField(db_column='QltyControllerID')  # Field name made lowercase.
    mpyear = models.SmallIntegerField(db_column='MPYear')  # Field name made lowercase.
    mprefno = models.CharField(db_column='MPRefNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mpdate = models.DateTimeField(db_column='MPDate', blank=True, null=True)  # Field name made lowercase.
    refno = models.CharField(db_column='RefNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mainimagepath = models.CharField(db_column='MainImagePath', max_length=511, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    shipmentcompleted = models.SmallIntegerField(db_column='ShipmentCompleted')  # Field name made lowercase.
    closed = models.SmallIntegerField(db_column='Closed')  # Field name made lowercase.
    yarnporaised = models.IntegerField(db_column='YarnPORaised')  # Field name made lowercase.
    fabricporaised = models.IntegerField(db_column='FabricPORaised')  # Field name made lowercase.
    acceporaised = models.IntegerField(db_column='AccePORaised')  # Field name made lowercase.
    yarndelvraised = models.IntegerField(db_column='YarnDelvRaised')  # Field name made lowercase.
    knittingpgmraised = models.IntegerField(db_column='KnittingPgmRaised')  # Field name made lowercase.
    fabricdelvraised = models.IntegerField(db_column='FabricDelvRaised')  # Field name made lowercase.
    completedwo = models.SmallIntegerField(db_column='CompletedWO')  # Field name made lowercase.
    repeatorders = models.SmallIntegerField(db_column='RepeatOrders', blank=True, null=True)  # Field name made lowercase.
    seasonid = models.IntegerField(db_column='SeasonID', blank=True, null=True)  # Field name made lowercase.
    seasonyear = models.SmallIntegerField(db_column='SeasonYear', blank=True, null=True)  # Field name made lowercase.
    statusid = models.SmallIntegerField(db_column='StatusID')  # Field name made lowercase.
    sorequired = models.SmallIntegerField(db_column='SORequired', blank=True, null=True)  # Field name made lowercase.
    materialplanning = models.SmallIntegerField(db_column='MaterialPlanning', blank=True, null=True)  # Field name made lowercase.
    acceplan_employeeid = models.IntegerField(db_column='AccePlan_EmployeeID', blank=True, null=True)  # Field name made lowercase.
    orderfollowup_employeeid = models.IntegerField(db_column='OrderFollowUp_EmployeeID', blank=True, null=True)  # Field name made lowercase.
    duration = models.DecimalField(db_column='Duration', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    joborderraised = models.SmallIntegerField(db_column='JobOrderRaised', blank=True, null=True)  # Field name made lowercase.
    horefno = models.CharField(db_column='HORefNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prodauthorized = models.SmallIntegerField(db_column='ProdAuthorized', blank=True, null=True)  # Field name made lowercase.
    acceincharge_employeeid = models.IntegerField(db_column='AcceIncharge_EmployeeID', blank=True, null=True)  # Field name made lowercase.
    ordercancelled = models.SmallIntegerField(db_column='OrderCancelled', blank=True, null=True)  # Field name made lowercase.
    cancel = models.SmallIntegerField(db_column='Cancel', blank=True, null=True, db_comment='Cancelling the order thru Orde')  # Field name made lowercase.
    yarnstraised = models.IntegerField(db_column='YarnSTRaised', blank=True, null=True)  # Field name made lowercase.
    fabricstraised = models.IntegerField(db_column='FabricSTRaised', blank=True, null=True)  # Field name made lowercase.
    fabriccutraised = models.IntegerField(db_column='FabricCutRaised', blank=True, null=True)  # Field name made lowercase.
    yarnstcraised = models.IntegerField(db_column='YarnSTCRaised', blank=True, null=True)  # Field name made lowercase.
    fabricstcraised = models.IntegerField(db_column='FabricSTCRaised', blank=True, null=True)  # Field name made lowercase.
    fabricincharge_employeeid = models.IntegerField(db_column='FabricIncharge_EmployeeID', blank=True, null=True)  # Field name made lowercase.
    purchaseprice = models.DecimalField(db_column='PurchasePrice', max_digits=19, decimal_places=4)  # Field name made lowercase.
    purchasepricetype = models.SmallIntegerField(db_column='PurchasePriceType')  # Field name made lowercase.
    piecercptraised = models.IntegerField(db_column='PieceRcptRaised', blank=True, null=True)  # Field name made lowercase.
    piecestkraised = models.IntegerField(db_column='PieceStkRaised', blank=True, null=True)  # Field name made lowercase.
    pieceprodraised = models.IntegerField(db_column='PieceProdRaised', blank=True, null=True)  # Field name made lowercase.
    aprvlsubraised = models.IntegerField(db_column='AprvlSubRaised', blank=True, null=True)  # Field name made lowercase.
    ihapprvlraised = models.IntegerField(db_column='IHApprvlRaised', blank=True, null=True)  # Field name made lowercase.
    billexpenseraised = models.IntegerField(db_column='BillExpenseRaised', blank=True, null=True)  # Field name made lowercase.
    docproformainvraised = models.IntegerField(db_column='DocProformaInvRaised', blank=True, null=True)  # Field name made lowercase.
    doclcraised = models.IntegerField(db_column='DocLCRaised', blank=True, null=True)  # Field name made lowercase.
    docinvraised = models.IntegerField(db_column='DocInvRaised', blank=True, null=True)  # Field name made lowercase.
    gendlvyraised = models.IntegerField(db_column='GenDlvyRaised', blank=True, null=True)  # Field name made lowercase.
    geninwdraised = models.IntegerField(db_column='GenInwdRaised', blank=True, null=True)  # Field name made lowercase.
    mktcostingraised = models.IntegerField(db_column='MktCostingRaised', blank=True, null=True)  # Field name made lowercase.
    accplanraised = models.IntegerField(db_column='AccPlanRaised', blank=True, null=True)  # Field name made lowercase.
    prdrateplanraised = models.IntegerField(db_column='PrdRatePlanRaised', blank=True, null=True)  # Field name made lowercase.
    prdctngfabrcptraised = models.IntegerField(db_column='PrdCtngFabRcptRaised', blank=True, null=True)  # Field name made lowercase.
    qcprdcommentsraised = models.IntegerField(db_column='QCPrdCommentsRaised', blank=True, null=True)  # Field name made lowercase.
    qcmesurechartraised = models.IntegerField(db_column='QCMesureChartRaised', blank=True, null=True)  # Field name made lowercase.
    qccmtquotraised = models.IntegerField(db_column='QCCMTQuotRaised', blank=True, null=True)  # Field name made lowercase.
    sampleorderraised = models.IntegerField(db_column='SampleOrderRaised', blank=True, null=True)  # Field name made lowercase.
    sheduleplanraised = models.IntegerField(db_column='ShedulePlanRaised', blank=True, null=True)  # Field name made lowercase.
    prdsheduleraised = models.IntegerField(db_column='PrdSheduleRaised', blank=True, null=True)  # Field name made lowercase.
    despatchstatusraised = models.IntegerField(db_column='DespatchStatusRaised', blank=True, null=True)  # Field name made lowercase.
    workorderraised = models.IntegerField(db_column='WorkOrderRaised', blank=True, null=True)  # Field name made lowercase.
    accstkraised = models.IntegerField(db_column='AccStkRaised', blank=True, null=True)  # Field name made lowercase.
    accstkcompraised = models.IntegerField(db_column='AccStkCompRaised', blank=True, null=True)  # Field name made lowercase.
    styarnreqraised = models.IntegerField(db_column='STYarnReqRaised', blank=True, null=True)  # Field name made lowercase.
    stfabricreqraised = models.IntegerField(db_column='STFabricReqRaised', blank=True, null=True)  # Field name made lowercase.
    accporaised = models.IntegerField(db_column='AccPORaised', blank=True, null=True)  # Field name made lowercase.
    accprocessdlvyraised = models.IntegerField(db_column='AccProcessDlvyRaised', blank=True, null=True)  # Field name made lowercase.
    recalculatepl = models.SmallIntegerField(db_column='ReCalculatePL')  # Field name made lowercase.
    imagedesc = models.CharField(db_column='ImageDesc', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    insdate = models.DateTimeField(blank=True, null=True)
    vessel_dt = models.DateTimeField(db_column='Vessel_DT', blank=True, null=True)  # Field name made lowercase.
    contractno = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ordid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'txOrderDetStyles'
