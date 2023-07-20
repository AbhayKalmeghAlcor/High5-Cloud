# Generated by Django 4.2.2 on 2023-07-13 12:05

from django.db import migrations, models
import uuid


def copy_id_data_to_uuid(apps, schema_editor):
    Comment = apps.get_model('homepage', 'comments')
    for comment in Comment.objects.all():
        comment.uuid_id = uuid.uuid4()  # Generate a new UUID for each comment
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(copy_id_data_to_uuid),
        migrations.RemoveField(
            model_name='comments',
            name='id',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='uuid_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='created',
            field=models.DateField(auto_created=True),
        ),
    ]
