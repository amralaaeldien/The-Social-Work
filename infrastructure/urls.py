from django.urls import path, include

from . import forms
from . import views
app_name = 'infrastructure'
urlpatterns = [
	path('', views.results, name='index' ),
	path('accounts/', include('django.contrib.auth.urls')),
	path("register", views.register, name="register"),
	path('about', views.about, name='about'),
	path('posts_guide', views.posts_guide, name='posts-guide'),
	path('comments_guide', views.comments_guide, name='comments-guide'),
	path('accounts/edit/<slug>/', views.ProfileUpdate.as_view(), name='edit-user-profile' ),
	path('accounts/<slug>/', views.ProfileDetail.as_view(), name='display-profile' ),
	path('accounts/<slug>/orgs', views.UserOrgsView, name='user-orgs-view' ),
	path('tags/<tag_name>/', views.TagUserView, name='tag-user-view'),
	path('tags/', views.TagsView, name='tags-view'),
	path('org/create', views.OrganizationCreate.as_view(), name = 'org-create'),
	path('org/<slug>', views.OrganizationDetail.as_view(), name='org-detail'),
	path('org/<slug>/edit', views.OrganizationUpdate.as_view(), name='org-edit'),
	path('publish_post/user/<slug>', views.PublishPostView, name='publish-post-user'),
	path('publish_post/org/<slug>', views.PublishPostView, name='publish-post-org'),
	path('post/<id>', views.PostView, name='post-detail'),
	path('comments/<id>', views.CommentsCreation, name='comments-creation'), #the id here is for the post that is having the comment
	path('upvote/<id>', views.PostUpView, name='upvote'),
	path('unvote/<id>', views.PostUnvoteView, name='unvote'),
	path('order_by_time', views.OrderingByTime, name='order-by-time'),
	path('order_by_votes', views.OrderingByVotes, name='order-by-votes')



]