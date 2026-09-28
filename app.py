import streamlit as st
import pandas as pd
import numpy as np
import os
import re

# FUNGSI DETEKSI LOGO
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
# HALAMAN LOGIN
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
# DASHBOARD UTAMA
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Guru Login:** `{st.session_state.user_nama}`")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.sidebar.radio("Navigasi Menu:", [
    "Beranda Utama", 
    "Upload Kisi-Kisi Soal", 
    "Analisis Kualitatif (Aiken's V)", 
    "Folder Bank Soal",
    "Rekap Laporan"
])

if menu == "Beranda Utama":
    st.title("Q-BANK SMANETA Pangkalpinang")
    st.write("Sistem Analisis Validitas & Bank Soal Resmi SMAN 3 Pangkalpinang")
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Asesmen", "Formatif & Sumatif")
    m2.metric("Opsi Soal", "A - B - C - D - E")
    m3.metric("Status", "Aktif ✅")

elif menu == "Upload Kisi-Kisi Soal":
    st.header("📑 Upload Kisi-Kisi Soal")
    file_kisi = st.file_uploader("Unggah File (.xlsx / .csv)", type=["xlsx", "csv"])
    if file_kisi:
        try:
            skip_rows = st.number_input("Abaikan Baris Atas (Kop/Kosong):", 0, 20, 0)
            df = pd.read_csv(file_kisi, skiprows=skip_rows) if file_kisi.name.endswith('.csv') else pd.read_excel(file_kisi, skiprows=skip_rows)
            st.dataframe(df.dropna(how='all'), use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

elif menu == "Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    mapel = st.selectbox("Mata Pelajaran:", ["Biologi", "Fisika", "Kimia", "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Lainnya"])
    
    file_val = st.file_uploader("Upload File Penilaian Validator (.xlsx/.csv)", type=["xlsx", "csv"])
    if file_val:
        try:
            df = pd.read_csv(file_val) if file_val.name.endswith('.csv') else pd.read_excel(file_val)
            cols = [c for c in df.columns if 'v' in c.lower() or 'skor' in c.lower()]
            if not cols:
                cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if cols:
                df["Indeks Aiken V"] = ((df[cols].sum(axis=1) - (len(cols)*1)) / (len(cols)*4)).round(3)
                df["Status"] = df["Indeks Aiken V"].apply(lambda x: "VALID ✅" if x >= 0.6 else "REVISI ❌")
                st.dataframe(df[["Indeks Aiken V", "Status"]], use_container_width=True)
                
                if st.button("💾 Simpan ke Folder Bank Soal"):
                    st.session_state.bank_soal_folder.setdefault(mapel, []).append(df)
                    st.success(f"Tersimpan di Bank Soal {mapel}!")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "Folder Bank Soal":
    st.header("📁 Bank Soal Teruji")
    if not st.session_state.bank_soal_folder:
        st.info("Belum ada data bank soal tersimpan.")
    else:
        m = st.selectbox("Pilih Mata Pelajaran:", list(st.session_state.bank_soal_folder.keys()))
        for i, df_item in enumerate(st.session_state.bank_soal_folder[m]):
            st.write(f"**Paket Soal #{i+1}**")
            st.dataframe(df_item, use_container_width=True)

elif menu == "Rekap Laporan":
    st.header("📥 Rekap & Lembar Pengesahan TTD")
    st.success("Laporan Excel mencakup pengesahan Waka Kurikulum (Era, S.T., M.M - NIP. 198012292005012012).")
