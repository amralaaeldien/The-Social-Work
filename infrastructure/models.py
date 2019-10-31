from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.TextField()
	verified = models.BooleanField(default=False)

class Profile(User):
	user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE)
	bio = models.TextField()
	location = models.TextField()
	tags = models.ManyToManyField(Tag)
	contact_information = models.TextField()
	verified = models.BooleanField(default=False)

class Organization(models.Model):
	moderators = models.ManyToManyField(Profile)
	name = models.TextField()
	bio = models.TextField()
	location = models.TextField()
	tags = models.ManyToManyField(Tag)
	contact_information = models.TextField()
	verified = models.BooleanField(default=False)
	
