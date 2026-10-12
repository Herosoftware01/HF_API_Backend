from django.db import models

class Committee_Master(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    committee_name = models.CharField(max_length=100, unique=True)
    committee_members = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.committee_name

