# Generated by Django 5.0.6 on 2024-06-26 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_ssh_pass_connection_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='host',
            new_name='ssh_host',
        ),
        migrations.RenameField(
            model_name='connection',
            old_name='password',
            new_name='ssh_pass',
        ),
        migrations.RenameField(
            model_name='connection',
            old_name='port',
            new_name='ssh_port',
        ),
        migrations.RenameField(
            model_name='connection',
            old_name='username',
            new_name='ssh_user',
        ),
    ]
