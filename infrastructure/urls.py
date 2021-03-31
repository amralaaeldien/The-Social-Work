from django.urls import path

from . import forms
from . import views
app_name = 'infrastructure'
urlpatterns = [
	path('', views.results, name='index' ),
	path('accounts/edit/<slug>/', views.ProfileUpdate.as_view(), name='edit-user-profile' ),
	path('accounts/<slug>/', views.ProfileDetail.as_view(), name='display-profile' ),
	path('accounts/<slug>/orgs', views.UserOrgsView, name='user-orgs-view' ),
	path('tags/<tag_name>/', views.TagUserView, name='tag-user-view'),
	path('tags/', views.TagsView, name='tags-view'),
	path('org/create', views.OrganizationCreate.as_view(), name = 'org-create'),
	path('org/<slug>', views.OrganizationDetail.as_view(), name='org-detail'),
	path('org/<slug>/edit', views.OrganizationUpdate.as_view(), name='org-edit'),


]