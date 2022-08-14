from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default="default.png",upload_to='profile_pics')
    courses = models.ManyToManyField(Course,blank=True)
    staff_cred = models.BooleanField(default=False)

    def __str__(self):
        if(self.staff_cred): return f'{self.user.username} Profile (Staff)'
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=30)

    def __str__(self):
        return self.code


# class Staff(models.Model):
#     profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
#     courses = models.ManyToManyField(Course)
    
# class SlotLimit(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     slots_booked = models.IntegerField(default=0)