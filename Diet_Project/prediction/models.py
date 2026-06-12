from django.db import models
from django.contrib.auth.models import User

class HealthData(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderate', 'Moderate'),
        ('Very Active', 'Very Active'),
        ('Extra Active', 'Extra Active'),
    ]

    GOAL_CHOICES = [
        ('Weight Loss', 'Weight Loss'),
        ('Maintenance', 'Maintenance'),
        ('Weight Gain', 'Weight Gain'),
    ]

    MEDICAL_CONDITION_CHOICES = [
        ('None', 'None'),
        ('Diabetes', 'Diabetes'),
        ('Hypertension', 'Hypertension'),
        ('PCOS', 'PCOS'),
        ('Thyroid', 'Thyroid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    medical_condition = models.CharField(max_length=20, choices=MEDICAL_CONDITION_CHOICES, default='None')
    
    # Prediction Results
    bmi = models.FloatField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    protein = models.IntegerField(null=True, blank=True)
    carbs = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    disease_risk = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s Health Data - {self.created_at.strftime('%Y-%m-%d')}"
