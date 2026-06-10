import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ==========================================
# MODELS
# ==========================================

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "dataset/processed/featured_dataset.csv"
)

print("\nDataset Loaded Successfully")

# ==========================================
# ENCODE CATEGORICAL DATA
# ==========================================

encoder = LabelEncoder()

categorical_cols = df.select_dtypes(
    include=['object', 'string']
).columns

for col in categorical_cols:

    df[col] = encoder.fit_transform(
        df[col]
    )

print("\nCategorical Data Encoded")

# ==========================================
# FEATURES & TARGET
# ==========================================

X = df.drop(
    'NObeyesdad',
    axis=1
)

y = df['NObeyesdad']

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain Test Split Completed")

# ==========================================
# MODEL DICTIONARY
# ==========================================

models = {

    "Logistic Regression":

    LogisticRegression(
        max_iter=200,
        C=0.2,
        solver='lbfgs'
    ),

    "Random Forest":

    RandomForestClassifier(
        n_estimators=25,
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
}

# ==========================================
# TRAINING & EVALUATION
# ==========================================

best_accuracy = 0
best_model = None
best_model_name = ""

for name, model in models.items():

    print("\n============================")
    print(f"Training {name}...")
    print("============================")

    # ======================================
    # TRAIN MODEL
    # ======================================

    model.fit(
        X_train,
        y_train
    )

    # ======================================
    # PREDICT
    # ======================================

    predictions = model.predict(
        X_test
    )

    # ======================================
    # ACCURACY
    # ======================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    accuracy_percent = round(
        accuracy * 100,
        2
    )

    print(
        f"\n{name} Accuracy: "
        f"{accuracy_percent}%"
    )

    # ======================================
    # PRECISION
    # ======================================

    precision = precision_score(
        y_test,
        predictions,
        average='weighted'
    )

    print(
        f"Precision: "
        f"{round(precision, 2)}"
    )

    # ======================================
    # RECALL
    # ======================================

    recall = recall_score(
        y_test,
        predictions,
        average='weighted'
    )

    print(
        f"Recall: "
        f"{round(recall, 2)}"
    )

    # ======================================
    # F1 SCORE
    # ======================================

    f1 = f1_score(
        y_test,
        predictions,
        average='weighted'
    )

    print(
        f"F1 Score: "
        f"{round(f1, 2)}"
    )

    # ======================================
    # CONFUSION MATRIX
    # ======================================

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print("\nConfusion Matrix:\n")

    print(cm)

    # ======================================
    # CLASSIFICATION REPORT
    # ======================================

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    # ======================================
    # SAVE BEST MODEL
    # ======================================

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "saved_models/best_model.pkl"
)

# ==========================================
# FINAL RESULTS
# ==========================================

print("\n===================================")

print(
    f"Best Model: "
    f"{best_model_name}"
)

print(
    f"Best Accuracy: "
    f"{round(best_accuracy * 100, 2)}%"
)

print("\nBest model saved successfully")