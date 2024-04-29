from django.db import models
import uuid

# Create your models here.
class Dashboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True,null=True, unique=True)
    dashboard_layout = models.TextField(blank=True)
    type_dashboard = models.CharField(max_length=100, blank=True,null=True, unique=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.name