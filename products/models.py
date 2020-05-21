from django.db import models
from bills.models import Bill

# Create your models here.
class Product(models.Model):
    id          = models.CharField(max_length = 100, primary_key = True)
    name        = models.CharField(max_length = 150, blank = False,  default = '')
    description = models.CharField(max_length = 300,blank = False, default = '')
    avalible    = models.BooleanField(default = True)
    bills       = models.ManyToManyField(Bill)
