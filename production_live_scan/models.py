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
    emp_id = models.CharField(max_length=20, blank=True, null=True)
    entry_mode = models.CharField(max_length=20, blank=True, null=True)
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
    or_only = models.BooleanField(default=False)
    verify_user = models.CharField(max_length=50, blank=True, null=True)
    verify_date = models.DateTimeField(blank=True, null=True)
    # assemply_scan = models.BooleanField(default=False)



class dependency_data(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    tb_id = models.IntegerField()
    process_id = models.IntegerField()
    desc_ord_no = models.IntegerField()
    descriptions = models.CharField(max_length=50)
    or_data = models.BooleanField(default=False)
    and_data = models.BooleanField(default=False)
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


class PreporatoryEntry(models.Model):
  jobno = models.CharField(max_length=50)
  topbottom = models.CharField(max_length=100)
  process = models.CharField(max_length=100)
  selected_processes = models.CharField(max_length=100, blank=True, null=True)
  elastic_status = models.BooleanField(
      default=False
  )  # Elastic switch status (True/False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = (
        "jobno",
        "topbottom",
        "process",
    ) 
  def __str__(self):
    return f"{self.jobno} - {self.topbottom} - Process {self.process}"



class ViewRibdelPreparatory(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    siz = models.CharField(max_length=35)
    clrcomb = models.CharField(max_length=50)
    unitname = models.CharField(db_column='UnitName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotno = models.CharField(db_column='LOTNO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    delpc = models.IntegerField(blank=True, null=True)
    indpart = models.CharField(max_length=50)
    process = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'view_ribdel_preparatory'


class RibdelEntry(models.Model):
    employee_id = models.CharField(max_length=50)
    jobno = models.CharField(max_length=50)
    topbottom_des = models.CharField(max_length=50, blank=True, null=True)
    clrcomb = models.CharField(max_length=50)
    siz = models.CharField(max_length=35)
    lotno = models.CharField(max_length=10, blank=True, null=True)
    total_qty = models.IntegerField()
    entered_qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


################################## USer Permission Models ########################################


class user_unit_permission(models.Model):

    APP_CHOICES = (
        ("qcapp", "QC App"),
        ("live_app", "Live App"),
    )

    user = models.ForeignKey(
        "herofashion.User",
        on_delete=models.CASCADE,
        related_name="unit_permissions"
    )

    app = models.CharField(
        max_length=20,
        choices=APP_CHOICES
    )

    unit = models.ForeignKey(
        "qcapp.unit",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_unit_permission"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "app", "unit"],
                name="unique_user_app_unit"
            )
        ]
    