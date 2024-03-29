# Generated by Django 4.2.2 on 2023-07-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_comments_id_alter_posts_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='updated',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='created',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='updated',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='properties',
            name='created',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='properties',
            name='updated',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
