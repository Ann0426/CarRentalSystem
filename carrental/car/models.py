from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

############## refer to others

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
      verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=255)
    custid = models.IntegerField()


