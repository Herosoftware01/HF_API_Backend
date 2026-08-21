from django.db import models

# Create your models here.
class TrsStickerdtls(models.Model):
    planno = models.IntegerField()
    sl = models.IntegerField(primary_key=True)
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    topbott_id = models.IntegerField(db_column='TopBott_ID')  # Field name made lowercase.
    clrcombo = models.CharField(db_column='Clrcombo', max_length=80)  # Field name made lowercase.
    colour = models.IntegerField(db_column='Colour')  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50)  # Field name made lowercase.
    sc = models.CharField(db_column='SC', max_length=1)  # Field name made lowercase.
    plansl = models.IntegerField(db_column='Plansl')  # Field name made lowercase.
    sizeid = models.IntegerField(db_column='SizeID')  # Field name made lowercase.
    ratio = models.IntegerField(db_column='Ratio')  # Field name made lowercase.
    pc = models.IntegerField(db_column='Pc')  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=35)  # Field name made lowercase.
    portion_des = models.CharField(db_column='PORTION_DES', max_length=50)  
    porid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trs_StickerDtls'


class Stickemp(models.Model):
    code = models.IntegerField(primary_key=True)
    attdt = models.DateTimeField(db_column='AttDt', blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    employee = models.CharField(db_column='Employee', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stickemp'


class VueMistakePartDetails(models.Model):
    rownum = models.BigIntegerField(db_column='RowNum', primary_key=True)  # Field name made lowercase.
    qrid = models.IntegerField(db_column='QrID')
    planno = models.IntegerField(db_column='Planno')  # Field name made lowercase.
    jobno = models.CharField(max_length=50)
    markerno = models.IntegerField(db_column='Markerno')  # Field name made lowercase.
    det_main_part = models.CharField(max_length=50, blank=True, null=True)
    det_part = models.CharField(max_length=70, blank=True, null=True)
    topbottom_id = models.IntegerField(db_column='TopBottom_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vue_mistake_part_details'


class bit_checking_updates(models.Model):
    scaner_id = models.IntegerField()
    emp_id = models.IntegerField()
    descriptions = models.CharField(max_length=50)
    out_pcs = models.TextField()
    mistake_pcs = models.TextField()
    out_pcs_count = models.IntegerField()
    ok_pcs = models.IntegerField()
    total_qty = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    plan_no = models.IntegerField()
    total_select_pcs = models.TextField()
    entry_mood=models.CharField(max_length=50, blank=True, null=True)
    types = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    # r_p = models.BooleanField(default=False)



class BitcheckingPlyDetails(models.Model):
    sno = models.AutoField(db_column='Sno', primary_key=True)  
    emp_id = models.IntegerField(db_column='Emp_id')
    qr_id = models.IntegerField(db_column='Qr_id') 
    total_pcs = models.IntegerField(db_column='Total_pcs') 
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  
    result = models.CharField(db_column='Result', max_length=200, blank=True, null=True)  
    final_tpcs = models.CharField(db_column='Final_tpcs', max_length=50, blank=True, null=True)  
    out_ply = models.CharField(db_column='Out_ply', max_length=100, blank=True, null=True)
    ok_pcs = models.CharField(db_column='Ok_pcs', max_length=50, blank=True, null=True)
    mistake_pcs = models.CharField(db_column='Mistake_pcs', max_length=50, blank=True, null=True)
    mistake_ply = models.CharField(db_column='Mistake_ply', max_length=100, blank=True, null=True) 
    r_p = models.BooleanField(default=False)
    entry_mode = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)   
    typ = models.CharField(db_column='TYP', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bitchecking_ply_details'


class TrsCutstickerprodNew(models.Model):
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    qrid = models.IntegerField(db_column='QrID', primary_key=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tbid = models.IntegerField(db_column='TBID')  # Field name made lowercase.
    comboclr = models.CharField(db_column='Comboclr', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sizid = models.IntegerField(db_column='SIZID')  # Field name made lowercase.
    planno = models.IntegerField(db_column='Planno')  # Field name made lowercase.
    plansl = models.IntegerField(db_column='Plansl')  # Field name made lowercase.
    pc = models.IntegerField(db_column='Pc')  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ratio = models.IntegerField(db_column='Ratio', blank=True, null=True)  # Field name made lowercase.
    porid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trs_CutStickerProd_New'


class TrsCutstickerprodNew1(models.Model):
    t = models.CharField(db_column='T', max_length=50)  # Field name made lowercase.
    qrid = models.IntegerField(db_column='QRID', primary_key=True)  # Field name made lowercase.
    planno = models.IntegerField()
    jobno = models.CharField(db_column='JobNo', max_length=50)  # Field name made lowercase.
    topbott_id = models.IntegerField(db_column='TopBott_ID')  # Field name made lowercase.
    clrcombo = models.CharField(db_column='Clrcombo', max_length=80)  # Field name made lowercase.
    lotno = models.CharField(db_column='LotNo', max_length=50)  # Field name made lowercase.
    plansl = models.IntegerField(db_column='Plansl')  # Field name made lowercase.
    sizeid = models.IntegerField(db_column='SizeID')  # Field name made lowercase.
    ratio = models.IntegerField(db_column='Ratio')  # Field name made lowercase.
    pc = models.IntegerField(db_column='Pc')  # Field name made lowercase.
    porid = models.IntegerField(blank=True, null=True)
    portion_des = models.CharField(db_column='PORTION_DES', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trs_CutStickerProd_New1'


class bit_start_end_time(models.Model):
    qrid = models.IntegerField()
    empid = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    types = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    

class ViewAccinwardVerification(models.Model):
    slno = models.BigIntegerField(db_column='SlNo', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    record_pk = models.CharField(db_column='pk', max_length=319, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=35, blank=True, null=True)  # Field name made lowercase.
    supplierdcno = models.CharField(db_column='SupplierDCNo', max_length=50)  # Field name made lowercase.
    pono = models.IntegerField(db_column='PONo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    items = models.CharField(db_column='Items', max_length=71, blank=True, null=True)  # Field name made lowercase.
    clr_siz = models.CharField(max_length=101)
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=4)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=25)  # Field name made lowercase.
    bill_rate = models.DecimalField(db_column='Bill_Rate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    gst = models.CharField(db_column='GST', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='BillDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_accinward_verification'


class Accessory_Verification(models.Model): 
    pk_name = models.CharField(max_length=400, blank=True, null=True)
    verify1 = models.BooleanField(default=False)
    verify2 = models.BooleanField(default=False)
    verify1_date = models.DateTimeField(blank=True, null=True)
    verify2_date = models.DateTimeField(blank=True, null=True)


class user_accessory_verification(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    verify1 = models.BooleanField(default=False)
    verify2 = models.BooleanField(default=False)



