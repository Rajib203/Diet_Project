def predict_health_metrics(data):
    """
    Placeholder for ML service. Calculates basic health metrics heuristically.
    """
    weight = data.weight
    height = data.height
    age = data.age
    gender = data.gender
    activity_level = data.activity_level
    goal = data.goal

    # 1. Calculate BMI
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    # 2. Calculate BMR (Mifflin-St Jeor)
    if gender == 'Male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # 3. Calculate TDEE (Total Daily Energy Expenditure)
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderate': 1.55,
        'Very Active': 1.725,
        'Extra Active': 1.9,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    # 4. Adjust for Goal
    if goal == 'Weight Loss':
        calories = tdee - 500
    elif goal == 'Weight Gain':
        calories = tdee + 500
    else:
        calories = tdee

    calories = int(round(calories, 0))

    # 5. Calculate Macros
    # Protein: ~2.2g per kg or ~30%
    protein_cals = calories * 0.30
    protein = int(round(protein_cals / 4, 0))

    # Fat: ~25%
    fat_cals = calories * 0.25
    fat = int(round(fat_cals / 9, 0))

    # Carbs: Remaining
    carb_cals = calories - (protein_cals + fat_cals)
    carbs = int(round(carb_cals / 4, 0))

    # 6. Disease Risk (Simple heuristic)
    risk = "Low"
    if bmi > 30 or data.medical_condition != 'None':
        risk = "High"
    elif bmi > 25:
        risk = "Moderate"

    return {
        'bmi': bmi,
        'calories': calories,
        'protein': protein,
        'carbs': carbs,
        'fat': fat,
        'disease_risk': risk
    }
