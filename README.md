# ❤️ Sistem Deteksi Risiko Penyakit Jantung

Aplikasi berbasis **Streamlit** untuk mendeteksi risiko penyakit jantung menggunakan model **Random Forest** yang dilatih pada dataset *Heart Attack Prediction in Indonesia* dari Kaggle.

## ✨ Fitur
- **Prediksi risiko** penyakit jantung (Berisiko / Tidak Berisiko) dengan probabilitas
- **Keterangan tiap variabel** yang diisi — apakah normal, perlu perhatian, atau bahaya
- **Rekomendasi makanan** yang disesuaikan dengan kondisi kesehatan pengguna

## 📦 Struktur Proyek
```
heart_attack_app/
├── app.py                  # Aplikasi Streamlit utama
├── train_model.py          # Script pelatihan model (jalankan sekali)
├── requirements.txt        # Dependensi Python
├── assets/
│   └── style.css           # Styling CSS
├── utils/
│   └── interpret.py        # Logika interpretasi variabel & rekomendasi makanan
└── model/
    └── heart_attack_model.pkl  # Model terlatih (dibuat setelah train_model.py)
```

## 🚀 Cara Menjalankan Secara Lokal

### 1. Clone repositori
```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependensi
```bash
pip install -r requirements.txt
```

### 3. Siapkan dataset
Unduh dataset dari Kaggle:  
👉 [Heart Attack Prediction in Indonesia](https://www.kaggle.com/datasets/ankushpanday2/heart-attack-prediction-in-indonesia)

Letakkan file `heart_attack_prediction_indonesia.csv` di direktori yang sama dengan `train_model.py`.

### 4. Latih model
```bash
python train_model.py
```
Script ini akan menghasilkan file `model/heart_attack_model.pkl`.

### 5. Jalankan aplikasi
```bash
streamlit run app.py
```

## ☁️ Deploy ke Streamlit Cloud

1. Push semua file ke GitHub **termasuk folder `model/`** (pastikan `heart_attack_model.pkl` ikut di-commit).
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Hubungkan ke repositori GitHub Anda
4. Set **Main file path** ke `app.py`
5. Klik **Deploy**!

> **Catatan:** File `.pkl` bisa cukup besar. Jika ukurannya > 100 MB, gunakan [Git LFS](https://git-lfs.com/) atau simpan model di cloud storage dan download saat startup.

## ⚠️ Disclaimer
Sistem ini merupakan alat bantu edukatif dan **bukan pengganti diagnosis medis profesional**. Selalu konsultasikan kondisi kesehatan Anda dengan dokter atau tenaga medis.

## 📊 Tentang Model
- **Algoritma:** Random Forest Classifier
- **Dataset:** 158.355 data pasien dari Indonesia
- **Akurasi:** ~72.6%
- **Fitur yang digunakan:** 21 variabel (usia, gender, BMI, tekanan darah, kolesterol, gula darah, gaya hidup, riwayat penyakit)
