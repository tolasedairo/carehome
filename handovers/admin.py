from django.contrib import admin
from .models import Handover


@admin.register(Handover)
class HandoverAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'shift',
        'priority',
        'resident',
        'created_by',
        'is_completed',
        'created_at'
    ]
    list_filter = [
        'shift',
        'priority',
        'is_completed',
        'created_at'
    ]
    search_fields = [
        'title',
        'notes',
        'resident__first_name',
        'resident__last_name'
    ]
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'resident', 'shift', 'priority')
        }),
        ('Details', {
            'fields': ('notes', 'is_completed')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
