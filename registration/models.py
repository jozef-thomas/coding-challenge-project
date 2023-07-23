from django.db import models

# Create your models here.

class UpdateForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
