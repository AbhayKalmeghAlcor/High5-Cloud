# Generated by Django 4.2.2 on 2023-07-20 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_alter_comments_react_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ('-created',), 'verbose_name': 'posts', 'verbose_name_plural': 'posts'},
        ),
    ]
