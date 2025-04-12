from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_user')
    telegram_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    notification_time = models.TimeField(default='09:00')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'

    def __str__(self):
        return f'{self.user.username} - {self.telegram_id}'