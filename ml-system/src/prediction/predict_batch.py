import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "saved_models/best_model.pkl"
)

# ==========================================
# LOAD USER INPUT CSV
# ==========================================

df = pd.read_csv(
    "dataset/raw/new.csv"
)

# ==========================================
# REMOVE TARGET COLUMN IF EXISTS
# ==========================================

if 'NObeyesdad' in df.columns:
    df = df.drop('NObeyesdad', axis=1)

# ==========================================
# CREATE BMI COLUMN
# ==========================================

df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# ==========================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================

categorical_mappings = {
    'Gender': {'Female': 0, 'Male': 1},
    'family_history_with_overweight': {'no': 0, 'yes': 1},
    'FAVC': {'no': 0, 'yes': 1},
    'CAEC': {'Always': 0, 'Frequently': 1, 'Sometimes': 2, 'no': 3},
    'SMOKE': {'no': 0, 'yes': 1},
    'SCC': {'no': 0, 'yes': 1},
    'CALC': {'Always': 0, 'Frequently': 1, 'Sometimes': 2, 'no': 3},
    'MTRANS': {'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 'Public_Transportation': 3, 'Walking': 4}
}

for col, mapping in categorical_mappings.items():
    if col in df.columns:
        df[col] = df[col].map(mapping).fillna(0).astype(int)

# ==========================================
# SCALE DATA
# ==========================================

scaler = joblib.load("saved_models/scaler.pkl")
X_scaled = scaler.transform(df)

# ==========================================
# PREDICT HEALTH CATEGORY
# ==========================================

predictions = model.predict(X_scaled)

# ==========================================
# DECODE PREDICTIONS
# ==========================================

label_map = {
    0: "Insufficient Weight",
    1: "Normal Weight",
    2: "Obesity Type I",
    3: "Obesity Type II",
    4: "Obesity Type III",
    5: "Overweight Level I",
    6: "Overweight Level II"
}

decoded_predictions = [
    label_map[p]
    for p in predictions
]

# ==========================================
# USER GOAL
# ==========================================

goal = "Weight Loss"

# Other options:
# goal = "Weight Gain"
# goal = "Maintain Weight"

# ==========================================
# ADD PREDICTION COLUMN
# ==========================================

df['Prediction'] = decoded_predictions

# ==========================================
# DAILY CALORIE ESTIMATION (Mifflin-St Jeor Equation)
# ==========================================

def get_activity_multiplier(faf):
    if faf < 0.5:
        return 1.2
    elif faf < 1.5:
        return 1.375
    elif faf < 2.5:
        return 1.55
    else:
        return 1.725

def calculate_calories(row):
    w = row['Weight']
    h = row['Height'] * 100 if row['Height'] < 3.0 else row['Height']
    age = row['Age']
    gender = row['Gender']
    faf = row['FAF']
    
    if gender == 1 or gender == 'Male':
        bmr = (10 * w) + (6.25 * h) - (5 * age) + 5
    else:
        bmr = (10 * w) + (6.25 * h) - (5 * age) - 161
        
    multiplier = get_activity_multiplier(faf)
    tdee = bmr * multiplier
    
    if goal == 'Weight Loss':
        calories = tdee - 500
    elif goal == 'Weight Gain':
        calories = tdee + 500
    else:
        calories = tdee
        
    return int(round(calories, 0))

df['Daily_Calories'] = df.apply(calculate_calories, axis=1)

# ==========================================
# WATER INTAKE ESTIMATION
# ==========================================

df['Water_Intake_Liters'] = (
    df['Weight'] * 0.033
).round(1)

# ==========================================
# DIET RECOMMENDATION
# ==========================================

diet_list = []

for prediction in decoded_predictions:

    # ======================================
    # WEIGHT LOSS
    # ======================================

    if goal == "Weight Loss":

        if prediction in [
            "Overweight Level I",
            "Overweight Level II",
            "Obesity Type I",
            "Obesity Type II",
            "Obesity Type III"
        ]:

            diet_list.append(
                "Strict Low Carb Fat Loss Diet"
            )

        elif prediction == "Normal Weight":

            diet_list.append(
                "Balanced Low Calorie Diet"
            )

        else:

            diet_list.append(
                "Healthy Weight Management Diet"
            )

    # ======================================
    # WEIGHT GAIN
    # ======================================

    elif goal == "Weight Gain":

        if prediction == "Insufficient Weight":

            diet_list.append(
                "High Protein Muscle Gain Diet"
            )

        else:

            diet_list.append(
                "Healthy High Calorie Diet"
            )

    # ======================================
    # MAINTAIN WEIGHT
    # ======================================

    else:

        diet_list.append(
            "Balanced Maintenance Diet"
        )

df['Recommended_Diet'] = diet_list

# ==========================================
# WORKOUT SUGGESTION
# ==========================================

workout_list = []

for prediction in decoded_predictions:

    # ======================================
    # WEIGHT LOSS
    # ======================================

    if goal == "Weight Loss":

        if prediction in [
            "Overweight Level I",
            "Overweight Level II",
            "Obesity Type I",
            "Obesity Type II",
            "Obesity Type III"
        ]:

            workout_list.append(
                "Cardio + HIIT + Walking"
            )

        else:

            workout_list.append(
                "Light Cardio + Yoga"
            )

    # ======================================
    # WEIGHT GAIN
    # ======================================

    elif goal == "Weight Gain":

        if prediction == "Insufficient Weight":

            workout_list.append(
                "Strength Training + Gym"
            )

        else:

            workout_list.append(
                "Muscle Building Workout"
            )

    # ======================================
    # MAINTAIN WEIGHT
    # ======================================

    else:

        workout_list.append(
            "Mixed Exercise Routine"
        )

df['Workout_Suggestion'] = workout_list

# ==========================================
# MEAL PLAN
# ==========================================

meal_plan_list = []

for prediction in decoded_predictions:

    # ======================================
    # WEIGHT LOSS
    # ======================================

    if goal == "Weight Loss":

        if prediction in [
            "Overweight Level I",
            "Overweight Level II",
            "Obesity Type I",
            "Obesity Type II",
            "Obesity Type III"
        ]:

            meal_plan_list.append(
                "Breakfast: Oats & Green Tea | "
                "Lunch: Salad & Grilled Chicken | "
                "Dinner: Soup & Vegetables"
            )

        else:

            meal_plan_list.append(
                "Breakfast: Fruits & Oats | "
                "Lunch: Rice & Dal | "
                "Dinner: Light Soup"
            )

    # ======================================
    # WEIGHT GAIN
    # ======================================

    elif goal == "Weight Gain":

        if prediction == "Insufficient Weight":

            meal_plan_list.append(
                "Breakfast: Eggs & Milk | "
                "Lunch: Rice & Chicken | "
                "Dinner: Paneer & Roti"
            )

        else:

            meal_plan_list.append(
                "Breakfast: Banana Shake | "
                "Lunch: Protein Rice Bowl | "
                "Dinner: Chicken & Vegetables"
            )

    # ======================================
    # MAINTAIN WEIGHT
    # ======================================

    else:

        meal_plan_list.append(
            "Breakfast: Fruits & Oats | "
            "Lunch: Balanced Meal | "
            "Dinner: Light Healthy Dinner"
        )

df['Meal_Plan'] = meal_plan_list

# ==========================================
# SAVE OUTPUT CSV
# ==========================================

df.to_csv(
    "dataset/output/prediction_results.csv",
    index=False
)

# ==========================================
# SUCCESS MESSAGE
# ==========================================

print("\nBatch prediction completed successfully")

print(
    "\nOutput File Saved At:\n"
    "dataset/output/prediction_results.csv"
)