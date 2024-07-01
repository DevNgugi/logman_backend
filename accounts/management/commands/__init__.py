def create_groups(groups_permissions):
    for group_name, permissions in groups_permissions.items():
        # Create the group if it doesn't exist
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f'Group "{group_name}" created.')
        else:
            print(f'Group "{group_name}" already exists.')

        # Clear existing permissions
        group.permissions.clear()

        # Assign new permissions
        for perm in permissions:
            try:
                # Find the permission by its codename
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
                print(f'Permission "{perm}" added to group "{group_name}".')
            except Permission.DoesNotExist:
                print(f'Permission "{perm}" does not exist.')
