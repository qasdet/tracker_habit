from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    frequency = models.CharField('Периодичность', max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    start_date = models.DateField('Дата начала', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_status(self):
        """Проверяет статус выполнения привычки на текущий период"""
        now = timezone.now()
        last_log = self.logs.first()
        
        if not last_log:
            return False
            
        if self.frequency == 'daily':
            return last_log.completed_at.date() == now.date()
        elif self.frequency == 'weekly':
            return (now - last_log.completed_at).days <= 7
        elif self.frequency == 'monthly':
            return last_log.completed_at.month == now.month and last_log.completed_at.year == now.year
        return False

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_at = models.DateTimeField('Дата выполнения', auto_now_add=True)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Запись о выполнении'
        verbose_name_plural = 'Записи о выполнении'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.habit.name} - {self.completed_at.strftime("%Y-%m-%d %H:%M")}'