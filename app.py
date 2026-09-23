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

# Inisialisasi Session State untuk Menyimpan Data Soal Valid & Metadata
if "soal_valid_kuali" not in st.session_state:
    st.session_state.soal_valid_kuali = pd.DataFrame()
if "meta_info" not in st.session_state:
    st.session_state.meta_info = {}

# CSS Custom Tampilan
st.markdown("""
    <style>
    .main-header {
        font-size: 30px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 20px;
    }
    .card-info {
        background-color: #F3F4F6;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #2563EB;
        margin-bottom: 15px;
    }
    .card-success {
        background-color: #ECFDF5;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #10B981;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigasi
st.sidebar.markdown("# 🏫")
st.sidebar.title("Q Bank System")
st.sidebar.caption("📍 SMAN 3 Pangkalpinang")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Menu Navigasi:",
    ["🏠 Beranda", "📋 Analisis Kualitatif (Aiken's V)", "📊 Analisis Kuantitatif (Empiris)", "📥 Rekap & Download Laporan"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Multi-Guru & Multi-Mapel:** Dapat digunakan oleh seluruh Guru Mata Pelajaran di SMAN 3 Pangkalpinang.")

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
                <p>Fitur penelaahan instrumen soal dengan metadata lengkap untuk semua guru.</p>
                <ul>
                    <li>Input Kelompok Mapel, Fase/Kelas, & Kode Soal</li>
                    <li>Input Indikator, Level Kognitif, & Teks Soal</li>
                    <li>Input Nama Validator & Skor Nilai (1–5)</li>
                    <li>Kalkulasi Otomatis Indeks Aiken's V</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='card-success'>
                <h3>📊 2. Analisis Uji Empiris (Kuantitatif)</h3>
                <p>Fitur pengujian kualitas butir soal berdasarkan data hasil ujian siswa.</p>
                <ul>
                    <li>Validitas Butir Soal (Korelasi Pearson)</li>
                    <li>Reliabilitas Tes (Cronbach's Alpha)</li>
                    <li>Tingkat Kesukaran & Daya Pembeda Soal</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("📌 Alur Penggunaan Aplikasi untuk Guru")
    st.write("""
    1. Buka menu **Analisis Kualitatif**, pilih Kelompok Mapel, Fase/Kelas, dan isi nama Validator.
    2. Ketik Indikator, Level Kognitif, Teks Soal, dan berikan nilai dari para validator (Skala 1–5).
    3. Klik **Simpan Rekap Soal Valid ke Sistem**.
    4. Masuk ke menu **Rekap & Download Laporan** untuk mengunduh rekapitulasi Excel lengkap.
    """)

# ---------------------------------------------------------
# 2. ANALISIS KUALITATIF (AIKEN'S V)
# ---------------------------------------------------------
elif menu == "📋 Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    st.write("Silakan lengkapi identitas kelompok mata pelajaran, fase/kelas, validator, dan detail butir soal.")
    
    # --- SECTION A: IDENTITAS MATA PELAJARAN & KELAS ---
    with st.expander("📌 **A. Identitas Mata Pelajaran & Kelas**", expanded=True):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            kelompok_mapel = st.selectbox(
                "Kelompok / Rumpun Mapel:",
                ["MIPA (IPA)", "IPS / Sosial", "Bahasa", "Pancasila & Agama", "Seni & PJOK", "Informatika / Lintas Minat"]
            )
            nama_mapel = st.text_input("Nama Mata Pelajaran:", value="Biologi")
        with col_m2:
            fase_kelas = st.selectbox("Fase / Kelas:", ["Fase E - Kelas 10", "Fase F - Kelas 11", "Fase F - Kelas 12"])
            penyusun = st.text_input("Nama Guru Penyusun Soal:", value="Guru SMAN 3, S.Pd.")
        with col_m3:
            kode_soal = st.text_input("Kode / Paket Soal:", value="PAS-BIO-01")
            tahun_ajaran = st.text_input("Tahun Ajaran & Semester:", value="2024/2025 - Ganjil")

    # --- SECTION B: PARAMETER & NAMA VALIDATOR ---
    with st.expander("👤 **B. Parameter & Nama Validator Ahli**", expanded=True):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            n_soal = st.number_input("Jumlah Butir Soal:", min_value=1, max_value=100, value=5, step=1)
        with col_p2:
            n_val = st.number_input("Jumlah Validator:", min_value=1, max_value=10, value=3, step=1)
        with col_p3:
            c_category = st.number_input("Skala Tertinggi Penilaian:", min_value=3, max_value=5, value=5)

        st.caption("Masukkan Nama Guru Penelaah / Validator Ahli:")
        val_names = []
        cols_val = st.columns(int(n_val))
        for idx, col in enumerate(cols_val):
            with col:
                v_name = st.text_input(f"Nama Validator {idx+1}:", value=f"Validator {idx+1}")
                val_names.append(v_name)

    # --- SECTION C: TABEL INPUT DETIL SOAL & SKOR VALIDATOR ---
    st.subheader("📝 Tabel Input Detail Soal & Nilai Validator")
    st.caption("Ketik Indikator, pilih Level Kognitif, masukkan Teks Soal, dan beri Nilai dari Validator (Skala 1-5):")

    init_data = {
        "Mata Pelajaran": [nama_mapel for _ in range(int(n_soal))],
        "Fase/Kelas": [fase_kelas for _ in range(int(n_soal))],
        "Indikator Soal": [f"Indikator pembelajaran soal nomor {i+1}" for i in range(int(n_soal))],
        "Level Kognitif": ["C3 (Aplikasi)" for _ in range(int(n_soal))],
        "Teks Soal": [f"Ketik/tempel naskah soal nomor {i+1} di sini..." for i in range(int(n_soal))]
    }
    
    for v_name in val_names:
        init_data[v_name] = [4] * int(n_soal)
    
    df_input = pd.DataFrame(init_data, index=[f"Soal No {i+1}" for i in range(int(n_soal))])
    
    edited_df = st.data_editor(
        df_input,
        column_config={
            "Level Kognitif": st.column_config.SelectboxColumn(
                "Level Kognitif",
                options=["C1 (Mengingat)", "C2 (Memahami)", "C3 (Aplikasi)", "C4 (Analisis)", "C5 (Evaluasi)", "C6 (Mencipta)"],
                required=True
            )
        },
        use_container_width=True
    )
    
    # Hitung Aiken's V
    scores_df = edited_df[val_names]
    s_df = scores_df - 1
    sum_s = s_df.sum(axis=1)
    v_index = sum_s / (n_val * (c_category - 1))
    
    res_df = pd.DataFrame({
        "Nomor Soal": [f"Soal No {i+1}" for i in range(int(n_soal))],
        "Kelompok Mapel": kelompok_mapel,
        "Mata Pelajaran": edited_df["Mata Pelajaran"],
        "Fase/Kelas": edited_df["Fase/Kelas"],
        "Indikator Soal": edited_df["Indikator Soal"],
        "Level Kognitif": edited_df["Level Kognitif"],
        "Naskah Soal": edited_df["Teks Soal"],
        "Total Skor (s)": sum_s,
        "Indeks Aiken's V": v_index.round(3)
    })
    
    res_df["Kategori Validitas"] = res_df["Indeks Aiken's V"].apply(
        lambda x: "Tinggi (Sangat Valid)" if x >= 0.8 else ("Sedang (Valid)" if x >= 0.6 else "Rendah (Kurang Valid)")
    )
    res_df["Status Keputusan"] = res_df["Indeks Aiken's V"].apply(
        lambda x: "VALID ✅" if x >= 0.6 else "REVISI / GUGUR ❌"
    )

    st.subheader("📊 Hasil Perhitungan Indeks Validitas Isi (Aiken's V)")
    st.dataframe(res_df, use_container_width=True)

    df_valid_only = res_df[res_df["Indeks Aiken's V"] >= 0.6].reset_index(drop=True)
    
    st.success(f"🎉 **Ringkasan:** Terdeteksi **{len(df_valid_only)} dari {n_soal} soal** dinyatakan **VALID** dan layak digunakan.")

    if st.button("💾 Simpan Rekap Soal Valid ke Sistem"):
        st.session_state.soal_valid_kuali = df_valid_only
        st.session_state.meta_info = {
            "Kelompok": kelompok_mapel,
            "Mapel": nama_mapel,
            "Kode Soal": kode_soal,
            "Fase/Kelas": fase_kelas,
            "Penyusun": penyusun,
            "Tahun/Semester": tahun_ajaran,
            "Validator": ", ".join(val_names)
        }
        st.toast("Data soal valid beserta metadata lengkap berhasil disimpan!", icon="✅")

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

    st.subheader("📈 Ringkasan Statistik Empiris")
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
    st.write("Halaman ini merangkum seluruh butir soal teruji **VALID** beserta metadata lengkapnya.")

    if not st.session_state.soal_valid_kuali.empty:
        meta = st.session_state.meta_info
        st.markdown(f"""
        **Identitas Dokumen Laporan:**
        * **Rumpun / Kelompok Mapel:** {meta.get('Kelompok', '-')} | **Mata Pelajaran:** {meta.get('Mapel', '-')}
        * **Fase / Kelas:** {meta.get('Fase/Kelas', '-')} | **Kode Soal:** {meta.get('Kode Soal', '-')}
        * **Guru Penyusun:** {meta.get('Penyusun', '-')} | **Tahun/Semester:** {meta.get('Tahun/Semester', '-')}
        * **Validator Ahli:** {meta.get('Validator', '-')}
        """)
        st.markdown("---")

        st.subheader("📋 Tabel Rekap Soal Valid Siap Pakai")
        st.dataframe(st.session_state.soal_valid_kuali, use_container_width=True)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.soal_valid_kuali.to_excel(writer, sheet_name='Soal Valid', index=False)
        
        st.download_button(
            label="📥 Unduh Laporan Rekap Soal Valid (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"Laporan_Soal_Valid_{meta.get('Mapel','SMAN3')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Belum ada rekap data soal valid yang disimpan. Silakan lakukan perhitungan di menu **Analisis Kualitatif (Aiken's V)** dan klik tombol 'Simpan Rekap Soal Valid'.")
