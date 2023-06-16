# Generated by Django 4.2.2 on 2023-06-16 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
    ]
