from django.shortcuts import render
#from .forms import ProfileForm
from .models import Profile
# Create your views here.
#from .forms import SubjectTagForm
from django.core import exceptions
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Profile, Tag, Organization, Post, Comment, Voters
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import TagForm
from django.db.models import Q

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def results(request):
	ids = []
	slug = None
	if request.user.is_authenticated:
		slug = request.user.slug
		voted_users = Voters.objects.filter(voter = request.user)
		for vote in voted_users:
			ids.append(vote.post.id)		
	user_posts = Post.objects.all().exclude(publisher_user__isnull = True)
	org_posts = Post.objects.all().exclude(publisher_org__isnull=True)
	return render(request, 'index.html', {'ids' : ids,'slug' : slug, 'user_posts': user_posts, 'org_posts': org_posts})

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
		'tags',
		'contact_information'
		]

	def get_object(self):
		obj = Profile.objects.get(slug = self.kwargs.get('slug'))
		if obj != self.request.user:
			raise exceptions.PermissionDenied()
		return obj

	def get_context_data(self, **kwargs):
		context = super(ProfileUpdate, self).get_context_data(**kwargs)
		context['tag_form'] = TagForm
		return context 
	
	def get_queryset(self):
		base_qs = super(ProfileUpdate, self).get_queryset()
		return base_qs.filter(username=self.request.user.username)

class OrganizationUpdate(UpdateView):
	model = Organization
	fields = [
		'name',
		'slug',
		'bio',
		'avatar_thumbnail',
		'location',
		'tags',
		'contact_information'
	]

	def get_object(self):
		obj = Organization.objects.get(slug = self.kwargs.get('slug'))
		if self.request.user not in obj.moderators.all() :
			raise exceptions.PermissionDenied()
		return obj

	def form_valid(self, form):
		self.object = form.save()
		self.object.save()
		return super().form_valid(form)


class ProfileDetail(DetailView):
	model = Profile

	def get_object(self):
		return Profile.objects.get(slug = self.kwargs.get('slug'))

	def get_context_data(self, **kwargs):
		context = super(ProfileDetail, self).get_context_data(**kwargs)
		request = self.request
		slug =None
		ids=[]
		if request.user.is_authenticated:
			slug = request.user.slug
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
		'tags',
		'contact_information',
	]

	def form_valid(self, form):
		form.instance.save()
		my_p = Profile.objects.get(username=self.request.user.username)
		form.instance.moderators.add(my_p)
		return super().form_valid(form)

	#def get_object(self):
	#	return Organization.objects.get(pk = self.kwargs.get('org_pk'))

class OrganizationDetail(DetailView):
	model = Organization

def UserOrgsView(request, slug):
	orgs = Profile.objects.get(slug=slug).organization_set
	print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeey')
	print(Profile.objects.get(slug=slug).organization_set)
	return render(request, 'user_orgs.html', { 'orgs' : orgs})

def PublishPostView(request, slug):
	content = request.POST.get("text")
	path = request.get_full_path()
	if 'publish_post/user/' in path :
		Post.objects.create(content=content, publisher_user=request.user)
		return HttpResponseRedirect(reverse('infrastructure:display-profile', args=(slug,)))
	else :
		publisher_org = Organization.objects.get(slug = slug)
		Post.objects.create(content=content, publisher_org=publisher_org)
		return HttpResponseRedirect(reverse('infrastructure:org-detail', args=(slug,)))

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
