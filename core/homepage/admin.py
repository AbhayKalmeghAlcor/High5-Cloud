from django.contrib import admin
from .models import Posts, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = ('point', 'recipients', 'sender', 'hashtags', 'comments')
    list_display_links = ('point', 'recipients', 'sender')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created', 'react_by', 'created_by', 'active')
    list_display_links = ('comment',)


admin.site.register(Comments, CommentAdmin)
admin.site.register(Posts, PostAdmin)




