from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utils.generators import *

from django.utils.translation import gettext as _


# Create your models here.
def user_directory_path(instance, filename):
    filename = "{0}.jpg".format(instance.public_id)
    return '{0}/{1}'.format(instance.public_id, filename)

	
class User(AbstractUser):

	email = models.EmailField('email address', unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	USER_TYPE = (
		('customer', 'Customer'),
		('coach', 'Coach'),
		('nutritionist', 'Nutritionist')
	)

	USER_MODULES = (
		('training', 'Training'),
		('nutrition', 'Nutrition'),
		('tracking', 'Tracking'),
	)

	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	phone = models.CharField(null=True, max_length=15, blank=True)
	user_type = models.CharField(choices= USER_TYPE, default='customer', max_length=20)
	birth_day=models.DateField(blank=True, null=True)
	weight= models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
	height= models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

	address = models.CharField(max_length=100, null=True, blank=True)
	zip_code = models.CharField(max_length=50, blank=True, null=True)

	image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
	public_id = models.SlugField(unique=True, blank=True, null=True)
	short_description = models.TextField(max_length=255, blank=True, null=True)

	enable_training = models.BooleanField(default=False)
	enable_nutrition = models.BooleanField(default=False)
	enable_tracking = models.BooleanField(default=False)

	is_email_confirmed = models.BooleanField(default=False)
	is_whatsapp = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Users"

	def __str__(self):
		return str(self.email)
	
@receiver(pre_save, sender=User)
def pre_save_user(sender, instance, **kwargs):
	if not instance.public_id:
		instance.public_id = "{0}".format(random_string_generator(size=16))

