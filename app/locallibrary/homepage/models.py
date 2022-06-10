from django.db import models

class History(models.Model):
    cmd = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    executed_at = models.DateField()

    def __str__(self):
        return self.id

