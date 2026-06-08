import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(
    "dataset/processed/featured_dataset.csv"
)

# ==========================
# BMI HISTOGRAM
# ==========================

plt.figure(figsize=(8, 5))

plt.hist(
    df['BMI'],
    bins=20
)

# ==========================
# TITLE
# ==========================

plt.title("BMI Distribution")

plt.xlabel("BMI")

plt.ylabel("Count")

# ==========================
# SAVE GRAPH
# ==========================

plt.savefig(
    "graphs/bmi_distribution.png"
)

# ==========================
# SHOW GRAPH
# ==========================

plt.show()