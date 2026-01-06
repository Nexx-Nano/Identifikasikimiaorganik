import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    page_title="Identifikasi Senyawa Organik",
    layout="wide"
)

# ================= DATA MATERI =================
materi = {
    "Beranda": """
### Identifikasi Senyawa Organik

Identifikasi senyawa organik merupakan tahapan awal yang penting dalam kajian kimia
untuk mengenali karakteristik senyawa yang mengandung karbon. Senyawa organik
memiliki peranan luas dalam kehidupan, baik sebagai penyusun sistem biologis
maupun sebagai bahan dasar berbagai industri seperti farmasi, pangan, dan material.

Website ini dibuat sebagai media pembelajaran untuk membantu mahasiswa
Nanoteknologi Pangan tingkat awal dalam memahami praktikum Kimia Organik
secara sistematis, terstruktur, dan mudah dipahami.
""",

    "Bab 1 – Hidrokarbon": [
        {
            "judul": "Percobaan 1 – Pembuatan dan Uji Kimia Alkana",
            "prinsip": "Pemanasan natrium asetat dengan sodalime menghasilkan gas metana.",
            "alat": "Tabung reaksi bertutup selang, pipet tetes, bunsen",
            "bahan": "Natrium asetat, sodalime, larutan brom",
            "cara": [
                "Masukkan campuran sodalime dan natrium asetat ke tabung reaksi kering",
                "Panaskan campuran hingga terbentuk gas",
                "Alirkan gas ke larutan brom",
                "Amati perubahan warna larutan"
            ]
        }
    ],

    "Bab 2 – Alkohol dan Fenol": [
        {
            "judul": "Percobaan 1 – Uji Kelarutan Alkohol",
            "prinsip": "Gugus hidroksil (–OH) membentuk ikatan hidrogen dengan air.",
            "alat": "Tabung reaksi dan pipet tetes",
            "bahan": "Etanol, 1-butanol, air suling",
            "cara": [
                "Masukkan air suling ke tabung reaksi",
                "Tambahkan alkohol tetes demi tetes",
                "Homogenkan dan amati kelarutan"
            ]
        },
        {
            "judul": "Percobaan 2 – Pembentukan Ester",
            "prinsip": "Alkohol bereaksi dengan asam karboksilat membentuk ester beraroma.",
            "alat": "Tabung reaksi, penangas air",
            "bahan": "Etanol, asam asetat, asam sulfat pekat",
            "cara": [
                "Campurkan alkohol dan asam asetat",
                "Tambahkan katalis asam sulfat",
                "Panaskan dalam penangas air",
                "Amati aroma ester yang terbentuk"
            ]
        }
    ],

    "Bab 3 – Aldehid dan Keton": [
        {
            "judul": "Pereaksi Tollens",
            "prinsip": "Aldehida teroksidasi membentuk cermin perak.",
            "alat": "Tabung reaksi dan penangas air",
            "bahan": "Asetaldehida, pereaksi Tollens",
            "cara": [
                "Masukkan pereaksi Tollens ke tabung",
                "Tambahkan aldehida",
                "Panaskan perlahan",
                "Amati terbentuknya cermin perak"
            ]
        }
    ],

    "Bab 4 – Asam Karboksilat": [
        {
            "judul": "Reaksi Penggaraman",
            "prinsip": "Asam karboksilat bereaksi dengan basa membentuk garam.",
            "alat": "Tabung reaksi",
            "bahan": "Asam asetat, NaHCO₃",
            "cara": [
                "Masukkan asam karboksilat ke tabung",
                "Tambahkan larutan NaHCO₃",
                "Amati terbentuknya gas CO₂"
            ]
        }
    ],

    "Bab 5 – Amina": [
        {
            "judul": "Uji Kelarutan dan Kebasaan",
            "prinsip": "Amina bersifat basa dan dapat larut dalam air.",
            "alat": "Tabung reaksi dan kertas pH",
            "bahan": "Etilamina, air suling",
            "cara": [
                "Larutkan amina dalam air",
                "Uji pH larutan",
                "Catat nilai pH"
            ]
        }
    ],

    "Bab 6 – Lemak dan Minyak": [
        {
            "judul": "Reaksi Penyabunan",
            "prinsip": "Hidrolisis lemak oleh basa menghasilkan sabun.",
            "alat": "Tabung reaksi dan penangas air",
            "bahan": "Minyak, NaOH",
            "cara": [
                "Campurkan minyak dengan NaOH",
                "Panaskan",
                "Amati terbentuknya sabun"
            ]
        }
    ],

    "Bab 7 – Karbohidrat": [
        {
            "judul": "Uji Molisch",
            "prinsip": "Karbohidrat terdehidrasi membentuk furfural.",
            "alat": "Tabung reaksi",
            "bahan": "Glukosa, α-naftol, H₂SO₄ pekat",
            "cara": [
                "Tambahkan α-naftol ke sampel",
                "Tambahkan H₂SO₄ pekat perlahan",
                "Amati cincin ungu"
            ]
        }
    ],

    "Bab 8 – Protein": [
        {
            "judul": "Uji Biuret",
            "prinsip": "Ikatan peptida bereaksi dengan Cu²⁺ membentuk warna ungu.",
            "alat": "Tabung reaksi",
            "bahan": "Protein, NaOH, CuSO₄",
            "cara": [
                "Tambahkan NaOH ke sampel",
                "Tambahkan CuSO₄",
                "Amati warna ungu"
            ]
        }
    ]
}

# ================= UI =================
st.title("🔬 Identifikasi Senyawa Organik")

menu = st.sidebar.radio("📚 Daftar Materi", list(materi.keys()))

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
        st.markdown("---")
