from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


# @receiver(pre_save, sender=Course)
# def delete_slots(sender, instance, **kwargs):
#     for user in instance.user:
#         user