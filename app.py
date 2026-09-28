# ---------------------------------------------------------
# 🔑 HALAMAN COVER & LOGIN GURU SMANETA
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_path = get_logo_path()
        logo_src = logo_path if logo_path else "https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_SMA_Negeri_3_Pangkalpinang.png"
        
        # Menggunakan HTML flexbox agar logo pas di tengah (simetris) & ukurannya pas
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 15px;">
                <img src="file/{logo_src}" style="width: 140px; height: auto;" alt="Logo SMANETA">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div class='main-header'>Q-BANK SMANETA</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Quality Question Bank — SMA Negeri 3 Pangkalpinang</div>", unsafe_allow_html=True)

        # Audio Jingle SMANETA
        jingle_mp3 = "Generasi Milenial - Jingel Smaneta #2.mp3"
        jingle_wav = "Generasi Milenial - Jingel Smaneta #2.wav"
        if os.path.exists(jingle_mp3):
            st.audio(jingle_mp3, format="audio/mp3")
        elif os.path.exists(jingle_wav):
            st.audio(jingle_wav, format="audio/wav")

        # Form Login Guru
        with st.form("login_form"):
            st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>🔐 Login Guru SMANETA</h4>", unsafe_allow_html=True)
            username_input = st.text_input("Nama Lengkap Guru (Tanpa Gelar & Spasi, Huruf Kecil):", placeholder="contoh: lisasumartini")
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
