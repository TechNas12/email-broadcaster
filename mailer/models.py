from django.db import models
from django_cryptography.fields import encrypt

# Create your models here.
class Sender(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    app_password = encrypt(models.CharField(max_length=19))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sender Email Account"
        verbose_name_plural = "Sender Email Accounts"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Sender Name: {self.name} | Sender email: {self.email}"