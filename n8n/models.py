from django.db import models

class TxNotification(models.Model):
    emp_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    wunit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cat = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    punch_time = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    sl = models.AutoField(primary_key=True)
    processed = models.BooleanField(blank=True, null=True)
    pic = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    late = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tx_notification'