# Generated by Django 5.0.6 on 2024-06-27 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_source_file_name_source_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='file_name',
        ),
    ]
