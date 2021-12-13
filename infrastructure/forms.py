from django.forms import ModelForm
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
'''
class ProfileForm(ModelForm):
	class Meta:
		model = models.Profile
		fields= [
			'bio',
			'avatar_thumbnail',
			'location',
			'tags',
			'contact_information'
		]
'''  

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
		

	def save(self):
		#from .views import ProfileUpdate
		print('hellloo')
		pass
		print('hello')
		#instance = forms.ModelForm.save(self, False)
		#instance.topping_set.add(*self.cleaned_data['subject_tag'])
		#return instance

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