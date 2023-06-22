from django.db import models
from accounts.models import Account
import uuid
from django.contrib.postgres.fields import ArrayField


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
    # recipients = models.OneToOneField(Account, models.CASCADE)
    recipients = models.JSONField(default=list)
    # recipients = ArrayField(models.ForeignKey(Account, on_delete=models.DO_NOTHING))
    sender = models.JSONField(default=dict)
    hashtags = models.JSONField(default=list, null=True)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos/user_form', null=True, max_length=255)
    gif = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    flag_transaction = models.BooleanField(default=False)
    created = models.DateField(auto_created=True)
    react_by = models.JSONField(default=dict, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    updated = models.DateField(auto_created=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+', null=True)
    #  Parent Transaction ID   sub transaction
    #  Points Received - Number



    class Meta:
        verbose_name = 'posts'
        verbose_name_plural = 'posts'

    def __str__(self):
        return "%s %s %s %s" % (self.point, self.recipients, self.comments, self.hashtags)


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



# Properties Table
# Active
# ID
# Company ID – Foreign Key from Company Table
# Hashtags: List of hashtags to be shown at the time of appreciating someone, Add up-to 10. (For ex: #alcor #teams #oneTeam #Teambuilding) – Array
# Monthly Allowance: Maximum High5 points a user can give in a month.
# Points Given: Set the range of the points that a user can give someone while appreciating. This should be a comma separated list (For ex: 10, 20, 30, etc)
# Birthday Points: Points to be gifted to a user on their Birthday – Number
# Anniversary Points: Points to be gifted to a user on their Anniversary – Number
# Email Anniversary: Email of High5 User that is to be used as Anniversary Bot
# Email Birthday: Email of High5 User that is to be used as Birthday Bot
# Created (Date/Time)
# Created By (User)
# Updated (Date/TIme)
# Updated By (User)
