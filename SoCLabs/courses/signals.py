from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

users = []

@receiver(pre_save, sender=Course)
def getUsers(sender, instance, **kwargs):
    print('ok', instance.students)

@receiver(post_save, sender=Course)
def updateUsers(sender, instance, **kwargs):
    print('ok')
    print(users)
    print('ok')