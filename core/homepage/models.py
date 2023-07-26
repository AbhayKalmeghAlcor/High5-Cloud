from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import Account
from utils.models import BaseModel


class Reaction(models.Model):
    reaction_hash = models.CharField(max_length=50)

    def __str__(self):
        return self.reaction_hash


class Hashtag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    parent = parent = models.ForeignKey(
        'self', 
        related_name='children', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )
    point = models.IntegerField(default=10, null=False)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transfers')
    recipients = models.ManyToManyField(Account, related_name='received_transfers')
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, blank=True)
    gif = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    react_by = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ('-created',)

    def __str__(self):
        return "%s %s %s" % (self.point, self.recipients, self.hashtags)


class Comments(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    react_by = models.JSONField(default=dict)
    flagged_comment = models.BooleanField(default=False)
    image = models.ImageField(upload_to='photos/user_form', null=True, blank=True)
    gif = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = 'comments'


class UserReaction(BaseModel):
    reaction = models.ForeignKey(
        Reaction, 
        related_name="user_reactions", 
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('created_by', 'object_id', 'content_type')
    
    def __str__(self):
        return f"UserReaction - ID: {self.pk}, Reaction: {self.reaction}, Content Type: {self.content_type}, Object ID: {self.object_id}"


class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    company_type = models.CharField(max_length=255, null=True)
    description = models.TextField(default='', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
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
