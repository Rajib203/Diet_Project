import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "dataset/processed/cleaned_dataset.csv"
)

# Create BMI feature
df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# Save dataset
df.to_csv(
    "dataset/processed/featured_dataset.csv",
    index=False
)

print("Feature engineering completed")