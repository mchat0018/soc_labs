from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from courses.models import Course

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(m2m_changed,sender=Course.professors.through)
def add_course_profs(sender,instance,action,**kwargs):
    print('Signal sent')
    if action == 'post_add':
        print(instance.professors.all())
        for professor in instance.professors.all():
            pf = Profile.objects.get(user=professor)
            pf.courses.add(instance)
            pf.staff_cred = True
            pf.save()
            print('Profile updated')
            professor.profile.save()

@receiver(m2m_changed,sender=Course.staff.through)
def add_course_staff(sender,instance,action,**kwargs):
    print('Signal sent')
    if action == 'post_add':
        print(instance.staff.all())
        for ta in instance.staff.all():
            pf = Profile.objects.get(user=ta)
            pf.courses.add(instance)
            pf.staff_cred = True
            pf.save()
            ta.profile.save()

@receiver(m2m_changed,sender=Course.students.through)
def add_course_student(sender,instance,action,**kwargs):
    print('Signal sent')
    if action == 'post_add':
        for student in instance.students.all():
            pf = Profile.objects.get(user=student)
            pf.courses.add(instance)
            pf.save()
            student.profile.save()

# @receiver(post_save,sender=Course)
# def save_courses(sender,instance,**kwargs):
#     for professor in instance.professors.all():
#         professor.profile.save()

#     for ta in instance.staff.all():
#         ta.profile.save()

#     for student in instance.students.all():
#         student.profile.save()