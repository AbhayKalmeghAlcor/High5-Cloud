from django.contrib import admin
from .models import Posts, Comments, Properties, Company


class PostAdmin(admin.ModelAdmin):
    list_display = ('point', 'recipients', 'sender', 'hashtags')
    list_display_links = ('point', 'recipients', 'sender')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created', 'react_by', 'created_by', 'active')
    list_display_links = ('comment',)


admin.site.register(Comments, CommentAdmin)
admin.site.register(Posts, PostAdmin)
admin.site.register(Properties)
admin.site.register(Company)




