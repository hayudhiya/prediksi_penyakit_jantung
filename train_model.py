"""
train_model.py
Jalankan script ini SEKALI untuk melatih model dan menyimpannya ke model/heart_attack_model.pkl
Cara pakai:
    pip install -r requirements.txt
    python train_model.py
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings

warnings.filterwarnings("ignore")

# ── Cari dataset ──────────────────────────────────────────────────────────────
DATASET_NAMES = [
    "heart_attack_prediction_indonesia.csv",
    "data/heart_attack_prediction_indonesia.csv",
]

dataset_path = None
for name in DATASET_NAMES:
    if os.path.exists(name):
        dataset_path = name
        break

if dataset_path is None:
    print("=" * 60)
    print("ERROR: Dataset tidak ditemukan!")
    print("Letakkan file CSV dataset ke direktori yang sama dengan")
    print("train_model.py, dengan nama:")
    print("  heart_attack_prediction_indonesia.csv")
    print()
    print("Download dari: https://www.kaggle.com/datasets/ankushpanday2/heart-attack-prediction-in-indonesia")
    print("=" * 60)
    sys.exit(1)

print(f"Memuat dataset dari: {dataset_path}")
df = pd.read_csv(dataset_path)
print(f"Dataset dimuat: {df.shape[0]:,} baris, {df.shape[1]} kolom")

# ── Validasi kolom ────────────────────────────────────────────────────────────
required_cols = [
    "age", "gender", "bmi", "waist_circumference", "sleep_hours",
    "blood_pressure_systolic", "blood_pressure_diastolic",
    "cholesterol_level", "cholesterol_ldl", "cholesterol_hdl",
    "triglycerides", "fasting_blood_sugar",
    "smoking_status", "physical_activity", "diet_quality", "alcohol_consumption",
    "diabetes", "hypertension", "obesity", "previous_heart_disease",
    "family_history", "heart_attack"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    print(f"PERINGATAN: Kolom berikut tidak ditemukan di dataset: {missing}")
    print("Kolom yang tersedia:", df.columns.tolist())
    # Coba lanjutkan dengan kolom yang ada
    required_cols = [c for c in required_cols if c in df.columns]

# ── Persiapan data ────────────────────────────────────────────────────────────
feature_cols = [c for c in required_cols if c != "heart_attack"]
X = df[feature_cols]
y = df["heart_attack"]

print(f"\nDistribusi target:")
print(y.value_counts().to_string())

# ── Identifikasi tipe kolom ───────────────────────────────────────────────────
numerical_features = X.select_dtypes(include=np.number).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
print(f"\nFitur numerik ({len(numerical_features)}): {numerical_features}")
print(f"Fitur kategorikal ({len(categorical_features)}): {categorical_features}")

# ── Preprocessing + Model Pipeline ───────────────────────────────────────────
preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numerical_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        n_jobs=-1,
        class_weight="balanced"
    ))
])

# ── Split dan Training ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nData latih: {X_train.shape[0]:,} | Data uji: {X_test.shape[0]:,}")

print("\nMemulai pelatihan model Random Forest...")
model_pipeline.fit(X_train, y_train)
print("Pelatihan selesai!")

# ── Evaluasi ──────────────────────────────────────────────────────────────────
y_pred = model_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAkurasi: {acc * 100:.2f}%")
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred, target_names=["Tidak Berisiko", "Berisiko"]))

# ── Simpan model ──────────────────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
model_path = "model/heart_attack_model.pkl"
joblib.dump(model_pipeline, model_path)
print(f"\n✅ Model berhasil disimpan ke: {model_path}")
print("Sekarang Anda bisa menjalankan: streamlit run app.py")
