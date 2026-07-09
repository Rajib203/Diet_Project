from django import forms
from .models import HealthData


class PredictionForm(forms.ModelForm):
    class Meta:
        model = HealthData

        fields = [
            "age",
            "gender",
            "height",
            "weight",
            "activity_level",
            "sleep_duration",
            "exercise_frequency",
            "daily_steps",
            "medical_condition",
            "food_allergies",
            "goal",
            "food_preferences",
        ]

        widgets = {
            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Age",
                "min": 1,
                "max": 100
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "height": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Height (cm)",
                "step": "0.1"
            }),

            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Weight (kg)",
                "step": "0.1"
            }),

            "activity_level": forms.Select(attrs={
                "class": "form-select"
            }),

            "sleep_duration": forms.Select(attrs={
                "class": "form-select"
            }),

            "exercise_frequency": forms.Select(attrs={
                "class": "form-select"
            }),

            "daily_steps": forms.Select(attrs={
                "class": "form-select"
            }),

            "medical_condition": forms.Select(attrs={
                "class": "form-select"
            }),

            "food_allergies": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Example: Peanut, Milk"
            }),

            "goal": forms.Select(attrs={
                "class": "form-select"
            }),

            "food_preferences": forms.Select(attrs={
                "class": "form-select"
            }),
        }

        labels = {
            "age": "Age",
            "gender": "Gender",
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "activity_level": "Activity Level",
            "sleep_duration": "Sleep Duration",
            "exercise_frequency": "Exercise Frequency",
            "daily_steps": "Daily Steps",
            "medical_condition": "Medical Condition",
            "food_allergies": "Food Allergies",
            "goal": "Fitness Goal",
            "food_preferences": "Food Preference",
        }

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 1 or age > 100:
            raise forms.ValidationError(
                "Age must be between 1 and 100."
            )
        return age

    def clean_height(self):
        height = self.cleaned_data["height"]
        if height < 50 or height > 250:
            raise forms.ValidationError(
                "Height must be between 50 and 250 cm."
            )
        return height

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if weight < 20 or weight > 300:
            raise forms.ValidationError(
                "Weight must be between 20 and 300 kg."
            )
        return weight