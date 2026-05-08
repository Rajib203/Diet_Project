import pandas as pd

# Load dataset
df = pd.read_csv("dataset/raw/new.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv(
    "dataset/processed/cleaned_dataset.csv",
    index=False
)

print("Data cleaned successfully")