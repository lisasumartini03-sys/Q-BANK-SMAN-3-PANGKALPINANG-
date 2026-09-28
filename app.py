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
# 4. FUNGSI ANALISIS KUANTITATIF & KRITERIA
# ==========================================

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

# Sidebar - Logo & Navigasi
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=140)

st.sidebar.title("📌 Navigasi Aplikasi")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Halaman Sampul (Cover)", "📊 Analisis Soal (Kualitatif & Kuantitatif)"])

st.sidebar.markdown("---")
st.sidebar.header("🔐 Akses Guru")
username_input = st.sidebar.text_input("Username (nama kecil tanpa spasi):").strip().lower()

# ----------------------------------------------------
# HALAMAN 1: SAMPUL / COVER PAGE
# ----------------------------------------------------
if menu == "🏠 Halaman Sampul (Cover)":
    # Menampilkan Logo di Halaman Sampul (Tengah)
    if os.path.exists(LOGO_PATH):
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            st.image(LOGO_PATH, width=160)

    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Q-BANK SMAN 3 PANGKALPINANG</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4B5563;'>Sistem Bank Soal & Analisis Kualitas Butir Soal</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        ### 🏫 Informasi Sekolah
        * **Nama Sekolah:** SMAN 3 Pangkalpinang
        * **Modul Utama:** 
          1. **Uji Kualitatif** (Telaah Materi, Konstruksi, dan Bahasa)
          2. **Uji Kuantitatif** (Validitas, Reliabilitas, Tingkat Kesukaran, Daya Pembeda, & Efektivitas Pengecoh)
        * **Dukungan Mata Pelajaran:** 18 Mata Pelajaran (termasuk Prakarya, Bahasa Arab, & Bahasa Jepang)
        """)
        st.write("👈 *Silakan masukkan username di sidebar kiri untuk mulai menggunakan modul analisis.*")

# ----------------------------------------------------
# HALAMAN 2: ANALISIS SOAL (KUALITATIF & KUANTITATIF)
# ----------------------------------------------------
else:
    if username_input in USER_DATABASE:
        user_info = USER_DATABASE[username_input]
        st.sidebar.success(f"Selamat Datang, **{user_info['nama']}**")
        
        selected_mapel = st.sidebar.selectbox("Pilih Mata Pelajaran:", DAFTAR_MAPEL)
        
        st.title("📑 Modul Analisis Butir Soal")
        st.subheader(f"Mata Pelajaran: {selected_mapel}")
        
        # TAB UTAMA: KUALITATIF VS KUANTITATIF
        tab_kualitatif, tab_kuantitatif = st.tabs(["📝 UJI KUALITATIF SOAL", "📈 UJI KUANTITATIF SOAL"])
        
        # ----------------------------------------------------
        # FITUR: UJI KUALITATIF (TELAAH KAIDAH PENULISAN SOAL)
        # ----------------------------------------------------
        with tab_kualitatif:
            st.header("Telaah Kualitatif Butir Soal (Materi, Konstruksi, Bahasa)")
            st.caption("Penelaahan butir soal berdasarkan kaidah penulisan soal pilihan ganda.")
            
            soal_num = st.number_input("Nomor Soal yang Ditelaah:", min_value=1, max_value=100, value=1)
            
            st.subheader("Form Checklist Penelaahan Soal")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("#### A. Aspek Materi")
                m1 = st.checkbox("1. Soal sesuai dengan indikator")
                m2 = st.checkbox("2. Pilihan jawaban homogen & logis")
                m3 = st.checkbox("3. Ada satu kunci jawaban yang tepat")
                
            with col_b:
                st.markdown("#### B. Aspek Konstruksi")
                k1 = st.checkbox("1. Pokok soal dirumuskan tegas & jelas")
                k2 = st.checkbox("2. Pokok soal tidak memberi petunjuk kunci")
                k3 = st.checkbox("3. Tidak menggunakan pernyataan negatif ganda")
                k4 = st.checkbox("4. Panjang opsi jawaban relatif sama")
                
            with col_c:
                st.markdown("#### C. Aspek Bahasa")
                b1 = st.checkbox("1. Menggunakan bahasa baku (PUEBI)")
                b2 = st.checkbox("2. Komunikatif & mudah dipahami")
                b3 = st.checkbox("3. Tidak menggunakan bahasa lokal/tabu")
            
            catatan = st.text_area("Catatan / Rekomendasi Perbaikan Soal:")
            tot_skor = sum([m1, m2, m3, k1, k2, k3, k4, b1, b2, b3])
            
            if tot_skor == 10:
                st.success(f"**Hasil Telaah Soal No. {soal_num}: Diterima (Sangat Baik)** ({tot_skor}/10 Kriteria Terpenuhi)")
            elif tot_skor >= 7:
                st.warning(f"**Hasil Telaah Soal No. {soal_num}: Revisi (Perlu Perbaikan Kecil)** ({tot_skor}/10 Kriteria Terpenuhi)")
            else:
                st.error(f"**Hasil Telaah Soal No. {soal_num}: Ditolak / Dibuang** ({tot_skor}/10 Kriteria Terpenuhi)")

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
            
            # Simulasi Data Respon Siswa (Dummy)
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
