import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
import django
django.setup()

from telegram.ext import Updater, CommandHandler
from django.conf import settings
from telegram_bot.models import TelegramUser

def start(update, context):
    telegram_id = str(update.effective_user.id)
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        update.message.reply_text(f'С возвращением, {telegram_user.user.username}! Вы будете получать уведомления о ваших привычках.')
    except TelegramUser.DoesNotExist:
        update.message.reply_text('Пожалуйста, свяжите свой аккаунт через веб-интерфейс.')

def send_reminder(user, habit):
    try:
        telegram_user = user.telegram_user
        if not telegram_user:
            print(f'Telegram user not found for user {user.username}')
            return
        if not telegram_user.is_active:
            print(f'Telegram user {telegram_user.telegram_id} is not active')
            return
        if not settings.TELEGRAM_BOT_TOKEN:
            print('Telegram bot token is not configured')
            return
            
        try:
            bot = Updater(settings.TELEGRAM_BOT_TOKEN).bot
            message = f'Напоминание о привычке "{habit.name}"\nОписание: {habit.description}'
            bot.send_message(chat_id=telegram_user.telegram_id, text=message)
            print(f'Successfully sent reminder to user {user.username} for habit {habit.name}')
        except Exception as e:
            print(f'Error sending message to Telegram: {str(e)}\nUser: {user.username}\nTelegram ID: {telegram_user.telegram_id}')
    except TelegramUser.DoesNotExist:
        print(f'TelegramUser does not exist for user {user.username}')
    except Exception as e:
        print(f'Unexpected error in send_reminder: {str(e)}\nUser: {user.username}')

def setup_bot():
    updater = Updater(settings.TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    return updater


def main():
    try:
        updater = setup_bot()
        print('Telegram бот запущен. Нажмите Ctrl+C для остановки.')
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(f'Ошибка при запуске бота: {str(e)}')

if __name__ == '__main__':
    main()
