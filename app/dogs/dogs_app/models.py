from django.db import models

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)

    def __str__(self):
        return self.title
    
