import streamlit as st

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(
    page_title="Identifikasi Senyawa Organik",
    page_icon="🔬",
    layout="wide"
)

# =============================
# CSS SEDERHANA & AMAN
# =============================
st.markdown("""
<style>
body {font-family: Poppins, sans-serif;}
h1, h2, h3 {color:#0D47A1;}
.result {
    border-left:5px solid #388E3C;
    background:#E8F5E9;
    padding:1rem;
    border-radius:8px;
}
button {font-weight:600;}
</style>
""", unsafe_allow_html=True)

# =============================
# DATA ALUR IDENTIFIKASI
# =============================
FLOW = {
    "molisch": {
        "question": "Hasil uji Molisch?",
        "options": ["Cincin ungu", "Tidak bereaksi"],
        "next": {
            "Cincin ungu": "moore",
            "Tidak bereaksi": "ninhidrin"
        }
    },

    "moore": {
        "question": "Hasil uji Moore?",
        "options": ["Positif", "Negatif"],
        "next": {
            "Positif": "seliwanoff",
            "Negatif": "Pati"
        }
    },

    "seliwanoff": {
        "question": "Hasil uji Seliwanoff?",
        "options": ["Merah cepat", "Tidak berubah"],
        "next": {
            "Merah cepat": "Fruktosa (ketosa)",
            "Tidak berubah": "benedict"
        }
    },

    "benedict": {
        "question": "Hasil uji Benedict?",
        "options": ["Merah bata", "Tetap biru"],
        "next": {
            "Merah bata": "Gula pereduksi (glukosa/laktosa)",
            "Tetap biru": "Karbohidrat non-pereduksi"
        }
    },

    "ninhidrin": {
        "question": "Hasil uji Ninhidrin?",
        "options": ["Ungu", "Tidak berubah"],
        "next": {
            "Ungu": "Protein / Asam amino",
            "Tidak berubah": "ceric"
        }
    },

    "ceric": {
        "question": "Hasil uji Ceric Nitrat?",
        "options": ["Merah", "Kuning"],
        "next": {
            "Merah": "Alkohol",
            "Kuning": "Bukan alkohol"
        }
    }
}

# =============================
# SESSION STATE MINIMAL
# =============================
if "step" not in st.session_state:
    st.session_state.step = "molisch"

# =============================
# TAMPILAN APLIKASI
# =============================
st.title("🔬 Aplikasi Identifikasi Senyawa Organik")
st.caption("Berbasis uji kualitatif kimia organik sederhana")

current = st.session_state.step

# =============================
# JIKA SUDAH HASIL AKHIR
# =============================
if current not in FLOW:
    st.markdown(f"""
    <div class='result'>
        <h3>✅ Hasil Identifikasi</h3>
        <p><b>{current}</b></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Ulangi Identifikasi"):
        st.session_state.step = "molisch"
        st.rerun()

# =============================
# JIKA MASIH DALAM PROSES
# =============================
else:
    node = FLOW[current]
    st.subheader(node["question"])
    choice = st.radio("Pilih hasil pengujian:", node["options"])

    if st.button("➡️ Lanjut"):
        st.session_state.step = node["next"][choice]
        st.rerun()
