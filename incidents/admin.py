from django.contrib import admin
from .models import Incident

# Register your models here.


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['id', 'resident', 'incident_type', 'created_by', 'created_at', 'is_resolved']
    list_filter = ['incident_type', 'is_resolved', 'created_at']
    search_fields = ['resident__first_name', 'resident__last_name', 'description']
    readonly_fields = ['created_by', 'created_at']
    date_hierarchy = 'created_at'
