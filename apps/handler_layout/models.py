import uuid
from django.db import models
from ..handler_data.models import StoreProcedure

# Create your models here.

class KPI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sp = models.ForeignKey(StoreProcedure,on_delete =models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=100, blank=True,null=True, unique=True)
    type = models.CharField(max_length=100, blank=True,null=True, )
    operation = models.CharField(max_length=100, blank=True,null=True)
    variable_categorical = models.TextField(blank=True, null=True)
    variable_numerical = models.TextField(blank=True, null=True)
    figure = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.name
