# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewMistakeqtyPrint(models.Model):
    frm = models.CharField(max_length=750, blank=True, null=True)
    toad = models.CharField(max_length=750, blank=True, null=True)
    dcno = models.IntegerField()
    dt = models.DateTimeField()
    jobno = models.CharField(db_column='Jobno', max_length=50)  # Field name made lowercase.
    topbottom_des = models.CharField(db_column='TopBottom_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mistake_des = models.CharField(db_column='Mistake_des', max_length=50, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50)  # Field name made lowercase.
    lotno = models.CharField(db_column='Lotno', max_length=50)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    trstype = models.CharField(db_column='Trstype', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_mistakeqty_print'
