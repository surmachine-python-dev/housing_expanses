from django.contrib import admin
from .models import MeterReading

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'utility_type', 'date', 'reading_value')
    list_filter = ('user', 'utility_type', 'date')
    search_fields = ('user__username', 'utility_type')

