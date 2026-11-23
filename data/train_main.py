from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)


# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "diabetes_health_indicators.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "diabetes_model.joblib"
FEATURE_FILE = MODEL_DIR / "feature_names.joblib"
METRICS_FILE = MODEL_DIR / "model_comparison.csv"


# =========================================================
# 2. LOAD DATASET
# =========================================================

print("=" * 60)
print("DIABETES AWARENESS - MODEL TRAINING")
print("=" * 60)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Check that diabetes_health_indicators.csv is inside data/."
    )

df = pd.read_csv(DATA_FILE)

TARGET = "Diabetes_binary"

FEATURES = [
    "HighBP",
    "HighChol",
    "BMI",
    "Smoker",
    "Stroke",
    "HeartDiseaseorAttack",
    "PhysActivity",
    "Fruits",
    "Veggies",
    "HvyAlcoholConsump",
    "GenHlth",
    "PhysHlth",
    "Age",
]

required_columns = FEATURES + [TARGET]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing dataset columns: {missing_columns}"
    )

df = df[required_columns].copy()

# Convert invalid values to missing values.
for column in required_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )

# The target must be known for training.
df = df.dropna(subset=[TARGET])

# The target must contain only binary classes.
df = df[df[TARGET].isin([0, 1])]

df[TARGET] = df[TARGET].astype(int)

if df[TARGET].nunique() != 2:
    raise ValueError(
        "The target column must contain both classes 0 and 1."
    )

X = df[FEATURES]
y = df[TARGET]

print(f"\nTotal records: {len(df):,}")
print(f"Number of features: {len(FEATURES)}")

print("\nClass distribution:")
print(
    y.value_counts()
    .sort_index()
    .rename(index={
        0: "Class 0",
        1: "Class 1",
    })
)

print("\nClass percentages:")
print(
    (y.value_counts(normalize=True) * 100)
    .sort_index()
    .round(2)
)


# =========================================================
# 3. SPLIT INTO TRAINING AND TESTING DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

training_percentage = (
    len(X_train) / len(df)
) * 100

testing_percentage = (
    len(X_test) / len(df)
) * 100

print("\n" + "=" * 60)
print("TRAINING AND TESTING SPLIT")
print("=" * 60)

print(f"Training records: {len(X_train):,}")
print(f"Testing records:  {len(X_test):,}")

print(f"Training percentage: {training_percentage:.1f}%")
print(f"Testing percentage:  {testing_percentage:.1f}%")


# =========================================================
# 4. CREATE HISTGRADIENTBOOSTING MODEL
# =========================================================

model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median"),
    ),
    (
        "classifier",
        HistGradientBoostingClassifier(
            learning_rate=0.08,
            max_iter=250,
            max_leaf_nodes=20,
            min_samples_leaf=40,
            l2_regularization=2.0,
            random_state=42,
        ),
    ),
])


# =========================================================
# 5. TRAIN MODEL
# =========================================================

print("\n" + "=" * 60)
print("TRAINING HISTGRADIENTBOOSTING")
print("=" * 60)

model.fit(X_train, y_train)

print("Training completed successfully.")


# =========================================================
# 6. EVALUATE MODEL ON UNSEEN TEST DATA
# =========================================================

print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(
    y_test,
    y_pred,
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0,
)

roc_auc = roc_auc_score(
    y_test,
    y_prob,
)


# =========================================================
# 7. DISPLAY PERFORMANCE METRICS
# =========================================================

print("\nFINAL TEST RESULTS")
print("-" * 40)

print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1-score : {f1 * 100:.2f}%")
print(f"ROC-AUC  : {roc_auc * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Class 0",
            "Class 1",
        ],
        zero_division=0,
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
    )
)


# =========================================================
# 8. SAVE TRAINED MODEL
# =========================================================

joblib.dump(
    model,
    MODEL_FILE,
)

joblib.dump(
    FEATURES,
    FEATURE_FILE,
)

print("\nSaved trained model:")
print(MODEL_FILE)

print("\nSaved feature names:")
print(FEATURE_FILE)


# =========================================================
# 9. SAVE PERFORMANCE METRICS
# =========================================================

results = pd.DataFrame([
    {
        "Model": "HistGradientBoosting",
        "Total_Records": len(df),
        "Training_Records": len(X_train),
        "Testing_Records": len(X_test),
        "Training_Percentage": round(
            training_percentage,
            2,
        ),
        "Testing_Percentage": round(
            testing_percentage,
            2,
        ),
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1,
        "ROC_AUC": roc_auc,
    }
])

# Write the file directly. Close it in Excel first if it is open.
results.to_csv(
    METRICS_FILE,
    index=False,
)

print("\nSaved evaluation results:")
print(METRICS_FILE)


# =========================================================
# 10. FINAL SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("TRAINING SUMMARY")
print("=" * 60)

print(f"Training split: {training_percentage:.1f}%")
print(f"Testing split:  {testing_percentage:.1f}%")
print(f"Accuracy:       {accuracy * 100:.2f}%")
print(f"Precision:      {precision * 100:.2f}%")
print(f"Recall:         {recall * 100:.2f}%")
print(f"F1-score:       {f1 * 100:.2f}%")
print(f"ROC-AUC:        {roc_auc * 100:.2f}%")

if accuracy >= 0.80:
    print("\nAccuracy is at least 80% on this test split.")
else:
    print(
        "\nAccuracy is below 80%. Further evaluation and "
        "careful tuning may be needed."
    )

if recall < 0.50:
    print(
        "WARNING: Recall is below 50%. The model misses "
        "many positive cases in this test dataset."
    )

print(
    "\nScientific limitation: this dataset classifies existing "
    "diabetes-related status. It does not validate future diabetes "
    "onset prediction."
)

print("\nAll done!")