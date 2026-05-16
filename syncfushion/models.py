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
    

class TrsMaildtls(models.Model):
    sl = models.AutoField(db_column='Sl', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='Dt')  # Field name made lowercase.
    ordid = models.CharField(db_column='OrdID', max_length=50, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.
    mail_content = models.CharField(db_column='Mail_Content', max_length=750, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trs_Maildtls'


