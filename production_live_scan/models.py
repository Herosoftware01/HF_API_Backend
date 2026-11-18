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
    unit_transfer = models.BooleanField(default=False)
    edit_data = models.BooleanField(default=False)
    allocate_id = models.IntegerField()
    # process_des = models.CharField(max_length=500)


class bundle_transfer(models.Model):
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
    lot = models.CharField(max_length=50)
    emp_id = models.CharField(max_length=20, blank=True, null=True)


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
    part=models.CharField(max_length=50, blank=True, null=True)
    trn = models.CharField(max_length=50, blank=True, null=True) 
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
    emp_id = models.CharField(max_length=20, blank=True, null=True)
    reject_pcs = models.IntegerField(default=0)
    rework_pcs = models.IntegerField(default=0)
    ok_pcs = models.IntegerField(default=0)


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


################################## User Permission Models ########################################


class user_unit_permission(models.Model):

    APP_CHOICES = (
        ("qcapp", "QC App"),
        ("live_app", "Live App"),
        ("machine_transfer", "Machine Transfer"),
        ("employee_allocation", "Employee Allocation"),
        ("bundle_scan", "Bundle Scan"),
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

################################

class VueCutPlnStat(models.Model):
    ordno = models.CharField(max_length=50, blank=True, null=True)
    topbottom_id = models.IntegerField(db_column='Topbottom_id', blank=True, null=True)  # Field name made lowercase.
    clr = models.CharField(max_length=50, blank=True, null=True)
    siz = models.CharField(max_length=50, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    ord1 = models.IntegerField(blank=True, null=True)
    stk = models.IntegerField(blank=True, null=True)
    stkact = models.IntegerField(blank=True, null=True)
    ord2 = models.IntegerField(blank=True, null=True)
    ordact2 = models.IntegerField(blank=True, null=True)
    zsact = models.IntegerField()
    zoact = models.IntegerField()
    hcut = models.IntegerField(blank=True, null=True)
    rjqty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vue_cut_pln_stat'


class sub_bundle_unit_transfer(models.Model):
    bundle_id=models.CharField(max_length=50)
    from_unit = models.IntegerField()
    to_unit = models.IntegerField()
    date = models.DateTimeField()



class ViewOrderdetails(models.Model):
    orderno = models.CharField(db_column='OrderNo', max_length=50, primary_key=True)  # Field name made lowercase.
    prdsl = models.IntegerField(blank=True, null=True)
    product = models.CharField(max_length=50, blank=True, null=True)
    clr = models.CharField(db_column='Clr', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    sizename = models.TextField(db_column='SizeName', blank=True, null=True)  # Field name made lowercase.
    ordqty = models.IntegerField(blank=True, null=True)
    merch = models.CharField(max_length=35, blank=True, null=True)
    buyer = models.CharField(max_length=15, blank=True, null=True)
    prdnunit = models.CharField(max_length=35, blank=True, null=True)
    finaldelvdate = models.CharField(max_length=4000, blank=True, null=True)
    style = models.CharField(max_length=35, blank=True, null=True)
    img1 = models.CharField(max_length=94, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_orderdetails'


class ViewOrdersummary(models.Model):
    ordno = models.CharField(db_column='OrdNo', max_length=50, primary_key=True)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    clr = models.CharField(db_column='Clr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    siz = models.CharField(db_column='Siz', max_length=50, blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_OrderSummary'


class ViewAccessoryorderqtyElastic(models.Model):
    orderno = models.CharField(db_column='OrderNo', max_length=50, primary_key=True)  # Field name made lowercase.
    accessory = models.CharField(db_column='Accessory', max_length=158)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=38, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_AccessoryOrderQty_Elastic'

class ViewElasticCons(models.Model):
    jobno = models.CharField(db_column='JobNo', max_length=50, primary_key=True)  # Field name made lowercase.
    sl1 = models.IntegerField(blank=True, null=True)
    sizedescr = models.CharField(max_length=50)
    cons = models.DecimalField(max_digits=18, decimal_places=2)
    topbott = models.CharField(max_length=50)
    color = models.CharField(max_length=1800, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_elastic_cons'

class elastic_cons(models.Model):
    jobno = models.CharField(max_length=50)
    sizedescr = models.CharField(max_length=50)
    cons = models.DecimalField(max_digits=18, decimal_places=2)
    topbott = models.CharField(max_length=50)
    color = models.CharField(max_length=1800, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'elastic_cons'


class ViewCuttingQtyDetails(models.Model):
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)
    jobno = models.CharField(max_length=50,primary_key=True)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    clrcombo = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    noofpcs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_cutting_qty_details'


class Elastic_cutting_qty(models.Model):
    entry_no = models.AutoField(primary_key=True)
    order_no = models.CharField(max_length=50)
    topbottom = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    elastic_description = models.CharField(max_length=100, blank=True, null=True)
    inward_mtrs = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField()
    actual_consumption = models.CharField(max_length=50, blank=True, null=True)
    wastage = models.CharField(max_length=50, blank=True, null=True)
    total_cutting_qty = models.CharField(max_length=50, blank=True, null=True)
    estimate_mtrs = models.CharField(max_length=50, blank=True, null=True)

class Elastic_cutting_qty_details(models.Model):
    bdl_id = models.AutoField(primary_key=True)
    entry_no = models.ForeignKey(Elastic_cutting_qty, on_delete=models.CASCADE, related_name='cutting_qty_details')
    size = models.CharField(max_length=50, blank=True, null=True)
    len_cm = models.CharField(max_length=50, blank=True, null=True)
    order_qty = models.CharField(max_length=50, blank=True, null=True)
    pcs_cut = models.CharField(max_length=50, blank=True, null=True)
    elastic_cutting_qty = models.CharField(max_length=50, blank=True, null=True)
    estimate_mtrs = models.CharField(max_length=50, blank=True, null=True)
    bdl_no = models.CharField(max_length=50, blank=True, null=True)
    bdl_qty = models.CharField(max_length=50, blank=True, null=True)
    delivery = models.BooleanField(default=False)
    delivery_id = models.IntegerField(blank=True, null=True)


class ViewOrdersummaryUnit(models.Model):
    ordno = models.CharField(db_column='OrdNo', max_length=50, primary_key=True)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    clr = models.CharField(db_column='Clr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    siz = models.CharField(db_column='Siz', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty = models.IntegerField(blank=True, null=True)
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='UnitName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_OrderSummary_unit'

class ViewCuttingQtyDetailsUnit(models.Model):
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(max_length=50, primary_key=True)
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comboclr = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    noofpcs = models.IntegerField(blank=True, null=True)
    unitname = models.CharField(db_column='UnitName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_cutting_qty_details_unit'
    
class ElasticDelivery(models.Model):
    id = models.AutoField(primary_key=True)
    job_no = models.CharField(max_length=50)
    topbottom = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    unit = models.CharField(max_length=100)
    delivery_date = models.DateTimeField(auto_now_add=True)

class ElasticDeliveryDetails(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_id = models.ForeignKey(ElasticDelivery, on_delete=models.CASCADE, related_name='details')
    unit_ord_qty = models.IntegerField()
    unit_cut_qty = models.IntegerField()
    size = models.CharField(max_length=50)
    cur_del_qty = models.IntegerField()
    total_bdl = models.IntegerField()
    delivery_date = models.DateTimeField(auto_now_add=True)


