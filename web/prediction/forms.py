from django import forms
from .models import HealthData

class PredictionForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = [
            'name', 'age', 'gender', 'height', 'weight', 
            'activity_level', 'goal', 'medical_condition'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '25'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '175'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
            'medical_condition': forms.Select(attrs={'class': 'form-select'}),
        }
