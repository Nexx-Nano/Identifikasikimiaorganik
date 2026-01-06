import streamlit as st

st.set_page_config(
    page_title="Pengenalan Uji Senyawa Organik",
    page_icon="🧪",
    layout="centered"
)

menu = st.sidebar.radio(
    "Menu",
    ["Beranda", "Daftar Uji", "Tentang"]
)

# ======================
# BERANDA
# ======================
if menu == "Beranda":
    st.title("🧪 Pengenalan Uji Kualitatif Senyawa Organik")

    st.write("""
    Aplikasi ini dibuat sebagai tugas mata kuliah Kimia Organik.
    Aplikasi ini bertujuan untuk membantu memahami berbagai
    uji kualitatif yang digunakan dalam analisis senyawa organik.
    
    Informasi yang ditampilkan bersifat teoritis dan tidak
    dimaksudkan sebagai pengganti kegiatan praktikum di laboratorium.
    """)

# ======================
# DAFTAR UJI
# ======================
elif menu == "Daftar Uji":
    st.title("📖 Daftar Uji Kualitatif")

    with st.expander("Uji Molisch"):
        st.write("""
        Uji Molisch digunakan untuk mendeteksi keberadaan karbohidrat.
        Hasil positif ditandai dengan terbentuknya cincin ungu pada
        batas larutan.
        """)

    with st.expander("Uji Benedict"):
        st.write("""
        Uji Benedict digunakan untuk mendeteksi gula pereduksi.
        Hasil positif ditandai dengan terbentuknya endapan merah bata.
        """)

    with st.expander("Uji Ninhidrin"):
        st.write("""
        Uji Ninhidrin digunakan untuk mendeteksi protein atau asam amino.
        Hasil positif ditandai dengan perubahan warna menjadi ungu.
        """)

    with st.expander("Uji Iodoform"):
        st.write("""
        Uji Iodoform digunakan untuk mendeteksi senyawa yang
        mengandung gugus metil keton atau etanol.
        Hasil positif ditandai dengan endapan kuning.
        """)

# ======================
# TENTANG
# ======================
elif menu == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")

    st.write("""
    Aplikasi ini dibuat sebagai bagian dari tugas perkuliahan
    dan bertujuan untuk membantu mahasiswa memahami teori dasar
    uji kualitatif senyawa organik.
    
    Aplikasi ini tidak melakukan analisis atau identifikasi
    senyawa secara langsung.
    """)
