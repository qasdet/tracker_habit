from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'telegram_id')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'telegram_id')
        return self.readonly_fields