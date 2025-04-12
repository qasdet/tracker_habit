from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TelegramUser

@login_required
def link_telegram(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        notification_time = request.POST.get('notification_time', '09:00')
        if telegram_id:
            # Проверяем, не привязан ли уже этот Telegram ID к другому пользователю
            if TelegramUser.objects.filter(telegram_id=telegram_id).exists():
                messages.error(request, 'Этот Telegram ID уже привязан к другому аккаунту.')
                return redirect('telegram_bot:link_telegram')
            
            # Создаем или обновляем привязку Telegram
            telegram_user, created = TelegramUser.objects.get_or_create(
                user=request.user,
                defaults={
                    'telegram_id': telegram_id,
                    'notification_time': notification_time
                }
            )
            if not created:
                telegram_user.telegram_id = telegram_id
                telegram_user.notification_time = notification_time
                telegram_user.save()
            
            messages.success(request, 'Telegram успешно привязан к вашему аккаунту!')
            return redirect('/')
    
    # Проверяем, есть ли уже привязанный Telegram
    try:
        telegram_user = request.user.telegram_user
        telegram_id = telegram_user.telegram_id
    except TelegramUser.DoesNotExist:
        telegram_id = None
    
    return render(request, 'telegram_bot/link_telegram.html', {
        'telegram_id': telegram_id,
        'notification_time': getattr(telegram_user, 'notification_time', '09:00') if telegram_id else '09:00'
    })