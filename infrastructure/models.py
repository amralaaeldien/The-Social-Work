from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser

class Tag(models.Model):
	name = models.TextField()
	verified = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class SubjectTag(models.Model):
	name = models.TextField()
	verified = models.BooleanField(default=False)
	tags = models.ManyToManyField(Tag, related_name='subject_tag')
	def __str__(self):
		return self.name
		
class Profile(AbstractUser):
	#user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE)
	bio = models.TextField()
	slug = models.SlugField(unique=True, blank=True)
	avatar_thumbnail = ProcessedImageField(upload_to='images/',
											default='/images/default.png',
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 60})
	location = models.TextField()
	tags = models.ManyToManyField(Tag)
	contact_information = models.TextField()
	verified = models.BooleanField(default=False)

	def __str__(self):
		return self.slug

	def save(self, *args, **kwargs):
		self.slug = self.username
		super(Profile, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('infrastructure:edit-user-profile', kwargs={'slug': self.slug})

	objects = UserManager()





class Organization(models.Model):
	moderators = models.ManyToManyField(Profile)
	name = models.CharField(max_length=500, unique=True)
	slug = models.SlugField(max_length=500, unique=True, blank=True)
	bio = models.TextField()
	avatar_thumbnail = ProcessedImageField(upload_to='images/',
											default='/images/default2.png',
                                           processors=[ResizeToFill(100, 50)],
                                           format='JPEG',
                                           options={'quality': 60})
	location = models.TextField()
	tags = models.ManyToManyField(Tag)
	contact_information = models.TextField()
	verified = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Organization, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('infrastructure:org-detail', kwargs={'slug': self.slug})