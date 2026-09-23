import streamlit as st
import pandas as pd
import numpy as np
import io

# Konfigurasi Halaman & Tema Web Sekolah
st.set_page_config(
    page_title="Q-BANK SMAN 3 Pangkalpinang",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL Logo Resmi SMAN 3 Pangkalpinang (SMANETA)
URL_LOGO_SMANETA = "https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_SMA_Negeri_3_Pangkalpinang.png"

# Inisialisasi Session State
if "soal_valid_kuali" not in st.session_state:
    st.session_state.soal_valid_kuali = pd.DataFrame()
if "meta_info" not in st.session_state:
    st.session_state.meta_info = {}
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "🏠 Beranda"

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
    "Ferdinan Pahala, S.Th (NIP. -)",
    "Lainnya (Ketik Manual)"
]

# CSS Custom Tampilan
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 15px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 20px;
    }
    .interactive-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    .interactive-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.12);
        border-color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigasi dengan Logo SMANETA
st.sidebar.image(URL_LOGO_SMANETA, width=110)
st.sidebar.title("Q-BANK SMANETA")
st.sidebar.caption("📍 SMA Negeri 3 Pangkalpinang")
st.sidebar.markdown("---")

menu_options = [
    "🏠 Beranda", 
    "📋 Analisis Kualitatif (Aiken's V)", 
    "📊 Analisis Kuantitatif (Empiris)", 
    "📥 Rekap & Download Laporan"
]

menu = st.sidebar.radio(
    "Pilih Menu Navigasi:",
    menu_options,
    index=menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0
)

st.session_state.selected_menu = menu
st.sidebar.markdown("---")
st.sidebar.info("💡 **Aplikasi Resmi SMAN 3 Pangkalpinang:** Q-BANK (Quality Question Bank) terintegrasi uji Kualitatif & Kuantitatif.")

