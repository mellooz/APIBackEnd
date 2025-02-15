from django.db import models
from django.contrib.auth.models import AbstractUser # => Django custom User
# from django.contrib.auth.models import User  => Django Default User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.




# Django User Default fields = ['username' , 'email' , 'first_name' , 'last_name' ,  'password' , ...]

class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # to make user login ONLY with email use USERNAME_FIELD = 'email'
    # by default USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'email'
    # make this field required when u make superuser
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    # def profile(self):
    #     ''' This function act like Signals but i used signals ( we dont need it now ) '''
    #     profile, created = Profile.objects.get_or_create(user=self)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images/", default="default.jpg")
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.full_name




@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Signal to create or update profile whenever user is saved """
    if created:
        profile = Profile.objects.create(user=instance)
        profile.full_name = f"{instance.first_name} {instance.last_name}"
        profile.save()
    else:
        instance.profile.full_name = f"{instance.first_name} {instance.last_name}"
        instance.profile.save()




####################################################################

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # to make sure the profile is exist
#     if hasattr(instance, 'profile'):
#         instance.profile.save()

#####################################################################

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)