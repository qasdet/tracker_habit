from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from .models import TelegramUser
from .bot import send_reminder
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_habits_and_send_reminders():
    now = timezone.now()
    current_time = now.strftime('%H:%M')
    logger.info(f'Starting habit check at {current_time}')
    
    # Получаем привычки пользователей, у которых настроено текущее время для уведомлений
    logger.info(f'Current hour: {now.hour}, minute: {now.minute}')
    
    # Проверяем всех активных пользователей
    all_active_users = TelegramUser.objects.filter(is_active=True)
    logger.info(f'Total active users: {all_active_users.count()}')
    
    # Проверяем пользователей с уведомлениями на текущее время
    current_time = now.time().replace(second=0, microsecond=0)
    logger.info(f'Checking for notifications at time: {current_time}')
    
    # Получаем пользователей, у которых время уведомлений совпадает с текущим временем
    telegram_users = all_active_users.filter(notification_time=current_time)
    
    # Добавляем дополнительное логирование для отладки
    logger.info(f'Current time for comparison: {current_time}')
    logger.info(f'Current time components - hour: {current_time.hour}, minute: {current_time.minute}')
    
    # Логируем время уведомлений каждого пользователя для отладки
    for user in all_active_users:
        logger.info(f'User {user.user.username} notification time: {user.notification_time.strftime("%H:%M")}')
    
    logger.info(f'Found {telegram_users.count()} users with notifications scheduled for {current_time}')
    
    for telegram_user in telegram_users:
        logger.info(f'Processing habits for user {telegram_user.user.username}')
        habits = Habit.objects.filter(user=telegram_user.user)
        
        for habit in habits:
            should_remind = False
            try:
                if habit.frequency == 'daily' and not habit.get_status():
                    should_remind = True
                    logger.info(f'Daily habit {habit.name} needs reminder')
                elif habit.frequency == 'weekly' and habit.logs.exists():
                    last_log = habit.logs.first()
                    if last_log and (now - last_log.completed_at).days >= 6:
                        should_remind = True
                        logger.info(f'Weekly habit {habit.name} needs reminder')
                elif habit.frequency == 'monthly' and now.day == habit.start_date.day:
                    should_remind = True
                    logger.info(f'Monthly habit {habit.name} needs reminder')
                
                if should_remind:
                    logger.info(f'Sending reminder for habit {habit.name} to user {telegram_user.user.username}')
                    send_reminder(telegram_user.user, habit)
            except Exception as e:
                logger.error(f'Error processing habit {habit.id} for user {telegram_user.user.username}: {str(e)}')