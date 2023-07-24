from django.db import models
from accounts.models import Account
import uuid
from django.utils import timezone
from django.contrib.auth.models import User


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.UUIDField(null=True, blank=True)
    point = models.IntegerField(default=10, null=False)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transfers')
    recipients = models.ManyToManyField(Account, related_name='received_transfers')
    hashtags = models.JSONField(default=list, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, blank=True)
    gif = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    react_by = models.JSONField(default=dict, null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    created = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'posts'
        verbose_name_plural = 'posts'
        ordering = ('-created', 'active')

    def __str__(self):
        return "%s %s %s" % (self.point, self.recipients, self.hashtags)


class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    react_by = models.JSONField(default=dict, null=True, blank=True)
    flagged_comment = models.BooleanField(default=False)
    image = models.ImageField(upload_to='photos/user_form', null=True, blank=True)
    gif = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    created = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = 'comments'


class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    company_type = models.CharField(max_length=255, null=True)
    description = models.TextField(default='', null=True)
    created_date = models.DateTimeField(auto_now=True)
    logo = models.ImageField(upload_to='company/logo', blank=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class Properties(models.Model):
    monthly_allowance = models.IntegerField(default=170)
    birthday_points = models.IntegerField(default=50)
    anniversary_points = models.IntegerField(default=50)
    email_anniversary = models.EmailField(max_length=500)
    email_birthday = models.EmailField(max_length=500)
    active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'properties'
        verbose_name_plural = 'properties'


class Userpoints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    monthly_points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='%(class)s_created_by')
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='%(class)s_updated_by')

    class Meta:
        verbose_name = 'userpoints'
        verbose_name_plural = 'userpoints'

    def __str__(self):
        return f'{self.user.email} - Points: {self.monthly_points}'




