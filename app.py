import streamlit as st
import pandas as pd
import numpy as np
import os
import re

# FUNGSI DETEKSI LOGO SMANETA
def get_logo_path():
    possible_names = [
        "66b480c34cb96SMAN_3_PANGKALPINANG-removebg-preview (1).png",
        "images (9).jfif", "images (9).png", "images (9).jpg", "images (8).png"
    ]
    for fname in possible_names:
        if os.path.exists(fname):
            return fname
    return None

logo_favicon = get_logo_path() or "https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_SMA_Negeri_3_Pangkalpinang.png"

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Q-BANK SMANETA Pangkalpinang",
    page_icon=logo_favicon,
    layout="wide"
)

# DAFTAR RESMI GURU
DAFTAR_GURU_SMAN3 = [
    "Suryadi, S.Pd., M.Pd (NIP. 197311272005011006)",
    "Dra. Musaadatul Uhro, M.M (NIP. 196710061998022001)",
    "Yusnaidah Siregar,S.Pd.Kim (NIP. 196807231992012001)",
    "Somad, S.Pd (NIP. 196812031998021002)",
    "Siti Nabsiati, S.Pd (NIP. 197001211998022001)",
    "Rita, S.Pd (NIP. 197902072005012008)",
    "Etty Afriani, S.Pd., M.M (NIP. 198104282006042009)",
    "Era, S.T., M.M (NIP. 198012292005012012)",
    "Hermawati, S.Pd., M.Pd (NIP. 198406282009032001)",
    "Lisa Sumartini, S.Pd (NIP. 198703102010012015)"
]

def clean_guru_name(fullname):
    name_only = fullname.split(' (NIP')[0]
    gelar_pattern = r'\b(dra|drs|s\.pd|m\.pd|s\.pd\.kim|s\.pd\.i|m\.eng|s\.t|m\.m|s\.e|s\.si)\b'
    name_cleaned = re.sub(gelar_pattern, '', name_only, flags=re.IGNORECASE)
    return re.sub(r'[^a-z]', '', name_cleaned.lower())

USERNAMES_GURU = [clean_guru_name(g) for g in DAFTAR_GURU_SMAN3]

# INITIAL SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_nama" not in st.session_state:
    st.session_state.user_nama = ""
if "bank_soal_folder" not in st.session_state:
    st.session_state.bank_soal_folder = {}

# STYLE
st.markdown("<style>.stApp {background-color: #FFFFFF; color: #1E293B;}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------
# HALAMAN LOGIN GURU
# ---------------------------------------------------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_path = get_logo_path()
        if logo_path:
            st.image(logo_path, width=150)
        st.title("Q-BANK SMANETA")
        st.subheader("SMA Negeri 3 Pangkalpinang")

        with st.form("login_form"):
            st.markdown("### 🔐 Login Guru SMANETA")
            username_input = st.text_input("Nama Guru (Huruf Kecil, Tanpa Spasi/Gelar):", placeholder="contoh: lisasumartini")
            password_input = st.text_input("Password:", type="password", placeholder="12345")
            submit_login = st.form_submit_button("Masuk", use_container_width=True)

            if submit_login:
                user_clean = re.sub(r'[^a-z]', '', username_input.lower())
                if (user_clean in USERNAMES_GURU or len(user_clean) > 2) and password_input == "12345":
                    st.session_state.logged_in = True
                    st.session_state.user_nama = username_input
                    st.success("Login Berhasil!")
                    st.rerun()
                else:
                    st.error("Nama atau Password (12345) salah!")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR & NAVIGASI MENU
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Guru Login:** `{st.session_state.user_nama}`")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.sidebar.radio("Navigasi Menu:", [
    "Beranda Utama", 
    "Kisi-Kisi Soal", 
    "Analisis Kualitatif (Aiken's V)", 
    "Analisis Kuantitatif (Empiris)",
    "Folder Bank Soal",
    "Rekap Laporan"
])

# ---------------------------------------------------------
# 1. BERANDA UTAMA
# ---------------------------------------------------------
if menu == "Beranda Utama":
    st.title("Q-BANK SMANETA Pangkalpinang")
    st.write("Sistem Analisis Validitas & Bank Soal Resmi SMAN 3 Pangkalpinang")
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Asesmen", "Formatif & Sumatif")
    m2.metric("Opsi Soal", "A - B - C - D - E")
    m3.metric("Status", "Aktif ✅")

