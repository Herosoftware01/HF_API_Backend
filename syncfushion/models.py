from django.db import models
from django.conf import settings  # <-- important

class GridSetting(models.Model):
    name = models.CharField(max_length=255)
    data = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- dynamic reference
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name