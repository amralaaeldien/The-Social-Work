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


def results(request):
	slug = request.user.slug
	user_posts = Post.objects.all().exclude(publisher_user__isnull = True)
	voted_users = Voters.objects.filter(voter = request.user)
	print(voted_users)
	ids = []
	for vote in voted_users:
		ids.append(vote.post.id)
	print(ids)
	print('hooooooooooooooooooooooooooooooooooooooooooo')
	org_posts = Post.objects.all().exclude(publisher_org__isnull=True)
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
	comments = Comment.objects.filter(post=post)
	return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def CommentsCreation(request, id):
	post = Post.objects.get(id = id)
	Comment.objects.create(content = request.POST.get('comment'), publisher_user=request.user, post = post)
	return HttpResponseRedirect(reverse('infrastructure:post-detail', args=(post.id,)))


#def PostUpView(request, id):
#	post = Post.objects.get(id = id)
#	if(request.user not in post.get_voters):
#		post.up_vote()
#		post.save()
	#path1 = request.get_full_path()
	#path2 = post.get_aboslute_url()
	#if ('/accounts/' in path) and ('/orgs' in path):
	#	return HttpResponseRedirect(reverse('infrastructure:', args=(post.id,)))
#	previous_url = request.META.get('HTTP_REFERER')
#	post.add_voter(request.user)
#	print(post.get_voters)
#	print(post.get_votes())
#	print('hello')
#	return HttpResponseRedirect(previous_url)

def PostUpView(request, id):
	post = Post.objects.get(id = id)
	users = Voters.objects.filter(post = post)
	if not users:
		Voters.objects.create(post = post, voter = request.user)
	print('mother')
	print(users)
	empty_list = []
	#for user in users:
		#empty_list.append(user['voter'])
	for user in users:
		empty_list.append(user.voter.slug)
	if request.user.slug not in empty_list:
		print('print empty_list')
		print(empty_list)
		post.up_vote()
		Voters.objects.create(post = post, voter = request.user)
		post.save()
	else:
		print(empty_list)

	print('hello')
	print(post.get_votes())
	previous_url = request.META.get('HTTP_REFERER')

	return HttpResponseRedirect(previous_url)



def PostUnvoteView(request, id):
#	post = Post.objects.get(id = id)
#	if post.get_votes() > 0 :
#		post.down_vote()
#	post.save()
#	post.voters_list.remove(request.user)
#	print(post.get_voters())
#	print(post.get_votes())
#	print('hello')
	previous_url = request.META.get('HTTP_REFERER')
	#Voters.objects.create(post = post, voter = request.user)
#	return HttpResponseRedirect(previous_url)
	#post_user = Post.objects.get(id = id).posts_of_voters.all()
	post = Post.objects.get(id = id)
	t=post.posts_of_voters
	print('nonononon')
	Voters.objects.filter(Q(post_id= id) & Q(voter=request.user)).delete()
	post.down_vote()
	post.save()
	print(post.get_votes())

	#users = Voters.objects.filter(post = post)
	#if request.user in post_user:
	#	post.down_vote()
	#	post_user.filter(Q(id=id) & Q(publisher_user=request.user)).delete()
	return HttpResponseRedirect(previous_url)