# ---------------------------------------------------------
# 2. KISI-KISI & NASKAH SOAL
# ---------------------------------------------------------
elif menu == "Kisi-Kisi Soal":
    st.header("📑 Management Kisi-Kisi & Naskah Soal")
    
    # Identitas Soal
    c1, c2, c3 = st.columns(3)
    with c1:
        mapel_kisi = st.selectbox("Mata Pelajaran:", ["Biologi", "Fisika", "Kimia", "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Lainnya"], key="mp_kisi")
    with c2:
        fase_kelas = st.selectbox("Fase / Kelas:", ["Fase E (Kelas 10)", "Fase F (Kelas 11)", "Fase F (Kelas 12)"])
    with c3:
        semester = st.selectbox("Semester:", ["Ganjil", "Genap"])

    st.markdown("---")
    metode_kisi = st.radio("Pilih Metode Input Kisi-Kisi:", ["📤 Upload File (.xlsx/.csv)", "✍️ Input Manual di Tabel"], horizontal=True)

    if "Upload" in metode_kisi:
        file_kisi = st.file_uploader("Unggah File Kisi-Kisi (.xlsx / .csv)", type=["xlsx", "csv"])
        if file_kisi:
            try:
                skip_rows = st.number_input("Abaikan Baris Atas (Kop/Kosong):", 0, 20, 0)
                df = pd.read_csv(file_kisi, skiprows=skip_rows) if file_kisi.name.endswith('.csv') else pd.read_excel(file_kisi, skiprows=skip_rows)
                st.success(f"✅ File Kisi-Kisi Berhasil Dimuat! ({mapel_kisi} - {fase_kelas} - Sem {semester})")
                st.dataframe(df.dropna(how='all'), use_container_width=True)
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")
    else:
        n_kisi = st.number_input("Jumlah Indikator Soal:", min_value=1, max_value=50, value=5)
        init_kisi = {
            "No Soal": [i+1 for i in range(int(n_kisi))],
            "Fase / Kelas": [fase_kelas] * int(n_kisi),
            "Semester": [semester] * int(n_kisi),
            "Capaian Pembelajaran / KD": [""] * int(n_kisi),
            "Indikator Soal": [""] * int(n_kisi),
            "Teks Soal / Naskah Soal": [""] * int(n_kisi),
            "Kunci Jawaban": ["A"] * int(n_kisi),
            "Level Kognitif": ["L2"] * int(n_kisi),
            "Bentuk Soal": ["Pilihan Ganda"] * int(n_kisi)
        }
        st.write("✍️ **Ketik Kisi-Kisi & Teks Soal Langsung di Tabel:**")
        df_kisi_edited = st.data_editor(pd.DataFrame(init_kisi), use_container_width=True)
        
        if st.button("💾 Simpan Kisi-Kisi & Soal"):
            kelas_folder = fase_kelas.split("(")[-1].replace(")", "").strip()
            if mapel_kisi not in st.session_state.bank_soal_folder:
                st.session_state.bank_soal_folder[mapel_kisi] = {}
            if kelas_folder not in st.session_state.bank_soal_folder[mapel_kisi]:
                st.session_state.bank_soal_folder[mapel_kisi][kelas_folder] = []
                
            st.session_state.bank_soal_folder[mapel_kisi][kelas_folder].append(df_kisi_edited)
            st.success(f"Kisi-Kisi & Soal berhasil disimpan ke Folder [{mapel_kisi} - {kelas_folder}]!")

