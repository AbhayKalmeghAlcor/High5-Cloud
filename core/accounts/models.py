from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True, default='Abhay')
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    manager_email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    hire_date = models.DateField(null=True)
    birth_date = models.DateField(null=True)
    country = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    react = models.CharField(max_length=200, null=True)
    avtar = models.ImageField(upload_to='photos/users', blank=True)
    user_mode = models.CharField(max_length=20, default='normal', null=True)
    created_by = models.CharField(max_length=100, default='admin', null=True)
    updated_by = models.CharField(max_length=100, default='admin', null=True)
    interest = models.JSONField(default=list)
    # allowance_boost = models.IntegerField(default=200)
    points_available = models.IntegerField(default=170)  # under select points section, point given by company. CJ run
    points_received = models.IntegerField(default=0)  # part of 390 in design
    points_redeemed = models.IntegerField(default=0)  #
    achievements_notification = models.BooleanField(default=True)
    activity_update_notification = models.BooleanField(default=True)
    allowance_notification = models.BooleanField(default=True)
    bonus_notification = models.BooleanField(default=True)
    comments_notification = models.BooleanField(default=True)

    # Required
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    @property
    def full_name(self):
        # return "%s %s" % (self.first_name, self.last_name)
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
