from django.db import models

class Machine_category_master(models.Model):
    id = models.AutoField(primary_key=True)
    machine_name = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_name
                                    
class Operation_Category_master(models.Model):
    id = models.AutoField(primary_key=True)
    machine_cate_id = models.ForeignKey(Machine_category_master, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=20)
    operations = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.category_type} - {self.operations}"
