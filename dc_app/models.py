from django.db import models

class ViewCuttingDelPrint(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo')  # Field name made lowercase.
    name = models.CharField(max_length=35)
    b = models.CharField(max_length=8000, blank=True, null=True)
    comboclr = models.CharField(max_length=50, blank=True, null=True)
    sizid = models.IntegerField(db_column='SizID')  # Field name made lowercase.
    noofpcs = models.IntegerField(blank=True, null=True)
    lotno = models.CharField(db_column='LotNo', max_length=10)  # Field name made lowercase.
    frkg = models.DecimalField(db_column='FRKG', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fdkg = models.DecimalField(db_column='FDKG', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    frmt = models.DecimalField(db_column='FRMT', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fdmt = models.DecimalField(db_column='FDMT', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    mbud = models.CharField(db_column='MBUD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dcaddres = models.CharField(max_length=750, blank=True, null=True)
    del_field = models.CharField(db_column='del', max_length=750, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sample_descr = models.CharField(db_column='Sample_Descr', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_cutting_del_print'


class ViewKnitDelivery(models.Model):
    sl = models.BigIntegerField(db_column='Sl',primary_key=True)  # Field name made lowercase.
    itemno1 = models.SmallIntegerField()
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=12)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(db_column='Place', max_length=66, blank=True, null=True)  # Field name made lowercase.
    reg = models.CharField(db_column='Reg', max_length=36, blank=True, null=True)  # Field name made lowercase.
    hed = models.CharField(db_column='Hed', max_length=22)  # Field name made lowercase.
    knit_name = models.CharField(db_column='Knit_Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    p_add1 = models.CharField(db_column='P_Add1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    p_add2 = models.CharField(db_column='P_Add2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    p_add3 = models.CharField(db_column='P_Add3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    p_gst = models.CharField(db_column='P_Gst', max_length=66, blank=True, null=True)  # Field name made lowercase.
    dcno = models.IntegerField(db_column='DCNo')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    pgmo = models.IntegerField(db_column='PGMo')  # Field name made lowercase.
    pgm_date = models.DateTimeField(db_column='PGM_Date')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=58, blank=True, null=True)  # Field name made lowercase.
    style_no = models.CharField(db_column='Style_No', max_length=35)  # Field name made lowercase.
    process_descr = models.CharField(db_column='Process_descr', max_length=35)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=35)  # Field name made lowercase.
    incharge = models.CharField(db_column='Incharge', max_length=35)  # Field name made lowercase.
    yarn = models.CharField(db_column='Yarn', max_length=122, blank=True, null=True)  # Field name made lowercase.
    mill = models.CharField(db_column='Mill', max_length=35, blank=True, null=True)  # Field name made lowercase.
    full_bags = models.IntegerField(db_column='Full_Bags')  # Field name made lowercase.
    loose_bags = models.IntegerField(db_column='Loose_Bags')  # Field name made lowercase.
    full_cones = models.IntegerField(db_column='Full_Cones', blank=True, null=True)  # Field name made lowercase.
    loose_cones = models.IntegerField(db_column='Loose_Cones', blank=True, null=True)  # Field name made lowercase.
    full_weight = models.DecimalField(db_column='Full_Weight', max_digits=18, decimal_places=4)  # Field name made lowercase.
    loose_weight = models.DecimalField(db_column='Loose_Weight', max_digits=18, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_knit_delivery'

class VueAccProdDel(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    auom = models.CharField(max_length=25)
    auomscale = models.IntegerField()
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    uom = models.CharField(max_length=25, blank=True, null=True)
    uomscale = models.IntegerField(blank=True, null=True)
    siz = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    acc_grp = models.CharField(max_length=35)
    acc_name = models.CharField(max_length=35)
    incharge = models.CharField(max_length=35)
    frmdpt = models.CharField(max_length=35)
    todept = models.CharField(max_length=35)
    supplier = models.CharField(max_length=35)
    supadd1 = models.CharField(max_length=50)
    supadd2 = models.CharField(max_length=50)
    supadd3 = models.CharField(max_length=50)
    supgst = models.CharField(max_length=66)
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
    no = models.IntegerField()
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(max_length=12)
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(max_length=66, blank=True, null=True)
    regno = models.CharField(db_column='RegNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_acc_prod_del'

class TrsGatemodule(models.Model):
    module = models.CharField(db_column='Module', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    qr_code_dtls = models.CharField(db_column='Qr_Code_Dtls', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companyid = models.IntegerField(db_column='CompanyID')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    no = models.IntegerField(db_column='No')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    jobno = models.CharField(db_column='Jobno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    suppliername = models.CharField(db_column='SupplierName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    descr = models.CharField(db_column='Descr', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    rls_bdls = models.IntegerField()
    kg = models.DecimalField(max_digits=18, decimal_places=3)
    mtrs = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Trs_Gatemodule'