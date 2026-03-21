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


class qc_piece_data(models.Model):
    bundle_no = models.CharField(max_length=20)
    bundle_id = models.CharField(max_length=20)
    unit =models.IntegerField()
    line =models.IntegerField()
    jobno = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    total_pieces = models.IntegerField()
    piece_no = models.IntegerField()
    category = models.CharField(max_length=50)
    mistake_name = models.CharField(max_length=50)
    mistake_count = models.IntegerField()
    total_mistake = models.IntegerField()
    mistake_percentage = models.CharField(max_length=20)

class qc_piece_final(models.Model):
    bundle_no = models.CharField(max_length=20)
    bundle_id = models.CharField(max_length=20)
    unit =models.IntegerField()
    line =models.IntegerField()
    jobno = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    total_pieces = models.IntegerField()
    checked_piece = models.IntegerField()
    force_save = models.BooleanField(default=False)


