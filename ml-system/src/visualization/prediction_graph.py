import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# LOAD PREDICTION RESULTS
# ==========================

df = pd.read_csv(
    "dataset/output/prediction_results.csv"
)

# ==========================
# COUNT PREDICTIONS
# ==========================

prediction_counts = (
    df['Prediction']
    .value_counts()
)

# ==========================
# CREATE PIE CHART
# ==========================

plt.figure(figsize=(7, 7))

plt.pie(
    prediction_counts,
    labels=prediction_counts.index,
    autopct='%1.1f%%'
)

# ==========================
# TITLE
# ==========================

plt.title(
    "Prediction Category Distribution"
)

# ==========================
# SAVE GRAPH
# ==========================

plt.savefig(
    "graphs/prediction_chart.png"
)

# ==========================
# SHOW GRAPH
# ==========================

plt.show()