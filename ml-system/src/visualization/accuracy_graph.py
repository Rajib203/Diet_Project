import matplotlib.pyplot as plt

# ==========================
# MODEL NAMES
# ==========================

models = [
    "Logistic Regression",
    "Random Forest"
]

# ==========================
# ACCURACY VALUES
# ==========================

accuracy = [
    88,
    96
]

# ==========================
# CREATE GRAPH
# ==========================

plt.figure(figsize=(8, 5))

plt.bar(models, accuracy)

# ==========================
# TITLE
# ==========================

plt.title(
    "Model Accuracy Comparison"
)

# ==========================
# LABELS
# ==========================

plt.xlabel("Models")

plt.ylabel("Accuracy (%)")

# ==========================
# SHOW VALUES
# ==========================

for i, value in enumerate(accuracy):

    plt.text(
        i,
        value + 1,
        str(value) + "%",
        ha='center'
    )

# ==========================
# SAVE GRAPH
# ==========================

plt.savefig(
    "graphs/model_accuracy.png"
)

# ==========================
# SHOW GRAPH
# ==========================

plt.show()