from django.db import models
from clients.models import Client

# Create your models here.
class Bill(models.Model):
    id           = models.CharField(max_length = 20, primary_key = True)
    company_name = models.CharField(max_length = 150)
    nit          = models.CharField(max_length = 20)
    code         = models.CharField(max_length = 20)
    client_id       = models.ForeignKey(Client, on_delete = models.CASCADE,
                                    null = False, blank = False)
    created_at   = models.DateTimeField(auto_now_add = True)
