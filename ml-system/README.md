# ML System

This is the machine learning module for the Diet Project.

## Structure
- `config/`: Configuration files (e.g., hyperparameter tuning parameters)
- `dataset/`: Raw and processed datasets
- `graphs/`: Generated visualization graphs
- `notebooks/`: Jupyter notebooks for exploratory data analysis (EDA)
- `saved_models/`: Serialized models (e.g., `.pkl` files)
- `src/`: The core ML package (features, preprocessing, prediction, training, visualization)
- `tests/`: Unit tests for the modules

## Installation
Ensure you activate your virtual environment, then run:
```bash
pip install -r requirements.txt
```

## Step-by-Step Running Process

To run the full machine learning pipeline from scratch, open your terminal (ensure you are in the `ml-system` directory) and run the scripts in the following order:

### 1. Data Preprocessing
Cleans the raw dataset and prepares it for feature extraction.
```bash
python src/preprocessing/clean_data.py
```

### 2. Feature Engineering
Builds the required features from the cleaned dataset.
```bash
python src/features/build_features.py
```

### 3. Model Training
Trains the ML models (Logistic Regression & Random Forest), scales the data, and saves the best model and scaler to the `saved_models/` folder.
```bash
python src/training/train_model.py
```

### 4. Batch Prediction
Loads the saved model and scaler, processes new user data from `dataset/raw/new.csv`, and generates diet/workout plans.
```bash
python src/prediction/predict_batch.py
```
*Note: The final results will be saved to `dataset/output/prediction_results.csv`.*

### 5. Visualization (Optional)
Generates and displays accuracy graphs and correlation charts.
```bash
python src/visualization/accuracy_graph.py
python src/visualization/prediction_graph.py
```
