from django.db import models
from django.conf import settings  # <-- important

class GridSetting(models.Model):
    name = models.CharField(max_length=255)
    data = models.JSONField()
    user = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- dynamic reference
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class DiWasg(models.Model):
    asgby_code = models.CharField(db_column='ASGBY_CODE', max_length=50, blank=True, null=True)
    asgby_name = models.CharField(db_column='ASGBY_NAME', max_length=100, primary_key=True)
    asgdt = models.DateTimeField(db_column='ASGDT', blank=True, null=True)
    issued_for = models.CharField(db_column='ISSUED_FOR', max_length=15, blank=True, null=True)
    wrkdtls = models.CharField(db_column='WRKDTLS', max_length=1550, blank=True, null=True)
    wrkreqdt = models.DateTimeField(db_column='WRKREQDT', blank=True, null=True)
    entryno = models.IntegerField(db_column='ENTRYNO', blank=True, null=True)
    worktype = models.CharField(db_column='WorkType', max_length=20, blank=True, null=True)
    worktype1 = models.CharField(db_column='workType1', max_length=20, blank=True, null=True)
    jobno = models.CharField(max_length=1550, blank=True, null=True)
    party = models.CharField(max_length=1550, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    field_empcode = models.CharField(db_column='_empcode', max_length=100, blank=True, null=True)
    field_empname = models.CharField(db_column='_empname', max_length=200, blank=True, null=True)
    wrk1 = models.CharField(max_length=500, blank=True, null=True)
    wrk2 = models.CharField(max_length=50, blank=True, null=True)
    wrk3 = models.CharField(max_length=50, blank=True, null=True)
    wrk4 = models.CharField(max_length=50, blank=True, null=True)
    wrk5 = models.CharField(max_length=50, blank=True, null=True)
    rep1 = models.CharField(max_length=500, blank=True, null=True)
    rep2 = models.CharField(max_length=50, blank=True, null=True)
    rep3 = models.CharField(max_length=50, blank=True, null=True)
    rep4 = models.CharField(max_length=50, blank=True, null=True)
    rep5 = models.CharField(max_length=50, blank=True, null=True)
    wrkcat = models.CharField(db_column='Wrkcat', max_length=50, blank=True, null=True)
    wrkentbycd = models.IntegerField(db_column='WrkEntBycd', blank=True, null=True)
    wrkentbynam = models.CharField(db_column='WrkEntBynam', max_length=70, blank=True, null=True)
    attachment = models.CharField(db_column='Attachment', max_length=1550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'di_Wasg'

class DiWasg_img(models.Model):
    asgby_code = models.CharField(db_column='ASGBY_CODE', max_length=50, blank=True, null=True)
    asgby_name = models.CharField(db_column='ASGBY_NAME', max_length=100, primary_key=True)
    asgdt = models.DateTimeField(db_column='ASGDT', blank=True, null=True)
    issued_for = models.CharField(db_column='ISSUED_FOR', max_length=15, blank=True, null=True)
    wrkdtls = models.CharField(db_column='WRKDTLS', max_length=1550, blank=True, null=True)
    wrkreqdt = models.DateTimeField(db_column='WRKREQDT', blank=True, null=True)
    entryno = models.IntegerField(db_column='ENTRYNO', blank=True, null=True)
    worktype = models.CharField(db_column='WorkType', max_length=20, blank=True, null=True)
    worktype1 = models.CharField(db_column='workType1', max_length=20, blank=True, null=True)
    jobno = models.CharField(max_length=1550, blank=True, null=True)
    party = models.CharField(max_length=1550, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    field_empcode = models.CharField(db_column='_empcode', max_length=100, blank=True, null=True)
    field_empname = models.CharField(db_column='_empname', max_length=200, blank=True, null=True)
    wrk1 = models.CharField(max_length=500, blank=True, null=True)
    wrk2 = models.CharField(max_length=50, blank=True, null=True)
    wrk3 = models.CharField(max_length=50, blank=True, null=True)
    wrk4 = models.CharField(max_length=50, blank=True, null=True)
    wrk5 = models.CharField(max_length=50, blank=True, null=True)
    rep1 = models.CharField(max_length=500, blank=True, null=True)
    rep2 = models.CharField(max_length=50, blank=True, null=True)
    rep3 = models.CharField(max_length=50, blank=True, null=True)
    rep4 = models.CharField(max_length=50, blank=True, null=True)
    rep5 = models.CharField(max_length=50, blank=True, null=True)
    wrkcat = models.CharField(db_column='Wrkcat', max_length=50, blank=True, null=True)
    wrkentbycd = models.IntegerField(db_column='WrkEntBycd', blank=True, null=True)
    wrkentbynam = models.CharField(db_column='WrkEntBynam', max_length=70, blank=True, null=True)
    attachment = models.CharField(db_column='Attachment', max_length=1550, blank=True, null=True)
    photo_url= models.CharField(db_column='photo_url', max_length=1550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dI_Wasg_img'


    
class TrsMaildtls(models.Model):
    sl = models.AutoField(db_column='Sl', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    ordid = models.CharField(db_column='OrdID', max_length=50, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.
    mail_content = models.CharField(db_column='Mail_Content', max_length=750, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trs_Maildtls'


class SyncfushionKanban(models.Model):
    Id = models.AutoField(db_column='Id', primary_key=True)
    Title = models.CharField(db_column='Title', max_length=255)  
    Status = models.CharField(db_column='Status', max_length=50)  
    Description = models.TextField(db_column='Description',  blank=True, null=True)  
    Type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  
    Priority = models.CharField(db_column='Priority', max_length=20, blank=True, null=True)  
    Tags = models.CharField(db_column='Tags', max_length=255, blank=True, null=True)  
    Estimate = models.DecimalField(db_column='Estimate', max_digits=5, decimal_places=2, blank=True, null=True)  
    Assignee = models.CharField(db_column='Assignee', max_length=100, blank=True, null=True)  
    Rankid = models.IntegerField(db_column='RankId', blank=True, null=True)  
    Reporter = models.CharField(db_column='Reporter', max_length=100,  blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'syncfushion_kanban'

class SyncfusionGantt(models.Model):
    taskid = models.IntegerField(db_column='TaskId', primary_key=True) 
    taskname = models.CharField(db_column='TaskName', max_length=255, blank=True, null=True) 
    startdate = models.DateField(db_column='StartDate', blank=True, null=True) 
    enddate = models.DateField(db_column='EndDate', blank=True, null=True) 
    progress = models.IntegerField(db_column='Progress', blank=True, null=True) 
    status = models.CharField(db_column='Status', max_length=100, blank=True, null=True) 
    priority = models.CharField(db_column='Priority', max_length=50, blank=True, null=True) 
    assignee = models.CharField(db_column='Assignee', max_length=150, blank=True, null=True) 
    resourcesimage = models.TextField(db_column='resourcesImage', blank=True, null=True) 
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True) 
    predecessor = models.CharField(db_column='Predecessor', max_length=50, blank=True, null=True) 
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'syncfusion_gantt'

    def __str__(self):
        return f"{self.taskid} - {self.taskname}"
    
class BlockEditor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="Name of the block template")
    blocks = models.JSONField(default=list, help_text="JSON blocks from block editor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'syncfusion_blockeditor'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Block Template - {self.name}"
    
class FashionrResult(models.Model):
    slno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    result = models.JSONField(default=list)
    created_datetime = models.DateTimeField(blank=True, null=True)
    jobno = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'Fashionr_result'

class ViewAccinwpend(models.Model):
    poduedtfollow = models.CharField(db_column='poDuedtfollow', max_length=12)  # Field name made lowercase.
    orddtfollow = models.CharField(db_column='ordDtfollow', max_length=11)  # Field name made lowercase.
    img = models.CharField(max_length=450, blank=True, null=True)
    slno = models.BigIntegerField(primary_key=True)
    merch = models.CharField(max_length=35, blank=True, null=True)
    orderno = models.CharField(max_length=50, blank=True, null=True)
    no = models.IntegerField(db_column='NO')  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE')  # Field name made lowercase.
    duedate = models.DateTimeField(blank=True, null=True)
    dueday = models.IntegerField(db_column='Dueday', blank=True, null=True)  # Field name made lowercase.
    orderdt = models.DateField(blank=True, null=True)
    ordremday = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=35, blank=True, null=True)
    completed = models.SmallIntegerField()
    ag = models.CharField(max_length=35)
    an = models.CharField(max_length=35)
    sz = models.CharField(max_length=4000, blank=True, null=True)
    item = models.CharField(max_length=122, blank=True, null=True)
    quantity = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)
    inwqty = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)
    uom = models.CharField(max_length=25)
    phone = models.CharField(max_length=101, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_accinwpend'


class ViewCutBalpend(models.Model):
    slno = models.BigIntegerField(primary_key=True)
    itemno = models.SmallIntegerField(db_column='ItemNo')
    ordno = models.CharField(max_length=50, blank=True, null=True)
    o_finaldelvdate = models.DateTimeField(db_column='o_FinalDelvdate', blank=True, null=True)
    sl = models.IntegerField(blank=True, null=True)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)
    tbimg = models.CharField(max_length=1550, blank=True, null=True)
    clr = models.CharField(max_length=50, blank=True, null=True)
    siz = models.CharField(max_length=50, blank=True, null=True)
    order_qty = models.IntegerField(blank=True, null=True)
    rejection_qty = models.IntegerField(blank=True, null=True)
    required_qty = models.IntegerField(db_column='Required_Qty', blank=True, null=True)
    remdays = models.IntegerField(blank=True, null=True)
    risk = models.CharField(db_column='Risk', max_length=6)
    plan_qty = models.IntegerField(db_column='Plan_Qty', blank=True, null=True)
    plan_bal_pers = models.DecimalField(db_column='Plan_Bal_pers', max_digits=18, decimal_places=2, blank=True, null=True)
    actual_cut_qty = models.IntegerField(db_column='Actual_Cut_Qty', blank=True, null=True)
    hand_cutting = models.IntegerField(db_column='Hand_Cutting', blank=True, null=True)
    cutting_bal_pers = models.DecimalField(db_column='Cutting_Bal_pers', max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_cut_balpend'

class ViewAccessoryDel(models.Model):
    sl = models.IntegerField(primary_key=True)
    jobno = models.CharField(max_length=50)
    img = models.CharField(max_length=539, blank=True, null=True)
    clrcombo = models.CharField(max_length=150, blank=True, null=True)
    pono = models.IntegerField()
    posupplier = models.CharField(max_length=80)
    podate = models.CharField(max_length=50)
    podue = models.CharField(max_length=50)
    acc_item = models.CharField(db_column='Acc_Item', max_length=80)
    clr_siz = models.CharField(max_length=80)
    poqty = models.DecimalField(max_digits=18, decimal_places=2)
    uom = models.CharField(max_length=50)
    inwarddate = models.CharField(max_length=50)
    fddate = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField()
    inwardqty = models.DecimalField(max_digits=18, decimal_places=2)
    inwpendqty = models.DecimalField(max_digits=18, decimal_places=2)
    inwdiffqty = models.DecimalField(max_digits=18, decimal_places=2)
    issueunit = models.CharField(max_length=80)
    issuedt = models.CharField(max_length=50)
    delqty = models.DecimalField(max_digits=18, decimal_places=2)
    ret = models.DecimalField(max_digits=18, decimal_places=2)
    storestock = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=13)
    retmark = models.CharField(max_length=80)
    
    class Meta:
        managed = False
        db_table = 'view_accessory_del'

class TmpQms(models.Model):
    sl = models.IntegerField(primary_key=True)
    jobno = models.CharField(max_length=50)
    pono = models.IntegerField()
    acc_item = models.CharField(db_column='Acc_Item', max_length=80)
    clr_siz = models.CharField(max_length=80)
    retmark = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'Tmp_Qms'