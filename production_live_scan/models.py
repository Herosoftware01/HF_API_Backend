from django.db import models

class unit_input(models.Model):
    bundle_id = models.CharField(max_length=50)
    bdl_no = models.CharField(max_length=50) 
    mbud = models.CharField(max_length=50)
    unit = models.IntegerField()
    line = models.IntegerField()
    entry_date = models.DateTimeField()
    job_no = models.CharField(max_length=50)
    color = models.CharField(max_length=100)
    tb_id = models.IntegerField()
    tb_name = models.CharField(max_length=100)
    scan = models.BooleanField(default=False)
    size = models.CharField(max_length=50)
    size_id = models.IntegerField()
    pc = models.CharField(max_length=50)
    lot =models.CharField(max_length=50)
    date = models.DateTimeField()


class Msizes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sizegroup = models.IntegerField(db_column='SizeGroup', blank=True, null=True)  # Field name made lowercase.
    sorter = models.IntegerField(db_column='Sorter')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mSizes'


    