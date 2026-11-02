# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewEmployeePayslipDetails(models.Model):
    from_date = models.DateTimeField(db_column='From_Date')  # Field name made lowercase.
    to_date = models.DateTimeField(db_column='To_Date', blank=True, null=True)  # Field name made lowercase.
    un = models.CharField(max_length=50, blank=True, null=True)
    esino = models.CharField(db_column='ESINO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pfno = models.CharField(db_column='PFNO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uanno = models.CharField(db_column='Uanno', max_length=50, blank=True, null=True)  # Field name made lowercase.
    doj = models.DateTimeField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    empname = models.CharField(db_column='EmpName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=1)  # Field name made lowercase.
    sex = models.CharField(max_length=6)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    day = models.DecimalField(max_digits=24, decimal_places=2, blank=True, null=True)
    ot = models.IntegerField(blank=True, null=True)
    ipaysalary = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paidh = models.DecimalField(max_digits=38, decimal_places=20, blank=True, null=True)
    onehr_wag = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    dobwag = models.DecimalField(max_digits=24, decimal_places=6, blank=True, null=True)
    ot_amt = models.DecimalField(max_digits=35, decimal_places=6, blank=True, null=True)
    sum_ofwage = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    hra = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    earned = models.DecimalField(max_digits=38, decimal_places=6, blank=True, null=True)
    nesi = models.DecimalField(db_column='nESI', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    npf = models.DecimalField(db_column='nPF', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nnetamt = models.DecimalField(db_column='nNetamt', max_digits=23, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_employee_payslip_details'
