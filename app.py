import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from utils.interpret import interpret_all_features, get_food_recommendations

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deteksi Risiko Penyakit Jantung",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = "model/heart_attack_model.pkl"
    if not os.path.exists(model_path):
        st.error("Model tidak ditemukan. Jalankan `train_model.py` terlebih dahulu.")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>❤️ Sistem Deteksi Risiko Penyakit Jantung</h1>
    <p>Isi data kesehatan Anda di bawah ini untuk mengetahui risiko penyakit jantung dan mendapatkan rekomendasi kesehatan yang personal.</p>
    <p class="disclaimer">⚠️ Sistem ini hanya sebagai alat bantu awal, bukan pengganti diagnosis dokter.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Form Input ────────────────────────────────────────────────────────────────
st.markdown("### 📋 Data Diri & Kesehatan Anda")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 👤 Data Pribadi")
    age = st.number_input("Usia (tahun)", min_value=1, max_value=120, value=40, step=1)
    gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
    bmi = st.number_input("BMI (Indeks Massa Tubuh)", min_value=10.0, max_value=60.0, value=24.0, step=0.1,
                          help="Berat(kg) ÷ Tinggi²(m). Contoh: 70kg / (1.70m)² = 24.2")
    waist_circumference = st.number_input("Lingkar Pinggang (cm)", min_value=40.0, max_value=200.0, value=85.0, step=0.5)
    sleep_hours = st.number_input("Jam Tidur per Hari", min_value=1.0, max_value=24.0, value=7.0, step=0.5)

with col2:
    st.markdown("#### 🩺 Data Klinis")
    blood_pressure_systolic = st.number_input("Tekanan Darah Sistolik (mmHg)", min_value=60, max_value=300, value=120, step=1,
                                               help="Angka ATAS pada hasil tensi, contoh: 120/80 → isi 120")
    blood_pressure_diastolic = st.number_input("Tekanan Darah Diastolik (mmHg)", min_value=40, max_value=200, value=80, step=1,
                                                help="Angka BAWAH pada hasil tensi, contoh: 120/80 → isi 80")
    cholesterol_level = st.number_input("Kolesterol Total (mg/dL)", min_value=50, max_value=600, value=200, step=1)
    cholesterol_ldl = st.number_input("Kolesterol LDL (mg/dL)", min_value=20, max_value=400, value=130, step=1,
                                       help="LDL = kolesterol 'jahat'")
    cholesterol_hdl = st.number_input("Kolesterol HDL (mg/dL)", min_value=10, max_value=150, value=50, step=1,
                                       help="HDL = kolesterol 'baik'")
    triglycerides = st.number_input("Trigliserida (mg/dL)", min_value=20, max_value=1000, value=150, step=1)
    fasting_blood_sugar = st.number_input("Gula Darah Puasa (mg/dL)", min_value=50, max_value=500, value=100, step=1)

