from django.db import models

class CategoryMaster(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class SubCategoryMaster(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryMaster, on_delete=models.PROTECT, related_name="subcategories")
    subcategory_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subcategory_name

class Details(models.Model):
    slno = models.AutoField(primary_key=True)
    grievance_id = models.CharField(max_length=50, unique=True)
    subcategory = models.ForeignKey(SubCategoryMaster, on_delete=models.PROTECT, related_name="grievances")
    role = models.CharField(max_length=30)
    description = models.TextField()
    voice_note = models.FileField(upload_to='grievance_voice_notes/', null=True, blank=True)
    Attachment = models.FileField(upload_to='grievance_attachments/', null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    emp_code = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, default='Requested')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grievance_id    

class Transfer(models.Model):
    slno = models.AutoField(primary_key=True)
    grievance = models.ForeignKey(Details, on_delete=models.PROTECT, related_name="transfers")
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Investigation(models.Model):
    slno = models.AutoField(primary_key=True)
    grievance = models.ForeignKey(Details, on_delete=models.PROTECT, related_name="investigations")
    investigator_id = models.IntegerField()
    witness_id = models.IntegerField()
    witness_statement = models.TextField()
    attachment = models.FileField(upload_to='investigation_attachments/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class Solution(models.Model):
    slno = models.AutoField(primary_key=True)
    grievance = models.ForeignKey(Details, on_delete=models.PROTECT, related_name="solutions")
    investigator_id = models.IntegerField()
    opening_date = models.DateTimeField()
    statement = models.TextField()
    solution = models.TextField()
    attachment = models.FileField(upload_to='solution_attachments/', null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)