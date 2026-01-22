from django import forms
from .models import Trip, TripMedia


class TripForm(forms.ModelForm):
    """Форма для создания и редактирования поездок"""

    class Meta:
        model = Trip
        fields = ["resort", "start_date", "end_date", "comment", "is_public"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "is_public": "Показать всем пользователям",
        }


class TripMediaForm(forms.ModelForm):
    """Форма для загрузки медиафайлов поездки"""

    class Meta:
        model = TripMedia
        fields = ["image"]
