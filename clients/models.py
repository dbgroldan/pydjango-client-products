from django.db import models

# Create your models here.
class Client(models.Model):
    document   = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name  = models.CharField(max_length=150)
    password   = models.CharField(max_length=300, null=False, default='')
    email      = models.CharField(max_length=100, null=False, unique=True)
