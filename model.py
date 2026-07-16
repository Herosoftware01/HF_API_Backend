# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TrsWorkentry(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=100, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.
    entrydate = models.DateField(db_column='EntryDate')  # Field name made lowercase.
    project = models.CharField(db_column='Project', max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    subcat = models.CharField(db_column='SubCat', max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='StartDateTime', blank=True, null=True)  # Field name made lowercase.
    startstatus = models.CharField(db_column='StartStatus', max_length=20, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='EndDateTime', blank=True, null=True)  # Field name made lowercase.
    endstatus = models.CharField(db_column='EndStatus', max_length=20, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    durationminutes = models.IntegerField(db_column='DurationMinutes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trs_Workentry'
