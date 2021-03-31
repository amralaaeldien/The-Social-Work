from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from . import models
'''
class ProfileAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
    	super(UserAdmin,self).__init__(*args, **kwargs)
    	UserAdmin.fieldsets += (('profile', {'fields': ('bio', 'avatar_thumbnail', 'location', 'tags', 'contact_information', 'verified')}),)
'''
class SubjectTagAdmin(admin.TabularInline):
	model = models.SubjectTag.tags.through

class TagAdmin(admin.ModelAdmin):
	inlines=[SubjectTagAdmin, ]

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.SubjectTag)
#admin.site.unregister(User)
admin.site.register(models.Profile)#, ProfileAdmin)
admin.site.register(models.Organization)
