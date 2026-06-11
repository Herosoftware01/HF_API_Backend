# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewStickerHour(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    empid = models.IntegerField()
    dt = models.DateField(blank=True, null=True)
    v_pc = models.IntegerField(blank=True, null=True)
    vi_pc = models.IntegerField(blank=True, null=True)
    i_pc = models.IntegerField(blank=True, null=True)
    ii_pc = models.IntegerField(blank=True, null=True)
    iii_pc = models.IntegerField(blank=True, null=True)
    iv_pc = models.IntegerField(blank=True, null=True)
    v_pan = models.IntegerField(blank=True, null=True)
    vi_pan = models.IntegerField(blank=True, null=True)
    i_pan = models.IntegerField(blank=True, null=True)
    ii_pan = models.IntegerField(blank=True, null=True)
    iii_pan = models.IntegerField(blank=True, null=True)
    iv_pan = models.IntegerField(blank=True, null=True)
    s_hift = models.DecimalField(max_digits=38, decimal_places=2)
    amt = models.DecimalField(max_digits=38, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_sticker_hour'
