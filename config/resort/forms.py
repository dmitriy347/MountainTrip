from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    """Форма для создания и редактирования поездок"""
    class Meta:
        model = Trip
        fields = ['resort', 'start_date', 'end_date', 'comment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }