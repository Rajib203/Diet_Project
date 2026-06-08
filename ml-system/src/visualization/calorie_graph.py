import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(
    "dataset/output/prediction_results.csv"
)

# ==========================
# GRAPH
# ==========================

plt.figure(figsize=(8, 5))

plt.plot(
    df['Daily_Calories']
)

# ==========================
# TITLE
# ==========================

plt.title(
    "Daily Calories Analysis"
)

plt.xlabel("Users")

plt.ylabel("Calories")

# ==========================
# SAVE GRAPH
# ==========================

plt.savefig(
    "graphs/calories_chart.png"
)

# ==========================
# SHOW GRAPH
# ==========================

plt.show()