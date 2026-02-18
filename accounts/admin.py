from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
# This code registers the CustomUser model with the Django admin site, 
# allowing administrators to manage user accounts through the admin interface. 
# It extends the default UserAdmin to include additional fields such as 'role' and 'is_approved', 
# and customizes the list display and filtering options for better user management.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'is_approved')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'is_approved')
        }),
    )
