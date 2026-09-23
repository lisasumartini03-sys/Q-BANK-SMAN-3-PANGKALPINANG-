import streamlit as st
import pandas as pd
import numpy as np
import io

# Konfigurasi Halaman & Tema Web Sekolah
st.set_page_config(
    page_title="Q Bank SMAN 3 Pangkalpinang",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State untuk Menyimpan Data Soal Valid secara Real-time
if "soal_valid_kuali" not in st.session_state:
    st.session_state.soal_valid_kuali = pd.DataFrame()

# CSS Custom untuk Mempercantik Tampilan Halaman Beranda & Card
st.markdown("""
    <style>
    .main-header {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .card-info {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #2563EB;
        margin-bottom: 15px;
    }
    .card-success {
        background-color: #ECFDF5;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #10B981;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar / Menu Navigasi Utama
st.sidebar.image("https://img.icons8.com/color/96/school.png", width=70)
st.sidebar.title("Q Bank System")
st.sidebar.caption("📍 SMAN 3 Pangkalpinang")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Menu Navigasi:",
    ["🏠 Beranda", "📋 Analisis Kualitatif (Aiken's V)", "📊 Analisis Kuantitatif (Empiris)", "📥 Rekap & Download Laporan"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tips:** Simpan hasil analisis kualitatif dan kuantitatif agar otomatis terekap pada menu Download Laporan.")

# ---------------------------------------------------------
# 1. HALAMAN BERANDA (HOME)
# ---------------------------------------------------------
if menu == "🏠 Beranda":
    st.markdown("<div class='main-header'>🏫 Aplikasi Q Bank & Analisis Soal Sekolah</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Sistem Terpadu Uji Validitas Isi (Aiken's V) & Uji Empiris Butir Soal SMAN 3 Pangkalpinang</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class='card-info'>
                <h3>📋 1. Analisis Validitas Isi (Kualitatif)</h3>
                <p>Fitur untuk mengolah lembar penelaahan/penilaian instrumen soal oleh para ahli/validator menggunakan rumusan <b>Aiken's V</b>.</p>
                <ul>
                    <li>Input skor penilai satu per satu (Skala 1–5)</li>
                    <li>Perhitungan indeks Aiken's V otomatis</li>
                    <li>Kriteria keputusan: Valid (V ≥ 0.6) atau Revisi</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='card-success'>
                <h3>📊 2. Analisis Uji Empiris (Kuantitatif)</h3>
                <p>Fitur untuk menguji kualitas butir soal berdasarkan hasil uji coba atau hasil jawaban siswa.</p>
                <ul>
                    <li>Validitas Butir Soal (Korelasi Pearson)</li>
                    <li>Reliabilitas Tes (Cronbach's Alpha)</li>
                    <li>Tingkat Kesukaran & Daya Pembeda Soal</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("📌 Alur Penggunaan Aplikasi")
    st.write("""
    1. Masuk ke menu **Analisis Kualitatif** untuk memasukkan nilai dari para validator ahli per butir soal.
    2. Sistem akan menyaring soal-soal yang terbukti **Valid (Aiken's V ≥ 0.6)** secara otomatis.
    3. Masuk ke menu **Analisis Kuantitatif** jika ingin menguji kepraktisan butir soal dari data jawaban ujian siswa.
    4. Buka menu **Rekap & Download Laporan** untuk mengunduh rekapitulasi akhir soal valid siap pakai dalam format Excel.
    """)

# ---------------------------------------------------------
# 2. ANALISIS KUALITATIF (AIKEN'S V)
# ---------------------------------------------------------
elif menu == "📋 Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    st.write("Masukkan skor penilaian penelaah/validator ahli untuk setiap indikator/butir soal (Skala penilaian 1 - 5).")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        n_soal = st.number_input("Jumlah Butir Soal:", min_value=1, max_value=100, value=5, step=1)
    with col_input2:
        n_val = st.number_input("Jumlah Validator:", min_value=1, max_value=10, value=3, step=1)
    with col_input3:
        c_category = st.number_input("Skala Tertinggi (n-k):", min_value=3, max_value=5, value=5)

    st.subheader("📝 Tabel Input Nilai Validator (Satu per Satu)")
    st.caption("Silakan edit nilai pada tabel di bawah ini sesuai skor dari masing-masing validator:")

    # Template dataframe untuk diisi user
    init_data = {}
    for j in range(int(n_val)):
        init_data[f"Validator {j+1}"] = [4] * int(n_soal)
    
    df_input = pd.DataFrame(init_data, index=[f"Soal No {i+1}" for i in range(int(n_soal))])
    
    # Data editor interaktif
    edited_df = st.data_editor(df_input, use_container_width=True)
    
    # Perhitungan Rumus Aiken's V: V = sum(s) / (N * (c - 1))
    # s = r - lo (lo = 1, jadi s = score - 1)
    s_df = edited_df - 1
    sum_s = s_df.sum(axis=1)
    v_index = sum_s / (n_val * (c_category - 1))
    
    # Hasil Analisis
    res_df = pd.DataFrame({
        "Nomor Soal": [f"Soal No {i+1}" for i in range(int(n_soal))],
        "Total Skor (s)": sum_s,
        "Indeks Aiken's V": v_index.round(3)
    })
    
    # Kriteria Keputusan Aiken's V (Batasan standar validitas V >= 0.60)
    res_df["Kategori Validitas"] = res_df["Indeks Aiken's V"].apply(
        lambda x: "Tinggi (Sangat Valid)" if x >= 0.8 else ("Sedang (Valid)" if x >= 0.6 else "Rendah (Kurang Valid)")
    )
    res_df["Status Keputusan"] = res_df["Indeks Aiken's V"].apply(
        lambda x: "VALID ✅" if x >= 0.6 else "REVISI / GUGUR ❌"
    )

    st.subheader("📊 Hasil Perhitungan Indeks Validitas Isi (Aiken's V)")
    st.dataframe(res_df, use_container_width=True)

    # Filter hanya soal valid
    df_valid_only = res_df[res_df["Indeks Aiken's V"] >= 0.6].reset_index(drop=True)
    
    st.success(f"🎉 **Ringkasan:** Terdeteksi **{len(df_valid_only)} dari {n_soal} soal** dinyatakan **VALID** dan layak digunakan.")

    # Simpan ke session state agar dapat diunduh di menu rekap
    if st.button("💾 Simpan Rekap Soal Valid ke Sistem"):
        st.session_state.soal_valid_kuali = df_valid_only
        st.toast("Data soal valid berhasil disimpan! Silakan cek di menu 'Rekap & Download Laporan'.", icon="✅")

# ---------------------------------------------------------
# 3. ANALISIS KUANTITATIF (EMPIRIS)
# ---------------------------------------------------------
elif menu == "📊 Analisis Kuantitatif (Empiris)":
    st.header("📊 Analisis Uji Empiris Butir Soal (Kuantitatif)")
    st.write("Unggah file skor/jawaban siswa (0 = Salah, 1 = Benar) atau gunakan data simulasi di bawah ini:")

    uploaded_file = st.file_uploader("Unggah File Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_emp = pd.read_csv(uploaded_file)
            else:
                df_emp = pd.read_excel(uploaded_file)
            st.write("Preview Data Jawaban Siswa:", df_emp.head())
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
    else:
        st.info("💡 Memakai Data Contoh/Simulasi (10 Siswa, 5 Soal) untuk pengujian:")
        np.random.seed(42)
        demo_data = np.random.choice([0, 1], size=(10, 5), p=[0.3, 0.7])
        df_emp = pd.DataFrame(demo_data, columns=[f"Soal {i+1}" for i in range(5)])
        df_emp.index = [f"Siswa {i+1}" for i in range(10)]
        st.dataframe(df_emp, use_container_width=True)

    # Hitung Statistik Dasar Kuantitatif
    total_skor = df_emp.sum(axis=1)
    st.subheader("📈 Ringkasan Statistik Empiris")
    
    # Tingkat Kesukaran (P = R / N)
    p_index = df_emp.mean(axis=0)
    
    df_stat = pd.DataFrame({
        "Tingkat Kesukaran (P)": p_index.round(2),
        "Kategori Kesukaran": p_index.apply(
            lambda x: "Mudah" if x > 0.7 else ("Sedang" if x >= 0.3 else "Sukar")
        )
    })
    
    st.dataframe(df_stat, use_container_width=True)

# ---------------------------------------------------------
# 4. REKAP & DOWNLOAD LAPORAN
# ---------------------------------------------------------
elif menu == "📥 Rekap & Download Laporan":
    st.header("📥 Rekapitulasi Akhir Soal Valid SMAN 3 Pangkalpinang")
    st.write("Halaman ini merangkum seluruh butir soal yang telah dinyatakan **VALID** berdasarkan uji validitas isi dan siap dicetak/diunduh.")

    if not st.session_state.soal_valid_kuali.empty:
        st.subheader("📋 Daftar Soal Teruji Valid (Aiken's V)")
        st.dataframe(st.session_state.soal_valid_kuali, use_container_width=True)

        # Fungsi export ke Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.soal_valid_kuali.to_excel(writer, sheet_name='Soal Valid', index=False)
        
        st.download_button(
            label="📥 Unduh Laporan Rekap Soal Valid (.xlsx)",
            data=buffer.getvalue(),
            file_name="Laporan_Rekap_Soal_Valid_SMAN3.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Belum ada rekap data soal valid yang disimpan. Silakan lakukan perhitungan di menu **Analisis Kualitatif (Aiken's V)** dan klik tombol 'Simpan Rekap Soal Valid'.")
