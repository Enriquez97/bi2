from django.db import models
import uuid

# Create your models here.
class DataConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config_sp_name = models.CharField(max_length=200, blank=True,null=True, unique=True)
    config = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.config_sp_name
    
class StoreProcedure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sp_name = models.CharField(max_length=50, blank=True,null=True, unique=True)
    parameters = models.TextField(blank=True)
    config  = models.ForeignKey(DataConfig,on_delete =models.SET_NULL,null=True,blank=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.sp_name
    
