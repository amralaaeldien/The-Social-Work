from django.shortcuts import render
from .models import Profile
# Create your views here.
from django.core import exceptions
from django.http import HttpResponse, HttpResponseRedirect

import re
from . import forms
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Profile, Tag, Organization, Post, Comment, Voters, SubjectTag
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import PostForm, TagForm
from django.db.models import Q

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

from infrastructure import forms
from django.db.models import Q

def results(request):

	needer = 'n'
	highest= 'h'
	needer_or_helper = request.GET.get('needer_or_helper', needer)
	highest_or_recent = request.GET.get('highest_or_recent', highest)

	if (needer_or_helper == needer):
		if (highest_or_recent == highest):
			urgent_posts = Post.objects.filter(post_type=needer_or_helper, is_urgent = True).order_by('-votes')
			nonurgent_posts = Post.objects.filter(post_type=needer_or_helper, is_urgent = False).order_by('-votes')
		else:
			urgent_posts = Post.objects.filter(post_type=needer_or_helper, is_urgent = True).order_by('-created_at')
			nonurgent_posts = Post.objects.filter(post_type=needer_or_helper, is_urgent = False).order_by('-created_at')
	else:
		if (highest_or_recent == highest):
			urgent_posts = None
			nonurgent_posts = Post.objects.filter(post_type=needer_or_helper).order_by('-votes')

		else:
			urgent_posts= None
			nonurgent_posts = Post.objects.filter(post_type=needer_or_helper).order_by('-created_at')

	ids = []
	if request.user.is_authenticated:
		#Getting the ids of all the posts the current user has upvoted
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			#sending the ids of the upvoted posts to template to choose when to render upvote
			#and when to render unvote
			ids.append(vote.post.id)
	
	return render(request, 'index.html', {'ids': ids, 'urgent_posts': urgent_posts, 'nonurgent_posts': nonurgent_posts, 'needer_or_helper': needer_or_helper, 'highest_or_recent': highest_or_recent})
		
	'''
	ids = []
	slug = None
	if request.user.is_authenticated:
		slug = request.user.slug
		#Getting the ids of all the posts the current user has upvoted
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			#sending the ids of the upvoted posts to template to choose when to render upvote
			#and when to render unvote
			ids.append(vote.post.id)		
	user_posts = Post.objects.all().exclude(publisher_user__isnull = True)
	org_posts = Post.objects.all().exclude(publisher_org__isnull=True)
	return render(request, 'index.html', {'ids' : ids,'slug' : slug, 'user_posts': user_posts, 'org_posts': org_posts})
	'''
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("infrastructure:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def about(request):
	return render(request, 'about.html')

def comments_guide(request):
	return render(request, 'comments_guide.html')

def posts_guide(request):
	return render(request, 'posts_guide.html')

def OrderingByTime(request):
	slug = None
	ids = []
	if request.user.is_authenticated:
		slug = request.user.slug
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			ids.append(vote.post.id)
	user_posts = Post.objects.all().exclude(publisher_user__isnull = True).order_by("-created_at")
	org_posts = Post.objects.all().exclude(publisher_org__isnull=True).order_by("-created_at")
	return render(request, 'index.html', {'ids' : ids,'slug' : slug, 'user_posts': user_posts, 'org_posts': org_posts})

def OrderingByVotes(request):
	slug =None
	ids=[]
	if request.user.is_authenticated:
		slug = request.user.slug
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			ids.append(vote.post.id)
	user_posts = Post.objects.all().exclude(publisher_user__isnull = True).order_by('-votes')
	org_posts = Post.objects.all().exclude(publisher_org__isnull=True).order_by('-votes')
	return render(request, 'index.html', {'ids' : ids,'slug' : slug, 'user_posts': user_posts, 'org_posts': org_posts})


class ProfileUpdate(UpdateView):
	model = Profile
	fields= [
		'username',
		'bio',
		'avatar_thumbnail',
		'location',
		'contact_information'
		]

	def get_object(self):
		obj = Profile.objects.get(slug = self.kwargs.get('slug'))
		if obj != self.request.user:
			raise exceptions.PermissionDenied()
		return obj

	def get_success_url(self):
		user = self.get_object()
		POST = self.request.POST.copy()

		choice_tags = POST.getlist('tags2')
		tags = set()
		for tag in choice_tags:
			tag_obj = Tag.objects.get(name = tag)
			tags.add(tag_obj)

		text_input_tags = POST.getlist('tags1')[0]
		text_input_tags = text_input_tags.strip()
		text_inputs_tags = text_input_tags.split(' ')
		for tag in text_inputs_tags:
			if tag != '':
				if not tag.startswith('#') :
					tag = '#' + tag
				tag_obj = Tag.objects.get_or_create(name = tag, verified=False)[0]	
				tag_obj.save()
				tags.add(tag_obj)

		user.tags.set(tags)

		return super().get_success_url()


	def get_context_data(self, **kwargs):
		context = super(ProfileUpdate, self).get_context_data(**kwargs)
		subject_tags = SubjectTag.objects.all()
		context['subject_tags'] =  subject_tags
		return context 
	
	def get_queryset(self):
		base_qs = super(ProfileUpdate, self).get_queryset()
		return base_qs.filter(username=self.request.user.username)
	
	def post(self, request, *args, **kwargs):
		print(request.FILES)
		return super().post(request, *args, **kwargs)

class OrganizationUpdate(UpdateView):
	model = Organization
	form_class = forms.OrganizationForm

	def get_object(self):
		obj = Organization.objects.get(slug = self.kwargs.get('slug'))
		if self.request.user not in obj.moderators.all() :
			raise exceptions.PermissionDenied()
		return obj

	def get_success_url(self):

		org = self.get_object()
		POST = self.request.POST.copy()

		choice_tags = POST.getlist('tags2')
		tags = set()
		for tag in choice_tags:
			tag_obj = Tag.objects.get(name = tag)
			tags.add(tag_obj)

		text_input_tags = POST.getlist('tags1')[0]
		text_input_tags = text_input_tags.strip()
		text_inputs_tags = text_input_tags.split(' ')
		for tag in text_inputs_tags:
			if tag != '':
				if not tag.startswith('#') :
					tag = '#' + tag
				tag_obj = Tag.objects.get_or_create(name = tag)[0]	
				tag_obj.save()
				tags.add(tag_obj)

		org.tags.set(tags)

		return super().get_success_url()

	def get_context_data(self, **kwargs):
		context = {}
		subject_tags = SubjectTag.objects.all()
		context['subject_tags'] =  subject_tags
		context.update(kwargs)
		return super().get_context_data(**context)

from django.views.generic.edit import FormView

class ProfileDetail(DetailView, FormView):
	model = Profile
	form_class = PostForm

	def get_object(self):
		return Profile.objects.get(slug = self.kwargs.get('slug'))

	def get_context_data(self, **kwargs):
		context = super(ProfileDetail, self).get_context_data(**kwargs)
		request = self.request
		ids=[]
		if request.user.is_authenticated:
			voted_users = Voters.objects.filter(voter = request.user)
			for vote in voted_users:
				ids.append(vote.post.id)
		context['ids'] = ids

		return context

def TagUserView(request, tag_name):
	users = Tag.objects.get(name=tag_name).profile_set
	orgs = Tag.objects.get(name=tag_name).organization_set
	return render(request, 'tag_user.html', { 'users' : users, 'orgs' : orgs})

def TagsView(request):
	tags = Tag.objects.filter(verified=True).all()
	return render(request, 'tags.html', {'tags': tags})

class OrganizationCreate(CreateView):
	model = Organization
	fields = [
		'name',
		'bio',
		'avatar_thumbnail',
		'location',
		'contact_information',
	]

	def form_valid(self, form):
		form.instance.save()
		my_p = Profile.objects.get(username=self.request.user.username)
		form.instance.moderators.add(my_p)
		return super().form_valid(form)


class OrganizationDetail(DetailView):
	model = Organization

	def get_context_data(self, **kwargs) :
		context = super().get_context_data(**kwargs)
		context['form'] = PostForm
		return context

def UserOrgsView(request, slug):
	orgs = Profile.objects.get(slug=slug).organization_set
	return render(request, 'user_orgs.html', { 'orgs' : orgs})


class PostCreate(CreateView):
	from .forms import PostForm
	model = Post
	form_class = PostForm
	template_name ='profile_detail.html'

	def form_valid(self, form):
		post = form.instance
		path = self.request.get_full_path()
		if 'publish_post/user/' in path :
			post.publisher_user= self.request.user
			post.save()
		else :
			slug = self.kwargs.get('slug', None)
			publisher_org = Organization.objects.get(slug = slug)
			post.publisher_org= publisher_org
		return super().form_valid(form)

def PostView(request, id):
	post = Post.objects.get(id=id)
	if post.publisher_user :
		user = post.publisher_user
		org = None
	elif post.publisher_org :
		org = post.publisher_org
		user = None
	comments = Comment.objects.filter(post=post)
	votes = post.get_votes()
	ids = []

	if request.user.is_authenticated:
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			ids.append(vote.post.id)
	return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'votes': votes, 'ids': ids, 'user': user, 'org':org})

def CommentsCreation(request, id):
	post = Post.objects.get(id = id)
	Comment.objects.create(content = request.POST.get('comment'), publisher_user=request.user, post = post)
	return HttpResponseRedirect(reverse('infrastructure:post-detail', args=(post.id,)))

def PostUpView(request, id):
	post = Post.objects.get(id = id)
	users = Voters.objects.filter(post = post)
	if not users:
		Voters.objects.create(post = post, voter = request.user)

	empty_list = []

	for user in users:
		empty_list.append(user.voter.slug)
	if request.user.slug not in empty_list:

		post.up_vote()
		Voters.objects.create(post = post, voter = request.user)
		post.save()
	else:
		pass
	previous_url = request.META.get('HTTP_REFERER')

	return HttpResponseRedirect(previous_url)

def PostUnvoteView(request, id):

	previous_url = request.META.get('HTTP_REFERER')

	post = Post.objects.get(id = id)

	Voters.objects.filter(Q(post_id= id) & Q(voter=request.user)).delete()
	post.down_vote()
	post.save()

	return HttpResponseRedirect(previous_url)
