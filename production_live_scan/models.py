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


class Assembly_data(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField()
    line = models.IntegerField()
    job_no = models.CharField(max_length=50)
    tb_id = models.IntegerField()
    tb_name = models.CharField(max_length=100)
    machine = models.CharField(max_length=100)
    seq = models.CharField(max_length=500)
    date = models.DateTimeField()
    bundle_id = models.CharField(max_length=50)
    bdl_no = models.CharField(max_length=50)
    mbud = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    size_id = models.IntegerField()
    color = models.CharField(max_length=100)
    pc = models.CharField(max_length=50)
    entry_date = models.DateTimeField()
    scan = models.BooleanField(default=False)
    lot = models.CharField(max_length=50)
    # process_des = models.CharField(max_length=500)


class dependency(models.Model):
    id = models.AutoField(primary_key=True)
    job_no = models.CharField(max_length=50)
    tb_id = models.IntegerField()
    tb_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    process_des = models.CharField(max_length=50)
    mc = models.CharField(max_length=50)
    thrd = models.IntegerField()
    wsec = models.CharField(max_length=50)
    process_id = models.IntegerField()
    and_or = models.BooleanField(default=False)
    verify = models.BooleanField(default=False)
    # assemply_scan = models.BooleanField(default=False)



class dependency_data(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    tb_id = models.IntegerField()
    process_id = models.IntegerField()
    desc_ord_no = models.IntegerField()
    descriptions = models.CharField(max_length=50)
    dep_id = models.ForeignKey(dependency, on_delete=models.CASCADE, related_name='data_entries')

    
    
class end_line_data(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField()
    line = models.IntegerField()
    job_no = models.CharField(max_length=50)
    tb_id = models.IntegerField()
    tb_name = models.CharField(max_length=100)
    machine = models.CharField(max_length=100)
    date = models.DateTimeField()
    bundle_id = models.CharField(max_length=50)
    bdl_no = models.CharField(max_length=50)
    mbud = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    size_id = models.IntegerField()
    color = models.CharField(max_length=100)
    pc = models.CharField(max_length=50)
    entry_date = models.DateTimeField()
    scan = models.BooleanField(default=False)
    lot = models.CharField(max_length=50)


    