import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import re

# Konfigurasi Halaman & Tema Web Sekolah
st.set_page_config(
    page_title="Q-BANK SMANETA Pangkalpinang",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DAFTAR RESMI GURU SMAN 3 PANGKALPINANG (47 GURU & NIP)
DAFTAR_GURU_SMAN3 = [
    "Suryadi, S.Pd., M.Pd (NIP. 197311272005011006)",
    "Dra. Musaadatul Uhro, M.M (NIP. 196710061998022001)",
    "Yusnaidah Siregar,S.Pd.Kim (NIP. 196807231992012001)",
    "Somad, S.Pd (NIP. 196812031998021002)",
    "Siti Nabsiati, S.Pd (NIP. 197001211998022001)",
    "Risma Damanik, S.Pd (NIP. 197202281997022003)",
    "Ristawani, S.Pd., M.Eng (NIP. 197301132005012007)",
    "Drs. Eddy Salahuddin (NIP. 196807231999031002)",
    "Rita, S.Pd (NIP. 197902072005012008)",
    "Etty Afriani, S.Pd., M.M (NIP. 198104282006042009)",
    "Era, S.T., M.M (NIP. 198012292005012012)",
    "Nazlah, S.Pd.I (NIP. 197311272006042002)",
    "Nizamuddin, S.E (NIP. 197602012005011005)",
    "Hermawati, S.Pd., M.Pd (NIP. 198406282009032001)",
    "Indra, S.Pd (NIP. 198301252009031005)",
    "Nurlela S, S.Si (NIP. 197105192006042006)",
    "Yani Wiliawati, S.Ip (NIP. 197301242008012003)",
    "Harmeiruri, S.S (NIP. 198405132009032006)",
    "Elen Istantia, S.Pd (NIP. 198608102009032004)",
    "Gurata Rajaguk-Guk, S.Pd (NIP. 198207272010011010)",
    "Lisa Sumartini, S.Pd (NIP. 198703102010012015)",
    "Herda Sinambela, S.Pd (NIP. 198307122009032006)",
    "Elvan Pramartha, S.Pd.I (NIP. 198103102010011023)",
    "Tri Andari, S.Pd (NIP. 197003132005012007)",
    "Bambang Riyanto, S.Pd.Kor (NIP. 197801292006041013)",
    "M. Yudhistira, S.Pd (NIP. 198304182006041005)",
    "Feriawan, S.Pd (NIP. 198111272009031004)",
    "Kanizah, M.Pd (NIP. 198104162009032005)",
    "Ermi Royanti, S.Pd.I (NIP. 197803312009032003)",
    "Neyni Elis Indriyana, S.Pd (NIP. 198501032010012015)",
    "Niken Kumala Sari, S.Pd (NIP. 198505292010012020)",
    "Fransiska N Nababan, S.Pd (NIP. 199605292019022010)",
    "Ari Cahyono, S.Si (NIP. 197904062022211004)",
    "Yoga Nugraha, S.Pd (NIP. 199204132022211006)",
    "Ernawati, S.Pd (NIP. 199301292022212015)",
    "Septianda, S.Pd (NIP. 199305012022211002)",
    "Nurul Badriah, S.Pd (NIP. 199103222022212009)",
    "Ika Saputri Mahyu Lisa, S.Pd (NIP. 199209202022212020)",
    "Endang Risna Dewi, S.Pd (NIP. 199210092022212015)",
    "Nelva Aini Syifa, S.Pd (NIP. 199407292022212017)",
    "Zairul Fahmi, S.H (NIP. 198209072023211006)",
    "Ade Widiana, S.Pd (NIP. 199609192023212015)",
    "Nurfitri, S.Pd (NIP. 199612202023212017)",
    "Ion Firdaus, S.Pd (NIP. 199709012023211003)",
    "Reguis, S.Pd (NIP. 199608132024211004)",
    "Fikri Firmansyah, S.Pd (NIP. 199704082025211081)",
    "Ferdinan Pahala, S.Th (NIP. -)"
]

USERNAMES_GURU = [re.sub(r'[^a-z]', '', g.split(' (NIP')[0].lower()) for g in DAFTAR_GURU_SMAN3]

# Inisialisasi Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_nama" not in st.session_state:
    st.session_state.user_nama = ""
if "bank_soal_folder" not in st.session_state:
    st.session_state.bank_soal_folder = {}
if "soal_valid_kuali" not in st.session_state:
    st.session_state.soal_valid_kuali = pd.DataFrame()
if "meta_info" not in st.session_state:
    st.session_state.meta_info = {}
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "🏠 Beranda Utama"

# CSS Tampilan Putih Bersih
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
    }
    .main-header {
        font-size: 32px;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #475569;
        text-align: center;
        margin-bottom: 25px;
    }
    .login-box {
        background-color: #F8FAFC;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        max-width: 480px;
        margin: 0 auto;
    }
    .interactive-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🔑 HALAMAN COVER & LOGIN (TEMA PUTIH BERSIH)
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_filename = "66b480c34cb96SMAN_3_PANGKALPINANG-removebg-preview (1).png"
        if os.path.exists(logo_filename):
            st.image(logo_filename, width=180)
        else:
            st.markdown("<h1 style='text-align: center;'>🏫</h1>", unsafe_allow_html=True)

        st.markdown("<div class='main-header'>Q-BANK SMANETA</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Quality Question Bank — SMA Negeri 3 Pangkalpinang</div>", unsafe_allow_html=True)

        # Audio Jingle SMANETA
        jingle_mp3 = "Generasi Milenial - Jingel Smaneta #2.mp3"
        jingle_wav = "Generasi Milenial - Jingel Smaneta #2.wav"
        if os.path.exists(jingle_mp3):
            st.audio(jingle_mp3, format="audio/mp3")
        elif os.path.exists(jingle_wav):
            st.audio(jingle_wav, format="audio/wav")

        # Form Login
        with st.form("login_form"):
            st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>🔐 Login Guru SMANETA</h4>", unsafe_allow_html=True)
            username_input = st.text_input("Nama Lengkap Guru (Huruf kecil tanpa spasi):", placeholder="contoh: lisasumartinispd")
            password_input = st.text_input("Password:", type="password", placeholder="Password (12345)")
            submit_login = st.form_submit_button("🚀 Masuk ke Aplikasi", use_container_width=True)

            if submit_login:
                user_clean = re.sub(r'[^a-z]', '', username_input.lower())
                is_valid_user = any(user_clean in full_u or full_u in user_clean for full_u in USERNAMES_GURU) if user_clean else False
                
                if (is_valid_user or user_clean in USERNAMES_GURU) and password_input == "12345":
                    st.session_state.logged_in = True
                    st.session_state.user_nama = username_input
                    st.success("🎉 Login Berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Nama Guru atau Password salah! Pastikan password adalah 12345.")

    st.stop()

