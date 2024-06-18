from django.contrib import admin
# Register your models here.
from .models import Connection, Source

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'host', 'port', 'created_at', 'modified_at')
    list_filter = ('host', 'port', 'created_at', 'modified_at')
    search_fields = ('username', 'host')
    readonly_fields = ('created_at', 'modified_at')

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'connection', 'created_at', 'modified_at')
    list_filter = ('connection', 'created_at', 'modified_at')
    search_fields = ('title', 'connection__host')  # Assuming you want to search by connection host
    readonly_fields = ('created_at', 'modified_at')