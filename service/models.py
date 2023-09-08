from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    pan_card_number = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
