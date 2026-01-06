import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    page_title="Identifikasi Senyawa Organik",
    layout="wide"
)

st.title("🔬 Identifikasi Senyawa Organik")

# ================= DATA MATERI =================
materi = {
    "Beranda": """
Identifikasi senyawa organik merupakan tahapan awal yang penting dalam kajian kimia
untuk mengenali karakteristik suatu senyawa yang mengandung karbon. Senyawa organik
memiliki peranan luas dalam kehidupan, baik sebagai penyusun sistem biologis maupun
sebagai bahan dasar dalam berbagai bidang industri, seperti farmasi, pangan, dan
kimia material.

Setiap senyawa organik memiliki struktur dan gugus fungsi yang berbeda, sehingga
menunjukkan sifat kimia dan reaktivitas yang beragam. Perbedaan tersebut menjadi dasar
dalam proses identifikasi melalui respon kimia terhadap pereaksi tertentu.

Pendekatan awal yang umum digunakan adalah uji kualitatif yang ditandai dengan
perubahan warna, terbentuknya endapan, atau gejala fisik lainnya.

Website ini dibuat untuk membantu mahasiswa Nanoteknologi Pangan tingkat awal
dalam memahami praktikum Kimia Organik secara sistematis dan terstruktur.

Landasan teori merujuk pada:
- Afriani & Utami (2021)
- Irawan et al. (2025)
""",

    # ================= BAB 1 =================
    "Bab 1 – Hidrokarbon": [
        {
            "judul": "Percobaan 1 – Pembuatan dan Uji Kimia Alkana",
            "prinsip": "Pemanasan natrium asetat dengan sodalime menghasilkan metana yang bereaksi dengan larutan brom.",
            "alat": "Tabung reaksi bertutup selang, pipet tetes, bunsen",
            "bahan": "Natrium asetat, sodalime, larutan brom, KMnO₄, K₂Cr₂O₇",
            "cara": [
                "Masukkan campuran sodalime dan natrium asetat ke tabung reaksi kering",
                "Panaskan campuran",
                "Alirkan gas ke larutan brom",
                "Uji lanjutan dengan KMnO₄ dan K₂Cr₂O₇",
                "Amati perubahan warna"
            ],
            "catatan": "Sodalime adalah campuran Ca(OH)₂ dan NaOH"
        },
        {
            "judul": "Percobaan 2 – Larutan Brom dalam CCl₄",
            "prinsip": "Alkana, alkena, alkuna, dan benzena menunjukkan reaktivitas berbeda terhadap brom.",
            "alat": "Tabung reaksi dan pipet tetes",
            "bahan": "Heksana, minyak tanah, larutan brom 5%",
            "cara": [
                "Masukkan sampel ke tabung reaksi",
                "Tambahkan larutan brom setetes demi setetes",
                "Amati perubahan warna"
            ]
        },
        {
            "judul": "Percobaan 3 – Uji Bayer",
            "prinsip": "Alkena dan alkuna teroksidasi oleh KMnO₄.",
            "alat": "Tabung reaksi",
            "bahan": "Heksana, minyak tanah, KMnO₄",
            "cara": [
                "Tambahkan KMnO₄ ke sampel",
                "Amati perubahan warna ungu",
                "Perhatikan endapan MnO₂"
            ]
        }
    ],

    # ================= BAB 2 =================
    "Bab 2 – Alkohol, Fenol, Eter, Halogen Organik": [
        {
            "judul": "Percobaan 1 – Uji Kelarutan Alkohol dan Eter",
            "prinsip": "Gugus OH membentuk ikatan hidrogen dengan air.",
            "alat": "Tabung reaksi",
            "bahan": "Etanol, butanol, gliserol, eter",
            "cara": [
                "Masukkan air ke tabung",
                "Tambahkan sampel",
                "Amati terbentuknya dua fasa"
            ]
        },
        {
            "judul": "Percobaan 2 – Pembentukan Ester",
            "prinsip": "Alkohol bereaksi dengan asam membentuk ester beraroma.",
            "alat": "Tabung reaksi, penangas air",
            "bahan": "Etanol, asam asetat, H₂SO₄ pekat",
            "cara": [
                "Campurkan alkohol dan asam",
                "Tambahkan katalis",
                "Panaskan",
                "Amati aroma"
            ]
        },
        {
            "judul": "Percobaan 3 – Pereaksi Ceric Nitrat",
            "prinsip": "Alkohol membentuk kompleks merah dengan Ce(IV).",
            "alat": "Tabung reaksi",
            "bahan": "Butanol, fenol, pereaksi ceric nitrat",
            "cara": [
                "Tambahkan pereaksi",
                "Kocok",
                "Amati warna"
            ]
        }
    ],

    # ================= BAB 3 =================
    "Bab 3 – Aldehid dan Keton": [
        {
            "judul": "Pereaksi Na-Bisulfit",
            "prinsip": "Aldehid dan keton membentuk adisi bisulfit.",
            "alat": "Tabung reaksi",
            "bahan": "Asetaldehida, benzaldehida, aseton",
            "cara": [
                "Tambahkan Na-bisulfit",
                "Kocok",
                "Amati endapan putih"
            ]
        },
        {
            "judul": "Pereaksi Tollens",
            "prinsip": "Aldehida teroksidasi membentuk cermin perak.",
            "alat": "Tabung reaksi",
            "bahan": "Asetaldehida, pereaksi Tollens",
            "cara": [
                "Tambahkan pereaksi",
                "Panaskan",
                "Amati cermin perak"
            ]
        }
    ],

    # ================= BAB 4 =================
    "Bab 4 – Asam Karboksilat dan Derivat": [
        {
            "judul": "Pembentukan Asam Karboksilat",
            "prinsip": "Asam karboksilat larut dalam air.",
            "alat": "Tabung reaksi",
            "bahan": "Asam asetat, anhidrida asetat",
            "cara": [
                "Larutkan dalam air",
                "Panaskan jika perlu",
                "Amati kelarutan"
            ]
        },
        {
            "judul": "Reaksi Penggaraman",
            "prinsip": "Asam bereaksi dengan basa membentuk garam.",
            "alat": "Tabung reaksi",
            "bahan": "NaHCO₃, NaOH",
            "cara": [
                "Tambahkan basa",
                "Amati gas CO₂"
            ]
        }
    ],

    # ================= BAB 5 =================
    "Bab 5 – Amina": [
        {
            "judul": "Uji Kelarutan dan Kebasaan",
            "prinsip": "Amina bersifat basa.",
            "alat": "Tabung reaksi, kertas pH",
            "bahan": "Amonia, etilamina",
            "cara": [
                "Larutkan amina",
                "Uji pH"
            ]
        }
    ],

    # ================= BAB 6 =================
    "Bab 6 – Lemak dan Minyak": [
        {
            "judul": "Reaksi Penyabunan",
            "prinsip": "Hidrolisis lemak oleh basa.",
            "alat": "Tabung reaksi",
            "bahan": "Minyak, NaOH",
            "cara": [
                "Campurkan minyak dan NaOH",
                "Panaskan",
                "Amati sabun"
            ]
        }
    ],

    # ================= BAB 7 =================
    "Bab 7 – Karbohidrat": [
        {
            "judul": "Uji Molisch",
            "prinsip": "Karbohidrat membentuk cincin ungu.",
            "alat": "Tabung reaksi",
            "bahan": "Glukosa, α-naftol, H₂SO₄",
            "cara": [
                "Tambahkan pereaksi",
                "Amati cincin ungu"
            ]
        }
    ],

    # ================= BAB 8 =================
    "Bab 8 – Protein": [
        {
            "judul": "Uji Biuret",
            "prinsip": "Ikatan peptida bereaksi membentuk warna ungu.",
            "alat": "Tabung reaksi",
            "bahan": "Protein, NaOH, CuSO₄",
            "cara": [
                "Tambahkan NaOH",
                "Tambahkan CuSO₄",
                "Amati warna ungu"
            ]
        }
    ]
}

# ================= MENU =================
menu = st.sidebar.radio("📘 Daftar Materi", list(materi.keys()))

if menu == "Beranda":
    st.markdown(materi["Beranda"])
    st.markdown("---")
    st.markdown("""
**Dibuat oleh:**  
Kelompok 8 – Logika Pemrograman dan Komputasi Data  

**Sumber:**  
Irawan et al., 2025  
Afriani & Utami, 2021
""")
else:
    st.header(menu)
    for p in materi[menu]:
        st.subheader(p["judul"])
        st.write(f"**Prinsip:** {p['prinsip']}")
        st.write(f"**Alat:** {p['alat']}")
        st.write(f"**Bahan:** {p['bahan']}")
        st.markdown("**Cara Kerja:**")
        for i, langkah in enumerate(p["cara"], 1):
            st.write(f"{i}. {langkah}")
        if "catatan" in p:
            st.info(f"Catatan: {p['catatan']}")
        st.markdown("---")
