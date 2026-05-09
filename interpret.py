"""
interpret.py
Interpretasi setiap variabel kesehatan dan rekomendasi makanan.
"""


def interpret_all_features(row) -> list:
    results = []

    # ── Usia ──────────────────────────────────────────────────────────────────
    age = int(row["age"])
    if age < 40:
        results.append({"label": "Usia", "value": f"{age} tahun", "status": "normal",
                         "description": "Usia Anda masih tergolong muda. Risiko penyakit jantung umumnya meningkat setelah usia 40 tahun."})
    elif age < 60:
        results.append({"label": "Usia", "value": f"{age} tahun", "status": "perhatian",
                         "description": "Usia 40–59 tahun adalah periode di mana risiko penyakit jantung mulai meningkat. Penting untuk rutin memeriksakan kesehatan."})
    else:
        results.append({"label": "Usia", "value": f"{age} tahun", "status": "bahaya",
                         "description": "Usia ≥60 tahun merupakan faktor risiko signifikan untuk penyakit jantung. Sangat disarankan pemeriksaan rutin dengan dokter."})

    # ── Jenis Kelamin ─────────────────────────────────────────────────────────
    gender_label = "Laki-laki" if row["gender"] == "Male" else "Perempuan"
    if row["gender"] == "Male":
        results.append({"label": "Jenis Kelamin", "value": gender_label, "status": "perhatian",
                         "description": "Laki-laki memiliki risiko penyakit jantung lebih tinggi, terutama sebelum usia 55 tahun."})
    else:
        results.append({"label": "Jenis Kelamin", "value": gender_label, "status": "normal",
                         "description": "Perempuan umumnya terlindungi oleh hormon estrogen sebelum menopause. Setelah menopause, risiko meningkat."})

    # ── BMI ───────────────────────────────────────────────────────────────────
    bmi = float(row["bmi"])
    if bmi < 18.5:
        results.append({"label": "BMI (Indeks Massa Tubuh)", "value": f"{bmi:.1f}", "status": "perhatian",
                         "description": "Underweight (BMI < 18.5). Berat badan kurang dapat melemahkan sistem imun dan jantung. Ideal: 18.5–24.9."})
    elif bmi <= 24.9:
        results.append({"label": "BMI (Indeks Massa Tubuh)", "value": f"{bmi:.1f}", "status": "normal",
                         "description": "BMI normal (18.5–24.9). Berat badan Anda ideal dan sehat untuk jantung. Pertahankan!"})
    elif bmi <= 29.9:
        results.append({"label": "BMI (Indeks Massa Tubuh)", "value": f"{bmi:.1f}", "status": "perhatian",
                         "description": "Overweight (BMI 25–29.9). Berat badan berlebih meningkatkan risiko hipertensi dan diabetes. Disarankan menurunkan berat badan."})
    else:
        results.append({"label": "BMI (Indeks Massa Tubuh)", "value": f"{bmi:.1f}", "status": "bahaya",
                         "description": "Obesitas (BMI ≥ 30). Risiko penyakit jantung meningkat signifikan. Konsultasikan program penurunan berat badan dengan dokter."})

    # ── Lingkar Pinggang ──────────────────────────────────────────────────────
    wc = float(row["waist_circumference"])
    gender = row["gender"]
    wc_limit_danger = 102 if gender == "Male" else 88
    wc_limit_warn = 94 if gender == "Male" else 80
    if wc < wc_limit_warn:
        results.append({"label": "Lingkar Pinggang", "value": f"{wc:.1f} cm", "status": "normal",
                         "description": f"Lingkar pinggang Anda ideal (< {wc_limit_warn} cm untuk {('pria' if gender=='Male' else 'wanita')}). Lemak perut tidak berlebihan."})
    elif wc < wc_limit_danger:
        results.append({"label": "Lingkar Pinggang", "value": f"{wc:.1f} cm", "status": "perhatian",
                         "description": f"Lingkar pinggang sedikit berlebih ({wc_limit_warn}–{wc_limit_danger} cm). Lemak perut mulai berisiko untuk jantung."})
    else:
        results.append({"label": "Lingkar Pinggang", "value": f"{wc:.1f} cm", "status": "bahaya",
                         "description": f"Lingkar pinggang terlalu besar (≥ {wc_limit_danger} cm). Risiko penyakit jantung dan metabolik meningkat secara signifikan."})

    # ── Tekanan Darah Sistolik ────────────────────────────────────────────────
    sys_bp = int(row["blood_pressure_systolic"])
    dia_bp = int(row["blood_pressure_diastolic"])
    bp_str = f"{sys_bp}/{dia_bp} mmHg"
    if sys_bp < 120 and dia_bp < 80:
        results.append({"label": "Tekanan Darah", "value": bp_str, "status": "normal",
                         "description": "Tekanan darah normal (< 120/80 mmHg). Kondisi yang ideal untuk kesehatan jantung dan pembuluh darah."})
    elif sys_bp <= 129 and dia_bp < 80:
        results.append({"label": "Tekanan Darah", "value": bp_str, "status": "perhatian",
                         "description": "Tekanan darah 'Elevated' (120–129/< 80). Belum hipertensi, tapi perlu diperhatikan. Kurangi garam dan stres."})
    elif sys_bp <= 139 or (80 <= dia_bp <= 89):
        results.append({"label": "Tekanan Darah", "value": bp_str, "status": "perhatian",
                         "description": "Hipertensi Stadium 1 (130–139/80–89 mmHg). Tekanan darah tinggi. Konsultasikan dengan dokter dan ubah gaya hidup."})
    elif sys_bp <= 180 or (90 <= dia_bp <= 120):
        results.append({"label": "Tekanan Darah", "value": bp_str, "status": "bahaya",
                         "description": "Hipertensi Stadium 2 (≥ 140/≥ 90 mmHg). Tekanan darah sangat tinggi. Segera konsultasi dengan dokter untuk penanganan."})
    else:
        results.append({"label": "Tekanan Darah", "value": bp_str, "status": "bahaya",
                         "description": "Krisis Hipertensi (> 180/> 120 mmHg). BERBAHAYA! Segera cari pertolongan medis."})

    # ── Kolesterol Total ──────────────────────────────────────────────────────
    chol = int(row["cholesterol_level"])
    if chol < 200:
        results.append({"label": "Kolesterol Total", "value": f"{chol} mg/dL", "status": "normal",
                         "description": "Kolesterol total normal (< 200 mg/dL). Risiko penyakit jantung akibat kolesterol rendah."})
    elif chol <= 239:
        results.append({"label": "Kolesterol Total", "value": f"{chol} mg/dL", "status": "perhatian",
                         "description": "Kolesterol total perbatasan tinggi (200–239 mg/dL). Disarankan perubahan pola makan dan olahraga rutin."})
    else:
        results.append({"label": "Kolesterol Total", "value": f"{chol} mg/dL", "status": "bahaya",
                         "description": "Kolesterol total tinggi (≥ 240 mg/dL). Risiko penyakit jantung meningkat. Segera konsultasi dengan dokter."})

    # ── LDL ───────────────────────────────────────────────────────────────────
    ldl = int(row["cholesterol_ldl"])
    if ldl < 100:
        results.append({"label": "Kolesterol LDL (Jahat)", "value": f"{ldl} mg/dL", "status": "normal",
                         "description": "LDL optimal (< 100 mg/dL). Kadar kolesterol jahat Anda berada di level terbaik."})
    elif ldl <= 129:
        results.append({"label": "Kolesterol LDL (Jahat)", "value": f"{ldl} mg/dL", "status": "normal",
                         "description": "LDL hampir optimal (100–129 mg/dL). Masih dalam batas aman, pertahankan pola makan sehat."})
    elif ldl <= 159:
        results.append({"label": "Kolesterol LDL (Jahat)", "value": f"{ldl} mg/dL", "status": "perhatian",
                         "description": "LDL perbatasan tinggi (130–159 mg/dL). Kurangi lemak jenuh dan makanan olahan."})
    elif ldl <= 189:
        results.append({"label": "Kolesterol LDL (Jahat)", "value": f"{ldl} mg/dL", "status": "bahaya",
                         "description": "LDL tinggi (160–189 mg/dL). Risiko penyakit jantung meningkat. Perlu perubahan diet serius."})
    else:
        results.append({"label": "Kolesterol LDL (Jahat)", "value": f"{ldl} mg/dL", "status": "bahaya",
                         "description": "LDL sangat tinggi (≥ 190 mg/dL). Sangat berisiko untuk jantung. Segera konsultasi dokter untuk kemungkinan pengobatan."})

    # ── HDL ───────────────────────────────────────────────────────────────────
    hdl = int(row["cholesterol_hdl"])
    if hdl < 40:
        results.append({"label": "Kolesterol HDL (Baik)", "value": f"{hdl} mg/dL", "status": "bahaya",
                         "description": "HDL rendah (< 40 mg/dL). Kadar kolesterol baik terlalu rendah, meningkatkan risiko penyakit jantung."})
    elif hdl <= 59:
        results.append({"label": "Kolesterol HDL (Baik)", "value": f"{hdl} mg/dL", "status": "perhatian",
                         "description": "HDL sedang (40–59 mg/dL). Usahakan untuk meningkatkan HDL dengan olahraga rutin dan konsumsi lemak sehat."})
    else:
        results.append({"label": "Kolesterol HDL (Baik)", "value": f"{hdl} mg/dL", "status": "normal",
                         "description": "HDL tinggi (≥ 60 mg/dL). Kadar kolesterol baik Anda sangat bagus! Ini justru melindungi jantung."})

    # ── Trigliserida ──────────────────────────────────────────────────────────
    trig = int(row["triglycerides"])
    if trig < 150:
        results.append({"label": "Trigliserida", "value": f"{trig} mg/dL", "status": "normal",
                         "description": "Trigliserida normal (< 150 mg/dL). Kadar lemak darah dalam batas ideal."})
    elif trig <= 199:
        results.append({"label": "Trigliserida", "value": f"{trig} mg/dL", "status": "perhatian",
                         "description": "Trigliserida perbatasan tinggi (150–199 mg/dL). Kurangi gula, alkohol, dan makanan berlemak."})
    elif trig <= 499:
        results.append({"label": "Trigliserida", "value": f"{trig} mg/dL", "status": "bahaya",
                         "description": "Trigliserida tinggi (200–499 mg/dL). Meningkatkan risiko penyakit jantung. Perubahan pola makan diperlukan."})
    else:
        results.append({"label": "Trigliserida", "value": f"{trig} mg/dL", "status": "bahaya",
                         "description": "Trigliserida sangat tinggi (≥ 500 mg/dL). Risiko pankreatitis dan penyakit jantung sangat tinggi. Segera ke dokter."})

    # ── Gula Darah Puasa ──────────────────────────────────────────────────────
    fbs = int(row["fasting_blood_sugar"])
    if fbs < 100:
        results.append({"label": "Gula Darah Puasa", "value": f"{fbs} mg/dL", "status": "normal",
                         "description": "Gula darah puasa normal (< 100 mg/dL). Metabolisme glukosa Anda berjalan dengan baik."})
    elif fbs <= 125:
        results.append({"label": "Gula Darah Puasa", "value": f"{fbs} mg/dL", "status": "perhatian",
                         "description": "Prediabetes (100–125 mg/dL). Kadar gula darah sedikit tinggi. Risiko berkembang menjadi diabetes dan penyakit jantung meningkat."})
    else:
        results.append({"label": "Gula Darah Puasa", "value": f"{fbs} mg/dL", "status": "bahaya",
                         "description": "Gula darah tinggi – indikasi Diabetes (≥ 126 mg/dL). Segera periksakan ke dokter untuk konfirmasi dan penanganan."})

    # ── Jam Tidur ─────────────────────────────────────────────────────────────
    sleep = float(row["sleep_hours"])
    if sleep < 6:
        results.append({"label": "Durasi Tidur", "value": f"{sleep:.1f} jam/hari", "status": "bahaya",
                         "description": "Kurang tidur (< 6 jam). Tidur tidak cukup meningkatkan risiko hipertensi, obesitas, dan penyakit jantung."})
    elif sleep <= 9:
        results.append({"label": "Durasi Tidur", "value": f"{sleep:.1f} jam/hari", "status": "normal",
                         "description": "Durasi tidur ideal (6–9 jam). Waktu tidur Anda memadai untuk pemulihan dan kesehatan jantung."})
    else:
        results.append({"label": "Durasi Tidur", "value": f"{sleep:.1f} jam/hari", "status": "perhatian",
                         "description": "Terlalu banyak tidur (> 9 jam). Tidur berlebihan dapat menjadi tanda masalah kesehatan tertentu."})

    # ── Merokok ───────────────────────────────────────────────────────────────
    smoke_map = {"Never": ("Tidak Pernah Merokok", "normal", "Anda tidak merokok. Ini sangat baik untuk kesehatan jantung dan paru-paru."),
                 "Past": ("Mantan Perokok", "perhatian", "Anda pernah merokok. Risiko jantung mulai menurun setelah berhenti, tapi tetap lebih tinggi dari yang tidak pernah merokok."),
                 "Current": ("Perokok Aktif", "bahaya", "Merokok aktif meningkatkan risiko penyakit jantung hingga 2–4x lipat. Sangat disarankan untuk berhenti merokok.")}
    s = row["smoking_status"]
    results.append({"label": "Status Merokok", "value": smoke_map[s][0], "status": smoke_map[s][1], "description": smoke_map[s][2]})

    # ── Aktivitas Fisik ───────────────────────────────────────────────────────
    pa_map = {"Active": ("Aktif", "normal", "Aktivitas fisik rutin. Olahraga teratur sangat melindungi jantung dan menjaga berat badan ideal."),
              "Moderate": ("Sedang", "perhatian", "Aktivitas fisik sedang. Usahakan minimal 150 menit aktivitas aerobik sedang per minggu."),
              "Sedentary": ("Kurang Aktif", "bahaya", "Gaya hidup sedentari (kurang gerak) meningkatkan risiko penyakit jantung, obesitas, dan diabetes.")}
    pa = row["physical_activity"]
    results.append({"label": "Aktivitas Fisik", "value": pa_map[pa][0], "status": pa_map[pa][1], "description": pa_map[pa][2]})

    # ── Kualitas Diet ─────────────────────────────────────────────────────────
    diet_map = {"Healthy": ("Sehat", "normal", "Pola makan sehat mendukung kesehatan jantung secara langsung."),
                "Average": ("Cukup", "perhatian", "Pola makan cukup. Ada ruang untuk perbaikan, terutama perbanyak sayur, buah, dan kurangi makanan olahan."),
                "Unhealthy": ("Tidak Sehat", "bahaya", "Pola makan tidak sehat (tinggi gula, lemak jenuh, garam) meningkatkan risiko semua faktor risiko jantung.")}
    d = row["diet_quality"]
    results.append({"label": "Kualitas Diet", "value": diet_map[d][0], "status": diet_map[d][1], "description": diet_map[d][2]})

    # ── Alkohol ───────────────────────────────────────────────────────────────
    alc_map = {"None": ("Tidak Konsumsi", "normal", "Tidak konsumsi alkohol. Sangat baik untuk kesehatan jantung dan liver."),
               "Low": ("Rendah", "normal", "Konsumsi alkohol rendah. Masih dalam batas toleransi, namun tetap lebih baik tidak mengonsumsinya."),
               "Moderate": ("Sedang", "perhatian", "Konsumsi alkohol sedang. Mulai dapat mempengaruhi tekanan darah dan trigliserida."),
               "High": ("Tinggi", "bahaya", "Konsumsi alkohol tinggi meningkatkan tekanan darah, trigliserida, dan risiko penyakit jantung secara signifikan.")}
    alc = row["alcohol_consumption"]
    results.append({"label": "Konsumsi Alkohol", "value": alc_map[alc][0], "status": alc_map[alc][1], "description": alc_map[alc][2]})

    # ── Kondisi Medis ─────────────────────────────────────────────────────────
    results.append({"label": "Diabetes", "value": "Ya" if row["diabetes"] == 1 else "Tidak",
                     "status": "bahaya" if row["diabetes"] == 1 else "normal",
                     "description": "Diabetes meningkatkan risiko penyakit jantung 2x lipat. Kontrol gula darah sangat penting." if row["diabetes"] == 1 else "Tidak ada riwayat diabetes. Tetap jaga pola makan dan gaya hidup sehat."})
    results.append({"label": "Hipertensi", "value": "Ya" if row["hypertension"] == 1 else "Tidak",
                     "status": "bahaya" if row["hypertension"] == 1 else "normal",
                     "description": "Hipertensi adalah salah satu faktor risiko utama penyakit jantung. Kontrol tekanan darah secara rutin." if row["hypertension"] == 1 else "Tidak ada riwayat hipertensi. Pertahankan dengan diet rendah garam dan olahraga."})
    results.append({"label": "Obesitas", "value": "Ya" if row["obesity"] == 1 else "Tidak",
                     "status": "bahaya" if row["obesity"] == 1 else "normal",
                     "description": "Obesitas memperberat kerja jantung dan memicu hipertensi serta diabetes." if row["obesity"] == 1 else "Tidak ada riwayat obesitas. Jaga berat badan ideal dengan pola makan dan olahraga."})
    results.append({"label": "Riwayat Penyakit Jantung Sebelumnya", "value": "Ya" if row["previous_heart_disease"] == 1 else "Tidak",
                     "status": "bahaya" if row["previous_heart_disease"] == 1 else "normal",
                     "description": "Riwayat penyakit jantung sebelumnya adalah faktor risiko terbesar untuk kejadian berulang. Sangat penting untuk pengawasan ketat oleh dokter jantung." if row["previous_heart_disease"] == 1 else "Tidak ada riwayat penyakit jantung sebelumnya. Ini adalah faktor protektif yang baik."})
    results.append({"label": "Riwayat Keluarga Penyakit Jantung", "value": "Ya" if row["family_history"] == 1 else "Tidak",
                     "status": "perhatian" if row["family_history"] == 1 else "normal",
                     "description": "Riwayat keluarga dengan penyakit jantung meningkatkan risiko genetik. Skrining rutin sangat dianjurkan." if row["family_history"] == 1 else "Tidak ada riwayat keluarga penyakit jantung. Tetap jaga gaya hidup sehat."})

    return results


def get_food_recommendations(row, prediction: int) -> list:
    foods = []

    # Selalu sarankan makanan jantung sehat
    foods.append({
        "icon": "🫀",
        "title": "Makanan Baik untuk Jantung",
        "items": [
            "Ikan salmon, tuna, atau sarden (omega-3)",
            "Alpukat (lemak sehat)",
            "Kacang almond & kenari",
            "Oatmeal (menurunkan LDL)",
            "Biji chia & biji rami",
        ]
    })

    # Berdasarkan kolesterol
    chol = int(row["cholesterol_level"])
    ldl = int(row["cholesterol_ldl"])
    if chol >= 200 or ldl >= 130:
        foods.append({
            "icon": "🥦",
            "title": "Penurun Kolesterol",
            "items": [
                "Sayuran hijau (brokoli, bayam, kangkung)",
                "Buah beri (blueberry, strawberry)",
                "Kedelai & tahu (isoflavon)",
                "Bawang putih mentah",
                "Apel, pir (pektin tinggi serat)",
            ]
        })

    # Berdasarkan gula darah
    fbs = int(row["fasting_blood_sugar"])
    if fbs >= 100 or row["diabetes"] == 1:
        foods.append({
            "icon": "🍏",
            "title": "Kontrol Gula Darah",
            "items": [
                "Ubi jalar (indeks glikemik rendah)",
                "Sayuran non-pati (wortel, tomat)",
                "Kacang-kacangan (lentil, buncis)",
                "Kunyit & kayu manis",
                "Buah bit",
            ]
        })

    # Berdasarkan tekanan darah
    sys_bp = int(row["blood_pressure_systolic"])
    if sys_bp >= 130 or row["hypertension"] == 1:
        foods.append({
            "icon": "🍌",
            "title": "Penurun Tekanan Darah",
            "items": [
                "Pisang & kentang (kalium tinggi)",
                "Bayam & bit (nitrat alami)",
                "Biji labu & biji bunga matahari",
                "Dark chocolate (≥70% kakao)",
                "Yogurt rendah lemak",
            ]
        })

    # Berdasarkan trigliserida
    trig = int(row["triglycerides"])
    if trig >= 150:
        foods.append({
            "icon": "🫒",
            "title": "Penurun Trigliserida",
            "items": [
                "Minyak zaitun extra virgin",
                "Ikan berlemak 2–3x seminggu",
                "Cuka apel (sedikit sebelum makan)",
                "Bawang merah & bawang putih",
                "Teh hijau tanpa gula",
            ]
        })

    # Makanan yang harus dihindari
    avoid_items = []
    if prediction == 1 or sys_bp >= 130:
        avoid_items.append("Makanan tinggi garam (keripik, mie instan)")
    if chol >= 200 or ldl >= 130:
        avoid_items.append("Gorengan & makanan fast food")
    if fbs >= 100 or row["diabetes"] == 1:
        avoid_items.append("Minuman manis & kue-kue manis")
    if trig >= 150:
        avoid_items.append("Alkohol & minuman berenergi")
    if row["smoking_status"] == "Current":
        avoid_items.append("(Hentikan merokok segera)")
    if not avoid_items:
        avoid_items = ["Makanan ultra-proses berlebihan", "Lemak trans (margarin murah)"]

    foods.append({
        "icon": "🚫",
        "title": "Makanan yang Perlu Dihindari",
        "items": avoid_items[:5]
    })

    return foods
