from django.db import models
from django.contrib.auth.models import User
# from users.models import Profile
# from slots.models import TimeConfig,IPAddress
    
class Course(models.Model):
    course_code = models.CharField(max_length=5,null=True,blank=True)
    name = models.CharField(max_length=100)
    professors = models.ManyToManyField(User,related_name='professors')
    staff = models.ManyToManyField(User,related_name='staff')
    students = models.ManyToManyField(User,related_name='students')
    description = models.TextField(null=True)

    
    def __str__(self):
        return self.name

class Tutorial(models.Model):
    title = models.CharField(max_length=50,null=True)
    link = models.URLField(null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)

class Lab(models.Model):
    lab_no = models.IntegerField(default=1)
    lab_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)
    date_due = models.DateTimeField(null=True,blank=True)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    tutorials = models.FileField(upload_to='tutorials/',blank=True)

    def __str__(self):
        return self.lab_name