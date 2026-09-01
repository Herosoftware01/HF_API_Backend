from django.db import models

class ViewCuttingDelPrint(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True) 
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

class CuttingPrintembdel(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True) 
    frm = models.CharField(max_length=750, blank=True, null=True)
    toad = models.CharField(max_length=750, blank=True, null=True)
    id = models.IntegerField()
    dt = models.DateTimeField()
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True) 
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True) 
    qrid = models.IntegerField(db_column='QRID') 
    comboclr = models.CharField(max_length=50)
    lotno = models.CharField(max_length=50)
    portion_des = models.CharField(db_column='Portion_des', max_length=50, blank=True, null=True) 
    name = models.CharField(db_column='Name', max_length=35) 
    noofpcs = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vue_cutting_printembdel'

class ViewYarnProcessDelivery(models.Model):
    sl = models.BigIntegerField(db_column='Sl', primary_key=True)
    itemno1 = models.SmallIntegerField()
    companyid = models.SmallIntegerField()
    year = models.SmallIntegerField()
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)
    companyname = models.CharField(db_column='CompanyName', max_length=12)
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)
    place = models.CharField(db_column='Place', max_length=66, blank=True, null=True)
    reg = models.CharField(db_column='Reg', max_length=36, blank=True, null=True)
    hed = models.CharField(db_column='Hed', max_length=44, blank=True, null=True)
    sup_name = models.CharField(db_column='sup_Name', max_length=35, blank=True, null=True)
    p_add1 = models.CharField(db_column='P_Add1', max_length=50, blank=True, null=True)
    p_add2 = models.CharField(db_column='P_Add2', max_length=50, blank=True, null=True)
    p_add3 = models.CharField(db_column='P_Add3', max_length=50, blank=True, null=True)
    p_gst = models.CharField(db_column='P_Gst', max_length=66, blank=True, null=True)
    dcno = models.IntegerField(db_column='DCNo')
    date = models.DateTimeField(db_column='Date')
    orderno = models.CharField(db_column='OrderNo', max_length=58, blank=True, null=True)
    style_no = models.CharField(db_column='Style_No', max_length=35)
    process_descr = models.CharField(db_column='Process_descr', max_length=35)
    department = models.CharField(db_column='Department', max_length=35)
    incharge = models.CharField(db_column='Incharge', max_length=35)
    yarn = models.CharField(db_column='Yarn', max_length=122, blank=True, null=True)
    mill = models.CharField(db_column='Mill', max_length=35, blank=True, null=True)
    full_bags = models.IntegerField(db_column='Full_Bags', blank=True, null=True)
    loose_bags = models.IntegerField(db_column='Loose_Bags', blank=True, null=True)
    full_cones = models.IntegerField(db_column='Full_Cones')
    loose_cones = models.IntegerField(db_column='Loose_Cones', blank=True, null=True)
    full_weight = models.DecimalField(db_column='Full_Weight', max_digits=18, decimal_places=4)
    loose_weight = models.DecimalField(db_column='Loose_Weight', max_digits=18, decimal_places=4)
    dye_clr = models.CharField(max_length=50, blank=True, null=True)
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)
    del_to = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'view_yarn_process_delivery'


