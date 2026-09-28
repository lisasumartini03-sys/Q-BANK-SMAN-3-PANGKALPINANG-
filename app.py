import os
import pandas as pd
import numpy as np
import streamlit as st

# ==========================================
# 1. NAMA FILE LOGO SEKOLAH
# ==========================================
LOGO_PATH = "66b480c34cb96SMAN_3_PANGKALPINANG-removebg-preview (1).png"

# ==========================================
# 2. DATABASE USER (NAMA GURU SAJA - TANPA GELAR & TANPA TU)
# Username: huruf kecil tanpa spasi
# ==========================================
USER_DATABASE = {
    "lisasumartini": {"nama": "Lisa Sumartini", "role": "Guru"},
    "budianto": {"nama": "Budianto", "role": "Guru"},
    "sitinurbaya": {"nama": "Siti Nurbaya", "role": "Guru"},
    "ahmadfauzi": {"nama": "Ahmad Fauzi", "role": "Guru"},
    "dewilesteri": {"nama": "Dewi Lestari", "role": "Guru"},
}

# ==========================================
# 3. DAFTAR MATA PELAJARAN LENGKAP
# ==========================================
DAFTAR_MAPEL = [
    "Pendidikan Agama dan Budi Pekerti",
    "Pendidikan Pancasila dan Kewarganegaraan",
    "Bahasa Indonesia",
    "Matematika",
    "Sejarah",
    "Bahasa Inggris",
    "Biologi",
    "Fisika",
    "Kimia",
    "Ekonomi",
    "Geografi",
    "Sosiologi",
    "Informatika",
    "Seni Budaya",
    "Pendidikan Jasmani, Olahraga, dan Kesehatan",
    "Prakarya dan Kewirausahaan",
    "Bahasa Arab",
    "Bahasa Jepang"
]

# ==========================================
# 4. FUNGSI AIKEN'S V & KUANTITATIF
# ==========================================

def hitung_aiken_v(skor_list, r_min=0, r_max=1):
    """
    Menghitung Indeks Aiken's V
    Formula: V = SUM(r - r_min) / (n * (r_max - r_min))
    n = Jumlah Validator
    r_max = Skor Maksimum per Aspek (1 jika Binary Checklist)
    r_min = Skor Minimum per Aspek (0 jika Binary Checklist)
    """
    n = len(skor_list)
    if n == 0 or (r_max - r_min) == 0:
        return 0.0
    sum_s = sum([r - r_min for r in skor_list])
    v = sum_s / (n * (r_max - r_min))
    return round(v, 3)

def get_kriteria_aiken(v_val):
    if v_val >= 0.80:
        return "Tinggi / Valid"
    elif v_val >= 0.40:
        return "Sedang / Perlu Revisi"
    else:
        return "Rendah / Tidak Valid"

def get_kriteria_kesukaran(p):
    if p < 0.20:
        return "Sangat Sukar"
    elif p <= 0.30:
        return "Sukar"
    elif p <= 0.70:
        return "Sedang"
    elif p <= 0.80:
        return "Mudah"
    else:
        return "Sangat Mudah"

def get_kriteria_daya_beda(dp):
    if dp >= 0.40:
        return "Sangat Baik"
    elif dp >= 0.30:
        return "Baik"
    elif dp >= 0.20:
        return "Cukup (Perlu Revisi)"
    elif dp >= 0.00:
        return "Jelek (Harus Dibuang/Revisi)"
    else:
        return "Sangat Jelek (Harus Dibuang)"

def get_kriteria_validitas(r_hitung, r_tabel=0.30):
    if r_hitung >= r_tabel:
        return f"Valid (r = {r_hitung:.3f} >= {r_tabel})"
    else:
        return f"Tidak Valid (r = {r_hitung:.3f} < {r_tabel})"

