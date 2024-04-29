from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AccessKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(days=180)) 
    is_active=models.BooleanField(default=True) 

    def save(self, *args, **kwargs):
        # Set expiration date to 6 months from creation
        self.expiration_date = self.created_at + timedelta(days=180)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key