# ---------------------------------------------------------
# 3. ANALISIS KUALITATIF AIKEN'S V
# ---------------------------------------------------------
elif menu == "Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    
    col_mp, col_kls = st.columns(2)
    with col_mp:
        mapel = st.selectbox("Mata Pelajaran:", ["Biologi", "Fisika", "Kimia", "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Lainnya"])
    with col_kls:
        kelas = st.selectbox("Kelas:", ["Kelas 10", "Kelas 11", "Kelas 12"])

    metode_kuali = st.radio("Pilih Metode Penilaian:", ["📤 Upload File Penilaian Validator", "✍️ Input Manual Skor Validator"], horizontal=True)
    df_hitung_kuali = None

    if "Upload" in metode_kuali:
        file_val = st.file_uploader("Upload File Penilaian Validator (.xlsx/.csv)", type=["xlsx", "csv"])
        if file_val:
            try:
                df_upload = pd.read_csv(file_val) if file_val.name.endswith('.csv') else pd.read_excel(file_val)
                cols = [c for c in df_upload.columns if 'v' in c.lower() or 'skor' in c.lower()]
                if not cols:
                    cols = df_upload.select_dtypes(include=[np.number]).columns.tolist()
                
                if cols:
                    df_hitung_kuali = df_upload.copy()
                    df_hitung_kuali["Indeks Aiken V"] = ((df_hitung_kuali[cols].sum(axis=1) - (len(cols)*1)) / (len(cols)*4)).round(3)
            except Exception as e:
                st.error(f"Error memproses file: {e}")
    else:
        n_soal = st.number_input("Jumlah Soal Ditelaah:", min_value=1, max_value=50, value=5)
        init_data = {
            "Nomor Soal": [f"Soal {i+1}" for i in range(int(n_soal))],
            "Skor Validator 1 (1-5)": [4]*int(n_soal),
            "Skor Validator 2 (1-5)": [4]*int(n_soal),
            "Skor Validator 3 (1-5)": [5]*int(n_soal)
        }
        df_input = st.data_editor(pd.DataFrame(init_data), use_container_width=True)
        
        skor_cols = ["Skor Validator 1 (1-5)", "Skor Validator 2 (1-5)", "Skor Validator 3 (1-5)"]
        v_score = ((df_input[skor_cols].sum(axis=1) - (len(skor_cols) * 1)) / (len(skor_cols) * 4)).round(3)
        df_hitung_kuali = df_input.copy()
        df_hitung_kuali["Indeks Aiken V"] = v_score

    if df_hitung_kuali is not None and "Indeks Aiken V" in df_hitung_kuali.columns:
        df_hitung_kuali["Status"] = df_hitung_kuali["Indeks Aiken V"].apply(lambda x: "VALID ✅" if x >= 0.6 else "REVISI ❌")
        st.subheader("📊 Hasil Perhitungan Validitas Isi (Aiken's V)")
        st.dataframe(df_hitung_kuali[["Indeks Aiken V", "Status"]], use_container_width=True)
        
        if st.button("💾 Simpan Hasil Kualitatif ke Bank Soal"):
            if mapel not in st.session_state.bank_soal_folder:
                st.session_state.bank_soal_folder[mapel] = {}
            if kelas not in st.session_state.bank_soal_folder[mapel]:
                st.session_state.bank_soal_folder[mapel][kelas] = []
                
            st.session_state.bank_soal_folder[mapel][kelas].append(df_hitung_kuali)
            st.success(f"Berhasil disimpan di Folder Bank Soal [{mapel} - {kelas}]!")

