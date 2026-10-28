from django.db import models

class VueAccPodetails1(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)
    companyid = models.IntegerField(db_column='CompanyID')
    year = models.IntegerField(db_column='Year')
    no = models.IntegerField(db_column='No')
    taxdetails = models.CharField(db_column='TaxDetails', max_length=500, blank=True, null=True)
    taxamount = models.DecimalField(db_column='TaxAmount', max_digits=19, decimal_places=4, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vue_acc_podetails1'

class VueAccPodetails(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)
    companyid = models.SmallIntegerField(db_column='CompanyID')
    year = models.SmallIntegerField(db_column='Year')
    no = models.IntegerField(db_column='No')
    companyname = models.CharField(max_length=12)
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)
    gst = models.CharField(max_length=36, blank=True, null=True)
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)
    hed = models.CharField(max_length=24)
    pono = models.IntegerField()
    date = models.DateTimeField(db_column='Date')
    ag = models.CharField(db_column='Ag', max_length=21)
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)
    styleno = models.CharField(db_column='StyleNo', max_length=35)
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=35)
    deliveryothers = models.CharField(db_column='DeliveryOthers', max_length=50, blank=True, null=True)
    accname = models.CharField(max_length=35)
    itemspec = models.CharField(db_column='ItemSpec', max_length=255, blank=True, null=True)
    szname = models.CharField(max_length=50, blank=True, null=True)
    sizespec = models.CharField(db_column='SizeSpec', max_length=255, blank=True, null=True)
    clrname = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4)
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4)
    rate = models.DecimalField(db_column='Rate', max_digits=19, decimal_places=4, blank=True, null=True)
    per = models.CharField(db_column='Per', max_length=50, blank=True, null=True)
    hsncode = models.CharField(max_length=20, blank=True, null=True)
    tax = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(db_column='Amount', max_digits=19, decimal_places=4, blank=True, null=True)
    supplier = models.CharField(max_length=35, blank=True, null=True)
    sadd1 = models.CharField(max_length=50, blank=True, null=True)
    sadd2 = models.CharField(max_length=50, blank=True, null=True)
    sadd3 = models.CharField(max_length=50, blank=True, null=True)
    scity = models.CharField(max_length=51, blank=True, null=True)
    gstno = models.CharField(db_column='GSTNo', max_length=50, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vue_acc_podetails'

class TrsGatemoduleInward(models.Model):
    module = models.CharField(db_column='Module', max_length=50)
    qr = models.CharField(primary_key=True, db_column='Qr_Code_Dtls', max_length=200)
    companyid = models.IntegerField(db_column='CompanyID')
    year = models.IntegerField(db_column='Year')
    no = models.IntegerField(db_column='No')
    date = models.DateTimeField(db_column='Date')
    jobno = models.CharField(db_column='Jobno', max_length=50, blank=True, null=True)
    suppliername = models.CharField(db_column='SupplierName', max_length=200)
    descr = models.CharField(db_column='Descr', max_length=500)
    rls_bdls = models.IntegerField()
    kg = models.DecimalField(max_digits=18, decimal_places=3)
    mtrs = models.DecimalField(max_digits=18, decimal_places=2)
    verify = models.CharField(db_column='Verify', max_length=50, blank=True, null=True)
    prepered = models.CharField(max_length=50, blank=True, null=True)
    fhero = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trs_Gatemodule_Inward'



class Lotsticker(models.Model):
    sl = models.AutoField(db_column='Sl', primary_key=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fabric = models.CharField(db_column='Fabric', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    rollno = models.CharField(db_column='RollNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dcno = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    wgt = models.DecimalField(db_column='Wgt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    m1 = models.CharField(db_column='M1', max_length=550, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    m2 = models.CharField(db_column='M2', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m3 = models.CharField(db_column='M3', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m4 = models.CharField(db_column='M4', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m5 = models.CharField(db_column='M5', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m6 = models.CharField(db_column='M6', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m7 = models.CharField(db_column='M7', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m8 = models.CharField(db_column='M8', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m9 = models.CharField(db_column='M9', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m10 = models.CharField(db_column='M10', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    m12 = models.CharField(db_column='M12', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fdia = models.CharField(db_column='Fdia', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mtr = models.DecimalField(db_column='Mtr', max_digits=18, decimal_places=2)  # Field name made lowercase.
    m11 = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    jobno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dia = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    gsm = models.IntegerField(blank=True, null=True)
    re = models.CharField(max_length=650, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    em = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    u = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LotSticker'
