from django.db import models
from encrypted_model_fields.fields import EncryptedCharField

# Create your models here.
class Sender(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    app_password = EncryptedCharField(max_length=19)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sender Email Account"
        verbose_name_plural = "Sender Email Accounts"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Sender Name: {self.name} | Sender email: {self.email}"
    
class EmailOperations(models.Model):
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name="emails")
    recipient = models.EmailField(unique=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} -> {self.recipient}"