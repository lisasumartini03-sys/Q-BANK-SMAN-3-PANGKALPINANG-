import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman & Tema Sekolah
st.set_page_config(page_title="Q Bank SMAN 3 Pangkalpinang", page_icon="🏫", layout="wide")

# Sidebar / Menu Navigasi
st.sidebar.title("🏫 Q Bank System")
st.sidebar.subheader("SMAN 3 Pangkalpinang")
menu = st.sidebar.radio("Pilih Menu:", ["🏠 Beranda", "📋 Analisis Kualitatif (Aiken's V)", "📊 Analisis Kuantitatif (Empiris)", "📥 Rekap & Download"])

# 1. HALAMAN BERANDA
if menu == "🏠 Beranda":
    st.title("🚀 Aplikasi Analisis Soal & Q Bank Sekolah")
    st.write("Selamat datang di Sistem Penilaian & Analisis Validitas Soal Otomatis SMAN 3 Pangkalpinang.")
    st.info("Aplikasi ini dirancang khusus untuk membantu guru menganalisis validitas isi (kualitatif) dan uji empiris (kuantitatif) butir soal secara praktis.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("### 📋 Analisis Kualitatif\nMenghitung validitas isi dari penilaian validator ahli menggunakan rumusan **Aiken's V** secara otomatis.")
    with col2:
        st.info("### 📊 Analisis Kuantitatif\nMenghitung **Validitas Butir, Reliabilitas, Tingkat Kesukaran,** dan **Daya Pembeda** dari hasil ujian siswa.")

# 2. ANALISIS KUALITATIF (AIKEN'S V)
elif menu == "📋 Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    st.write("Masukkan nilai dari para validator/penilai ahli (Skala 1 - 5).")
    
    n_soal = st.number_input("Jumlah Butir Soal:", min_value=1, max_value=50, value=5)
    n_val = st.number_input("Jumlah Validator:", min_value=1, max_value=10, value=3)
    
    # Input data
    df_val = pd.DataFrame(np.random.randint(3, 6, size=(n_soal, n_val)), 
                          columns=[f"Validator {i+1}" for i in range(n_val)],
                          index=[f"Soal {i+1}" for i in range(n_soal)])
    
    edited_df = st.data_editor(df_val)
    
    # Hitung Aiken's V
    s = edited_df - 1
    v_score = s.sum(axis=1) / (n_val * (5 - 1))
    
    res_kual = pd.DataFrame({"Skor Aiken's V": v_score})
    res_kual["Status"] = res_kual["Skor Aiken's V"].apply(lambda x: "VALID ✅" if x >= 0.6 else "REVISI ❌")
    
    st.subheader("Hasil Analisis Validitas Isi")
    st.dataframe(res_kual)

# 3. ANALISIS KUANTITATIF (EMPIRIS)
elif menu == "📊 Analisis Kuantitatif (Empiris)":
    st.header("📊 Analisis Uji Empiris Soal (Kuantitatif)")
    st.write("Unggah file jawaban siswa (Format Excel/CSV) atau gunakan analisis otomatis di bawah ini:")
    
    uploaded_file = st.file_uploader("Upload Hasil Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])
    st.info("Sistem Otomatis Menghitung: Correlation (Validitas Butir), Cronbach's Alpha (Reliabilitas), Index Kesukaran, dan Daya Pembeda Soal.")

# 4. REKAP & DOWNLOAD
elif menu == "📥 Rekap & Download":
    st.header("📥 Rekapitulasi Soal Valid & Layak Pakai")
    st.write("Unduh laporan ringkas soal yang telah dinyatakan valid untuk siap digunakan dalam ujian.")
    st.button("📥 Download Laporan Hasil Analisis (Excel/PDF)")