def hitung_reliabilitas_kr20(df_jawaban):
    n = df_jawaban.shape[1]
    N = df_jawaban.shape[0]
    if n <= 1 or N <= 1:
        return 0, "Data tidak cukup"
    
    p = df_jawaban.mean(axis=0)
    q = 1 - p
    pq_sum = (p * q).sum()
    
    total_skor = df_jawaban.sum(axis=1)
    var_total = total_skor.var(ddof=1)
    
    if var_total == 0:
        return 0, "Varians Total Nol"
        
    r_11 = (n / (n - 1)) * (1 - (pq_sum / var_total))
    
    if r_11 >= 0.70:
        kriteria = f"Tinggi / Reliabel (r_11 = {r_11:.3f})"
    elif r_11 >= 0.40:
        kriteria = f"Sedang / Cukup Reliabel (r_11 = {r_11:.3f})"
    else:
        kriteria = f"Rendah / Tidak Reliabel (r_11 = {r_11:.3f})"
        
    return r_11, kriteria

def analisis_efektivitas_pengecoh(df_pilihan, kunci_jawaban):
    hasill_distraktor = []
    n_siswa = len(df_pilihan)
    
    for col in df_pilihan.columns:
        kunci = kunci_jawaban.get(col, "")
        counts = df_pilihan[col].value_counts()
        detail_soal = {}
        for opsi in ['A', 'B', 'C', 'D', 'E']:
            if opsi == kunci:
                detail_soal[opsi] = "Kunci Jawaban"
            else:
                persen = (counts.get(opsi, 0) / n_siswa) * 100
                if persen >= 5.0:
                    status = f"Efektif ({persen:.1f}%)"
                else:
                    status = f"Kurang Efektif ({persen:.1f}%)"
                detail_soal[opsi] = status
        hasill_distraktor.append({"Soal": col, **detail_soal})
        
    return pd.DataFrame(hasill_distraktor)

# ==========================================
# 5. TAMPILAN APLIKASI STREAMLIT
# ==========================================

st.set_page_config(page_title="Q-BANK SMAN 3 PANGKALPINANG", layout="wide")

# Sidebar Logo & Navigasi
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=140)

st.sidebar.title("📌 Navigasi Aplikasi")
menu = st.sidebar.radio("Pilih Halaman:", [
    "🏠 Halaman Sampul (Cover)", 
    "📋 Kisi-Kisi Soal", 
    "📊 Analisis Soal (Kualitatif Aiken's V & Kuantitatif)"
])

st.sidebar.markdown("---")
st.sidebar.header("🔐 Akses Guru")
username_input = st.sidebar.text_input("Username (nama kecil tanpa spasi):").strip().lower()

