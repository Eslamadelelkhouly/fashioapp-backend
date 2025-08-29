from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    title =  models.CharField(max_length=255 , unique=True)
    image = models.URLField(blank=False)

    def __str__(self):
        return self.title
