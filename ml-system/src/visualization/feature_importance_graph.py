import joblib
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    "saved_models/best_model.pkl"
)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "dataset/processed/featured_dataset.csv"
)

# ==========================================
# FEATURE NAMES
# ==========================================

X = df.drop(
    "NObeyesdad",
    axis=1
)

feature_names = X.columns

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

# ==========================================
# PLOT GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.title(
    "Feature Importance - Random Forest"
)

plt.xlabel(
    "Importance Score"
)

plt.ylabel(
    "Features"
)

plt.tight_layout()

# ==========================================
# SAVE GRAPH
# ==========================================

plt.savefig(
    "graphs/feature_importance.png"
)

plt.show()