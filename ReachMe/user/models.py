from django.db import models
from django.contrib.auth.models import User
from django.db.models import deletion
from django.db.models.signals import post_save
from django.dispatch import receiver


class Interest(models.Model):
    name = models.CharField(max_length=127, null=True, unique=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    GENDER_OPTIONS = (
                    ('Male', 'Male'),
                    ('Female', 'Female'),
                    ('Transgender', 'Transgender'),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, to_field='username')
    name = models.CharField(max_length=127, null=True)
    phone = models.CharField(max_length=31, null=True)
    profile_pic = models.ImageField(null=True, blank = True)
    date_of_birth = models.DateField(max_length=8, null=True)
    gender = models.CharField(max_length=15, null=True, blank=True, choices=GENDER_OPTIONS)
    city = models.CharField(max_length=127, null=True)
    interests = models.ManyToManyField(Interest)
    bio = models.CharField(max_length=56, null=True)
    match = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

class FriendShipStatus(models.Model):
    STATUS_OPTIONS = (
        ('ab', 'ab'),
        ('ba', 'ba'),
        ('axb', 'axb'),
    )
    user_a = models.ForeignKey(User, on_delete=deletion.CASCADE, related_name='+')
    user_b = models.ForeignKey(User, on_delete=deletion.CASCADE, related_name='+')
    status = models.CharField(max_length=3, choices=STATUS_OPTIONS)