# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UnitUnituser(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    user_id = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI')
    password = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'unit_unituser'
