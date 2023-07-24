from django.contrib import admin
from .models import Transaction, Properties, Company, Comments, Hashtag


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('point',  'get_hashtags')
    list_display_links = ('point', )

    def get_hashtags(self, obj):
        return ", ".join(hashtag.name for hashtag in obj.hashtags.all())

    get_hashtags.short_description = 'Hashtags'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created', 'react_by', 'created_by', 'active')
    list_display_links = ('comment',)


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('monthly_allowance', 'anniversary_points', 'email_anniversary', 'created')
    list_display_links = ('monthly_allowance',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'description', 'created_date')
    list_display_links = ('name',)

#
admin.site.register(Comments, CommentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Hashtag, HashtagAdmin)
