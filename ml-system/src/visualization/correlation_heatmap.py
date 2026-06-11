import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "dataset/processed/featured_dataset.csv"
)

# ==========================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================

for col in df.select_dtypes(
    include=['object', 'string']
).columns:

    df[col] = pd.factorize(
        df[col]
    )[0]

# ==========================================
# CORRELATION MATRIX
# ==========================================

corr_matrix = df.corr()

# ==========================================
# PLOT HEATMAP
# ==========================================

plt.figure(
    figsize=(12, 8)
)

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

# ==========================================
# TITLES
# ==========================================

plt.title(
    "Correlation Heatmap"
)

plt.tight_layout()

# ==========================================
# SAVE GRAPH
# ==========================================

plt.savefig(
    "graphs/correlation_heatmap.png"
)

# ==========================================
# SHOW GRAPH
# ==========================================

plt.show()