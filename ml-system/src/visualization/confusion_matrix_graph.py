import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix

# ==========================================
# SAMPLE CONFUSION MATRIX
# ==========================================

cm = [
    [45, 2, 1],
    [3, 40, 4],
    [1, 2, 42]
]

# ==========================================
# CLASS LABELS
# ==========================================

labels = [
    "Insufficient",
    "Normal",
    "Overweight"
]

# ==========================================
# FIGURE SIZE
# ==========================================

plt.figure(figsize=(8, 6))

# ==========================================
# HEATMAP GRAPH
# ==========================================

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=labels,
    yticklabels=labels
)

# ==========================================
# TITLE
# ==========================================

plt.title(
    "Confusion Matrix Heatmap"
)

# ==========================================
# AXIS LABELS
# ==========================================

plt.xlabel(
    "Predicted Labels"
)

plt.ylabel(
    "Actual Labels"
)

# ==========================================
# SAVE GRAPH
# ==========================================

plt.savefig(
    "graphs/confusion_matrix_heatmap.png"
)

# ==========================================
# SHOW GRAPH
# ==========================================

plt.show()