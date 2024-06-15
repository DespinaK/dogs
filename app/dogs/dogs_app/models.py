import uuid
from django.db import models
from django.contrib.gis.db import models as gis_models 

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class Location(models.Model):
    temp_id = models.UUIDField(default=uuid.uuid4, primary_key=True,unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    #location = gis_models.PointField(srid=4326, null=True, default=None)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    
    #location = models.ForeignKey(Location, on_delete=models.CASCADE)
    #latitude = models.DecimalField(max_digits=9, decimal_places=8, null=True, blank=True)
    #longitude = models.DecimalField(max_digits=9, decimal_places=8, null=True, blank=True)
    #location = models.PointField(srid=4326, null=True, default=None)


