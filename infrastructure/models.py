#from typing_extensions import Required
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
	name = models.TextField(primary_key=True)
	verified = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class SubjectTag(models.Model):
	name = models.TextField(primary_key=True)
	verified = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, related_name='subject_tag')
	def __str__(self):
		return self.name

		
class Profile(AbstractUser):
	bio = models.TextField()
	slug = models.SlugField(unique=True, blank=True)
	avatar_thumbnail = ProcessedImageField(upload_to='images/',
											default='/images/default.png',
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 60})
	location = models.TextField()
	tags = models.ManyToManyField(Tag, null=True)
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
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 60})
	location = models.TextField()
	tags = models.ManyToManyField(Tag, null=True)
	contact_information = models.TextField()
	verified = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			if slugify(self.name):
				self.slug = slugify(self.name)
			else:
				self.slug = self.name.replace(" ", "")
		super(Organization, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('infrastructure:org-detail', kwargs={'slug': self.slug})


class Post(models.Model):
	NEEDER = 'n'
	HELPER = 'h'

	POST_TYPES = (
		(NEEDER, 'needer'),
		(HELPER, 'helper')
	)

	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	post_type = models.CharField(choices=POST_TYPES, max_length=1, default=NEEDER)
	publisher_user = models.ForeignKey(Profile, related_name='user_post', on_delete=models.CASCADE, null = True,
		blank = True)
	publisher_org = models.ForeignKey(Organization, related_name='org_post', on_delete=models.CASCADE, null = True,
		blank = True)
	votes = models.IntegerField(default = 0)
	fulfilled = models.BooleanField(default = False)
	is_urgent = models.BooleanField(default = False)

	def __init__(self, *args, **kwargs):
		self.voters_list = []
		return super().__init__(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('infrastructure:post-detail', kwargs={'id': self.id})
	def get_votes(self):
		return self.votes
	def up_vote(self):
		self.votes = self.votes + 1
	def add_voter(self, voter) :
		if voter not in self.voters_list:
			self.voters_list.append(voter)
		else: 
			pass
		return self.voters_list	

	@property	
	def get_voters(self):
		return self.voters_list	

	def down_vote(self):
		self.votes = self.votes -1


class Voters(models.Model):
	voter = models.ForeignKey(Profile, related_name='list_of_voted_users', on_delete=models.CASCADE, null = True,
		blank = True)
	post = models.ForeignKey(Post, related_name='posts_of_voters', on_delete=models.CASCADE, null = True,
		blank = True)

class Comment(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	publisher_user = models.ForeignKey(Profile, related_name='user_comment', on_delete=models.CASCADE, null = True,
		blank = True)
	publisher_org = models.ForeignKey(Organization, related_name='org_comment', on_delete=models.CASCADE, null=True,
		blank = True)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	votes = models.IntegerField(default = 0)
	
	def get_votes(self):
		return self.votes
	def up_vote(self):
		self.votes = self.votes + 1
	def down_vote(self):
		self.votes = self.votes -1



