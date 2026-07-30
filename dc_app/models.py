from django.db import models

class ViewCuttingDelPrint(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)  # Field name made lowercase.
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
