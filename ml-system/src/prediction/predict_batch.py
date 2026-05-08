import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "saved_models/model.pkl"
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

# BMI Formula:
# BMI = Weight / Height^2

df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# ==========================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================

encoder = LabelEncoder()

categorical_cols = df.select_dtypes(
    include=['object']
).columns

for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# ==========================================
# PREDICT HEALTH CATEGORY
# ==========================================

predictions = model.predict(df)

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
# ADD PREDICTION COLUMN
# ==========================================

df['Prediction'] = decoded_predictions

# ==========================================
# DAILY CALORIE ESTIMATION
# ==========================================

df['Daily_Calories'] = df['Weight'] * 30

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

    if prediction == "Insufficient Weight":
        diet_list.append("High Protein Diet")

    elif prediction == "Normal Weight":
        diet_list.append("Balanced Diet")

    elif prediction == "Overweight Level I":
        diet_list.append("Low Carb Diet")

    elif prediction == "Overweight Level II":
        diet_list.append("Low Fat Diet")

    elif prediction == "Obesity Type I":
        diet_list.append("Strict Fat Reduction Diet")

    elif prediction == "Obesity Type II":
        diet_list.append("Medical Weight Loss Diet")

    else:
        diet_list.append("Doctor Supervised Diet")

df['Recommended_Diet'] = diet_list

# ==========================================
# WORKOUT SUGGESTION
# ==========================================

workout_list = []

for prediction in decoded_predictions:

    if prediction == "Insufficient Weight":
        workout_list.append("Strength Training")

    elif prediction == "Normal Weight":
        workout_list.append("Mixed Exercise")

    else:
        workout_list.append("Cardio + Walking")

df['Workout_Suggestion'] = workout_list

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