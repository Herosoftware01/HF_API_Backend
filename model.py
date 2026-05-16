# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class QcappQcPieceFinal(models.Model):
    id = models.BigAutoField(primary_key=True)
    bundle_no = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    bundle_id = models.CharField(max_length=20, db_collation='Latin1_General_CI_AI')
    jobno = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    product = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    color = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    size = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    total_pieces = models.IntegerField()
    checked_piece = models.IntegerField()
    force_save = models.BooleanField()
    line = models.IntegerField()
    unit = models.IntegerField()
    qc_type = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')
    date = models.DateTimeField()
    user_id = models.IntegerField()
    seq = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    machine_id = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'qcapp_qc_piece_final'
