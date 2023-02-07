from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Photo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    description = models.TextField('Description')
    photos = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return f'{self.creator}: {self.name}'