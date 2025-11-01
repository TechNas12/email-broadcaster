from django.contrib import admin
from .models import Sender
from .models import EmailOperations

# Register your models here
admin.site.register(Sender)
admin.site.register(EmailOperations)
