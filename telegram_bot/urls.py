from django.urls import path
from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('link/', views.link_telegram, name='link_telegram'),
]