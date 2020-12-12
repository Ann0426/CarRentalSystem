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


class Profile(models.Model):
    types = [('individual', 'Individual'), ('corporate', 'Corporate')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=30, blank=True)
    # last_name =  models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    customer_type = models.CharField(max_length=20, default='individual', choices=types)
    corporation_name = models.CharField(max_length=50, blank=True)
    # profile = models.CharField(max_length=50, blank=True)
    # profile = models.CharField(max_length=50, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()