from django.db import models
from django.conf import settings

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=200)
    coord_y = models.CharField(max_length=20, null=True)
    coord_x = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)