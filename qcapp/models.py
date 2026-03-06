from django.db import models
from django.db import models


class QcAdminMistake(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='qc_admin_mistakes/')

    def __str__(self):
        return self.name
    

class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Line(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lines")
    line_number = models.IntegerField()

    class Meta:
        unique_together = ['unit', 'line_number']

    def __str__(self):
        return f"{self.unit.name} - Line {self.line_number}"