# Generated by Django 4.2.2 on 2023-07-11 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company_type', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('logo', models.ImageField(blank=True, upload_to='company/logo')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Recognition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateField(auto_created=True, null=True)),
                ('created', models.DateField(auto_created=True)),
                ('monthly_allowance', models.IntegerField(default=170)),
                ('birthday_points', models.IntegerField(default=50)),
                ('anniversary_points', models.IntegerField(default=50)),
                ('email_anniversary', models.EmailField(max_length=500)),
                ('email_birthday', models.EmailField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='homepage.company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'properties',
                'verbose_name_plural': 'properties',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('updated', models.DateField(auto_created=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('parent_id', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('point', models.IntegerField(default=10)),
                ('hashtags', models.JSONField(default=list, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/user_form')),
                ('gif', models.CharField(blank=True, max_length=500, null=True)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
                ('flag_transaction', models.BooleanField(default=False)),
                ('react_by', models.JSONField(blank=True, default=dict, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('recipients', models.ManyToManyField(related_name='received_transfers', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transfers', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'posts',
                'verbose_name_plural': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateField(auto_created=True, blank=True, null=True)),
                ('created', models.DateField(auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('react_by', models.JSONField(default=dict)),
                ('flagged_comment', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/user_form')),
                ('gif', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.posts')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comments',
                'verbose_name_plural': 'comments',
            },
        ),
    ]
