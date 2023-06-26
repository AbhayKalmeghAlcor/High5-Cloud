from django.db import models
from accounts.models import Account
import uuid
# from django.contrib.postgres.fields import ArrayField, JSONField
# from django.db.models import JSONField
# from rest_framework.renderers import JSONRenderer as JSONBField


class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    point = models.IntegerField(default=10, null=False)
    recipients = models.JSONField(default=dict)
    sender = models.JSONField(default=dict)
    hashtags = models.JSONField(default=list, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, blank=True, max_length=255)
    gif = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    react_by = models.JSONField(default=dict, null=True,blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    created = models.DateField(auto_created=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateField(auto_created=True)

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
    updated = models.DateField(auto_created=True, null=True, blank=True)

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
    created = models.DateField(auto_created=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    updated = models.DateField(auto_created=True, null=True)

    class Meta:
        verbose_name = 'properties'
        verbose_name_plural = 'properties'

# recipients = models.OneToOneField(Account, models.CASCADE)
# recipients = JSONRenderer()
# recipients = models.JSONBField(default=list, null=True, blank=True)
# recipients = ArrayField(models.ForeignKey(Account, on_delete=models.DO_NOTHING))
# hashtags = models.JSONField(
#     max_length=30,
#     choices=HASHTAG_CHOICES,
#     # default='#OneTeam'
# )

# hashtags = ArrayField(
#     models.CharField(max_length=100, blank=True),
#     default=list(("OneTeam", "Vision", "Collaboration", "Culture", "Training", "Quality", "ProblemSolving",
#                   "Teambuilding")))

# monthly_allowance = models.IntegerField(default=200)
# points_given = models.CharField(
#     max_length=3,
#     choices=POINT_CHOICES,
#     default='10'
# )

# HASHTAG_CHOICES = (
#     ("#OneTeam", "#OneTeam"),
#     ("#Vision", "#Vision"),
#     ("#Collaboration", "#Collaboration"),
#     ("#Culture", "#Culture"),
#     ("#Training", "#Quality"),
#     ("#ProblemSolving", "#ProblemSolving"),
#     ("#Teambuilding", "#Teambuilding"),
# )
# POINT_CHOICES = (
#     ("10", "10"),
#     ("20", "20"),
#     ("30", "30"),
#     ("40", "40"),
#     ("50", "50"),
# )