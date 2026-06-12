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

encoder = LabelEncoder()

categorical_cols = df.select_dtypes(
    include=['object', 'string']
).columns

for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

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
    2: "Overweight Level I",
    3: "Overweight Level II",
    4: "Obesity Type I",
    5: "Obesity Type II",
    6: "Obesity Type III"
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
# DAILY CALORIE ESTIMATION
# ==========================================

df['Daily_Calories'] = (
    df['Weight'] * 30
)

# ==========================================
# WATER INTAKE ESTIMATION
# ==========================================

df['Water_Intake_Liters'] = (
    df['Weight'] * 0.035
).round(2)

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