# ---------------------------------------------------------
# 1. HALAMAN BERANDA
# ---------------------------------------------------------
if menu == "🏠 Beranda":
    col_logo1, col_head, col_logo2 = st.columns([1, 4, 1])
    with col_logo1:
        st.image(URL_LOGO_SMANETA, width=120)
    with col_head:
        st.markdown("<div class='main-header'>🏫 Q-BANK (Quality Question Bank)</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-top: -10px;'>SMA Negeri 3 Pangkalpinang</h3>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Sistem Penjaminan Mutu Soal: Uji Kualitatif (Aiken's V) & Uji Empiris Kuantitatif Komprehensif</div>", unsafe_allow_html=True)
    with col_logo2:
        st.image(URL_LOGO_SMANETA, width=120)

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Jenis Asesmen", value="Formatif & Sumatif", delta="Kurikulum Merdeka")
    with m2:
        st.metric(label="Import Jawaban", value="Opsi ABCDE", delta="Skoring Otomatis")
    with m3:
        st.metric(label="Analisis Empiris", value="5 Indikator", delta="Pearson, K-R20, Distraktor")
    with m4:
        st.metric(label="Lembar Pengesahan", value="TTD & NIP Resmi", delta="Waka Kurikulum & Validator")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class='interactive-card' style='border-top: 5px solid #2563EB;'>
                <h3 style='color: #1E3A8A;'>📋 Analisis Kualitatif (Aiken's V)</h3>
                <p>Penelaahan instrumen soal mencakup indikator Materi, Konstruksi, dan Bahasa oleh Validator Guru SMAN 3 Pangkalpinang.</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Buka Analisis Kualitatif", use_container_width=True):
            st.session_state.selected_menu = "📋 Analisis Kualitatif (Aiken's V)"
            st.rerun()

    with c2:
        st.markdown("""
            <div class='interactive-card' style='border-top: 5px solid #10B981;'>
                <h3 style='color: #065F46;'>📊 Analisis Kuantitatif (Empiris)</h3>
                <p>Uji statistik otomatis dari file mentah jawaban siswa (ABCDE) untuk menghitung Validitas Butir, Reliabilitas, Kesukaran, Daya Pembeda, dan Pengecoh.</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📈 Buka Analisis Kuantitatif", use_container_width=True):
            st.session_state.selected_menu = "📊 Analisis Kuantitatif (Empiris)"
            st.rerun()

# ---------------------------------------------------------
# 2. ANALISIS KUALITATIF (AIKEN'S V)
# ---------------------------------------------------------
elif menu == "📋 Analisis Kualitatif (Aiken's V)":
    st.header("📋 Analisis Validitas Isi (Aiken's V)")
    st.write("Penelaahan instrumen butir soal berdasarkan 3 aspek: **Materi, Konstruksi, dan Bahasa**.")
    
    with st.expander("📌 **A. Identitas Mata Pelajaran & Jenis Asesmen**", expanded=True):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            jenis_asesmen = st.selectbox(
                "Jenis / Kelompok Soal:",
                [
                    "Asesmen Formatif (Ulangan Harian / Kuis)",
                    "Asesmen Sumatif Lingkup Materi (Bab/TP)",
                    "Asesmen Sumatif Akhir Semester (SAS / PAS)",
                    "Asesmen Sumatif Akhir Tahun (SAT / PAT)",
                    "Uji Coba / Try Out Ujian Sekolah"
                ]
            )
            kelompok_mapel = st.selectbox("Kelompok Mapel:", ["MIPA (IPA)", "IPS / Sosial", "Bahasa", "Pancasila & Agama", "Seni & PJOK", "Informatika / PKWU"])
            daftar_mapel = ["Biologi", "Fisika", "Kimia", "Matematika", "Ekonomi", "Geografi", "Sosiologi", "Sejarah", "Bahasa Indonesia", "Bahasa Inggris", "Pendidikan Pancasila", "PAI", "PJOK", "Informatika", "PKWU", "Lainnya"]
            mapel_sel = st.selectbox("Mata Pelajaran:", daftar_mapel)
            nama_mapel = st.text_input("Mapel (Lainnya):", value="") if mapel_sel == "Lainnya" else mapel_sel
        with col_m2:
            fase_kelas = st.selectbox("Fase / Kelas:", ["Fase E - Kelas 10", "Fase F - Kelas 11", "Fase F - Kelas 12"])
            penyusun_sel = st.selectbox("Guru Penyusun Soal:", DAFTAR_GURU_SMAN3, index=20)
            penyusun = st.text_input("Nama Penyusun (Ketik):", value="") if "Lainnya" in penyusun_sel else penyusun_sel
        with col_m3:
            kode_soal = st.text_input("Kode Soal:", value="PAS-BIO-01")
            tahun_ajaran = st.text_input("TA & Semester:", value="2026/2027 - Ganjil")

    with st.expander("👤 **B. Identitas Validator Ahli (Guru SMAN 3) & Parameter**", expanded=True):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            n_soal = st.number_input("Jumlah Butir Soal:", min_value=1, max_value=100, value=5, step=1)
        with col_p2:
            n_val = st.number_input("Jumlah Validator:", min_value=1, max_value=3, value=3, step=1)
        with col_p3:
            c_category = 5

        val_list = []
        val_nip_list = []
        st.caption("Pilih Nama Guru SMAN 3 Pangkalpinang sebagai Validator:")
        cols_v = st.columns(int(n_val))
        
        default_idx = [0, 1, 2]
        for idx, col in enumerate(cols_v):
            with col:
                v_sel = st.selectbox(f"Validator {idx+1}:", DAFTAR_GURU_SMAN3, index=default_idx[idx % len(default_idx)])
                if "Lainnya" in v_sel:
                    v_nama = st.text_input(f"Nama Val {idx+1}:", value=f"Validator {idx+1}")
                    v_nip = st.text_input(f"NIP Val {idx+1}:", value="-")
                else:
                    v_nama = v_sel.split(" (NIP.")[0].strip()
                    v_nip = "NIP. " + v_sel.split(" (NIP. ")[1].replace(")", "").strip() if "(NIP." in v_sel else "-"
                val_list.append(v_nama)
                val_nip_list.append(v_nip)

    st.subheader("📝 Tabel Penelaahan Indikator (Materi, Konstruksi, Bahasa)")
    st.caption("Isikan skor (1-5) untuk Aspek Materi (M), Konstruksi (K), dan Bahasa (B) dari masing-masing validator:")

    init_data = {
        "Indikator Soal": [f"Indikator pembelajaran no {i+1}" for i in range(int(n_soal))],
        "Level Kognitif": ["C3 (Aplikasi)" for _ in range(int(n_soal))],
        "Teks Naskah Soal": [f"Ketik naskah soal nomor {i+1}..." for i in range(int(n_soal))]
    }
    
    score_cols = []
    for idx, v_name in enumerate(val_list):
        for asp in ["Materi", "Konstruksi", "Bahasa"]:
            col_id = f"V{idx+1}_{asp}"
            init_data[col_id] = [4] * int(n_soal)
            score_cols.append(col_id)

    df_input = pd.DataFrame(init_data, index=[f"Soal No {i+1}" for i in range(int(n_soal))])
    edited_df = st.data_editor(
        df_input,
        column_config={
            "Level Kognitif": st.column_config.SelectboxColumn("Level Kognitif", options=["C1 (Mengingat)", "C2 (Memahami)", "C3 (Aplikasi)", "C4 (Analisis)", "C5 (Evaluasi)", "C6 (Mencipta)"], required=True)
        },
        use_container_width=True
    )

    scores_only = edited_df[score_cols] - 1
    v_all = scores_only.sum(axis=1) / (len(score_cols) * (c_category - 1))
    
    res_df = pd.DataFrame({
        "Nomor Soal": [f"Soal No {i+1}" for i in range(int(n_soal))],
        "Jenis Soal": jenis_asesmen,
        "Mata Pelajaran": nama_mapel,
        "Indikator Soal": edited_df["Indikator Soal"],
        "Level Kognitif": edited_df["Level Kognitif"],
        "Naskah Soal": edited_df["Teks Naskah Soal"],
        "Rata Indeks Aiken V": v_all.round(3)
    })
    
    res_df["Kategori"] = res_df["Rata Indeks Aiken V"].apply(lambda x: "Tinggi (Sangat Valid)" if x >= 0.8 else ("Sedang (Valid)" if x >= 0.6 else "Rendah (Gugur)"))
    res_df["Status Keputusan"] = res_df["Rata Indeks Aiken V"].apply(lambda x: "VALID ✅" if x >= 0.6 else "REVISI / GUGUR ❌")

    st.subheader("📊 Hasil Indeks Validitas Aiken's V")
    st.dataframe(res_df, use_container_width=True)

    df_valid_only = res_df[res_df["Rata Indeks Aiken V"] >= 0.6].reset_index(drop=True)
    st.success(f"🎉 Terdeteksi **{len(df_valid_only)} dari {n_soal} soal** dinyatakan **VALID**.")

    if st.button("💾 Simpan Rekap Soal Valid ke Sistem"):
        st.session_state.soal_valid_kuali = df_valid_only
        st.session_state.meta_info = {
            "JenisSoal": jenis_asesmen,
            "Kelompok": kelompok_mapel,
            "Mapel": nama_mapel,
            "Kode Soal": kode_soal,
            "Fase/Kelas": fase_kelas,
            "Penyusun": penyusun,
            "Tahun/Semester": tahun_ajaran,
            "Validators": val_list,
            "ValidatorNIPs": val_nip_list
        }
        st.toast("Data Rekap Validitas Kualitatif Berhasil Disimpan!", icon="✅")

# ---------------------------------------------------------
# 3. ANALISIS KUANTITATIF (EMPIRIS)
# ---------------------------------------------------------
elif menu == "📊 Analisis Kuantitatif (Empiris)":
    st.header("📊 Analisis Uji Empiris Kuantitatif Soal")
    st.write("Unggah data jawaban mentah siswa berupa opsi **A, B, C, D, E** dan masukkan kunci jawaban.")

    col_k1, col_k2 = st.columns([2, 1])
    with col_k1:
        kunci_str = st.text_input("🔑 Kunci Jawaban (Pisahkan dengan koma / titik koma):", value="A, B, C, D, E")
    with col_k2:
        r_tabel_val = st.number_input("Nilai r-Tabel (N=30, alpha=5%):", value=0.361, step=0.001)

    kunci_raw = kunci_str.replace(";", ",").split(",")
    kunci_list = [x.strip().upper() for x in kunci_raw if x.strip()]

    uploaded_file = st.file_uploader("Unggah File Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])

    if uploaded_file is not None:
        df_raw = None
        if uploaded_file.name.endswith(".csv"):
            try:
                df_raw = pd.read_csv(uploaded_file, header=None)
            except Exception:
                uploaded_file.seek(0)
                df_raw = pd.read_csv(uploaded_file, sep=';', header=None)
        else:
            excel_engines = [None, 'openpyxl', 'calamine', 'xlrd']
            for engine in excel_engines:
                try:
                    uploaded_file.seek(0)
                    df_raw = pd.read_excel(uploaded_file, header=None, engine=engine) if engine else pd.read_excel(uploaded_file, header=None)
                    if df_raw is not None:
                        break
                except Exception:
                    continue

        if df_raw is not None:
            if len(df_raw.columns) == 1:
                df_split = df_raw[0].astype(str).str.replace(';', ',').str.split(',', expand=True)
                df_raw = df_split

            first_val = str(df_raw.iloc[0, 0]).strip().lower()
            if any(k in first_val for k in ["nama", "siswa", "nis", "no", "soal"]):
                df_raw = df_raw.iloc[1:].reset_index(drop=True)

            sample_val = str(df_raw.iloc[0, 0]).strip()
            if len(sample_val) > 2 and not sample_val.upper() in ["A", "B", "C", "D", "E"]:
                df_jawaban = df_raw.iloc[:, 1:].reset_index(drop=True)
            else:
                df_jawaban = df_raw.reset_index(drop=True)

            n_soal_emp = df_jawaban.shape[1]
            df_jawaban.columns = [f"Soal_{i+1}" for i in range(n_soal_emp)]

            try:
                st.write("Preview Jawaban Mentah Siswa (Sudah Dibersihkan):", df_jawaban.head())

                df_scores = pd.DataFrame()
                for idx, col in enumerate(df_jawaban.columns):
                    kunci = kunci_list[idx] if idx < len(kunci_list) else (kunci_list[0] if len(kunci_list) > 0 else "A")
                    jawaban_siswa = df_jawaban[col].astype(str).str.strip().str.upper()
                    df_scores[f"Soal_{idx+1}"] = (jawaban_siswa == kunci).astype(int)

                n_siswa = len(df_scores)
                total_skor = df_scores.sum(axis=1)

                st.subheader(f"📈 Hasil Analisis Empiris ({n_soal_emp} Butir Soal Terdeteksi)")

                p_index = df_scores.mean(axis=0)

                r_hit = []
                for col in df_scores.columns:
                    corr = np.corrcoef(df_scores[col], total_skor)[0, 1]
                    r_hit.append(corr if not np.isnan(corr) else 0)

                df_temp = df_scores.copy()
                df_temp["Total"] = total_skor
                df_sorted = df_temp.sort_values(by="Total", ascending=False)
                n_group = max(1, int(n_siswa * 0.27))
                
                top_group = df_sorted.iloc[:n_group, :-1]
                bottom_group = df_sorted.iloc[-n_group:, :-1]
                dp_index = top_group.mean(axis=0) - bottom_group.mean(axis=0)

                res_emp = pd.DataFrame({
                    "Butir Soal": [f"Soal {i+1}" for i in range(n_soal_emp)],
                    "Kunci": [kunci_list[i] if i < len(kunci_list) else (kunci_list[0] if len(kunci_list) > 0 else "A") for i in range(n_soal_emp)],
                    "Tingkat Kesukaran (P)": p_index.values.round(2),
                    "Kategori Kesukaran": ["Mudah" if p > 0.7 else ("Sedang" if p >= 0.3 else "Sukar") for p in p_index],
                    "Daya Pembeda (DP)": dp_index.values.round(2),
                    "Kategori DP": ["Sangat Baik" if d >= 0.4 else ("Baik" if d >= 0.3 else ("Cukup" if d >= 0.2 else "Jelek / Buruk")) for d in dp_index],
                    "r-Hitung": np.round(r_hit, 3),
                    "r-Tabel": r_tabel_val,
                    "Status Validitas": ["VALID ✅" if r >= r_tabel_val else "INVALID ❌" for r in r_hit]
                })

                st.dataframe(res_emp, use_container_width=True)

                var_item = df_scores.var(axis=0, ddof=1).sum()
                var_total = total_skor.var(ddof=1)
                alpha = (n_soal_emp / (n_soal_emp - 1)) * (1 - (var_item / var_total)) if var_total > 0 and n_soal_emp > 1 else 0
                
                st.info(f"📊 **Reliabilitas Tes (Cronbach's Alpha):** `{round(alpha, 3)}` | Kategori: **{'Sangat Tinggi' if alpha>=0.8 else ('Tinggi' if alpha>=0.6 else 'Rendah')}**")

                st.subheader("🎯 Efektivitas Pengecoh (Distraktor ABCDE)")
                st.caption("💡 *Teori Evaluasi:* Pengecoh berfungsi baik jika dipilih **≥ 5% siswa**.")

                dist_data = []
                for idx, col in enumerate(df_jawaban.columns):
                    kunci = kunci_list[idx] if idx < len(kunci_list) else (kunci_list[0] if len(kunci_list) > 0 else "A")
                    counts = df_jawaban[col].astype(str).str.strip().str.upper().value_counts(normalize=True) * 100
                    
                    dist_status = []
                    for opt in ["A", "B", "C", "D", "E"]:
                        pct = counts.get(opt, 0)
                        if opt == kunci:
                            continue
                        if pct >= 5.0:
                            dist_status.append(f"{opt}: Bekerja ✅")
                        else:
                            dist_status.append(f"{opt}: Tidak Bekerja ❌")

                    dist_data.append({
                        "Soal": f"Soal {idx+1}",
                        "Kunci Jawaban": kunci,
                        "Opt A (%)": f"{round(counts.get('A', 0), 1)}%",
                        "Opt B (%)": f"{round(counts.get('B', 0), 1)}%",
                        "Opt C (%)": f"{round(counts.get('C', 0), 1)}%",
                        "Opt D (%)": f"{round(counts.get('D', 0), 1)}%",
                        "Opt E (%)": f"{round(counts.get('E', 0), 1)}%",
                        "Keputusan Distraktor": " | ".join(dist_status)
                    })
                st.dataframe(pd.DataFrame(dist_data), use_container_width=True)

            except Exception as e:
                st.error(f"Gagal memproses data jawaban: {e}")
    else:
        st.info("💡 Silakan unggah file Excel/CSV berisi jawaban siswa (opsi A, B, C, D, E).")

# ---------------------------------------------------------
# 4. REKAP & DOWNLOAD LAPORAN BER-TTD
# ---------------------------------------------------------
elif menu == "📥 Rekap & Download Laporan":
    st.header("📥 Rekap Laporan & Lembar Pengesahan Soal Valid")
    st.write("Format laporan resmi SMAN 3 Pangkalpinang dilengkapi dengan tabel pengesahan TTD Validator dan Waka Kurikulum.")

    if not st.session_state.soal_valid_kuali.empty:
        meta = st.session_state.meta_info
        st.markdown(f"""
        **Dokumen Informasi Laporan:**
        * **Aplikasi:** Q-BANK (Quality Question Bank) SMA Negeri 3 Pangkalpinang
        * **Jenis / Kelompok Soal:** {meta.get('JenisSoal', '-')}
        * **Mata Pelajaran:** {meta.get('Mapel', '-')} | **Kelompok:** {meta.get('Kelompok', '-')}
        * **Fase / Kelas:** {meta.get('Fase/Kelas', '-')} | **Kode Soal:** {meta.get('Kode Soal', '-')}
        * **Guru Penyusun:** {meta.get('Penyusun', '-')} | **TA / Semester:** {meta.get('Tahun/Semester', '-')}
        """)
        st.markdown("---")

        st.subheader("📋 Daftar Soal Teruji Valid")
        st.dataframe(st.session_state.soal_valid_kuali, use_container_width=True)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.soal_valid_kuali.to_excel(writer, sheet_name='Soal Valid', index=False)
            
            workbook = writer.book
            worksheet = workbook.add_worksheet('Lembar Pengesahan')
            
            title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
            header_format = workbook.add_format({'bold': True, 'align': 'left'})
            center_format = workbook.add_format({'align': 'center'})
            bold_center = workbook.add_format({'bold': True, 'align': 'center'})
            
            worksheet.merge_range('A1:E1', 'LEMBAR PENGESAHAN ANALISIS VALIDITAS SOAL', title_format)
            worksheet.merge_range('A2:E2', 'SMA NEGERI 3 PANGKALPINANG', title_format)
            
            worksheet.write('A4', 'Jenis Asesmen / Soal', header_format)
            worksheet.write('B4', f": {meta.get('JenisSoal', '-')}")
            worksheet.write('A5', 'Mata Pelajaran', header_format)
            worksheet.write('B5', f": {meta.get('Mapel', '-')}")
            worksheet.write('A6', 'Fase / Kelas', header_format)
            worksheet.write('B6', f": {meta.get('Fase/Kelas', '-')}")
            worksheet.write('A7', 'Guru Penyusun', header_format)
            worksheet.write('B7', f": {meta.get('Penyusun', '-')}")
            
            worksheet.write('A10', 'Tim Validator Ahli:', header_format)
            vals = meta.get('Validators', ['Validator 1', 'Validator 2', 'Validator 3'])
            nips = meta.get('ValidatorNIPs', ['-', '-', '-'])
            
            col_letters = ['A', 'C', 'E']
            for i in range(min(3, len(vals))):
                col = col_letters[i]
                worksheet.write(f'{col}12', f'Validator {i+1}', bold_center)
                worksheet.write(f'{col}16', vals[i], bold_center)
                worksheet.write(f'{col}17', nips[i], center_format)
                
            worksheet.write('C20', 'Mengetahui,', center_format)
            worksheet.write('C21', 'Wakil Kepala Sekolah Bidang Kurikulum', bold_center)
            worksheet.write('C25', 'Era, S.T., M.M.', bold_center)
            worksheet.write('C26', 'NIP. 198012292005012012', center_format)

        st.download_button(
            label="📥 Unduh Laporan Rekap Soal Valid & Lembar TTD (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"Laporan_Rekap_Validitas_{meta.get('Mapel','SMANETA')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Belum ada rekap data soal valid yang disimpan. Silakan lakukan perhitungan di menu **Analisis Kualitatif (Aiken's V)** dan klik tombol 'Simpan Rekap Soal Valid'.")
