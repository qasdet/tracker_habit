from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('<int:pk>/complete/', views.habit_complete, name='habit_complete'),
    path('<int:pk>/', views.habit_detail, name='habit_detail'),
]