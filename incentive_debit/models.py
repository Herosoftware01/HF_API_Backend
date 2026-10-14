from django.db import models

class Employeeworking(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    workunit = models.CharField(db_column='WorkUnit', max_length=70, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=70, blank=True, null=True)
    type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'EmployeeWorking'

class Empwisesal(models.Model):
    dept = models.CharField(max_length=50, blank=True, null=True)
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    salary = models.DecimalField(
        db_column='Salary',
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(max_length=25, blank=True, null=True)
    photo = models.CharField(max_length=400, blank=True, null=True)

    designation = models.CharField(
        db_column='mcategory',
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'EmpwiseSal'




class Staffdtls(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=70,db_collation='SQL_Latin1_General_CP1_CI_AS',blank=True,null=True)
    photo = models.CharField(max_length=400,db_collation='SQL_Latin1_General_CP1_CI_AS',blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'staffdtls'


class Staffodtls(models.Model):
    code = models.OneToOneField(
        Staffdtls,
        to_field='code',
        db_column='code',
        primary_key=True,
        on_delete=models.DO_NOTHING,
        related_name='office_details'
    )

    name = models.CharField(
        max_length=70,
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )
    dept = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        db_column='wunit',
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )
    Designation = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        db_column='cat',
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )
    status = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_collation='SQL_Latin1_General_CP1_CI_AS'
    )

    class Meta:
        managed = False
        db_table = 'staffodtls'




class IncdebStatus(models.Model):
    req_id = models.AutoField(db_column='Req_ID', primary_key=True)  # Field name made lowercase.
    req_dt = models.DateField(db_column='Req_Dt', blank=True, null=True)  # Field name made lowercase.
    req_type = models.CharField(max_length=150, db_column='Req_Type', blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField(db_column='Code', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dept_unit = models.CharField(db_column='Dept_Unit', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    design_category = models.CharField(db_column='Design_category', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    purpose = models.CharField(db_column='Purpose', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    amt = models.DecimalField(db_column='Amt', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status_dt = models.DateField(db_column='Status_Dt', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IncDeb_Status'


class IncdebPurpose(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ste = models.CharField(db_column='STE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    purpose = models.CharField(db_column='Purpose', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IncDeb_Purpose'


class IncdebUsers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    screen_per = models.CharField(db_column='Screen_per', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    app_n = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IncDeb_Users'