# ---------------------------------------------------------
# 4. ANALISIS KUANTITATIF EMPIRIS
# ---------------------------------------------------------
elif menu == "Analisis Kuantitatif (Empiris)":
    st.header("📊 Analisis Kuantitatif Jawaban Siswa")
    
    col_mp_k, col_kls_k = st.columns(2)
    with col_mp_k:
        mapel_kuanti = st.selectbox("Mata Pelajaran:", ["Biologi", "Fisika", "Kimia", "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Lainnya"], key="mp_kuanti")
    with col_kls_k:
        kelas_kuanti = st.selectbox("Kelas:", ["Kelas 10", "Kelas 11", "Kelas 12"], key="kls_kuanti")

    metode_kuanti = st.radio("Pilih Metode Input Jawaban Siswa:", ["📤 Upload File Jawaban (.xlsx/.csv)", "✍️ Input/Edit Manual Jawaban Siswa"], horizontal=True)
    kunci_jawaban = st.text_input("🔑 Kunci Jawaban Soal (Gunakan Koma, Misal: A,B,C,D,E):", value="A,B,C,D,E")
    kunci_list = [k.strip().upper() for k in kunci_jawaban.split(",")]
    
    df_jawaban_siswa = None

    if "Upload" in metode_kuanti:
        file_jawab = st.file_uploader("Unggah File Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])
        if file_jawab:
            try:
                df_jawaban_siswa = pd.read_csv(file_jawab) if file_jawab.name.endswith('.csv') else pd.read_excel(file_jawab)
                st.write("📌 **Pratinjau Data Jawaban Siswa:**")
                st.dataframe(df_jawaban_siswa.head(), use_container_width=True)
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")
    else:
        c_sis, c_soal = st.columns(2)
        with c_sis:
            jml_siswa = st.number_input("Jumlah Siswa:", min_value=2, max_value=100, value=5)
        with c_soal:
            jml_soal_emp = st.number_input("Jumlah Soal:", min_value=1, max_value=50, value=5)
            
        init_jawaban = {"Nama Siswa": [f"Siswa {i+1}" for i in range(int(jml_siswa))]}
        for j in range(int(jml_soal_emp)):
            init_jawaban[f"Soal {j+1}"] = ["A"] * int(jml_siswa)
            
        st.write("✍️ **Ketik/Edit Jawaban Siswa (A/B/C/D/E) Langsung di Tabel:**")
        df_jawaban_siswa = st.data_editor(pd.DataFrame(init_jawaban), use_container_width=True)

    if df_jawaban_siswa is not None:
        if st.button("⚡ Hitung Analisis Empiris"):
            soal_cols = [c for c in df_jawaban_siswa.columns if c.lower() != "nama siswa" and c.lower() != "nama"]
            df_skor = pd.DataFrame()
            
            for idx, col in enumerate(soal_cols):
                kunci_soal = kunci_list[idx] if idx < len(kunci_list) else "A"
                df_skor[col] = df_jawaban_siswa[col].apply(lambda x: 1 if str(x).strip().upper() == kunci_soal else 0)
                
            res_kuanti = []
            for idx, col in enumerate(soal_cols):
                p_val = df_skor[col].mean()
                if p_val < 0.3:
                    kat_sukar = "Sukar 🔴"
                elif p_val <= 0.7:
                    kat_sukar = "Sedang 🟡"
                else:
                    kat_sukar = "Mudah 🟢"
                    
                res_kuanti.append({
                    "Nomor Soal": col,
                    "Tingkat Kesukaran (P)": round(p_val, 2),
                    "Kategori Kesukaran": kat_sukar,
                    "Status Soal": "DITERIMA ✅" if 0.2 <= p_val <= 0.8 else "REVISI/BUANG ❌"
                })
                
            df_res_kuanti = pd.DataFrame(res_kuanti)
            st.subheader("📈 Hasil Analisis Empiris")
            st.dataframe(df_res_kuanti, use_container_width=True)
            
            if st.button("💾 Simpan Hasil Kuantitatif ke Bank Soal"):
                if mapel_kuanti not in st.session_state.bank_soal_folder:
                    st.session_state.bank_soal_folder[mapel_kuanti] = {}
                if kelas_kuanti not in st.session_state.bank_soal_folder[mapel_kuanti]:
                    st.session_state.bank_soal_folder[mapel_kuanti][kelas_kuanti] = []
                    
                st.session_state.bank_soal_folder[mapel_kuanti][kelas_kuanti].append(df_res_kuanti)
                st.success(f"Berhasil disimpan di Folder Bank Soal [{mapel_kuanti} - {kelas_kuanti}]!")

# ---------------------------------------------------------
# 5. FOLDER BANK SOAL TERUJI (PER MAPEL & PER KELAS)
# ---------------------------------------------------------
elif menu == "Folder Bank Soal":
    st.header("📁 Folder Bank Soal Teruji")
    if not st.session_state.bank_soal_folder:
        st.info("💡 Belum ada data bank soal yang tersimpan di folder.")
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            m_select = st.selectbox("📂 Pilih Folder Mata Pelajaran:", list(st.session_state.bank_soal_folder.keys()))
        
        if m_select:
            list_kelas = list(st.session_state.bank_soal_folder[m_select].keys())
            if not list_kelas:
                st.warning("Belum ada data kelas pada mata pelajaran ini.")
            else:
                with col_f2:
                    k_select = st.selectbox("📑 Pilih Sub-Folder Kelas:", list_kelas)
                
                st.markdown("---")
                st.subheader(f"📂 Folder: {m_select} ➔ 📑 {k_select}")
                
                items = st.session_state.bank_soal_folder[m_select][k_select]
                for idx, df_item in enumerate(items):
                    with st.expander(f"📦 Paket Data Soal #{idx+1}", expanded=True):
                        st.dataframe(df_item, use_container_width=True)

# ---------------------------------------------------------
# 6. REKAP LAPORAN
# ---------------------------------------------------------
elif menu == "Rekap Laporan":
    st.header("📥 Rekap Laporan & Lembar Pengesahan TTD")
    st.success("Laporan Excel mencakup pengesahan Waka Kurikulum (Era, S.T., M.M - NIP. 198012292005012012).")