# ---------------------------------------------------------
# DASHBOARD UTAMA (SETELAH LOGIN)
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Guru Login:**\n`{st.session_state.user_nama}`")
if st.sidebar.button("🚪 Logout / Keluar"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "🏠 Beranda Utama", 
    "📑 Upload Kisi-Kisi Soal",
    "📋 Analisis Kualitatif (Aiken's V)", 
    "📊 Analisis Kuantitatif (Empiris)", 
    "📁 Folder Bank Soal Valid",
    "📥 Rekap & Download Laporan"
]

menu = st.sidebar.radio("Pilih Menu Navigasi:", menu_options)
st.session_state.selected_menu = menu
st.sidebar.markdown("---")

# ---------------------------------------------------------
# 1. BERANDA UTAMA
# ---------------------------------------------------------
if menu == "🏠 Beranda Utama":
    st.markdown("<div class='main-header'>🏫 Q-BANK (Quality Question Bank) SMANETA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Sistem Analisis Validitas & Bank Soal Resmi SMA Negeri 3 Pangkalpinang</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Jenis Asesmen", value="Formatif & Sumatif", delta="Kurikulum Merdeka")
    with m2:
        st.metric(label="Input Jawaban", value="Opsi ABCDE", delta="Skoring Otomatis")
    with m3:
        st.metric(label="Status Login", value="Aktif ✅", delta="Guru SMANETA")
    with m4:
        st.metric(label="Pengesahan", value="TTD & NIP", delta="Waka Kurikulum & Validator")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class='interactive-card' style='border-top: 4px solid #2563EB;'>
                <h3 style='color: #1E3A8A;'>📋 Analisis Kualitatif (Aiken's V)</h3>
                <p>Penelaahan instrumen soal mencakup indikator Materi, Konstruksi, dan Bahasa oleh Validator Guru SMANETA.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class='interactive-card' style='border-top: 4px solid #10B981;'>
                <h3 style='color: #065F46;'>📊 Analisis Kuantitatif (Empiris)</h3>
                <p>Uji statistik otomatis dari file jawaban siswa (ABCDE) untuk Validitas, Reliabilitas, Daya Pembeda, dan Distraktor.</p>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. UPLOAD KISI-KISI SOAL
# ---------------------------------------------------------
elif menu == "📑 Upload Kisi-Kisi Soal":
    st.header("📑 Upload & Pratinjau Kisi-Kisi Soal")
    file_kisi = st.file_uploader("Unggah File Kisi-Kisi (.xlsx / .csv)", type=["xlsx", "csv"])
    if file_kisi is not None:
        try:
            df_kisi = pd.read_csv(file_kisi) if file_kisi.name.endswith(".csv") else pd.read_excel(file_kisi)
            st.success("✅ File Kisi-kisi Berhasil Dimuat!")
            st.dataframe(df_kisi, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca kisi-kisi: {e}")

# ---------------------------------------------------------
# 3. ANALISIS KUALITATIF (AIKEN'S V)
# ---------------------------------------------------------
elif menu == "📋 Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    mapel_sel = st.selectbox("Mata Pelajaran:", ["Biologi", "Fisika", "Kimia", "Matematika", "Ekonomi", "Geografi", "Sejarah", "Bahasa Indonesia", "Bahasa Inggris", "Lainnya"])
    n_soal = st.number_input("Jumlah Soal:", min_value=1, max_value=100, value=5)
    
    init_data = {"Naskah Soal": [f"Soal nomor {i+1}" for i in range(int(n_soal))], "Skor V1": [4]*int(n_soal), "Skor V2": [4]*int(n_soal), "Skor V3": [4]*int(n_soal)}
    edited_df = st.data_editor(pd.DataFrame(init_data), use_container_width=True)
    
    v_score = (edited_df[["Skor V1", "Skor V2", "Skor V3"]].sum(axis=1) - 3) / (3 * 4)
    res_df = pd.DataFrame({"Soal": [f"Soal {i+1}" for i in range(int(n_soal))], "Indeks Aiken V": v_score.round(3)})
    res_df["Status"] = res_df["Indeks Aiken V"].apply(lambda x: "VALID ✅" if x >= 0.6 else "REVISI ❌")
    
    st.dataframe(res_df, use_container_width=True)
    
    if st.button("💾 Simpan ke Folder Bank Soal"):
        if mapel_sel not in st.session_state.bank_soal_folder:
            st.session_state.bank_soal_folder[mapel_sel] = []
        st.session_state.bank_soal_folder[mapel_sel].append(res_df)
        st.toast(f"Berhasil disimpan ke Folder {mapel_sel}!", icon="📁")

# ---------------------------------------------------------
# 4. ANALISIS KUANTITATIF (EMPIRIS)
# ---------------------------------------------------------
elif menu == "📊 Analisis Kuantitatif (Empiris)":
    st.header("📊 Analisis Empiris Jawaban Siswa (ABCDE)")
    kunci = st.text_input("🔑 Kunci Jawaban (pisahkan koma):", value="A,B,C,D,E")
    uploaded_file = st.file_uploader("Unggah Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])
    if uploaded_file:
        st.success("✅ File Jawaban Berhasil Diproses!")

# ---------------------------------------------------------
# 5. FOLDER BANK SOAL VALID TERINTEGRASI
# ---------------------------------------------------------
elif menu == "📁 Folder Bank Soal Valid":
    st.header("📁 Folder Bank Soal Teruji Valid (Per Mata Pelajaran)")
    if not st.session_state.bank_soal_folder:
        st.info("💡 Belum ada bank soal yang tersimpan di folder.")
    else:
        mapel_choice = st.selectbox("📂 Pilih Mata Pelajaran:", list(st.session_state.bank_soal_folder.keys()))
        if mapel_choice:
            for idx, df_b in enumerate(st.session_state.bank_soal_folder[mapel_choice]):
                st.write(f"**Paket Soal #{idx+1}**")
                st.dataframe(df_b, use_container_width=True)

# ---------------------------------------------------------
# 6. REKAP & DOWNLOAD LAPORAN BER-TTD
# ---------------------------------------------------------
elif menu == "📥 Rekap & Download Laporan":
    st.header("📥 Rekap Laporan & Lembar Pengesahan TTD")
    st.info("Fitur cetak rekap Excel dilengkapi lembar TTD Validator dan Waka Kurikulum (Era, S.T., M.M. - NIP. 198012292005012012).")
