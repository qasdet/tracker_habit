from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'frequency', 'start_date', 'created_at')
    list_filter = ('frequency', 'start_date', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('habit__name', 'notes')
    date_hierarchy = 'completed_at'