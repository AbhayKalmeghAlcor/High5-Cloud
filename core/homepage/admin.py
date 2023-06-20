from django.contrib import admin
from .models import Posts
from django.contrib.auth.admin import UserAdmin


class PostAdmin(admin.ModelAdmin):
    list_display = ('point', 'recipients', 'sender', 'hashtags', 'comments')
    list_display_links = ('point', 'recipients', 'sender')


admin.site.register(Posts, PostAdmin)
