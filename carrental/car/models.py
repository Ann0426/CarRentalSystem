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

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()



# class Car(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     daily_rent = models.IntegerField()

#     is_available = models.BooleanField()
#     objects = models.Manager()

#     def get_absolute_url(self):
#         return reverse('car-details', kwargs={'pk': self.pk})

#     def __str__(self):
#         return self.name
    
# class Booking(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)

#     customer_name = models.CharField(max_length=100)
#     customer_email = models.EmailField()
#     customer_phone_number = models.TextField()

#     booking_start_date = models.DateField()
#     booking_end_date = models.DateField()
#     booking_message = models.TextField()

#     is_approved = models.BooleanField()
#     objects = models.Manager()