class ViewKnitDelivery(models.Model):
    sl = models.BigIntegerField(db_column='Sl',primary_key=True)  # Field name made lowercase.
    itemno1 = models.SmallIntegerField()
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=12)  # Field name made lowercase.
    companyid = models.IntegerField(db_column='CompanyID') 
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
    companyid = models.IntegerField(db_column='CompanyID')
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    place = models.CharField(max_length=66, blank=True, null=True)
    regno = models.CharField(db_column='RegNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_acc_prod_del'

class VueAccProcDel(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    auom = models.CharField(max_length=25)
    auomscale = models.IntegerField()
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    uom = models.CharField(max_length=25, blank=True, null=True)
    uomscale = models.IntegerField(blank=True, null=True)
    companyid = models.IntegerField(db_column='CompanyID') 
    siz = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    acc_grp = models.CharField(max_length=35)
    acc_name = models.CharField(max_length=35)
    incharge = models.CharField(max_length=1)
    frmdpt = models.CharField(max_length=35)
    todept = models.CharField(max_length=1)
    supplier = models.CharField(max_length=35)
    supadd1 = models.CharField(max_length=50)
    supadd2 = models.CharField(max_length=50)
    supadd3 = models.CharField(max_length=50)
    supgst = models.CharField(max_length=66)
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
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
    dye_clr = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
      managed = False
      db_table = 'vue_acc_proc_del'


class VueAccInhTransfer(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo',  primary_key=True)  # Field name made lowercase.
    altquantity = models.DecimalField(db_column='AltQuantity', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    auom = models.CharField(max_length=25, blank=True, null=True)
    auomscale = models.IntegerField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    no = models.IntegerField()
    uom = models.CharField(max_length=25, blank=True, null=True)
    uomscale = models.IntegerField(blank=True, null=True)
    siz = models.CharField(max_length=50, blank=True, null=True)
    colour = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.IntegerField(db_column='CompanyID') 
    acc_grp = models.CharField(max_length=35)
    acc_name = models.CharField(max_length=35)
    incharge = models.CharField(max_length=35)
    frmdpt = models.CharField(max_length=35)
    todept = models.CharField(max_length=35)
    n = models.CharField(db_column='N', max_length=19, blank=True, null=True)  # Field name made lowercase.
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
        db_table = 'vue_acc_inh_transfer'


class ViewFabricDeliveryProcess(models.Model):
    companyid = models.SmallIntegerField(db_column='CompanyID')  # Field name made lowercase.
    year = models.SmallIntegerField(db_column='Year')  # Field name made lowercase.
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    lotno = models.SmallIntegerField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    su_name = models.CharField(db_column='su_Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    su_add1 = models.CharField(max_length=50, blank=True, null=True)
    su_add2 = models.CharField(max_length=50, blank=True, null=True)
    su_pin = models.CharField(max_length=15, blank=True, null=True)
    su_gst = models.CharField(max_length=50, blank=True, null=True)
    cmpy_phone1 = models.CharField(max_length=50, blank=True, null=True)
    companyname = models.CharField(max_length=12)
    cmpy_add1 = models.CharField(max_length=50, blank=True, null=True)
    cmpy_add2 = models.CharField(max_length=50, blank=True, null=True)
    cmpy_place = models.CharField(max_length=66, blank=True, null=True)
    cmpy_gst = models.CharField(max_length=20, blank=True, null=True)
    cmpy_state = models.CharField(max_length=34, blank=True, null=True)
    clr_name = models.CharField(max_length=50, blank=True, null=True)
    del_unit = models.CharField(max_length=35, blank=True, null=True)
    itemno1 = models.SmallIntegerField(db_column='ItemNo1')  # Field name made lowercase.
    ty = models.CharField(max_length=35)
    fab = models.CharField(max_length=35)
    gsm = models.SmallIntegerField(db_column='GSM', blank=True, null=True)  # Field name made lowercase.
    dia = models.CharField(max_length=35)
    finaldia = models.CharField(db_column='FinalDia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rolls = models.IntegerField(db_column='Rolls')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4)  # Field name made lowercase.
    yarninfo = models.CharField(db_column='YarnInfo', max_length=971, blank=True, null=True)  # Field name made lowercase.
    style = models.CharField(max_length=35)
    state_name = models.CharField(db_column='state_Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state_code = models.CharField(max_length=2, blank=True, null=True)
    place = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_fabric_delivery_process'

class ViewUnitPcdelivery(models.Model):
    slno = models.BigIntegerField(primary_key=True)
    frm = models.CharField(max_length=750, blank=True, null=True)
    tou = models.CharField(max_length=750, blank=True, null=True)
    dcno = models.IntegerField()
    dt = models.DateTimeField(blank=True, null=True)
    jobno = models.CharField(db_column='JobNo', max_length=50, blank=True, null=True)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)
    trstype = models.CharField(max_length=50, blank=True, null=True)
    clr = models.CharField(max_length=50, blank=True, null=True)
    lotno = models.CharField(max_length=10, blank=True, null=True)
    siz = models.CharField(max_length=50, blank=True, null=True)
    bdlno = models.IntegerField(blank=True, null=True)
    pcs = models.IntegerField(blank=True, null=True)
    pc = models.CharField(max_length=8000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_unit_pcdelivery'


class ViewCutsecFabricdelivery(models.Model):
    rlno = models.CharField(db_column='RlNo', max_length=50, primary_key=True)
    dcaddres = models.CharField(max_length=750, blank=True, null=True)
    delto = models.CharField(max_length=750, blank=True, null=True)
    dt = models.DateTimeField(db_column='Dt')
    dcno = models.IntegerField()
    purpose_name = models.CharField(db_column='Purpose_Name', max_length=80)
    jobno = models.CharField(max_length=50, blank=True, null=True)
    clr = models.CharField(max_length=50, blank=True, null=True)
    fab = models.CharField(max_length=35)
    lotno = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=35)
    wgtkgs = models.DecimalField(db_column='WgtKgs', max_digits=18, decimal_places=3)
    mtr = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_cutsec_fabricdelivery'


class ViewGdwnFabricDeliveryPlan(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase.
    frm = models.CharField(max_length=11)
    todept = models.CharField(max_length=12)
    dcno = models.IntegerField()
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    markerno = models.IntegerField(db_column='MarkerNo')  # Field name made lowercase.
    lotno = models.CharField(max_length=50)
    colour = models.CharField(db_column='Colour', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dia = models.CharField(db_column='Dia', max_length=35)  # Field name made lowercase.
    rls = models.IntegerField(blank=True, null=True)
    kg = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    mtr = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    rlno = models.CharField(max_length=8000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_gdwn_fabric_delivery_plan'

class VueRibDeliveryDetails(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo')  # Field name made lowercase.
    dcaddres = models.CharField(max_length=750, blank=True, null=True)
    deladd = models.CharField(max_length=750, blank=True, null=True)
    dc = models.IntegerField()
    dt = models.DateTimeField()
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trstype = models.IntegerField()
    s = models.CharField(max_length=50, blank=True, null=True)
    c = models.CharField(max_length=101, blank=True, null=True)
    lotno = models.CharField(db_column='LOTNO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    siz = models.CharField(max_length=35)
    delpc = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vue_rib_delivery_details'



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
    print_delivery_date = models.DateTimeField(db_column='Print_Delivery_date', blank=True, null=True)  # Field name made lowercase.
    gate_delivery_date = models.DateTimeField(db_column='Gate_Delivery_date', blank=True, null=True)  # Field name made lowercase.
    verify = models.CharField(db_column='Verify', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prepered = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fhero = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trs_Gatemodule'



class ViewAccinwardVerification(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    supplierdcno = models.CharField(db_column='SupplierDCNo', max_length=50)  # Field name made lowercase.
    pono = models.IntegerField(db_column='PONo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    items = models.CharField(db_column='Items', max_length=71, blank=True, null=True)  # Field name made lowercase.
    clr_siz = models.CharField(max_length=101, blank=True, null=True)
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=25)  # Field name made lowercase.
    bill_rate = models.DecimalField(db_column='Bill_Rate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    gst = models.CharField(db_column='GST', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_accinward_verification'




class ViewMistakeqtyPrint(models.Model):
    frm = models.CharField(max_length=750, blank=True, null=True)
    toad = models.CharField(max_length=750, blank=True, null=True)
    dcno = models.IntegerField(primary_key=True)
    dt = models.DateTimeField()
    jobno = models.CharField(db_column='Jobno', max_length=50)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mistake_des = models.CharField(db_column='Mistake_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50)  # Field name made lowercase.
    lotno = models.CharField(db_column='Lotno', max_length=50)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    trstype = models.CharField(db_column='Trstype', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_mistakeqty_print'

class ViewFabricDeliveryRepl(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', primary_key=True)  # Field name made lowercase.
    frm = models.CharField(max_length=11)
    todept = models.CharField(max_length=20, blank=True, null=True)
    dcno = models.IntegerField()
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    markerno = models.IntegerField(db_column='MarkerNo', blank=True, null=True)  # Field name made lowercase.
    lotno = models.CharField(max_length=50, blank=True, null=True)
    colour = models.CharField(db_column='Colour', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dia = models.CharField(db_column='Dia', max_length=35)  # Field name made lowercase.
    rls = models.IntegerField(blank=True, null=True)
    kg = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    mtr = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    rlno = models.CharField(max_length=8000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_fabric_delivery_repl'



class TrsApidtls(models.Model):
    sl = models.AutoField(primary_key=True)
    api = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    module = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'Trs_APIdtls'



class HerofashionUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, db_collation='Latin1_General_CI_AI')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Latin1_General_CI_AI')
    first_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI')
    last_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI')
    email = models.CharField(max_length=254, db_collation='Latin1_General_CI_AI')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    role = models.ForeignKey('herofashion.Role', models.DO_NOTHING, blank=True, null=True)
    default_submenu = models.ForeignKey('herofashion.SubMenu', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'herofashion_user'



class Holiday(models.Model):
    dt = models.DateTimeField()
    descr = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ty = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Holiday'


class RoleModulePermission(models.Model):
    role = models.CharField(max_length=100, db_index=True)
    module_id = models.CharField(max_length=100)
    module_name = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role_module_permissions'
        # Prevent duplicate role + module combinations
        unique_together = ('role', 'module_id')

    def __str__(self):
        return f"{self.role} - {self.module_name} ({'ON' if self.is_enabled else 'OFF'})"
