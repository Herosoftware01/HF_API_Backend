from django.db import models

class MasProcess(models.Model):
    process_id = models.IntegerField(db_column='Process_ID', primary_key=True)
    process_des = models.CharField(db_column='Process_des', max_length=150, blank=True, null=True)
    mc = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Mas_Process'


class Master_Operation_Category(models.Model):
    id = models.AutoField(primary_key=True)

    category_type = models.CharField(max_length=20)
    machine_name = models.CharField(max_length=50)
    operations = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Master_Operation_Category'

    def __str__(self):
        return f"{self.category_type} - {self.operations}"