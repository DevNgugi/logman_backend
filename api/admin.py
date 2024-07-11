from django.contrib import admin

from api.models import Connection, Organization, Source


admin.site.register(Organization)
admin.site.register(Source)
admin.site.register(Connection)