# ----------------------------------------------------
# HALAMAN 1: SAMPUL / COVER PAGE
# ----------------------------------------------------
if menu == "🏠 Halaman Sampul (Cover)":
    if os.path.exists(LOGO_PATH):
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            st.image(LOGO_PATH, width=160)

    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Q-BANK SMAN 3 PANGKALPINANG</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4B5563;'>Sistem Bank Soal, Kisi-Kisi & Analisis Kualitas Butir Soal</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        ### 🏫 Informasi Sekolah
        * **Nama Sekolah:** SMAN 3 Pangkalpinang
        * **Modul Utama:** 
          1. **Format Kisi-Kisi Soal**
          2. **Uji Kualitatif & Formula Aiken's V** (Penilaian Validator 1, 2, 3)
          3. **Uji Kuantitatif** (Validitas, Reliabilitas, Kesukaran, Daya Beda, Pengecoh)
        * **Dukungan Mata Pelajaran:** 18 Mata Pelajaran (termasuk Prakarya, Bahasa Arab, & Bahasa Jepang)
        """)
        st.write("👈 *Silakan masukkan username di sidebar kiri untuk mulai menggunakan modul.*")

# ----------------------------------------------------
# HALAMAN 2: KISI-KISI SOAL
# ----------------------------------------------------
elif menu == "📋 Kisi-Kisi Soal":
    if username_input in USER_DATABASE:
        user_info = USER_DATABASE[username_input]
        st.sidebar.success(f"Selamat Datang, **{user_info['nama']}**")
        selected_mapel = st.sidebar.selectbox("Pilih Mata Pelajaran:", DAFTAR_MAPEL)
        
        st.title("📋 Format Kisi-Kisi Penulisan Soal")
        st.subheader(f"Mata Pelajaran: {selected_mapel}")
        
        with st.form("form_kisi_kisi"):
            st.markdown("#### Input Item Kisi-Kisi Soal")
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                cp = st.text_area("Capaian Pembelajaran (CP) / Elemen:")
                materi = st.text_input("Materi / Pokok Bahasan:")
                indikator = st.text_area("Indikator Soal:")
            with col_k2:
                level_kognitif = st.selectbox("Level Kognitif:", ["L1 (Pemahaman/C1-C2)", "L2 (Penerapan/C3)", "L3 (Penalaran/C4-C6)"])
                bentuk_soal = st.selectbox("Bentuk Soal:", ["Pilihan Ganda", "Pilihan Ganda Kompleks", "Menjodohkan", "Isian Singkat", "Uraian"])
                no_soal = st.number_input("Nomor Soal:", min_value=1, max_value=100, value=1)
            
            submit_kisi = st.form_submit_button("➕ Tambah ke Tabel Kisi-Kisi")
        
        st.markdown("---")
        st.subheader("📌 Tabel Kisi-Kisi Soal")
        kisi_dummy = pd.DataFrame({
            "No. Soal": [1, 2, 3],
            "Capaian Pembelajaran": ["Peserta didik mampu menganalisis...", "Peserta didik memahami...", "Peserta didik mengevaluasi..."],
            "Materi": ["Materi Bab 1", "Materi Bab 1", "Materi Bab 2"],
            "Indikator Soal": ["Disajikan teks, siswa dapat...", "Disajikan data, siswa dapat...", "Disajikan kasus, siswa dapat..."],
            "Level Kognitif": ["L2 (C3)", "L1 (C2)", "L3 (C5)"],
            "Bentuk Soal": ["Pilihan Ganda", "Pilihan Ganda", "Pilihan Ganda"]
        })
        st.dataframe(kisi_dummy, use_container_width=True)

    elif username_input:
        st.sidebar.error("Username tidak ditemukan! Gunakan nama kecil tanpa spasi dan tanpa gelar.")
    else:
        st.info("Silakan masukkan Username pada sidebar untuk mengakses Kisi-Kisi.")

# ----------------------------------------------------
# HALAMAN 3: ANALISIS SOAL (KUALITATIF AIKEN & KUANTITATIF)
# ----------------------------------------------------
else:
    if username_input in USER_DATABASE:
        user_info = USER_DATABASE[username_input]
        st.sidebar.success(f"Selamat Datang, **{user_info['nama']}**")
        
        selected_mapel = st.sidebar.selectbox("Pilih Mata Pelajaran:", DAFTAR_MAPEL)
        
        st.title("📑 Modul Analisis Butir Soal")
        st.subheader(f"Mata Pelajaran: {selected_mapel}")
        
        tab_kualitatif, tab_kuantitatif = st.tabs(["📝 UJI KUALITATIF (VALIDITAS AIKEN'S V)", "📈 UJI KUANTITATIF SOAL"])
        
        # ----------------------------------------------------
        # FITUR: UJI KUALITATIF AIKEN'S V & IDENTITAS VALIDATOR
        # ----------------------------------------------------
        with tab_kualitatif:
            st.header("Telaah Kualitatif Soal & Analisis Indeks Aiken's V")
            st.caption("Penelaahan butir soal oleh Validator 1, 2, dan 3 berbasis perhitungan koefisien Aiken's V.")
            
            # Form Identitas Nama Validator
            st.markdown("### 👥 Identitas Tim Validator")
            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1:
                nama_val1 = st.text_input("Nama Validator 1:", value="Validator 1")
            with col_v2:
                nama_val2 = st.text_input("Nama Validator 2:", value="Validator 2")
            with col_v3:
                nama_val3 = st.text_input("Nama Validator 3:", value="Validator 3")
            
            st.markdown("---")
            soal_num = st.number_input("Nomor Soal yang Ditelaah:", min_value=1, max_value=100, value=1)
            
            # Daftar 10 Kriteria Penelaahan Soal
            ASPEK_LIST = [
                ("Materi", "1. Soal sesuai dengan indikator"),
                ("Materi", "2. Pilihan jawaban homogen & logis"),
                ("Materi", "3. Ada satu kunci jawaban yang tepat"),
                ("Konstruksi", "4. Pokok soal dirumuskan tegas & jelas"),
                ("Konstruksi", "5. Pokok soal bebas dari petunjuk kunci"),
                ("Konstruksi", "6. Bebas dari pernyataan negatif ganda"),
                ("Konstruksi", "7. Panjang opsi jawaban relatif sama"),
                ("Bahasa", "8. Menggunakan bahasa baku (PUEBI)"),
                ("Bahasa", "9. Komunikatif & mudah dipahami"),
                ("Bahasa", "10. Bebas bahasa lokal/tabu")
            ]
            
            st.subheader(f"Form Penilaian Checklist Soal No. {soal_num}")
            
            v1_tab, v2_tab, v3_tab = st.tabs([f"👤 {nama_val1}", f"👤 {nama_val2}", f"👤 {nama_val3}"])
            
            def get_validator_checklist(v_key, v_name):
                st.markdown(f"**Checklist Penilaian oleh {v_name}** *(Centang jika Terpenuhi/Sesuai)*")
                skor_dict = {}
                for idx, (aspek, item) in enumerate(ASPEK_LIST):
                    val = st.checkbox(f"[{aspek}] {item}", key=f"{v_key}_item_{idx}")
                    skor_dict[f"Item_{idx+1}"] = 1 if val else 0
                return skor_dict

            with v1_tab:
                skor_v1 = get_validator_checklist("v1", nama_val1)
            with v2_tab:
                skor_v2 = get_validator_checklist("v2", nama_val2)
            with v3_tab:
                skor_v3 = get_validator_checklist("v3", nama_val3)

            # Hitung Rekapitulasi Aiken's V per Item
            st.markdown("---")
            st.subheader("📊 Rekapitulasi Hasil Uji Kualitatif (Indeks Aiken's V)")
            
            rekap_rows = []
            semua_v = []
            
            for idx, (aspek, item) in enumerate(ASPEK_LIST):
                item_key = f"Item_{idx+1}"
                s1 = skor_v1[item_key]
                s2 = skor_v2[item_key]
                s3 = skor_v3[item_key]
                
                v_index = hitung_aiken_v([s1, s2, s3], r_min=0, r_max=1)
                semua_v.append(v_index)
                kriteria = get_kriteria_aiken(v_index)
                
                rekap_rows.append({
                    "No": idx + 1,
                    "Aspek": aspek,
                    "Kriteria Penelaahan": item,
                    nama_val1: "✓" if s1 == 1 else "✗",
                    nama_val2: "✓" if s2 == 1 else "✗",
                    nama_val3: "✓" if s3 == 1 else "✗",
                    "Indeks Aiken (V)": v_index,
                    "Kategori Validitas": kriteria
                })
            
            df_rekap_aiken = pd.DataFrame(rekap_rows)
            st.dataframe(df_rekap_aiken, use_container_width=True)
            
            # Mean Total Indeks Aiken's V
            mean_v = round(float(np.mean(semua_v)), 3)
            st.markdown(f"### **Rata-Rata Indeks Aiken's V (Soal No. {soal_num}): `{mean_v}`**")
            
            if mean_v >= 0.80:
                st.success(f"**Kesimpulan Uji Kualitatif Soal No. {soal_num}:** **VALID / SANGAT LAYAK** (Indeks V = {mean_v} >= 0.80)")
            elif mean_v >= 0.40:
                st.warning(f"**Kesimpulan Uji Kualitatif Soal No. {soal_num}:** **CUKUP VALID / REVISI KECIL** (Indeks V = {mean_v})")
            else:
                st.error(f"**Kesimpulan Uji Kualitatif Soal No. {soal_num}:** **TIDAK VALID / DIBUANG** (Indeks V = {mean_v} < 0.40)")

        # ----------------------------------------------------
        # FITUR: UJI KUANTITATIF
        # ----------------------------------------------------
        with tab_kuantitatif:
            st.header("Analisis Kuantitatif Respon Siswa")
            
            q_tab1, q_tab2, q_tab3, q_tab4, q_tab5 = st.tabs([
                "1. Validitas Butir", 
                "2. Reliabilitas", 
                "3. Tingkat Kesukaran", 
                "4. Daya Pembeda", 
                "5. Efektivitas Pengecoh"
            ])
            
            np.random.seed(42)
            sample_data = np.random.choice([0, 1], size=(20, 10), p=[0.3, 0.7])
            df_skor = pd.DataFrame(sample_data, columns=[f"Soal_{i+1}" for i in range(10)])
            
            with q_tab1:
                st.subheader("Uji Validitas Butir Soal")
                r_tabel = st.number_input("Nilai r-tabel rujukan:", value=0.30, step=0.01)
                
                total_skor = df_skor.sum(axis=1)
                validitas_res = []
                for col in df_skor.columns:
                    r_hitung = np.corrcoef(df_skor[col], total_skor)[0, 1]
                    kriteria = get_kriteria_validitas(r_hitung, r_tabel)
                    validitas_res.append({"Butir Soal": col, "r-Hitung": round(r_hitung, 3), "Kriteria": kriteria})
                    
                st.dataframe(pd.DataFrame(validitas_res), use_container_width=True)

            with q_tab2:
                st.subheader("Uji Reliabilitas Test (KR-20)")
                r_11, kriteria_rel = hitung_reliabilitas_kr20(df_skor)
                st.metric("Koefisien Reliabilitas (r_11)", round(r_11, 3))
                st.write(f"**Kriteria Reliabilitas:** {kriteria_rel}")

            with q_tab3:
                st.subheader("Uji Tingkat Kesukaran (Facility Value)")
                kesukaran_res = []
                p_values = df_skor.mean(axis=0)
                for col, p in p_values.items():
                    kesukaran_res.append({
                        "Butir Soal": col, 
                        "Indeks Kesukaran (p)": round(p, 3), 
                        "Kriteria": get_kriteria_kesukaran(p)
                    })
                st.dataframe(pd.DataFrame(kesukaran_res), use_container_width=True)

            with q_tab4:
                st.subheader("Uji Daya Pembeda (Discrimination Index)")
                n_siswa = len(df_skor)
                n_kelompok = max(1, int(n_siswa * 0.27))
                
                df_sorted = df_skor.copy()
                df_sorted['Total'] = df_sorted.sum(axis=1)
                df_sorted = df_sorted.sort_values(by='Total', ascending=False)
                
                kel_atas = df_sorted.iloc[:n_kelompok, :-1]
                kel_bawah = df_sorted.iloc[-n_kelompok:, :-1]
                
                dp_res = []
                for col in df_skor.columns:
                    p_atas = kel_atas[col].mean()
                    p_bawah = kel_bawah[col].mean()
                    dp = p_atas - p_bawah
                    dp_res.append({
                        "Butir Soal": col, 
                        "Indeks Daya Beda": round(dp, 3), 
                        "Kriteria": get_kriteria_daya_beda(dp)
                    })
                st.dataframe(pd.DataFrame(dp_res), use_container_width=True)

            with q_tab5:
                st.subheader("Uji Efektivitas Pengecoh / Distraktor")
                st.caption("Pengecoh dianggap **Efektif** jika dipilih minimal 5% dari total peserta ujian.")
                
                pilihan = ['A', 'B', 'C', 'D', 'E']
                df_pilihan = pd.DataFrame(
                    np.random.choice(pilihan, size=(20, 5)), 
                    columns=[f"Soal_{i+1}" for i in range(5)]
                )
                kunci_dummy = {"Soal_1": "A", "Soal_2": "B", "Soal_3": "C", "Soal_4": "D", "Soal_5": "E"}
                
                df_distraktor = analisis_efektivitas_pengecoh(df_pilihan, kunci_dummy)
                st.dataframe(df_distraktor, use_container_width=True)

    elif username_input:
        st.sidebar.error("Username tidak ditemukan! Gunakan nama kecil tanpa spasi dan tanpa gelar.")
    else:
        st.info("Silakan masukkan Username pada sidebar untuk mengakses modul analisis.")
