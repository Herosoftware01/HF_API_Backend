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