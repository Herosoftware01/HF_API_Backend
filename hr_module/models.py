from django.db import models

class Committee_Master(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    committee_name = models.CharField(max_length=100, unique=True)
    committee_members = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.committee_name

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


class ResignDtls(models.Model):
    slno = models.BigIntegerField(db_column='SlNo',primary_key=True)  # Field name made lowercase.
    code = models.IntegerField()
    photo = models.CharField(max_length=400, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    resigndt = models.DateTimeField(db_column='resignDt', blank=True, null=True)  # Field name made lowercase.
    days_worked = models.IntegerField(db_column='Days_Worked', blank=True, null=True)  # Field name made lowercase.
    ldt = models.DateTimeField(db_column='Ldt', blank=True, null=True)  # Field name made lowercase.

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

    class Meta:
        managed = False
        db_table = 'vue_empjoin'


class ViewActshift(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='Unitname', max_length=50)  # Field name made lowercase.
    id = models.IntegerField()
    actshift = models.DecimalField(db_column='Actshift', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    mno = models.IntegerField(blank=True, null=True)
    yr = models.IntegerField(blank=True, null=True)
    monthname = models.CharField(db_column='MonthName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_actshift'


class ViewActshiftDay(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='Unitname', max_length=50)  # Field name made lowercase.
    id = models.IntegerField()
    dt = models.DateTimeField()
    actshift = models.DecimalField(db_column='Actshift', max_digits=18, decimal_places=2)  # Field name made lowercase.
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_actshift_day'


class ViewEmployeeSalaryDetails(models.Model):
    company = models.CharField(max_length=50, blank=True, null=True)
    esino = models.CharField(max_length=50, blank=True, null=True)
    pfno = models.CharField(max_length=100, blank=True, null=True)
    uanno = models.CharField(max_length=50, blank=True, null=True)
    doj = models.DateTimeField(blank=True, null=True)
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    fname = models.CharField(db_column='Fname', max_length=1)  # Field name made lowercase.
    sex = models.CharField(max_length=6)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mon = models.IntegerField(db_column='MON', blank=True, null=True)  # Field name made lowercase.
    yr = models.IntegerField(blank=True, null=True)
    monthname = models.CharField(max_length=30, blank=True, null=True)
    day = models.DecimalField(db_column='DAY', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ot = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    salary1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paidholiday = models.IntegerField()
    onehr_wag = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    double_wag = models.DecimalField(max_digits=24, decimal_places=6, blank=True, null=True)
    ot_amt = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    sum_ofwage = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)
    hra = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    earned = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)
    esi = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)
    pf = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)
    netamt = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_employee_salary_details'

class ViewEmployeeAtt(models.Model):
    code = models.IntegerField()
    dt = models.DateTimeField(blank=True, null=True)
    ashift = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    aot = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    a = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_employee_att'



class TrsOverAllemb(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Trs_Over_AllEmb'


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


class ViewAbsentList(models.Model):
    id = models.IntegerField(primary_key=True)
    unitname = models.CharField(max_length=50)
    month = models.CharField(max_length=3, blank=True, null=True,db_column='m')
    year = models.IntegerField(blank=True, null=True, db_column='y')
    workingdays = models.IntegerField(blank=True, null=True, db_column='days')
    leave_days = models.IntegerField(blank=True, null=True, db_column='leavdays')
    informed = models.IntegerField(blank=True, null=True, db_column='inl')
    shiftdays = models.IntegerField(blank=True, null=True, db_column='actshiftdays')
    name = models.CharField(max_length=100, blank=True, null=True)
    photo = models.CharField(max_length=443, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    stat = models.IntegerField(db_column='Stat')
    mon_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'view_absent_list'

class ViewStaffAbsentMonth(models.Model):
    rn = models.BigIntegerField(primary_key=True)
    yr = models.IntegerField(blank=True, null=True)
    mn = models.IntegerField(blank=True, null=True)
    monthname = models.CharField(max_length=30, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    absentdays = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70)
    wunit = models.CharField(max_length=70, blank=True, null=True)
    cat = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_staff_absent_month'


class ViewStaffLateMonth(models.Model):
    rn = models.BigIntegerField(blank=True, null=True)
    yr = models.IntegerField(db_column='Yr', blank=True, null=True)
    mn = models.IntegerField(db_column='Mn', blank=True, null=True) 
    monthname = models.CharField(db_column='MonthName', max_length=30, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    wunit = models.CharField(max_length=70, blank=True, null=True)
    cat = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    latedays = models.IntegerField(db_column='LateDays', blank=True, null=True)
    latemins = models.IntegerField(db_column='LateMins', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_staff_late_month'

class VueOtAmountStaff(models.Model):  
    wunit = models.CharField(max_length=70, blank=True, null=True)
    cat = models.CharField(db_column='ACAT', max_length=70, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    otamt = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    otmins = models.DecimalField(db_column='OTmins', max_digits=38, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=70)
    monthname = models.CharField(db_column='Month_Name', max_length=3, blank=True, null=True)
    mn = models.IntegerField(db_column='MonthNo', blank=True, null=True)
    yr = models.IntegerField(db_column='YR', blank=True, null=True)
    code = models.IntegerField(db_column='EmpID')

    class Meta:
        managed = False
        db_table = 'vue_ot_amount_staff'