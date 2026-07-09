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

    SLEEP_DURATION_CHOICES = [
        ('<5 hours', '<5 hours'),
        ('5-6 hours', '5-6 hours'),
        ('7-8 hours', '7-8 hours'),
        ('>8 hours', '>8 hours'),
    ]

    EXERCISE_FREQUENCY_CHOICES = [
        ('Never', 'Never'),
        ('1-2 times/week', '1-2 times/week'),
        ('3-4 times/week', '3-4 times/week'),
        ('5+ times/week', '5+ times/week'),
    ]

    MEDICAL_CONDITION_CHOICES = [
        ('None', 'None'),
        ('Diabetes', 'Diabetes'),
        ('Hypertension', 'Hypertension'),
        ('PCOS', 'PCOS'),
        ('Thyroid', 'Thyroid'),
    ]

    GOAL_CHOICES = [
        ('Weight Loss', 'Weight Loss'),
        ('Maintenance', 'Maintenance'),
        ('Weight Gain', 'Weight Gain'),
    ]

    FOOD_PREFERENCES_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    sleep_duration = models.CharField(max_length=20, choices=SLEEP_DURATION_CHOICES, help_text="Sleep duration in hours")
    exercise_frequency = models.CharField(max_length=20, choices=EXERCISE_FREQUENCY_CHOICES, help_text="Exercise frequency per week")
    daily_steps = models.IntegerField(help_text="Average daily steps", choices=[(i, f"{i} steps") for i in range(0, 20001, 1000)])
    medical_condition = models.CharField(max_length=20, choices=MEDICAL_CONDITION_CHOICES, default='None')
    food_allergies = models.TextField(null=True, blank=True, help_text="List any food allergies")
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    food_preferences = models.TextField(null=True, blank=True, help_text="List any food preferences or restrictions", choices=FOOD_PREFERENCES_CHOICES)
    
    # Prediction Results
    bmi = models.FloatField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    protein = models.IntegerField(null=True, blank=True)
    carbs = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    disease_risk = models.CharField(max_length=20, null=True, blank=True)
    water_intake = models.FloatField(null=True, blank=True, help_text="Water intake in liters")
    diet_recommendation = models.TextField(null=True, blank=True, help_text="Dietary recommendations based on the user's health data and goals")
    recommended_foods = models.TextField(null=True, blank=True, help_text="List of recommended foods based on the user's health data and goals")
    meal_plan = models.TextField(null=True, blank=True, help_text="Suggested meal plan based on the user's health data and goals")
    lifestyle_recommendations = models.TextField(null=True, blank=True, help_text="Lifestyle recommendations based on the user's health data and goals")
    workout_plan = models.TextField(null=True, blank=True, help_text="Suggested workout plan based on the user's health data and goals")
    created_at = models.DateTimeField(auto_now_add=True)
    prediction_confidence = models.FloatField(null=True, blank=True, help_text="Confidence level of the predictions (0 to 100)%")

    def __str__(self):
        return f"Health Data - {self.created_at.strftime('%Y-%m-%d')}"
