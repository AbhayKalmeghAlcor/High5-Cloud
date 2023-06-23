from django.db import models
from accounts.models import Account
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import JSONField


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    point = models.IntegerField(default=10, null=False)
    # recipients = models.OneToOneField(Account, models.CASCADE)
    recipients = models.JSONField(default=dict)
    # recipients = JSONBField(default=list, null=True, blank=True)
    # recipients = ArrayField(models.ForeignKey(Account, on_delete=models.DO_NOTHING))
    # recipients = ArrayField(JSONField())
    sender = models.JSONField(default=dict)
    hashtags = models.JSONField(default=list, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, max_length=255)
    gif = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    react_by = models.JSONField(default=dict, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    created = models.DateField(auto_created=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateField(auto_created=True)

    #  Parent Transaction ID   sub transaction
    #  Points Received - Number

    class Meta:
        verbose_name = 'posts'
        verbose_name_plural = 'posts'

    def __str__(self):
        return "%s %s %s" % (self.point, self.recipients, self.hashtags)


class Comments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    react_by = models.JSONField(default=dict)
    flagged_comment = models.BooleanField(default=False)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    created = models.DateField(auto_created=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateField(auto_created=True)

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


HASHTAG_CHOICES = (
    ("#OneTeam", "#OneTeam"),
    ("#Vision", "#Vision"),
    ("#Collaboration", "#Collaboration"),
    ("#Culture", "#Culture"),
    ("#Training", "#Quality"),
    ("#ProblemSolving", "#ProblemSolving"),
    ("#Teambuilding", "#Teambuilding"),
)
POINT_CHOICES = (
    ("10", "10"),
    ("20", "20"),
    ("30", "30"),
    ("40", "40"),
    ("50", "50"),
)


class Properties(models.Model):
    hashtags = models.CharField(
        max_length=30,
        choices=HASHTAG_CHOICES,
        default='#OneTeam'
    )
    monthly_allowance = models.IntegerField(default=200)
    points_given = models.CharField(
        max_length=3,
        choices=POINT_CHOICES,
        default='10'
    )

    birthday_points = models.IntegerField(default=50)
    anniversary_points = models.IntegerField(default=50)
    email_anniversary = models.EmailField(max_length=500)
    email_birthday = models.EmailField(max_length=500)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    created = models.DateField(auto_created=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'properties'
        verbose_name_plural = 'properties'
