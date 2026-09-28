import pandas as pd
import numpy as np
import streamlit as st

# ==========================================
# 1. DATABASE USER (NAMA GURU SAJA - TANPA GELAR & TANPA TU)
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
# 2. DAFTAR MATA PELAJARAN LENGKAP
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
# 3. FUNGSI ANALISIS KUANTITATIF & KRITERIA
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
    # df_jawaban berisi skor 1 dan 0
    n = df_jawaban.shape[1] # Jumlah soal
    N = df_jawaban.shape[0] # Jumlah siswa
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
    # Mengecek persentase pemilih tiap opsi A, B, C, D, E
    # Kriteria Pengecoh Baik jika dipilih minimal 5% peserta
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
# 4. TAMPILAN APLIKASI STREAMLIT
# ==========================================

st.set_page_config(page_title="Q-BANK SMAN 3 PANGKALPINANG", layout="wide")

st.title("🏦 Q-BANK SMAN 3 PANGKALPINANG")
st.subheader("Modul Analisis Kuantitatif Soal")

# Sidebar - Login & Pilihan Mapel
st.sidebar.header("Pilih Akses & Mata Pelajaran")

username_input = st.sidebar.text_input("Username (nama kecil tanpa spasi):").strip().lower()

if username_input in USER_DATABASE:
    user_info = USER_DATABASE[username_input]
    st.sidebar.success(f"Selamat Datang, {user_info['nama']} ({user_info['role']})")
    
    selected_mapel = st.sidebar.selectbox("Pilih Mata Pelajaran:", DAFTAR_MAPEL)
    
    st.markdown(f"### Mapel Terpilih: **{selected_mapel}**")
    
    # Tab Fitur Uji Kuantitatif
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Uji Validitas Butir", 
        "2. Uji Reliabilitas", 
        "3. Tingkat Kesukaran", 
        "4. Daya Pembeda", 
        "5. Efektivitas Pengecoh"
    ])
    
    # --- Contoh Simulasi Input Data Respon Soal (0 dan 1) ---
    st.info("Unggah / Masukkan Data Hasil Ujian Siswa (Format Biner 0 dan 1 untuk Soal Pilihan Ganda)")
    
    # Data Sampel Dummy
    np.random.seed(42)
    sample_data = np.random.choice([0, 1], size=(20, 10), p=[0.3, 0.7])
    df_skor = pd.DataFrame(sample_data, columns=[f"Soal_{i+1}" for i in range(10)])
    
    with tab1:
        st.header("Uji Validitas Butir Soal")
        r_tabel = st.number_input("Nilai r-tabel rujukan:", value=0.30, step=0.01)
        
        # Hitung korelasi biserial sederhana (Point Biserial)
        total_skor = df_skor.sum(axis=1)
        validitas_res = []
        for col in df_skor.columns:
            r_hitung = np.corrcoef(df_skor[col], total_skor)[0, 1]
            kriteria = get_kriteria_validitas(r_hitung, r_tabel)
            validitas_res.append({"Butir Soal": col, "r-Hitung": round(r_hitung, 3), "Kriteria": kriteria})
            
        st.dataframe(pd.DataFrame(validitas_res), use_container_width=True)

    with tab2:
        st.header("Uji Reliabilitas (KR-20)")
        r_11, kriteria_rel = hitung_reliabilitas_kr20(df_skor)
        st.metric("Koefisien Reliabilitas (r_11)", round(r_11, 3))
        st.write(f"**Kriteria Reliabilitas:** {kriteria_rel}")

    with tab3:
        st.header("Uji Tingkat Kesukaran")
        kesukaran_res = []
        p_values = df_skor.mean(axis=0)
        for col, p in p_values.items():
            kesukaran_res.append({
                "Butir Soal": col, 
                "Indeks Kesukaran (p)": round(p, 3), 
                "Kriteria": get_kriteria_kesukaran(p)
            })
        st.dataframe(pd.DataFrame(kesukaran_res), use_container_width=True)

    with tab4:
        st.header("Uji Daya Pembeda")
        # Menggunakan Metode Kelompok Atas & Kelompok Bawah (27%)
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

    with tab5:
        st.header("Uji Efektivitas Pengecoh (Distraktor)")
        st.caption("Pengecoh dinyatakan **Efektif** jika dipilih sekurang-kurangnya oleh 5% peserta ujian.")
        
        # Dummy Pilihan Jawaban Siswa (A, B, C, D, E)
        pilihan = ['A', 'B', 'C', 'D', 'E']
        df_pilihan = pd.DataFrame(
            np.random.choice(pilihan, size=(20, 5)), 
            columns=[f"Soal_{i+1}" for i in range(5)]
        )
        kunci_dummy = {"Soal_1": "A", "Soal_2": "B", "Soal_3": "C", "Soal_4": "D", "Soal_5": "E"}
        
        df_distraktor = analisis_efektivitas_pengecoh(df_pilihan, kunci_dummy)
        st.dataframe(df_distraktor, use_container_width=True)

elif username_input:
    st.sidebar.error("Username tidak ditemukan! Pastikan menggunakan nama saja huruf kecil tanpa spasi dan tanpa gelar.")
else:
    st.info("Silakan masukkan Username pada sidebar untuk mengakses aplikasi.")
