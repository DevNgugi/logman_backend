# your_app/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create groups and assign permissions dynamically'

    def handle(self, *args, **kwargs):
        groups_permissions = {
            'Managers': ['add_source'],
            'Viewers': ['view_source'],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

            group.permissions.clear()

            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Permission "{perm}" added to group "{group_name}".'))
                except Permission.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Permission "{perm}" does not exist.'))
