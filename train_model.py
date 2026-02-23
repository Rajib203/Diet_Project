# train_model_advanced.py
# ✅ Advanced Diet Prediction Training (ONLY RandomForest + LogisticRegression)
# ✅ Pipeline (OneHot + Imputer) + Safe Stratify + Safe CV (fixes rare-class error)
# ✅ Saves: model_advanced.pkl  (best pipeline + metadata)

import pandas as pd
import numpy as np
import pickle
from collections import Counter

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


# -----------------------------
# Helpers (fix rare-class issue)
# -----------------------------
def can_stratify(y, min_count=2) -> bool:
    counts = Counter(y)
    return len(counts) > 1 and min(counts.values()) >= min_count


def safe_n_splits(y, desired=5) -> int:
    counts = Counter(y)
    if not counts:
        return 0
    return min(desired, min(counts.values()))


def merge_rare_classes(y, threshold=1, other_label="Other"):
    """
    Optional: merge rare labels into 'Other'
    threshold=1 -> merge classes with count==1
    """
    counts = Counter(y)
    rare = {k for k, v in counts.items() if v <= threshold}
    if rare:
        print(f"⚠️ Merging rare classes (count <= {threshold}) into '{other_label}': {len(rare)} classes")
        y = y.apply(lambda x: other_label if x in rare else x)
    return y


# -----------------------------
# Load + Clean
# -----------------------------
def load_and_clean(path="diet_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # ✅ Fix: strip spaces from column names (Food_Type  -> Food_Type)
    df.columns = df.columns.str.strip()

    # ✅ Strip string values
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].astype(str).str.strip()

    required = ["Age", "Gender", "Height_cm", "Weight_kg", "Activity_Level", "Goal", "Region", "Food_Type"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}\nFound columns: {list(df.columns)}")

    # ✅ BMI compute/fill
    if "BMI" not in df.columns:
        df["BMI"] = df["Weight_kg"] / ((df["Height_cm"] / 100) ** 2)
    else:
        computed_bmi = df["Weight_kg"] / ((df["Height_cm"] / 100) ** 2)
        df["BMI"] = df["BMI"].where(df["BMI"].notna(), computed_bmi)

    # ✅ Coerce numeric
    for col in ["Age", "Height_cm", "Weight_kg", "BMI"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop critical NaNs
    df = df.dropna(subset=["Age", "Height_cm", "Weight_kg", "BMI", "Food_Type"]).reset_index(drop=True)

    return df


# -----------------------------
# Preprocessor
# -----------------------------
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    num_pipe = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )

    cat_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", num_pipe, num_cols),
            ("cat", cat_pipe, cat_cols),
        ],
        remainder="drop",
    )


# -----------------------------
# Train + Pick Best (RF vs LogReg)
# -----------------------------
def train_and_select_best(df: pd.DataFrame, rare_merge_threshold=0):
    feature_cols = ["Age", "Gender", "Height_cm", "Weight_kg", "BMI", "Activity_Level", "Goal", "Region"]

    X = df[feature_cols].copy()
    y = df["Food_Type"].copy()

    # Optional: merge singletons into "Other" (recommended if many 1-count classes)
    if rare_merge_threshold > 0:
        y = merge_rare_classes(y, threshold=rare_merge_threshold, other_label="Other")

    # ✅ Safe stratify
    do_stratify = can_stratify(y, min_count=2)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if do_stratify else None,
    )

    if not do_stratify:
        print("⚠️ Stratify disabled (some class has < 2 samples).")

    preprocessor = build_preprocessor(X_train)

    # ✅ Only 2 models
    models = {
        "logistic_regression": LogisticRegression(max_iter=4000),
        "random_forest": RandomForestClassifier(
            n_estimators=600,
            random_state=42,
            class_weight="balanced",
        ),
    }

    # ✅ Safe CV folds
    n_splits = safe_n_splits(y_train, desired=5)
    if n_splits < 2:
        skf = None
        print("⚠️ Cross-validation skipped (not enough samples per class). Using test accuracy fallback.")
    else:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        print(f"✅ Using StratifiedKFold with n_splits={n_splits}")

    best_name = None
    best_score = -1.0
    best_pipe = None

    print("\n=== Comparing Logistic Regression vs Random Forest ===")
    for name, model in models.items():
        pipe = Pipeline(steps=[("prep", preprocessor), ("model", model)])

        if skf is None:
            # fallback: fit and score on test
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_test)
            score = accuracy_score(y_test, preds)
            print(f"{name}: fallback test accuracy = {score:.4f}")
        else:
            cv_scores = cross_val_score(pipe, X_train, y_train, cv=skf, scoring="accuracy")
            score = float(cv_scores.mean())
            print(f"{name}: CV accuracy = {score:.4f}  (scores={np.round(cv_scores, 4)})")

        if score > best_score:
            best_score = score
            best_name = name
            best_pipe = pipe

    # Fit best on full train
    best_pipe.fit(X_train, y_train)

    # Final evaluation
    test_preds = best_pipe.predict(X_test)
    test_acc = accuracy_score(y_test, test_preds)

    print("\n=== Best Model Selected ===")
    print("Best model:", best_name)
    print("Selection score:", round(best_score, 4), "(CV mean if available, else fallback test acc)")
    print("Holdout Test Accuracy:", round(test_acc, 4))

    print("\n=== Classification Report (Test) ===")
    print(classification_report(y_test, test_preds))

    print("\n=== Confusion Matrix (Test) ===")
    print(confusion_matrix(y_test, test_preds))

    meta = {
        "best_model_name": best_name,
        "selection_score": best_score,
        "test_accuracy": test_acc,
        "features": feature_cols,
        "target": "Food_Type",
        "rare_merge_threshold": rare_merge_threshold,
        "stratify_used": do_stratify,
        "cv_n_splits_used": n_splits if skf is not None else 0,
    }

    return best_pipe, meta


# -----------------------------
# Save
# -----------------------------
def save_artifacts(pipeline, meta, out_path="model_advanced.pkl"):
    payload = {"pipeline": pipeline, "meta": meta}
    with open(out_path, "wb") as f:
        pickle.dump(payload, f)
    print(f"\n✅ Saved model to: {out_path}")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    df = load_and_clean("diet_data.csv")

    # ✅ Recommended:
    # If you have many classes with only 1 row, set this to 1 to merge singletons into "Other".
    # Keep 0 if you don't want merging (still fixes stratify crash, but dataset may remain unstable).
    rare_merge_threshold = 1

    best_pipe, meta = train_and_select_best(df, rare_merge_threshold=rare_merge_threshold)
    save_artifacts(best_pipe, meta, out_path="model_advanced.pkl")