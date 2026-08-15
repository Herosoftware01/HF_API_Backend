# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HerofashionUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, db_collation='Latin1_General_CI_AI')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Latin1_General_CI_AI')
    first_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI')
    last_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI')
    email = models.CharField(max_length=254, db_collation='Latin1_General_CI_AI')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    role = models.ForeignKey('herofashion.Role', models.DO_NOTHING, blank=True, null=True)
    default_submenu = models.ForeignKey('herofashion.SubMenu', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'herofashion_user'
