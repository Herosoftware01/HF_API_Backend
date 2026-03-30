from django.db import models
from django.db import models
from django.core.exceptions import ValidationError


class QcAdminMistake(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='qc_admin_mistakes/')

    def __str__(self):
        return self.name
    

class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Line(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lines")
    line_number = models.IntegerField()

    class Meta:
        unique_together = ['unit', 'line_number']

    def __str__(self):
        return f"{self.unit.name} - Line {self.line_number}"


class qc_piece_data(models.Model):
    bundle_no = models.CharField(max_length=20)
    bundle_id = models.CharField(max_length=20)
    unit =models.IntegerField()
    line =models.IntegerField()
    jobno = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    total_pieces = models.IntegerField()
    piece_no = models.IntegerField()
    category = models.CharField(max_length=50)
    mistake_name = models.CharField(max_length=50)
    mistake_count = models.IntegerField()
    total_mistake = models.IntegerField()
    mistake_percentage = models.CharField(max_length=20)
    qc_type = models.CharField(max_length=50)

class qc_piece_final(models.Model):
    bundle_no = models.CharField(max_length=20)
    bundle_id = models.CharField(max_length=20)
    unit =models.IntegerField()
    line =models.IntegerField()
    jobno = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    total_pieces = models.IntegerField()
    checked_piece = models.IntegerField()
    force_save = models.BooleanField(default=False)
    qc_type = models.CharField(max_length=50)


class machine_details(models.Model):
    Identity = models.CharField(max_length=100)
    Item = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    mcgrp = models.CharField(max_length=50,blank=True, null=True)


class MachineAllocation(models.Model):
    machine = models.ForeignKey(
        machine_details,
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )

    line = models.ForeignKey(
        Line,
        on_delete=models.CASCADE,
    )

    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass
        # constraints = [
        #     models.UniqueConstraint(fields=['machine'], name='one_machine_one_line')
        # ]

    def clean(self):
        if self.line.unit != self.unit:
            raise ValidationError("Selected line does not belong to the selected unit")

    def __str__(self):
        return f"{self.machine.identity} → {self.unit.name} - Line {self.line.line_number}"




class Empwisesal(models.Model):
    dept = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    salary = models.DecimalField(db_column='Salary', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    night = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sl = models.IntegerField(blank=True, null=True)
    orissa = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    grp1 = models.IntegerField(blank=True, null=True)
    grp2 = models.IntegerField(blank=True, null=True)
    wrkunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    prs = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    disprs = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    hostel = models.CharField(db_column='Hostel', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    roomdtls = models.CharField(db_column='Roomdtls', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    shift_contract = models.CharField(db_column='Shift_Contract', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reportsl = models.IntegerField(db_column='Reportsl', blank=True, null=True)  # Field name made lowercase.
    intercom = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mobile = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    attach = models.CharField(max_length=1550, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    bank = models.CharField(db_column='Bank', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    accountdetails = models.CharField(db_column='Accountdetails', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    grp3 = models.IntegerField(blank=True, null=True)
    salary1 = models.DecimalField(db_column='Salary1', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otallowed = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    branch = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    badd = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ifscno = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    bank1 = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    branch1 = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    badd1 = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ifscno1 = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    accountdetails1 = models.CharField(db_column='Accountdetails1', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bact = models.IntegerField(blank=True, null=True)
    qualification = models.CharField(db_column='Qualification', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    jdt = models.DateTimeField(blank=True, null=True)
    joindt = models.DateTimeField(db_column='JoinDt', blank=True, null=True)  # Field name made lowercase.
    resigndt = models.DateTimeField(db_column='resignDt', blank=True, null=True)  # Field name made lowercase.
    rdt = models.DateTimeField(blank=True, null=True)
    rsysdt = models.DateTimeField(blank=True, null=True)
    grp4 = models.IntegerField(blank=True, null=True)
    pftype = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    curwrkunit = models.CharField(db_column='CurWrkUnit', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    inch = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nattgrp = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    northindian = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    inspection = models.CharField(db_column='Inspection', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ins_incharge = models.CharField(db_column='Ins_Incharge', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    atharrecd = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    atharcdob = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    aempwatch = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    photo = models.CharField(max_length=400, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    empprs = models.CharField(db_column='Empprs', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    skilled = models.CharField(db_column='Skilled', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ej = models.DateTimeField(blank=True, null=True)
    vanno = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    esino = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pfno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ladd1 = models.CharField(db_column='LADD1', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    padd1 = models.CharField(db_column='PADD1', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    padd2 = models.CharField(db_column='PADD2', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pcity = models.CharField(db_column='PCITY', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pstate = models.CharField(db_column='PSTATE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ppincode = models.CharField(db_column='PPINCODE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    emc = models.CharField(db_column='EMC', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ladd2 = models.CharField(db_column='LADD2', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lcity = models.CharField(db_column='LCITY', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lstate = models.CharField(db_column='LSTATE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lpincode = models.CharField(db_column='LPINCODE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    hra_per = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    hra_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    relation = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emc_pers = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pcsrate = models.CharField(db_column='Pcsrate', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    p_inch = models.IntegerField(db_column='P_Inch', blank=True, null=True)  # Field name made lowercase.
    l = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    grpnew = models.IntegerField(db_column='grpNew', blank=True, null=True)  # Field name made lowercase.
    mon_lab = models.CharField(db_column='Mon_Lab', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comm_lab = models.CharField(db_column='Comm_Lab', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comm_amt = models.DecimalField(db_column='Comm_Amt', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    comm_grp = models.CharField(db_column='Comm_grp', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pcat = models.IntegerField(blank=True, null=True)
    dcs = models.IntegerField(blank=True, null=True)
    bg = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    approved = models.CharField(db_column='Approved', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tasstaff = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monthlysalary = models.CharField(db_column='MonthlySalary', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mjoindt = models.DateField(blank=True, null=True)
    # ncat = models.ForeignKey('MempCategory', models.DO_NOTHING, blank=True, null=True)
    mcategory = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vc = models.TextField()  # This field type is a guess.
    # id = models.AutoField()
    aliasname = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    whatsappgrp = models.CharField(db_column='WhatsappGrp', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddt = models.DateTimeField(blank=True, null=True)
    modifieddt = models.DateTimeField(blank=True, null=True)
    dn = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EmpwiseSal'



class emp_allocate(models.Model):
    emp_code = models.CharField(max_length=50)

    machine = models.ForeignKey(
        machine_details,
        on_delete=models.CASCADE,
        related_name="emp_allocations"
    )

    date = models.DateField(auto_now_add=True)
    unit = models.IntegerField()
    line = models.IntegerField()
    status = models.BooleanField(default=False)


class VueProcessSequence(models.Model):
    jobno = models.CharField(db_column='JOBNO', max_length=50)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    slno = models.BigIntegerField(blank=True, null=True)
    tbid = models.IntegerField(db_column='TBID')  # Field name made lowercase.
    trn = models.CharField(db_column='TRN', max_length=1)  # Field name made lowercase.
    sl = models.IntegerField(db_column='SL',primary_key=True)  # Field name made lowercase.
    sl1 = models.IntegerField(db_column='SL1')  # Field name made lowercase.
    prsid = models.IntegerField(db_column='PRSID')  # Field name made lowercase.
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)  # Field name made lowercase.
    mc = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Vue_Process_Sequence'
