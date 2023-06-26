from django.contrib import admin
from .models import Posts, Comments, Properties, Company


class PostAdmin(admin.ModelAdmin):
    list_display = ('point', 'recipients', 'sender', 'hashtags')
    list_display_links = ('point', 'recipients', 'sender')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created', 'react_by', 'created_by', 'active')
    list_display_links = ('comment',)


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('monthly_allowance', 'anniversary_points', 'email_anniversary', 'created')
    list_display_links = ('monthly_allowance',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'description', 'created_date')
    list_display_links = ('name',)


admin.site.register(Comments, CommentAdmin)
admin.site.register(Posts, PostAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Company, CompanyAdmin)
