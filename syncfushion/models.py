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