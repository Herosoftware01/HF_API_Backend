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
    companyid=models.SmallIntegerField()
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


