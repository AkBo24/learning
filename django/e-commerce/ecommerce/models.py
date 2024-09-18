from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

"""
User has a website


Table Website:
- name
- description
- url
- number of visitors

"""

class Website(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    visitors = models.PositiveSmallIntegerField()
    