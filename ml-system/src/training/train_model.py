import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv(
    "dataset/processed/featured_dataset.csv"
)

# Encode categorical columns
encoder = LabelEncoder()

categorical_cols = df.select_dtypes(
    include='object'
).columns

for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# Features and target
X = df.drop('NObeyesdad', axis=1)

y = df['NObeyesdad']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Save model
joblib.dump(
    model,
    "saved_models/model.pkl"
)

print("Model trained successfully")