# Machine Learning System Cross-Check & Pipeline Analysis Report

This report presents a thorough cross-examination of the Machine Learning training and batch prediction pipelines (`ml-system/`) against the web application service integration (`web/prediction/ml_service.py` and `web/prediction/views.py`).

---

## 🔍 Key Findings & Architectural Discrepancies

After reviewing the codebases, we identified several major inconsistencies and bugs between the batch prediction script (`predict_batch.py`) and the Django integration (`ml_service.py`).

### 1. Swapped Class Index Mapping (CRITICAL BUG)
The target labels predicted by the Random Forest model represent classifications of obesity and weight levels. In the training script (`train_model.py`), the target column `NObeyesdad` is label-encoded using alphabetical order:
1. `Insufficient_Weight` ➔ **0**
2. `Normal_Weight` ➔ **1**
3. `Obesity_Type_I` ➔ **2**
4. `Obesity_Type_II` ➔ **3**
5. `Obesity_Type_III` ➔ **4**
6. `Overweight_Level_I` ➔ **5**
7. `Overweight_Level_II` ➔ **6**

The two prediction pipelines map these integers to human-readable strings differently:

| Class Index | actual Training Encoding | Web App Mapping (`ml_service.py`) | Batch Prediction Mapping (`predict_batch.py`) | Status |
| :---: | :---: | :---: | :---: | :---: |
| **0** | Insufficient Weight | Insufficient Weight | Insufficient Weight | ✅ Correct |
| **1** | Normal Weight | Normal Weight | Normal Weight | ✅ Correct |
| **2** | Obesity Type I | Obesity Type I | **Overweight Level I** | ❌ **Swapped Bug** |
| **3** | Obesity Type II | Obesity Type II | **Overweight Level II** | ❌ **Swapped Bug** |
| **4** | Obesity Type III | Obesity Type III | **Obesity Type I** | ❌ **Swapped Bug** |
| **5** | Overweight Level I | Overweight Level I | **Obesity Type II** | ❌ **Swapped Bug** |
| **6** | Overweight Level II | Overweight Level II | **Obesity Type III** | ❌ **Swapped Bug** |

> [!WARNING]
> **Impact:** The batch predictions saved in `dataset/output/prediction_results.csv` are labeled incorrectly. For example, a patient classified by the model as `Obesity Type I` (index 2) is output as `Overweight Level I` in the CSV, leading to incorrect calorie targets and fitness recommendation pipelines.

---

### 2. State-Dependent Categorical Encoding (CRITICAL PIPELINE DANGER)
In `predict_batch.py`, categorical features are encoded on the fly:
```python
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])
```
* **The Bug:** By fitting a new `LabelEncoder` instance directly on the batch inputs (`new.csv`), the labels are assigned numeric codes based *only* on the unique values present in the batch.
* **Example:** If `new.csv` only contains "Male" users, the encoder encodes "Male" as `0`. During model training, however, "Female" was encoded as `0` and "Male" as `1`. The model will receive `0` and classify these male users as females.
* **Resolution:** Serialized encoders (fitted standard label encoders or dict maps) must be loaded from `saved_models/` instead of calling `.fit_transform()` on new inference batches.

---

### 3. Metric Calculations & Estimations Discrepancies
There are calculation variances between the batch processing system and the web application:

* **Daily Calories Estimation:**
  * **Batch Script:** Simple baseline of `Weight * 30`.
  * **Web Application:** Leverages the scientific **Mifflin-St Jeor Equation** adjusted by activity levels (TDEE) and caloric offsets (deficit for Weight Loss, surplus for Weight Gain).
* **Water Intake (Liters):**
  * **Batch Script:** `Weight * 0.035` liters (rounded to 2 decimal places).
  * **Web Application:** `Weight * 0.033` liters (rounded to 1 decimal place).

---

## 🛠️ Actionable Recommendations

1. **Fix label map in `predict_batch.py`**:
   Align the index map to match the training sorting:
   ```python
   label_map = {
       0: "Insufficient Weight",
       1: "Normal Weight",
       2: "Obesity Type I",
       3: "Obesity Type II",
       4: "Obesity Type III",
       5: "Overweight Level I",
       6: "Overweight Level II"
   }
   ```
2. **Apply Static Encoder Maps in Batch Script**:
   Replace on-the-fly fit encoders with static dict mappings (like in the web app's `ml_service.py`) to prevent index drift.
3. **Align Caloric Formulas**:
   Integrate the Mifflin-St Jeor formula into the batch prediction script for highly accurate, scientifically backed calorie estimations.
