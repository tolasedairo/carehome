from django.contrib import admin
from .models import AuditLog

# Register your models here.


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'target_model', 'target_id')
    list_filter = ('action', 'timestamp', 'target_model')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'description')
    readonly_fields = ('user', 'action', 'target_model', 'target_id', 'timestamp', 'description')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        # Prevent manual creation of audit logs through admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of audit logs
        return False
