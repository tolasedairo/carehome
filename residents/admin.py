from django.contrib import admin
from .models import Resident

# Register your models here.


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'room_number',
        'is_active',
        'created_at'
    )

    list_filter = ('is_active', 'gender')
    search_fields = ('first_name', 'last_name', 'room_number')
