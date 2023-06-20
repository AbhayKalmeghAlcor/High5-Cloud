from django.db import models
from accounts.models import Account
import uuid


class Comments(models.Model):
    active = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    created = models.DateField(auto_created=True)
    react_by = models.JSONField(default=dict)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    flagged_comment = models.BooleanField(default=False)
    # Parent Comment ID
    # post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    updated = models.DateField(auto_created=True)
    # updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    point = models.IntegerField(default=10, null=False)
    #recipients = models.ForeignKey(Account, models.CASCADE)
    recipients = models.JSONField(default=list)
    sender = models.CharField(max_length=254)
    hashtags = models.JSONField(default=list, null=True)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, max_length=255)
    gif = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    created = models.DateField(auto_created=True)
    react_by = models.JSONField(default=dict, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    updated = models.DateField(auto_created=True)

    # updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    #  Parent Transaction ID   sub transaction
    #  Points Received - Number

    class Meta:
        verbose_name = 'posts'
        verbose_name_plural = 'posts'

    def __str__(self):
        return "%s %s %s %s" % (self.point, self.recipients, self.comments, self.hashtags)

# Create your models here.

# class Company(models.Model):
#     name = models.CharField(max_length=255, null=False)
#     company_type = models.CharField(max_length=255, null=True)
#     description = models.TextField(default='', null=True)
#     created_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = 'company'
#         verbose_name_plural = 'companies'
#
#     def __str__(self):
#         return self.name
