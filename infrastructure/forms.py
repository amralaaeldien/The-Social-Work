from django.forms import CharField, ModelForm
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm

import re

def valid_hashtag(value):
	values = value.split(' ')
	for value in values:
		if not re.match(r'\B(\#[a-zA-Z]+\b)(?!;)', value) :
			raise forms.ValidationError("Name should begin with #")

class PostForm(ModelForm):
	class Meta:
		model = models.Post
		fields = [
			'content',
			'post_type',
			'is_urgent',	
		]

class OrganizationForm(ModelForm):

	class Meta:
		model= models.Organization
		fields = [
			'name',
			'slug',
			'bio',
			'avatar_thumbnail',
			'location',
			'contact_information',
		]

class TagForm(ModelForm):
	class Meta:
		model = models.Tag
		fields = ['subject_tags',]
		exclude=['name',]
	subject_tags = forms.ModelMultipleChoiceField(queryset=models.SubjectTag.objects.all())

	def __init__(self, *args, **kwargs):
		if kwargs.get('instance'):
			initial = kwargs.setdefault('initial', {})
			initial['subject_tag'] = [t.pk for t in kwargs['instance'].subject_tag_set.all()]
		return forms.ModelForm.__init__(self, *args, **kwargs)
		

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = models.Profile
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user