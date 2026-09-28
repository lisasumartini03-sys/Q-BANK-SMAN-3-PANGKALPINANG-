# ---------------------------------------------------------
# 4. ANALISIS KUANTITATIF EMPIRIS (FIX TOTAL ERROR)
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
    kunci_list = [k.strip().upper() for k in kunci_jawaban.split(",") if k.strip()]
    
    df_jawaban_siswa = None

    if "Upload" in metode_kuanti:
        file_jawab = st.file_uploader("Unggah File Jawaban Siswa (.xlsx / .csv)", type=["xlsx", "csv"])
        if file_jawab:
            try:
                raw_df = pd.read_csv(file_jawab) if file_jawab.name.endswith('.csv') else pd.read_excel(file_jawab)
                df_jawaban_siswa = pd.DataFrame(raw_df)
                st.write("📌 **Pratinjau Data Jawaban Siswa:**")
                st.dataframe(df_jawaban_siswa.head(), use_container_width=True, hide_index=True)
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
        
        # Konversi tegas ke DataFrame
        editor_output = st.data_editor(pd.DataFrame(init_jawaban), use_container_width=True, hide_index=True)
        df_jawaban_siswa = pd.DataFrame(editor_output)

    if df_jawaban_siswa is not None:
        if st.button("⚡ Hitung Analisis Empiris"):
            try:
                # 1. Paksa konversi ulang ke DataFrame murni untuk membuang metadata Streamlit
                df_proc = pd.DataFrame(df_jawaban_siswa.to_dict(orient='records'))
                
                # 2. Ambil kolom soal saja (mengabaikan kolom Nama)
                soal_cols = [c for c in df_proc.columns if str(c).strip().lower() not in ["nama siswa", "nama", "siswa"]]
                
                if not soal_cols:
                    st.warning("Tidak ada kolom soal yang terdeteksi.")
                else:
                    df_skor = pd.DataFrame()
                    
                    # 3. Hitung skor per soal
                    for idx, col in enumerate(soal_cols):
                        kunci_soal = kunci_list[idx] if idx < len(kunci_list) else "A"
                        df_skor[col] = df_proc[col].astype(str).apply(lambda x: 1 if x.strip().upper() == kunci_soal else 0)
                        
                    res_kuanti = []
                    for idx, col in enumerate(soal_cols):
                        p_val = float(df_skor[col].mean())
                        if p_val < 0.3:
                            kat_sukar = "Sukar 🔴"
                        elif p_val <= 0.7:
                            kat_sukar = "Sedang 🟡"
                        else:
                            kat_sukar = "Mudah 🟢"
                            
                        res_kuanti.append({
                            "Nomor Soal": str(col),
                            "Tingkat Kesukaran (P)": round(p_val, 2),
                            "Kategori Kesukaran": kat_sukar,
                            "Status Soal": "DITERIMA ✅" if 0.2 <= p_val <= 0.8 else "REVISI/BUANG ❌"
                        })
                        
                    st.session_state.df_res_kuanti = pd.DataFrame(res_kuanti)
            except Exception as err:
                st.error(f"Gagal memproses perhitungan: {err}")

        if st.session_state.df_res_kuanti is not None:
            st.subheader("📈 Hasil Analisis Empiris")
            st.dataframe(st.session_state.df_res_kuanti, use_container_width=True, hide_index=True)
            
            if st.button("💾 Simpan Hasil Kuantitatif ke Bank Soal"):
                if mapel_kuanti not in st.session_state.bank_soal_folder:
                    st.session_state.bank_soal_folder[mapel_kuanti] = {}
                if kelas_kuanti not in st.session_state.bank_soal_folder[mapel_kuanti]:
                    st.session_state.bank_soal_folder[mapel_kuanti][kelas_kuanti] = []
                    
                st.session_state.bank_soal_folder[mapel_kuanti][kelas_kuanti].append(st.session_state.df_res_kuanti)
                st.success(f"Berhasil disimpan di Folder Bank Soal [{mapel_kuanti} - {kelas_kuanti}]!")
