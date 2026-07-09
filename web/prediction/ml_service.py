import os
import joblib
import pandas as pd

# Load ML models on startup to avoid loading on every request
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, 'ml-system', 'saved_models')

try:
    rf_model = joblib.load(os.path.join(MODELS_DIR, 'best_model.pkl'))
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    MODELS_LOADED = True
except Exception as e:
    print(f"Warning: Could not load ML models. {e}")
    MODELS_LOADED = False

def predict_health_metrics(data):
    """
    Uses the trained Random Forest model from ml-system to predict health metrics.
    """
    weight = data.weight
    height_m = data.height / 100 if data.height > 3 else data.height
    age = data.age
    gender = data.gender
    activity_level = data.activity_level
    goal = data.goal

    # 1. Calculate BMI
    bmi = round(weight / (height_m ** 2), 1)

    # 2. Base calculations for calories and macros
    if gender == 'Male':
        bmr = (10 * weight) + (6.25 * data.height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * data.height) - (5 * age) - 161

    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderate': 1.55,
        'Very Active': 1.725,
        'Extra Active': 1.9,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    if goal == 'Weight Loss':
        calories = tdee - 500
    elif goal == 'Weight Gain':
        calories = tdee + 500
    else:
        calories = tdee

    calories = int(round(calories, 0))
    protein_cals = calories * 0.30
    protein = int(round(protein_cals / 4, 0))
    fat_cals = calories * 0.25
    fat = int(round(fat_cals / 9, 0))
    carb_cals = calories - (protein_cals + fat_cals)
    carbs = int(round(carb_cals / 4, 0))

    # 3. Predict Disease Risk (Obesity Level) using ML Model
    risk = "Unknown"
    if MODELS_LOADED:
        # Map categorical variables based on alphabetical LabelEncoding from training
        gender_map = {'Female': 0, 'Male': 1, 'Other': 1} # Default Other to Male
        
        faf_map = {
            'Sedentary': 0,
            'Lightly Active': 1,
            'Moderate': 2,
            'Very Active': 3,
            'Extra Active': 3
        }

        # Build feature array in the exact order expected by the model
        features = [{
            'Gender': gender_map.get(gender, 1),
            'Age': age,
            'Height': height_m,
            'Weight': weight,
            'family_history_with_overweight': 0, # 'no'
            'FAVC': 0, # 'no'
            'FCVC': 2,
            'NCP': 3,
            'CAEC': 2, # 'Sometimes'
            'SMOKE': 0, # 'no'
            'CH2O': 2,
            'SCC': 0, # 'no'
            'FAF': faf_map.get(activity_level, 0),
            'TUE': 1,
            'CALC': 2, # 'Sometimes'
            'MTRANS': 3, # 'Public_Transportation'
            'BMI': bmi
        }]
        
        df = pd.DataFrame(features)
        
        # Scale and Predict
        X_scaled = scaler.transform(df)
        pred_idx = rf_model.predict(X_scaled)[0]

        probabilities = rf_model.predict_proba(X_scaled)[0]
        confidence = round(max(probabilities) * 100, 2)
        
        label_map = {
            0: "Insufficient Weight",
            1: "Normal Weight",
            2: "Obesity Type I",
            3: "Obesity Type II",
            4: "Obesity Type III",
            5: "Overweight Level I",
            6: "Overweight Level II"
        }
        
        risk = label_map.get(pred_idx, "Unknown")
    else:
        # Fallback if model fails to load
        if bmi > 30:
            risk = "Obesity"
        elif bmi > 25:
            risk = "Overweight"
        elif bmi < 18.5:
            risk = "Insufficient Weight"
        else:
            risk = "Normal Weight"

    return {
        'bmi': bmi,
        'calories': calories,
        'protein': protein,
        'carbs': carbs,
        'fat': fat,
        'disease_risk': risk,
        'prediction_confidence': confidence
    }
