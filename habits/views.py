from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Habit, HabitLog
from .forms import HabitForm, HabitLogForm

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Привычка успешно создана!')
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Создать привычку'})

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Привычка успешно обновлена!')
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Редактировать привычку'})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Привычка успешно удалена!')
        return redirect('habit_list')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def habit_complete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        if habit.get_status():
            messages.warning(request, 'Привычка уже отмечена как выполненная!')
            return redirect('habit_list')
        form = HabitLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.habit = habit
            log.save()
            messages.success(request, 'Отмечено выполнение привычки!')
            return redirect('habit_list')
    return redirect('habit_list')

@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    logs = habit.logs.all()[:10]
    form = HabitLogForm()
    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'logs': logs,
        'form': form
    })