from django import forms
from .models import Habit, HabitLog

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Добавьте заметку (необязательно)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False