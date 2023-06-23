# Generated by Django 4.2.2 on 2023-06-22 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
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
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_created=True)),
                ('hashtags', models.CharField(choices=[('#OneTeam', '#OneTeam'), ('#Vision', '#Vision'), ('#Collaboration', '#Collaboration'), ('#Culture', '#Culture'), ('#Training', '#Quality'), ('#ProblemSolving', '#ProblemSolving'), ('#Teambuilding', '#Teambuilding')], default='#OneTeam', max_length=30)),
                ('monthly_allowance', models.IntegerField(default=200)),
                ('points_given', models.CharField(choices=[('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50')], default='10', max_length=3)),
                ('birthday_points', models.IntegerField(default=50)),
                ('anniversary_points', models.IntegerField(default=50)),
                ('email_anniversary', models.EmailField(max_length=500)),
                ('email_birthday', models.EmailField(max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='homepage.company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('updated', models.DateField(auto_created=True)),
                ('created', models.DateField(auto_created=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('point', models.IntegerField(default=10)),
                ('recipients', models.JSONField()),
                ('sender', models.JSONField(default=dict)),
                ('hashtags', models.JSONField(default=list, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(max_length=255, null=True, upload_to='photos/user_form')),
                ('gif', models.CharField(max_length=500, null=True)),
                ('link', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('flag_transaction', models.BooleanField(default=False)),
                ('react_by', models.JSONField(default=dict, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
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
                ('updated', models.DateField(auto_created=True)),
                ('created', models.DateField(auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('react_by', models.JSONField(default=dict)),
                ('flagged_comment', models.BooleanField(default=False)),
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