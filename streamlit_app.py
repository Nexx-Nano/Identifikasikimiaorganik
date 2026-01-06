import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional

# =============================================================
# KONFIGURASI DASAR
# =============================================================
st.set_page_config(
    page_title="Identifikasi Senyawa Organik",
    page_icon="🔬",
    layout="wide"
)

# =============================================================
# SESSION STATE
# =============================================================
st.session_state.setdefault("current_node", "molisch")
st.session_state.setdefault("final_result", None)
st.session_state.setdefault("page", "Beranda")

def reset_flow():
    st.session_state.current_node = "molisch"
    st.session_state.final_result = None

# =============================================================
# DATA STRUCTURE
# =============================================================
@dataclass
class DecisionNode:
    id: str
    title: str
    prompt: str
    options: List[str]
    next_map: Dict[str, str]
    result: Optional[str] = None
    description: Optional[str] = None

NODES: Dict[str, DecisionNode] = {}

def add(node: DecisionNode):
    NODES[node.id] = node

def result_node(id, name, desc):
    return DecisionNode(
        id=id,
        title="Hasil Identifikasi",
        prompt="",
        options=[],
        next_map={},
        result=name,
        description=desc
    )

# =============================================================
# DECISION TREE (INTI APLIKASI)
# =============================================================
add(DecisionNode(
    id="molisch",
    title="Uji Molisch",
    prompt="Bagaimana hasil uji Molisch?",
    options=["Cincin ungu", "Tidak bereaksi"],
    next_map={
        "Cincin ungu": "moore",
        "Tidak bereaksi": "ninhidrin"
    }
))

add(DecisionNode(
    id="moore",
    title="Uji Moore",
    prompt="Bagaimana hasil uji Moore?",
    options=["Positif", "Negatif"],
    next_map={
        "Positif": "seliwanoff",
        "Negatif": "hasil_pati"
    }
))

add(DecisionNode(
    id="seliwanoff",
    title="Uji Seliwanoff",
    prompt="Bagaimana hasil uji Seliwanoff?",
    options=["Merah cepat", "Tidak berwarna"],
    next_map={
        "Merah cepat": "hasil_fruktosa",
        "Tidak berwarna": "benedict"
    }
))

add(DecisionNode(
    id="benedict",
    title="Uji Benedict",
    prompt="Bagaimana hasil uji Benedict?",
    options=["Endapan merah bata", "Tetap biru"],
    next_map={
        "Endapan merah bata": "hasil_laktosa",
        "Tetap biru": "hasil_tidak_dikenal"
    }
))

add(DecisionNode(
    id="ninhidrin",
    title="Uji Ninhidrin",
    prompt="Bagaimana hasil uji Ninhidrin?",
    options=["Ungu/Biru", "Tidak bereaksi"],
    next_map={
        "Ungu/Biru": "hasil_protein",
        "Tidak bereaksi": "hasil_non_protein"
    }
))

# =============================================================
# HASIL AKHIR
# =============================================================
add(result_node(
    "hasil_pati",
    "Pati",
    "Sampel kemungkinan merupakan polisakarida (pati)."
))

add(result_node(
    "hasil_fruktosa",
    "Fruktosa",
    "Monosakarida golongan ketosa."
))

add(result_node(
    "hasil_laktosa",
    "Laktosa",
    "Disakarida pereduksi dengan hasil Benedict positif."
))

add(result_node(
    "hasil_protein",
    "Protein / Asam Amino",
    "Terdeteksi gugus amina melalui uji Ninhidrin."
))

add(result_node(
    "hasil_non_protein",
    "Non-Protein",
    "Sampel tidak menunjukkan reaksi protein."
))

add(result_node(
    "hasil_tidak_dikenal",
    "Tidak Teridentifikasi",
    "Data uji tidak cukup untuk identifikasi."
))

# =============================================================
# RENDER NODE
# =============================================================
def render_node(node: DecisionNode):
    st.subheader(node.title)

    if node.result:
        st.success(f"**{node.result}**")
        st.write(node.description)
        st.button("🔄 Mulai Ulang", on_click=reset_flow)
        return

    choice = st.radio(node.prompt, node.options)

    if st.button("Lanjut"):
        next_id = node.next_map.get(choice)
        if next_id:
            st.session_state.current_node = next_id
        else:
            st.session_state.current_node = "hasil_tidak_dikenal"
        st.rerun()

# =============================================================
# SIDEBAR
# =============================================================
with st.sidebar:
    st.title("🧪 Menu")
    st.session_state.page = st.radio(
        "Navigasi",
        ["Beranda", "Identifikasi"]
    )

# =============================================================
# HALAMAN
# =============================================================
if st.session_state.page == "Beranda":
    st.title("🔬 Identifikasi Senyawa Organik")
    st.markdown("""
    Aplikasi ini digunakan sebagai **alat bantu pembelajaran**  
    untuk memahami **alur identifikasi senyawa organik**  
    menggunakan uji kualitatif dasar.
    """)
    st.info("Gunakan menu *Identifikasi* untuk memulai.")

elif st.session_state.page == "Identifikasi":
    node_id = st.session_state.current_node
    node = NODES.get(node_id)
    if node:
        render_node(node)
    else:
        st.error("Node tidak ditemukan.")