with col3:
    st.markdown("#### 🏃 Gaya Hidup & Riwayat")
    smoking_status = st.selectbox("Status Merokok", ["Never", "Past", "Current"],
                                   format_func=lambda x: {"Never": "Tidak Pernah", "Past": "Mantan Perokok", "Current": "Perokok Aktif"}[x])
    physical_activity = st.selectbox("Aktivitas Fisik", ["Active", "Moderate", "Sedentary"],
                                      format_func=lambda x: {"Active": "Aktif (rutin olahraga)", "Moderate": "Sedang", "Sedentary": "Kurang aktif/duduk terus"}[x])
    diet_quality = st.selectbox("Kualitas Diet", ["Healthy", "Average", "Unhealthy"],
                                  format_func=lambda x: {"Healthy": "Sehat", "Average": "Cukup", "Unhealthy": "Tidak Sehat"}[x])
    alcohol_consumption = st.selectbox("Konsumsi Alkohol", ["None", "Low", "Moderate", "High"],
                                        format_func=lambda x: {"None": "Tidak sama sekali", "Low": "Rendah", "Moderate": "Sedang", "High": "Tinggi"}[x])
    
    st.markdown("#### 🏥 Riwayat Penyakit")
    diabetes = st.radio("Diabetes", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya", horizontal=True)
    hypertension = st.radio("Hipertensi", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya", horizontal=True)
    obesity = st.radio("Obesitas", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya", horizontal=True)
    previous_heart_disease = st.radio("Riwayat Penyakit Jantung Sebelumnya", [0, 1],
                                       format_func=lambda x: "Tidak" if x == 0 else "Ya", horizontal=True)
    family_history = st.radio("Riwayat Keluarga Penyakit Jantung", [0, 1],
                               format_func=lambda x: "Tidak" if x == 0 else "Ya", horizontal=True)

st.markdown("---")

# ── Predict Button ────────────────────────────────────────────────────────────
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    predict_clicked = st.button("🔍 Analisis Risiko Saya", use_container_width=True, type="primary")

# ── Prediction ────────────────────────────────────────────────────────────────
if predict_clicked:
    input_data = pd.DataFrame([{
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "waist_circumference": waist_circumference,
        "sleep_hours": sleep_hours,
        "blood_pressure_systolic": blood_pressure_systolic,
        "blood_pressure_diastolic": blood_pressure_diastolic,
        "cholesterol_level": cholesterol_level,
        "cholesterol_ldl": cholesterol_ldl,
        "cholesterol_hdl": cholesterol_hdl,
        "triglycerides": triglycerides,
        "fasting_blood_sugar": fasting_blood_sugar,
        "smoking_status": smoking_status,
        "physical_activity": physical_activity,
        "diet_quality": diet_quality,
        "alcohol_consumption": alcohol_consumption,
        "diabetes": diabetes,
        "hypertension": hypertension,
        "obesity": obesity,
        "previous_heart_disease": previous_heart_disease,
        "family_history": family_history,
    }])

    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]
    risk_pct = round(proba[1] * 100, 1)

    st.markdown("---")
    st.markdown("## 📊 Hasil Analisis")

    # ── Diagnosis result ──────────────────────────────────────────────────────
    if prediction == 1:
        st.markdown(f"""
        <div class="result-box danger">
            <h2>⚠️ BERISIKO TERKENA PENYAKIT JANTUNG</h2>
            <p>Berdasarkan data yang Anda masukkan, sistem mendeteksi adanya risiko penyakit jantung.</p>
            <p class="risk-score">Probabilitas Risiko: <strong>{risk_pct}%</strong></p>
            <p>Segera konsultasikan kondisi Anda ke dokter atau tenaga medis profesional.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box safe">
            <h2>✅ TIDAK TERDETEKSI RISIKO TINGGI PENYAKIT JANTUNG</h2>
            <p>Berdasarkan data yang Anda masukkan, risiko penyakit jantung Anda saat ini relatif rendah.</p>
            <p class="risk-score">Probabilitas Risiko: <strong>{risk_pct}%</strong></p>
            <p>Tetap jaga gaya hidup sehat dan rutin periksa kesehatan!</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Interpretation per variable ───────────────────────────────────────────
    st.markdown("### 🔬 Keterangan Setiap Variabel Kesehatan Anda")
    interpretations = interpret_all_features(input_data.iloc[0])
    
    cols = st.columns(2)
    for i, item in enumerate(interpretations):
        with cols[i % 2]:
            status_color = {"normal": "green", "perhatian": "orange", "bahaya": "red"}.get(item["status"], "gray")
            icon = {"normal": "✅", "perhatian": "⚠️", "bahaya": "🔴"}.get(item["status"], "ℹ️")
            st.markdown(f"""
            <div class="var-card {item['status']}">
                <div class="var-header">{icon} <strong>{item['label']}</strong></div>
                <div class="var-value">Nilai Anda: <span class="value-highlight">{item['value']}</span></div>
                <div class="var-desc">{item['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Food recommendations ───────────────────────────────────────────────────
    st.markdown("### 🥗 Rekomendasi Makanan untuk Anda")
    foods = get_food_recommendations(input_data.iloc[0], prediction)

    food_cols = st.columns(3)
    for i, category in enumerate(foods):
        with food_cols[i % 3]:
            items_html = "".join([f"<li>{item}</li>" for item in category["items"]])
            st.markdown(f"""
            <div class="food-card">
                <div class="food-icon">{category['icon']}</div>
                <h4>{category['title']}</h4>
                <ul>{items_html}</ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Disclaimer:</strong> Hasil analisis ini bersifat informatif dan tidak menggantikan diagnosis medis profesional. 
        Selalu konsultasikan kondisi kesehatan Anda dengan dokter.
    </div>
    """, unsafe_allow_html=True)
