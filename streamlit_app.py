import streamlit as st
import datetime
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import urllib.parse  # untuk encode subject/body email Gmail
import urllib.parse  # untuk encode pesan WhatsApp


# =============================================================
SUCCESS = "#388E3C"       # Hijau success

st.markdown("""
<style>
* { font-family: 'Poppins', sans-serif; }
.stApp { background-color: #F5F7FA; }
h1,h2,h3 { color:#0D47A1; }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#0D47A1,#1976D2);
}
.stButton > button {
  background:#0D47A1;
  color:white;
  border-radius:6px;
}
.result-card {
  background:#E8F5E9;
  border-left:5px solid #388E3C;
  padding:1rem;
  border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# DATA STRUKTUR TEORI
# =============================================================
@dataclass
class Theory:
    name: str
    emoji: str
    detects: str
    principle: str
    reagents: str
    procedure: str
    positive: str
    negative: str
    notes: str
    safety: str = "Gunakan APD laboratorium standar (sarung tangan, kacamata, jas lab)."
    tips: str = ""
    img_url: Optional[str] = None

THEORY_LIST: List[Theory] = [
    Theory(
        name="Uji Molisch",
        emoji="🟣",
        detects="Semua karbohidrat (monosakarida, oligo, poli)",
        principle="Karbohidrat terdehidrasi oleh H2SO4 pekat menghasilkan furfural/derivat yang berkondensasi dengan α-naftol membentuk cincin ungu di batas larutan.",
        reagents="Larutan α-naftol dalam etanol; H2SO4 pekat (dituang melalui dinding tabung).",
        procedure="Campur sedikit sampel + air, tambahkan 2 tetes pereaksi α-naftol, lalu tambahkan H2SO4 pekat perlahan di dinding tabung sehingga terbentuk dua lapisan.",
        positive="Cincin ungu/ungu tua di batas dua lapisan.",
        negative="Tidak terbentuk cincin; larutan tetap bening/warna reagen.",
        notes="Sangat sensitif—sedikit gula pun positif. Protein & lipid umumnya negatif kecuali ada kontaminasi gula.",
        safety="H2SO4 pekat bersifat korosif kuat—gunakan pelindung mata & lakukan di lemari asam.",
        tips="Pastikan penambahan asam pelan agar lapisan jelas.",
    ),
    Theory(
        name="Uji Moore",
        emoji="🟠",
        detects="Gula pereduksi; perbedaan kasar pati vs gula",
        principle="Gula pereduksi menggelapkan warna (reaksi karamelisasi/aldol kondensasi) dalam suasana basa panas.",
        reagents="NaOH 10% atau basa kuat serupa.",
        procedure="Campur sampel dengan NaOH, panaskan beberapa menit (mandi air panas).",
        positive="Kuning kecoklatan hingga coklat gelap.",
        negative="Tetap pucat/tidak berubah warna.",
        notes="Pati murni biasanya negatif kecuali terhidrolisis.",
        safety="Basa kuat iritan kulit & mata.",
        tips="Gunakan tabung kontrol kosong untuk banding warna.",
    ),
    Theory(
        name="Uji Seliwanoff",
        emoji="🔴",
        detects="Membedakan ketosa (cepat) dari aldosa (lambat)",
        principle="Ketosa terdehidrasi lebih cepat dalam asam kuat membentuk furfural yang bereaksi dengan resorsinol → merah.",
        reagents="Pereaksi Seliwanoff: resorsinol + HCl pekat.",
        procedure="Tambahkan pereaksi ke sampel, panaskan 1–2 menit; amati perkembangan warna.",
        positive="Merah tua cepat (ketosa, mis. fruktosa).",
        negative="Tidak berwarna / perlahan merah muda (aldosa).",
        notes="Waktu penting! Reaksi lama dapat memberi positif palsu.",
        safety="Asam pekat korosif.",
        tips="Gunakan timer 1 menit untuk banding antar sampel.",
    ),
    Theory(
        name="Uji Benedict",
        emoji="🧪",
        detects="Gula pereduksi",
        principle="Cu2+ direduksi menjadi Cu2O (endapan merah bata) oleh gula pereduksi dalam suasana alkali kompleks sitrat.",
        reagents="Larutan Benedict (CuSO4 + natrium sitrat + Na2CO3).",
        procedure="Campur sampel & pereaksi, panaskan hingga mendidih ringan 2–5 mnt.",
        positive="Hijau → kuning → oranye → merah bata tergantung konsentrasi gula.",
        negative="Tetap biru.",
        notes="Fruktosa juga positif (isomerisasi dalam basa).",
        safety="Larutan basa; hindari kontak kulit.",
        tips="Gunakan skala warna semi-kuantitatif untuk latihan.",
    ),
    Theory(
        name="Uji Fehling",
        emoji="🧱",
        detects="Aldosa & gula pereduksi",
        principle="Cu2+ (tartrat/alkali) direduksi menjadi Cu2O merah bata oleh aldehid terbuka dari gula.",
        reagents="Fehling A (CuSO4) + Fehling B (alkali tartrat); dicampur segar.",
        procedure="Campur A+B, lalu tambah sampel; panaskan sampai mendidih.",
        positive="Endapan merah bata Cu2O.",
        negative="Tetap biru; tidak ada endapan.",
        notes="Keton tidak bereaksi; beberapa gula perlu pemanasan lebih lama.",
        safety="Alkali pekat; percikan panas.",
        tips="Gunakan tabung kontrol tanpa sampel.",
    ),
    Theory(
        name="Uji Ninhidrin",
        emoji="🔵",
        detects="Asam amino bebas / protein terhidrolisis",
        principle="Ninhidrin bereaksi dengan gugus α-amino menghasilkan kromofor ungu (Ruhemann's purple).",
        reagents="Larutan ninhidrin dalam pelarut organik (mis. etanol) + buffer.",
        procedure="Teteskan ninhidrin ke sampel (kertas/larutan), panaskan singkat.",
        positive="Ungu/biru; prolin → kuning.",
        negative="Tidak ada perubahan signifikan.",
        notes="Sangat sensitif, digunakan juga untuk sidik jari amino.",
        safety="Ninhidrin iritan; hindari inhalasi.",
        tips="Bandingkan intensitas untuk perkiraan semi-kuantitatif.",
    ),
    Theory(
        name="Uji Nilon",
        emoji="🧶",
        detects="Fenol aromatik dalam asam amino (mis. tirosin)",
        principle="Kondensasi fenol dengan formaldehid dalam suasana asam → warna merah.",
        reagents="Formaldehid + HCl pekat (atau reagen Nilon komersial).",
        procedure="Campur sampel, tambah formaldehid + HCl, panaskan; amati merah.",
        positive="Merah jelas.",
        negative="Tidak berubah / pucat.",
        notes="Selektif untuk tirosin relatif terhadap asam amino lain.",
        safety="Formaldehid toksik & volatil!",
        tips="Kerjakan di lemari asam; tutup tabung.",
    ),
    Theory(
        name="Uji Ceric Nitrat",
        emoji="🍷",
        detects="Alkohol (terutama primer & sekunder)",
        principle="Alkohol mengurangi Ce4+ → Ce3+ dengan perubahan warna kuning → merah/oker/cokelat.",
        reagents="Amonium ceric nitrat dalam HNO3 encer.",
        procedure="Campur 1 tetes sampel dgn pereaksi; amati segera.",
        positive="Merah ceri / oranye / kekeruhan cepat.",
        negative="Tetap kuning.",
        notes="Fenol & senyawa lain bisa ganggu.",
        safety="Pengoksidasi kuat; korosif.",
        tips="Bandingkan dengan kontrol kosong.",
    ),
    Theory(
        name="Uji FeCl₃",
        emoji="💜",
        detects="Fenol & enolat tertentu",
        principle="Kompleksasi fenolat dengan Fe3+ menghasilkan warna ungu/biru/hijau tergantung struktur.",
        reagents="Larutan FeCl3 1-2% dalam air/etanol.",
        procedure="Tambahkan beberapa tetes FeCl3 ke sampel netral/encer.",
        positive="Ungu-ungu tua / hijau / biru (variasi).",
        negative="Tetap kuning pucat/tidak berubah.",
        notes="Beberapa asam karboksilat terkonjugasi memberi warna palsu.",
        safety="FeCl3 korosif ringan; noda cokelat.",
        tips="Gunakan kontrol larutan pelarut saja.",
    ),
    Theory(
        name="Uji Jones",
        emoji="🟢",
        detects="Alkohol primer & sekunder (oksidasi)",
        principle="Cr(VI) oranye dikurangi menjadi Cr(III) hijau oleh alkohol p/s; t biasanya tidak bereaksi cepat.",
        reagents="Reagen Jones (CrO3 dalam H2SO4 + asetat).",
        procedure="Tambahkan beberapa tetes ke larutan alkohol; amati perubahan cepat.",
        positive="Hijau kebiruan cepat.",
        negative="Tetap oranye/jingga (alkohol tersier / non-reaktif).",
        notes="Sensitif terhadap pelarut & suhu.",
        safety="Kromium(VI) toksik & karsinogenik; wajib APD & disposal benar.",
        tips="Gunakan sedikit saja; jangan panaskan berlebih.",
    ),
    Theory(
        name="Uji Lucas",
        emoji="⚪",
        detects="Klasifikasi alkohol t > s > p",
        principle="Alkohol bereaksi dengan ZnCl2/HCl membentuk alkil klorida tak larut → kekeruhan/dua fase; laju tergantung tingkat substitusi.",
        reagents="Reagen Lucas: ZnCl2 anhidrat dalam HCl pekat.",
        procedure="Campur sampel + reagen; catat waktu kekeruhan.",
        positive="Kekeruhan <5 detik (t), ~5-10 mnt (s), lambat / tdk (p).",
        negative="Tetap jernih (primer).",
        notes="Suhu mempengaruhi laju; gunakan standar.",
        safety="HCl pekat korosif; ZnCl2 iritan.",
        tips="Gunakan stopwatch & tabel laju untuk latihan klasifikasi.",
    ),
    Theory(
        name="Uji Iodoform",
        emoji="🟡",
        detects="Metil keton & etanol",
        principle="Halogenasi α & fragmentasi menghasilkan CHI3 (iodoform) kuning berbau tajam.",
        reagents="Iodin + NaOH (atau NaOCl + KI).",
        procedure="Alkalinisasi sampel, tambah I2; panaskan ringan hingga endapan.",
        positive="Endapan kuning pucat (kadang tampak putih) iodoform.",
        negative="Tidak ada endapan; larutan cokelat I2 hilang tanpa CHI3.",
        notes="Masih dapat memberi hasil dengan etanol (oksidasi → asetaldehid).",
        safety="I2 menodai; bau kuat.",
        tips="Gunakan kertas uji bau khas CHI3 untuk edukasi.",
    ),
    Theory(
        name="Uji Schiff",
        emoji="🟣",
        detects="Aldehid",
        principle="Pereaksi Schiff (fuchsin sulfurous) tidak berwarna; aldehid mengembalikan kromofor → magenta/ungu.",
        reagents="Pereaksi Schiff siap pakai / disiapkan segar.",
        procedure="Tambahkan pereaksi ke larutan sampel; amati warna beberapa menit.",
        positive="Ungu/magenta cepat.",
        negative="Tetap pink pucat.",
        notes="Keton umumnya tidak bereaksi; aldehid aromatik bisa lebih lambat.",
        safety="Pewarna organik; hindari kontak kulit.",
        tips="Gunakan kontrol formaldehid (positif) & aseton (negatif).",
    ),
    Theory(
        name="Uji NaHSO₃",
        emoji="🧊",
        detects="Aldehid & keton tertentu (adisi bisulfit)",
        principle="Ion bisulfit (HSO3-) menambah ke karbonil → adisi kristalin putih/larut; bergantung struktur.",
        reagents="Larutan natrium bisulfit jenuh.",
        procedure="Campur volume sama sampel & NaHSO3; dinginkan; amati endapan/pelepasan panas.",
        positive="Endapan putih / pelepasan panas.",
        negative="Larutan tetap jernih.",
        notes="Keton terhalang sterik sering negatif.",
        safety="SO2 ringan bisa terlepas; ventilasi.",
        tips="Pendinginan memudahkan kristal.",
    ),
    Theory(
        name="Uji Esterifikasi",
        emoji="🍌",
        detects="Alkohol (aroma ester)",
        principle="Esterifikasi Fischer alkohol + asam karboksilat + H2SO4 → ester harum (amil asetat = pisang).",
        reagents="Alkohol + asam asetat / butirat / lainnya + H2SO4 pekat katalitik.",
        procedure="Campur reaktan kecil; panaskan lembut (water bath); cium aroma hati-hati.",
        positive="Aroma khas (pisang, balon, buah).",
        negative="Tidak ada aroma jelas.",
        notes="Reaksi lambat jika dingin; gunakan pemanasan lembut.",
        safety="H2SO4 & uap ester mudah menguap; jangan hirup langsung.",
        tips="Gunakan teknik wafting (kipas tangan) saat mencium.",
    ),
    Theory(
        name="Uji Iod Hubl",
        emoji="🛢️",
        detects="Tingkat ketidakjenuhan (ikatan rangkap C=C)",
        principle="I2/IKl diserap oleh ikatan rangkap; pemudaran warna sebanding dgn ketidakjenuhan (basis indeks iodin).",
        reagents="Larutan Hubl (I2 + KI dalam pelarut + HgCl2 klasik / versi lab aman).",
        procedure="Tambahkan pereaksi ke sampel minyak/larutan; amati pemudaran warna / titrasi lanjutan.",
        positive="Warna cokelat memudar cepat (tak jenuh).",
        negative="Tetap cokelat/merah bata (jenuh).",
        notes="Digunakan untuk analisis minyak & lemak.",
        safety="Beberapa formulasi mengandung HgCl2 toksik—gunakan versi bebas Hg jika tersedia.",
        tips="Kocok homogen agar reaksi merata.",
    )
# =============================================================
# STATE SESI
# =============================================================
if "decision_path" not in st.session_state:
    st.session_state.decision_path = []
if "current_node" not in st.session_state:
    st.session_state.current_node = "molisch"
if "final_result" not in st.session_state:
    st.session_state.final_result = None
if "page" not in st.session_state:
    st.session_state.page = "Beranda"


def reset_flow():
    st.session_state.decision_path = []
    st.session_state.current_node = "molisch"
    st.session_state.final_result = None

# =============================================================
# FUNGSI HELPER UNTUK PATH GAMBAR
# =============================================================
def get_image_path(relative_path: str) -> str:
    """Mendapatkan path gambar yang benar untuk deployment Streamlit."""
    # Normalisasi path (mengganti backslash dengan forward slash)
    normalized_path = relative_path.replace('\\', '/')
    
    # Untuk Streamlit Cloud, path relatif dari root biasanya bekerja
    # Coba beberapa lokasi yang mungkin
    possible_paths = [
        normalized_path,  # Path relatif langsung (biasanya bekerja di Streamlit Cloud)
        os.path.join(os.getcwd(), normalized_path),  # Dari current working directory
    ]
    
    # Jika __file__ tersedia (untuk local development)
    try:
        script_dir = Path(__file__).parent
        possible_paths.extend([
            str(script_dir / normalized_path),  # Dari folder script
            str(script_dir.parent / normalized_path),  # Dari parent folder
        ])
    except (NameError, AttributeError):
        # __file__ mungkin tidak tersedia di beberapa environment
        pass
    
    # Coba setiap path
    for path in possible_paths:
        # Normalisasi path untuk sistem operasi
        path_normalized = os.path.normpath(path)
        if os.path.exists(path_normalized):
            return path_normalized
        # Coba dengan forward slash juga (untuk cross-platform)
        if os.path.exists(path):
            return path
    
    # Jika tidak ditemukan, return path asli
    # Streamlit akan mencoba load gambar dengan path ini
    return normalized_path

# =============================================================
# FUNGSI RENDER NODE
# =============================================================

def render_node(node: DecisionNode):
    st.header(node.title)

    if node.result is not None:
        color = node.result_color or SUCCESS
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color:{color};'>
                <h3>{node.result_icon or '✅'} {node.result}</h3>
                <p>{node.result_desc or ''}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("🔄 Mulai Ulang Identifikasi", on_click=reset_flow, use_container_width=True)
        return

    choice = st.radio(node.prompt, node.options, key=node.id)
    col1, col2 = st.columns(2)
    with col1:
        lanjut = st.button("Lanjut ➡️", key=f"next_{node.id}", use_container_width=True)
    with col2:
        ulang = st.button("🔁 Reset", key=f"reset_{node.id}", use_container_width=True)

    if ulang:
        reset_flow()
        st.rerun()

    if lanjut:
        st.session_state.decision_path.append((node.title, choice))
        nxt = node.next_map.get(choice)
        if nxt is None:
            st.session_state.final_result = "warning_generic"
        else:
            if nxt in NODES and NODES[nxt].result is not None:
                st.session_state.final_result = nxt
            elif nxt in NODES:
                st.session_state.current_node = nxt
            else:
                st.session_state.final_result = "warning_generic"
        st.rerun()

# =============================================================
# SIDEBAR
# =============================================================
with st.sidebar:
    st.header("🧪Identifikasi Senyawa Organik")
    pages = ["Beranda", "Identifikasi Senyawa Organik", "Reaksi", "Istilah Penting"]
    selected = st.radio("Pilih halaman:", pages, label_visibility="collapsed")
    st.session_state.page = selected

    st.divider()

    

# =============================================================
# HALAMAN: Beranda
# =============================================================
if st.session_state.page == "Beranda":
    st.title("🔬 Identifikasi Senyawa Organik")
    st.subheader("Selamat Datang")
    
    st.markdown("""
    Identifikasi senyawa organik merupakan tahapan awal yang penting dalam kajian kimia untuk mengenali karakteristik suatu senyawa yang mengandung karbon. Senyawa organik memiliki peranan luas dalam kehidupan, baik sebagai penyusun sistem biologis maupun sebagai bahan dasar dalam berbagai bidang industri, seperti farmasi, pangan, dan kimia material. Oleh karena itu, pemahaman terhadap proses identifikasi senyawa organik menjadi dasar penting dalam pembelajaran kimia.

    Setiap senyawa organik memiliki struktur dan gugus fungsi yang berbeda, sehingga menunjukkan sifat kimia dan reaktivitas yang beragam. Perbedaan tersebut menjadi dasar dalam proses identifikasi, karena suatu senyawa dapat dikenali melalui respon kimianya terhadap pereaksi tertentu. Proses identifikasi tidak hanya bertujuan untuk menentukan jenis senyawa, tetapi juga untuk memahami hubungan antara struktur molekul dan sifat kimia yang dimilikinya.

    Pendekatan  umum yang digunakan pada tahap awal identifikasi adalah uji kualitatif. Metode ini memanfaatkan reaksi kimia sederhana untuk mendeteksi keberadaan gugus fungsi tertentu, yang ditunjukkan melalui perubahan warna, terbentuknya endapan, atau gejala fisik lainnya. Uji kualitatif masih banyak diterapkan karena bersifat praktis, mudah dilakukan, serta efektif sebagai langkah awal sebelum analisis lanjutan.

    Dalam praktik Kimia Organik pada mahasiswa Nanoteknologi Pangan, banyak sekali mahasiswa tingkat 1 yang merasa terkendala dan menjadi beban utama dalam perkuliahan karena kompleksnya materi dan kurangnya pemahaman mengenai reaksi kimia. Oleh karena itu, kami menciptakan solusi untuk permasalahan tersebut agar kedepannya dapat membantu mengatasi kendala dan beban mahasiswa Nanoteknologi Pangan tingkat 1, untuk bisa memahami dan lulus dalam mata kuliah ini. 

    Landasan teori dalam pembahasan identifikasi senyawa organik ini merujuk pada Penuntun Praktikum Kimia Organik (Afriani & Utami, 2021) dan buku Identifikasi Secara Kimia Gugus Fungsi Senyawa Organik (Irawan et al., 2025) sebagai sumber utama.     
    
    """)

    st.divider()

# =============================================================
# HALAMAN: Identifikasi Senyawa Organik
# =============================================================
elif st.session_state.page == "Identifikasi Senyawa Organik":
    st.title("📖 Identifikasi Senyawa Organik")
    
    st.markdown("#### 🧪 Uji Khusus: Hidrokarbon & Alkohol")
    st.markdown("Panduan lengkap untuk uji-uji pada bab spesifik dengan prinsip dan prosedur detail.")
    st.divider()

    # Create subcategories for special tests including Bab 5-8
    subcat1, subcat2, subcat3, subcat4, subcat5, subcat6, subcat7, subcat8 = st.tabs(
        [
            "🛢️ Bab 1: Hidrokarbon",
            "🍷 Bab 2: Alkohol & Fenol",
            "🧬 Bab 3: Aldehid & Keton",
            "🔗 Bab 4: Halogen Organik",
            "🧪 Bab 5: Amina",
            "🧴 Bab 6: Lemak & Minyak",
            "🍬 Bab 7: Karbohidrat",
            "🧫 Bab 8: Protein",
        ]
    )

    with subcat1:
        st.subheader("🛢️ Bab 1: Hidrokarbon (Alkana, Alkena, Alkuna, Aromatik)")
        st.markdown("---")

        test_hydro = {
            "Uji Pembentukan Alkana": {
                "emoji": "🔥",
                "prinsip": "Pemanasan natrium asetat dengan sodalime menghasilkan metana. Metana bereaksi dengan larutan bromin pada temperatur ruang dengan sinar UV membentuk tetrabromoetana (larutan bromin berubah dari merah kecoklatan menjadi tidak berwarna).",
                "pereaksi": "Natrium asetat, Sodalime (CaO:NaOH = 1:1), Larutan bromin, KMnO₄, K₂Cr₂O₇ 5%",
                "prosedur": "1. Campur sodalime + natrium asetat di tabung dengan selang\n2. Panaskan\n3. Alirkan gas ke tabung berisi Br₂, KMnO₄, K₂Cr₂O₇\n4. Amati perubahan warna",
                "positif": "Larutan bromin dan KMnO₄ berubah tidak berwarna",
                "negatif": "Warna larutan tetap/tidak berubah signifikan",
                "keselamatan": "Hati-hati dengan sodalime panas; gunakan APD lengkap"
            },
            "Uji Bromin dalam CCl₄": {
                "emoji": "🟠",
                "prinsip": "Heksana bereaksi dengan Br₂ pada T ruang + UV membentuk 1-bromoheksana. Alkena dan alkuna bereaksi cepat tanpa UV. Benzena hanya bereaksi dengan katalis Fe-Br₃.",
                "pereaksi": "Larutan bromin 5% dalam CCl₄/kloroform, Heksana, Minyak tanah",
                "prosedur": "1. Masukkan 0,1-0,2 mL heksana ke tabung\n2. Tambahkan Br₂ setetes demi setetes sambil dikocok\n3. Amati perubahan warna hingga warna Br₂ tidak berubah",
                "positif": "Warna bromin hilang/pudar (ada ikatan rangkap atau kondisi tertentu)",
                "negatif": "Warna bromin tetap merah kecokelatan",
                "keselamatan": "Bromin volatil dan beracun; kerjakan di lemari asam"
            },
            "Uji Bayer (KMnO₄)": {
                "emoji": "🟣",
                "prinsip": "Alkena dan alkuna teroksidasi oleh KMnO₄ membentuk alkohol/diол. Alkana dan benzena tidak bereaksi. Perubahan warna KMnO₄ dari ungu → tidak berwarna atau terbentuk endapan coklat MnO₂.",
                "pereaksi": "Larutan KMnO₄, Heksana, Minyak tanah",
                "prosedur": "1. Masukkan 0,1-0,2 mL heksana ke tabung\n2. Tambahkan KMnO₄ setetes demi setetes sambil dikocok\n3. Amati perubahan warna 0,5-1 menit",
                "positif": "Warna KMnO₄ hilang + endapan coklat MnO₂",
                "negatif": "Warna KMnO₄ tetap ungu",
                "keselamatan": "KMnO₄ dapat menodai; hindari kontak langsung"
            },
            "Uji Pembentukan Alkuna": {
                "emoji": "⚡",
                "prinsip": "Kalsium karbida (CaC₂) + air → etuna + Ca(OH)₂. Etuna bereaksi dengan Br₂ membentuk 1,1,2,2-tetrabromoheksana (larutan berubah tidak berwarna). Etuna teroksidasi KMnO₄ menjadi etanediol (warna hilang + endapan coklat).",
                "pereaksi": "Karbit (CaC₂), Larutan bromin, KMnO₄, K₂Cr₂O₇ 5%, Air suling",
                "prosedur": "1. Masukkan ±2g karbit ke tabung dengan selang\n2. Tambahkan ±1 mL air suling\n3. Alirkan gas ke Br₂, KMnO₄\n4. Amati perubahan warna (gas habis = tambah air lagi)",
                "positif": "Bromin hilang warna; KMnO₄ hilang + endapan coklat",
                "negatif": "Warna larutan tetap",
                "keselamatan": "Reaksi eksotermik; karbit sangat reaktif dengan air"
            },
            "Uji Fisika & Kimia Benzena": {
                "emoji": "♨️",
                "prinsip": "Benzena + HNO₃ pekat + H₂SO₄ pekat → Nitrobenzena (minyak kuning kental, mengendap). Dengan Fe-Br₃ → Bromobenzena (reaksi subsitusi elektrofilik aromatik).",
                "pereaksi": "Benzena, HNO₃ pekat, H₂SO₄ pekat, Air bromin, Logam Fe",
                "prosedur": "Uji Bakar: Teteskan benzena di cawan porselin, bakar\nBrominasi: 4mL benzena + 2mL air bromin + kocok. Pisahkan, tambahkan Fe ke salah satu",
                "positif": "Nyala sooty (jelaga hitam). Brominasi berbeda dengan/tanpa Fe",
                "negatif": "Nyala biru normal",
                "keselamatan": "Benzena karsinogenik; HNO₃/H₂SO₄ korosif kuat"
            }
        }

        for test_name, test_data in test_hydro.items():
            with st.expander(f"{test_data['emoji']} **{test_name}**", expanded=False):
                st.markdown(f"**Prinsip:**  \n{test_data['prinsip']}")
                st.markdown(f"**Pereaksi:**  \n{test_data['pereaksi']}")
                st.markdown(f"**Prosedur:**  \n{test_data['prosedur']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**✅ Positif:**  \n{test_data['positif']}")
                with col_b:
                    st.markdown(f"**❌ Negatif:**  \n{test_data['negatif']}")
                st.warning(f"⚠️ {test_data['keselamatan']}")

    with subcat2:
        st.subheader("🍷 Bab 2: Alkohol, Fenol, Eter")
        st.markdown("---")

        test_alcohol = {
            "Uji Kelarutan Alkohol & Eter": {
                "emoji": "💧",
                "prinsip": "Alkohol rantai pendek larut dalam air (ikatan H). Kelarutan ↑ saat gugus OH ↑. Eter < larut (tidak ada gugus OH).",
                "pereaksi": "Etanol, 1-butanol, 2-butanol, t-butanol, amil alkohol, gliserol, dimetil eter, Air suling",
                "prosedur": "1. Masukkan 1-2 mL air ke tabung\n2. Tambahkan contoh setetes demi setetes sambil dikocok\n3. Catat jumlah tetes sampai terbentuk 2 fase (tidak larut)",
                "positif": "Larutan homogen (larut dalam air)",
                "negatif": "Terbentuk 2 fase (tidak larut)",
                "keselamatan": "Alkohol mudah terbakar; ventilasi baik"
            },
            "Uji Esterifikasi (Pembentukan Aroma)": {
                "emoji": "🍌",
                "prinsip": "Alkohol + asam karboksilat + H₂SO₄ (katalis) → Ester (harum). Gliserol + KHSO₄ (panas) → Akrolein (bau tengik/lemak terbakar).",
                "pereaksi": "Etanol, Amil alkohol, Asam asetat, H₂SO₄ pekat",
                "prosedur": "1. Campur 1mL alkohol + 1mL asam asetat + 5 tetes H₂SO₄\n2. Panaskan 10 menit di penangas air\n3. Tuang ke piala berisi air\n4. Cium aroma dengan teknik wafting",
                "positif": "Aroma khas (etanol=balon/eter; amil=pisang)",
                "negatif": "Tidak ada aroma jelas",
                "keselamatan": "H₂SO₄ korosif; uap mudah menguap—jangan hirup langsung"
            },
            "Uji Ceric Nitrat (Pereaksi Ce)": {
                "emoji": "🔴",
                "prinsip": "Alkohol + Ce⁴⁺ → Kompleks berwarna merah Ce(IV).",
                "pereaksi": "1-butanol, 2-butanol, t-butanol, Fenol, Pereaksi ceric nitrat",
                "prosedur": "1. Masukkan 1 mL contoh ke tabung\n2. Tambahkan 4-5 tetes pereaksi ceric nitrat\n3. Kocok dan amati warna",
                "positif": "Warna merah/oranye terbentuk cepat",
                "negatif": "Tidak ada perubahan warna signifikan",
                "keselamatan": "Pereaksi oksidator; hindari kontak kulit"
            },
            "Uji Lucas (Klasifikasi Alkohol)": {
                "emoji": "⚪",
                "prinsip": "Alkohol + ZnCl₂/HCl → Alkil halida (emulsi putih). Tersier: <1 min | Sekunder: 5-10 min | Primer: >30 min (tidak terbentuk).",
                "pereaksi": "1-butanol, 2-butanol, t-butanol, Pereaksi Lucas (ZnCl₂-HCl)",
                "prosedur": "1. Masukkan 0,5 mL alkohol ke tabung\n2. Tambahkan ±1 mL pereaksi Lucas\n3. Tutup, kocok, catat waktu emulsi putih terbentuk",
                "positif": "Emulsi putih; waktu menunjukkan tingkat alkohol",
                "negatif": "Tetap jernih (alkohol primer)",
                "keselamatan": "HCl pekat korosif; ZnCl₂ iritan"
            },
            "Uji Jones (Oksidasi Alkohol)": {
                "emoji": "🟢",
                "prinsip": "Alkohol primer & sekunder teroksidasi oleh Cr(VI) → asam/keton. Tersier tidak bereaksi. Warna berubah jingga → hijau.",
                "pereaksi": "1-butanol, 2-butanol, t-butanol, Pereaksi Jones (CrO₃-H₂SO₄)",
                "prosedur": "1. Masukkan 1 mL aseton ke 3 tabung\n2. Tambahkan 2 tetes alkohol contoh\n3. Tambahkan 2 tetes pereaksi Jones\n4. Amati warna dalam 15 detik",
                "positif": "Warna hijau kebiruan terbentuk cepat",
                "negatif": "Warna jingga tetap (alkohol tersier/non-reaktif)",
                "keselamatan": "Cr(VI) karsinogenik & toksik; APD lengkap, disposal benar"
            },
            "Uji Iodoform": {
                "emoji": "🟡",
                "prinsip": "Etanol & alkohol sekunder (C-OH terikat pada C yang terikat CH₃) + I₂/NaOH → Iodoform (CHI₃) kuning + garam asam karboksilat.",
                "pereaksi": "Etanol, 2-butanol, Amil alkohol, NaOH 10%, Larutan I₂ (dalam KI)",
                "prosedur": "1. Masukkan 1 mL alkohol ke tabung\n2. Tambahkan 0,5-1 mL NaOH 10%\n3. Tambahkan I₂ setetes demi setetes hingga warna tidak hilang 2 min\n4. Jika perlu, panaskan di penangas air\n5. Amati endapan di dasar",
                "positif": "Endapan kuning kekuningan (CHI₃)",
                "negatif": "Larutan tetap jernih",
                "keselamatan": "I₂ menodai; bau tajam CHI₃ dapat menyebabkan pusing"
            },
            "Uji Kelarutan Fenol": {
                "emoji": "💜",
                "prinsip": "Fenol sedikit larut dalam air (T ruang); kelarutan ↑ saat dipanaskan (ikatan H). Fenol lebih asam dari alkohol (melepaskan H⁺).",
                "pereaksi": "Fenol, Air suling, Kertas lakmus merah/biru",
                "prosedur": "1. Masukkan 1-2 mL air ke tabung\n2. Tambahkan ±0,1g fenol padatan\n3. Amati kelarutan (T ruang)\n4. Panaskan di penangas air, amati lagi\n5. Uji pH dengan lakmus merah & biru",
                "positif": "Fenol larut saat dipanaskan; lakmus merah berubah biru (asam)",
                "negatif": "Tidak larut bahkan saat dipanaskan",
                "keselamatan": "Fenol kaustik; hindari kontak kulit dan pernafasan"
            },
            "Uji Fenol (NaOH, FeCl₃, Bromin)": {
                "emoji": "🔵",
                "prinsip": "Fenol + NaOH → Garam fenolat (putih). Fenol + FeCl₃ → Kompleks berwarna (ungu/hijau/biru/hitam tergantung jenis). Fenol + Br₂ → Difenol bromin (endapan putih).",
                "pereaksi": "Larutan fenol, NaOH, FeCl₃ 1-2%, Larutan bromin",
                "prosedur": "1. Buat larutan fenol di 3 tabung\n2. NaOH: Tambahkan NaOH setetes demi setetes\n3. FeCl₃: Tambahkan 2-5 tetes FeCl₃\n4. Bromin: Tambahkan Br₂ setetes demi setetes\n5. Amati warna & endapan",
                "positif": "NaOH → putih; FeCl₃ → ungu/hijau/biru; Br₂ → hilang warna + endapan putih",
                "negatif": "Tidak ada perubahan signifikan",
                "keselamatan": "FeCl₃ korosif; Br₂ beracun; HCl pekat korosif"
            }
        }

        for test_name, test_data in test_alcohol.items():
            with st.expander(f"{test_data['emoji']} **{test_name}**", expanded=False):
                st.markdown(f"**Prinsip:**  \n{test_data['prinsip']}")
                st.markdown(f"**Pereaksi:**  \n{test_data['pereaksi']}")
                st.markdown(f"**Prosedur:**  \n{test_data['prosedur']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**✅ Positif:**  \n{test_data['positif']}")
                with col_b:
                    st.markdown(f"**❌ Negatif:**  \n{test_data['negatif']}")
                st.warning(f"⚠️ {test_data['keselamatan']}")
    with subcat3:
        st.subheader("🧬 Bab 3: Aldehid & Keton")
        st.markdown("---")

        test_carbony = {
            "Uji Na-Bisulfit": {
                "emoji": "🧊",
                "prinsip": "Aldehid & keton bereaksi dengan Na-bisulfit jenuh membentuk senyawa adisi bisulfit (padatan putih) + pelepasan panas.",
                "pereaksi": "Asetaldehid, Benzaldehida, Aseton, Pereaksi Na-bisulfit jenuh",
                "prosedur": "1. Ke 3 tabung, masukkan 1 mL Na-bisulfit jenuh\n2. Tambahkan ±0,5 mL contoh, kocok kuat\n3. Amati endapan (panaskan jika perlu)\n4. Catat panas yang dihasilkan",
                "positif": "Endapan putih + pelepasan panas",
                "negatif": "Larutan tetap jernih",
                "keselamatan": "SO₂ dapat terlepas; ventilasi baik"
            },
            "Uji Schiff": {
                "emoji": "🟣",
                "prinsip": "Pereaksi Schiff (fuchsin sulfurous) tidak berwarna. Aldehid → magenta/ungu cepat. Keton → lambat/negatif.",
                "pereaksi": "Formaldehida, Asetaldehida, Benzaldehida, Aseton, Pereaksi Schiff",
                "prosedur": "1. Ke tabung, masukkan 1 mL pereaksi Schiff\n2. Tambahkan beberapa tetes contoh\n3. Catat warna & kecepatan reaksi",
                "positif": "Warna ungu/magenta cepat (aldehid) atau lambat (keton)",
                "negatif": "Tetap pink pucat",
                "keselamatan": "Pewarna organik; hindari kontak kulit"
            },
            "Uji Fehling": {
                "emoji": "🧱",
                "prinsip": "Aldehid + Cu²⁺ (Fehling A+B) → Cu₂O merah bata (endapan). Keton tidak bereaksi.",
                "pereaksi": "Asetaldehida, Benzaldehida, Aseton, Fehling A, Fehling B",
                "prosedur": "1. Masukkan 0,5 mL contoh ke tabung\n2. Campur Fehling A+B (1:1 saat digunakan)\n3. Tambahkan ke contoh\n4. Panaskan 5 menit di penangas air\n5. Amati endapan",
                "positif": "Endapan merah bata Cu₂O",
                "negatif": "Tetap biru (atau endapan coklat)",
                "keselamatan": "Larutan basa; hindari kontak mata"
            },
            "Uji Tollens (Cermin Perak)": {
                "emoji": "🪞",
                "prinsip": "Aldehid + Ag⁺ (pereaksi Tollens) → Ag logam (cermin perak/hitam menempel dinding). Keton tidak bereaksi.",
                "pereaksi": "Asetaldehida, Benzaldehida, Aseton, AgNO₃ 5%, NaOH 10%, NH₄OH encer",
                "prosedur": "1. Masukkan ±5 mL pereaksi Tollens ke 3 tabung\n2. Tambahkan contoh setetes demi setetes\n3. Panaskan di penangas air jika perlu\n4. Amati cermin perak pada dinding tabung",
                "positif": "Endapan Ag (cermin perak/hitam) menempel dinding",
                "negatif": "Tetap jernih atau endapan coklat",
                "keselamatan": "Tollens stabil ~2 hari; jangan simpan lama (risiko ledakan)"
            }
        }

        for test_name, test_data in test_carbony.items():
            with st.expander(f"{test_data['emoji']} **{test_name}**", expanded=False):
                st.markdown(f"**Prinsip:**  \n{test_data['prinsip']}")
                st.markdown(f"**Pereaksi:**  \n{test_data['pereaksi']}")
                st.markdown(f"**Prosedur:**  \n{test_data['prosedur']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**✅ Positif:**  \n{test_data['positif']}")
                with col_b:
                    st.markdown(f"**❌ Negatif:**  \n{test_data['negatif']}")
                st.warning(f"⚠️ {test_data['keselamatan']}")

    with subcat4:
        st.subheader("🔗 Bab 4: Halogen Organik (Alkil Halida)")
        st.markdown("---")

        test_halogen = {
            "Pembuatan Halogen Organik (Iodometana)": {
                "emoji": "⚡",
                "prinsip": "Alkohol + I₂/NaOH → Alkil halida (iodometana atau iodoalkana) yang tidak larut air (endapan kuning).",
                "pereaksi": "Etanol, 2-butanol, NaOH 10%, Larutan I₂ (dalam KI)",
                "prosedur": "1. Masukkan 1 mL alkohol ke tabung\n2. Tambahkan 0,5 mL NaOH 10%\n3. Tambahkan I₂ setetes demi setetes hingga warna tidak hilang 2 min\n4. Jika belum ada endapan, panaskan\n5. Dekantasi/filtrasi endapan\n6. Amati warna endapan",
                "positif": "Endapan kuning/coklat (iodometana/iodoalkana)",
                "negatif": "Larutan tetap jernih",
                "keselamatan": "I₂ menodai; bau kuat; ventilasi baik"
            },
            "Uji Kelarutan Halogen Organik": {
                "emoji": "💧",
                "prinsip": "Alkil halida sedikit polar → sedikit larut air, tetapi larut dalam pelarut nonpolar (aseton, CCl₄, minyak).",
                "pereaksi": "Iodometana, Kloroform, Air suling, Aseton",
                "prosedur": "1. Masukkan 1 mL pelarut (air atau aseton) ke tabung\n2. Tambahkan iodometana/kloroform sedikit demi sedikit\n3. Kocok dan amati kelarutan\n4. Ulangi dengan pelarut berbeda",
                "positif": "Larut dalam aseton; tidak larut dalam air (terbentuk 2 fase)",
                "negatif": "Terbentuk 2 fase dalam kedua pelarut",
                "keselamatan": "Iodometana & kloroform volatil; ventilasi baik"
            },
            "Uji Bakar Halogen Organik": {
                "emoji": "🔥",
                "prinsip": "Halogen organik dibakar → nyala yang berbeda (ada halogen → nyala hijau terang/chlorine flame).",
                "pereaksi": "Iodometana, Kloroform",
                "prosedur": "1. Ambil ±0,01g iodometana atau 2-3 tetes kloroform\n2. Letakkan di cawan porselin\n3. Bakar dengan api langsung di ruang asam\n4. Amati warna nyala",
                "positif": "Nyala hijau terang (chlorine flame) atau nyala kuning berkabut (iodine)",
                "negatif": "Nyala biasa/biru (tanpa halogen)",
                "keselamatan": "Kerjakan di lemari asam; produk pembakaran HCl/HI beracun"
            },
            "Uji Larutan Perak Nitrat (AgNO₃)": {
                "emoji": "⚪",
                "prinsip": "Alkil halida + AgNO₃ dalam alkohol → Endapan Ag-halida putih/kuning (AgCl putih, AgBr krem, AgI kuning).",
                "pereaksi": "Iodometana, Kloroform, AgNO₃ 0,1 M, Aseton",
                "prosedur": "1. Masukkan ±0,01g iodometana ke tabung\n2. Tambahkan 1 mL aseton\n3. Tambahkan 1 mL AgNO₃ dan homogenkan\n4. Amati warna endapan yang terbentuk\n5. Ulangi dengan kloroform",
                "positif": "Endapan putih (AgCl), krem (AgBr), atau kuning (AgI) terbentuk cepat",
                "negatif": "Larutan tetap jernih",
                "keselamatan": "AgNO₃ menodai hitam; hindari kontak kulit"
            }
        }

        for test_name, test_data in test_halogen.items():
            with st.expander(f"{test_data['emoji']} **{test_name}**", expanded=False):
                st.markdown(f"**Prinsip:**  \n{test_data['prinsip']}")
                st.markdown(f"**Pereaksi:**  \n{test_data['pereaksi']}")
                st.markdown(f"**Prosedur:**  \n{test_data['prosedur']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**✅ Positif:**  \n{test_data['positif']}")
                with col_b:
                    st.markdown(f"**❌ Negatif:**  \n{test_data['negatif']}")
                st.warning(f"⚠️ {test_data['keselamatan']}")

    # -----------------------
    # Bab 5: Amina
    # -----------------------
    with subcat5:
        st.subheader("Bab 5 — Uji Amina & Derivat")
        st.markdown("Ringkasan uji: kelarutan, Hinsberg, diazotisasi, kopling, uji nitril/amida.")
        tests_bab5 = {
            "Uji Kelarutan & Kebasaan": {
                "prinsip": "Amina primer/sekunder/tersier: kelarutan & pH; amina bersifat basa.",
                "prosedur": "Masukkan contoh ke air, catat kelarutan; uji pH dengan kertas pH.",
            },
            "Uji Hinsberg (Benzensulfonil klorida)": {
                "prinsip": "Bedakan amina primer/sekunder/tersier berdasarkan produk sulfonamida.",
                "prosedur": "Reaksikan dengan benzensulfonil klorida, tambah NaOH/HCl untuk pengamatan kelarutan/padatan.",
            },
            "Reaksi Diazotisasi & Kopling": {
                "prinsip": "Amina aromatik membentuk garam diazonium yang dapat digunakan untuk reaksi kopling (azo).",
                "prosedur": "Lakukan diazotisasi pada 0–5°C lalu lakukan reaksi kopling dengan β-naftol atau fenol.",
            },
        }
        for name, d in tests_bab5.items():
            with st.expander(f"🔎 {name}", expanded=False):
                st.markdown(f"**Prinsip:**  \n{d['prinsip']}")
                st.markdown(f"**Prosedur (singkat):**  \n{d['prosedur']}")

    # -----------------------
    # Bab 6: Lemak & Minyak
    # -----------------------
    with subcat6:
        st.subheader("Bab 6 — Uji Lemak dan Minyak")
        st.markdown("Uji kelarutan, penyabunan, ketidakjenuhan & ketengikan.")
        tests_bab6 = {
            "Uji Kelarutan": {
                "prinsip": "Minyak/lemak larut dalam pelarut nonpolar; kelarutan berbeda antar pelarut.",
                "prosedur": "Uji kelarutan contoh pada air, etanol, eter, kloroform; catat hasil.",
            },
            "Reaksi Penyabunan (Saponifikasi)": {
                "prinsip": "Hidrolisis ester lemak oleh NaOH → sabun (garam asam lemak).",
                "prosedur": "Reaksikan contoh dengan NaOH 5%, panaskan, amati pembentukan sabun/gas.",
            },
            "Uji Ketidakjenuhan (Iod Hubl) & Ketengikan (Kreis)": {
                "prinsip": "Iod Hubl menyerap ikatan rangkap; uji Kreis mendeteksi aldehida ketengikan.",
                "prosedur": "Tambahkan larutan Iod Hubl atau lakukan prosedur Kreis sesuai protokol.",
            },
        }
        for name, d in tests_bab6.items():
            with st.expander(f"🔎 {name}", expanded=False):
                st.markdown(f"**Prinsip:**  \n{d['prinsip']}")
                st.markdown(f"**Prosedur (singkat):**  \n{d['prosedur']}")

    # -----------------------
    # Bab 7: Karbohidrat
    # -----------------------
    with subcat7:
        st.subheader("Bab 7 — Uji Karbohidrat")
        st.markdown("Molisch, Seliwanoff, Benedict, Moore, Barfoed, iodium — ringkasan uji warna & reduksi.")
        tests_bab7 = {
            "Uji Molisch": {
                "prinsip": "Dehidrasi karbohidrat → furfural → kompleks ungu dengan α-naftol.",
                "prosedur": "Tambahkan α-naftol lalu H₂SO₄; amati cincin ungu pada antarmuka.",
            },
            "Uji Seliwanoff / Bial / Benedict / Moore": {
                "prinsip": "Membedakan ketosa/aldosa & gula pereduksi.",
                "prosedur": "Lakukan uji sesuai reagen: Seliwanoff (resorsinol+HCl), Benedict (panas), Moore (basa+panas).",
            },
            "Uji Iodium (pati)": {
                "prinsip": "Iodium membentuk kompleks dengan amilosa → warna biru/ungu.",
                "prosedur": "Tambahkan satu tetes larutan iodium 0.1 N ke contoh pati; amati warna.",
            },
        }
        for name, d in tests_bab7.items():
            with st.expander(f"🔎 {name}", expanded=False):
                st.markdown(f"**Prinsip:**  \n{d['prinsip']}")
                st.markdown(f"**Prosedur (singkat):**  \n{d['prosedur']}")

    # -----------------------
    # Bab 8: Protein
    # -----------------------
    with subcat8:
        st.subheader("Bab 8 — Uji Protein & Asam Amino")
        st.markdown("Biuret, Ninhidrin, Xanthoprotein, Millon, Hopkins-Cole — ringkasan uji protein.")
        tests_bab8 = {
            "Uji Biuret": {
                "prinsip": "Peptida/ikatan peptida bereaksi → kompleks ungu dengan Cu²⁺ dalam basa.",
                "prosedur": "Tambahkan NaOH + CuSO₄; amati warna ungu.",
            },
            "Uji Ninhidrin": {
                "prinsip": "Ninhidrin bereaksi dengan gugus α-amino → Ruhemann's purple (ungu).",
                "prosedur": "Tambah ninhidrin ke sampel, panaskan; amati warna ungu (prolin → kuning).",
            },
            "Uji Xanthoprotein / Millon / Hopkins-Cole": {
                "prinsip": "Uji gugus aromatik (tyrosine/tryptophan/phenylalanine) → warna khas.",
                "prosedur": "Lakukan uji masing‑masing dengan HNO₃ (xanthoprotein), Millon, atau asam glioksalat (Hopkins‑Cole).",
            },
        }
        for name, d in tests_bab8.items():
            with st.expander(f"🔎 {name}", expanded=False):
                st.markdown(f"**Prinsip:**  \n{d['prinsip']}")
                st.markdown(f"**Prosedur (singkat):**  \n{d['prosedur']}")

# =============================================================
# HALAMAN: Reaksi
# =============================================================
elif st.session_state.page == "Reaksi":
    st.title("📚 Panduan Praktikum Reaksi Kimia Organik")
    st.markdown("Panduan lengkap praktikum kimia organik dengan gambar hasil percobaan.")
    st.divider()
    
    # Struktur data untuk konten dari HTML
    reaksi_content = {
        "Bab 1. Hidrokarbon": {
            "Percobaan 1. Pembuatan dan Uji Kimia Alkana": ["image001.jpg", "images/image002.jpg"],
            "Percobaan 2. Larutan Brom dalam Karbon Tetra Klorida atau Kloroform": ["images/image003.jpg", "images/image004.jpg"],
            "Percobaan 3. Uji Bayer": ["images/image005.jpg", "images/image006.jpg", "images/image007.jpg", "images/image008.jpg"],
            "Percobaan 4. Pembuatan dan uji kimia alkuna": ["images/image009.jpg", "images/image010.jpg"],
            "Percobaan 5. Uji Fisika dan Kimia Benzena": ["images/image011.jpg", "images/image012.jpg"],
        },
        "Bab 2. Alkohol, Fenol, Eter, Halogen Organik": {
            "Percobaan 1. Uji Kelarutan Alkohol, Eter": ["images/image013.jpg", "images/image014.jpg"],
            "Percobaan 2. Pembentukan Senyawa Beraroma": ["images/image015.jpg", "images/image016.jpg"],
            "Percobaan 3. Pereaksi Ceric Nitrat": ["images/image017.jpg", "images/image018.jpg"],
            "Percobaan 4. Pereaksi Lucas": ["images/image019.jpg", "images/image020.jpg"],
            "Percobaan 5. Pereaksi Jones": ["images/image021.jpg", "images/image022.jpg"],
            "Percobaan 6. Uji Iodoform": ["images/image023.jpg", "images/image024.jpg"],
            "Percobaan 7. Uji Kelarutan dan Keasaman Fenol": ["images/image025.jpg", "images/image026.jpg"],
            "Percobaan 8. Uji dengan NaOH, FeCl₃ dan Larutan Brom": {
                "NaOH": ["images/image027.jpg", "images/image028.jpg"],
                "FeCl₃": ["images/image029.jpg", "images/image030.jpg"],
                "Larutan Brom": ["images/image031.jpg", "images/image032.jpg"],
            },
            "Percobaan 10. Uji Kelarutan, Uji Bakar Dan Uji Larutan Perak Nitrat Pada Senyawa Halogen Organik": ["images/image033.jpg", "images/image034.jpg"],
        },
        "Bab 3. Aldehid Dan Keton": {
            "Percobaan 1. Pereaksi Na-bisulfit": ["images/image035.jpg", "images/image036.jpg"],
            "Percobaan 2. Pereaksi Schiff": ["images/image037.jpg", "images/image038.jpg"],
            "Percobaan 3. Pereaksi Fehling": ["images/image039.jpg", "images/image040.jpg"],
            "Percobaan 4. Pereaksi Tollens": ["images/image041.jpg", "images/image042.jpg"],
        },
        "Bab 4. Asam karboksilat dan derivatnya": {
            "Percobaan 1. Pembentukan Asam Karboksilat dan Derivatnya": ["images/image043.jpg", "images/image044.jpg"],
            "Percobaan 2. Reaksi Penggaraman": ["images/image045.jpg", "images/image046.jpg"],
            "Percobaan 3. Reaksi oksidasi asam karboksilat": ["images/image047.jpg", "images/image048.jpg"],
            "Percobaan 4. Identifikasi ester dan anhidrida": ["images/image049.jpg", "images/image050.jpg"],
        },
        "Bab 5. Senyawa Amina dan derivatnya": {
            "Percobaan 1. Uji Kelarutan dan Kebasaan": ["images/image051.jpg", "images/image052.jpg"],
            "Percobaan 2. Pereaksi Benzensulfonil klorida (uji Hinsberg)": ["images/image053.jpg", "images/image054.jpg"],
            "Percobaan 3. Reaksi diazotisasi, kestabilan garam diazonium dan reaksi kopling": ["images/image055.jpg", "images/image056.jpg", "images/image057.jpg", "images/image058.jpg"],
            "Percobaan 4. Uji senyawa nitril dan amida": {
                "Nitril": ["images/image059.jpg", "images/image060.jpg"],
                "Amida": ["images/image061.jpg", "images/image062.jpg"],
            },
        },
        "Bab 6. Senyawa lemak dan minyak": {
            "Percobaan 2. Reaksi penyabunan": ["images/image063.jpg", "images/image064.jpg"],
            "Percobaan 3. Uji ketidakjenuhan dan ketengikan": {
                "Ketidakjenuhan": ["images/image065.jpg", "images/image066.jpg"],
                "Ketengikan": ["images/image067.jpg", "images/image068.jpg"],
            },
        },
        "Bab 7. Karbohidrat": {
            "Percobaan 1. Uji Warna Karbohidrat": {
                "Molisch": ["images/image069.jpg", "images/image070.jpg"],
                "Selliwanof dan Bial's": ["images/image071.jpg", "images/image072.jpg"],
            },
            "Percobaan 2. Uji Daya Reduksi Gula Pereduksi dan Non Pereduksi": {
                "Benedict": ["images/image073.jpg", "images/image074.jpg"],
                "Moore": ["images/image075.jpg", "images/image076.jpg"],
                "Barfoed": ["images/image077.jpg", "images/image078.jpg"],
                "Iodium": ["images/image079.jpg", "images/image080.jpg"],
            },
        },
        "Bab 8. Protein": {
            "Percobaan 1. Uji Umum Protein dan Asam Amino": {
                "Biuret": ["images/image081.jpg", "images/image082.jpg"],
                "Ninhidrin": ["images/image083.jpg", "images/image084.jpg"],
            },
            "Percobaan 2. Uji warna Protein dan Asam Amino": {
                "Xanthoprotein": ["images/image085.jpg", "images/image086.jpg"],
                "Millon": ["images/image087.jpg", "images/image088.jpg"],
                "Hopkins-cole": ["images/image089.jpg", "images/image090.jpg"],
            },
        },
    }
    
    # Buat tabs untuk setiap bab
    bab_tabs = st.tabs(list(reaksi_content.keys()))
    
    for idx, (bab_name, percobaan_dict) in enumerate(reaksi_content.items()):
        with bab_tabs[idx]:
            st.subheader(bab_name)
            st.divider()
            
            for percobaan_name, images in percobaan_dict.items():
                with st.expander(f"🔬 {percobaan_name}", expanded=False):
                    # Jika images adalah dict (ada sub-percobaan)
                    if isinstance(images, dict):
                        for sub_name, sub_images in images.items():
                            st.markdown(f"**{sub_name}**")
                            cols = st.columns(min(len(sub_images), 3))
                            for i, img_path in enumerate(sub_images):
                                actual_path = get_image_path(img_path)
                                try:
                                    # Coba load gambar - Streamlit akan handle error jika tidak ditemukan
                                    with cols[i % len(cols)]:
                                        st.image(actual_path, use_container_width=True, caption=f"{sub_name} - Gambar {i+1}")
                                except Exception as e:
                                    st.warning(f"Gambar tidak ditemukan: {img_path}")
                            st.divider()
                    else:
                        # Jika images adalah list langsung
                        cols = st.columns(min(len(images), 3))
                        for i, img_path in enumerate(images):
                            actual_path = get_image_path(img_path)
                            try:
                                # Coba load gambar - Streamlit akan handle error jika tidak ditemukan
                                with cols[i % len(cols)]:
                                    st.image(actual_path, use_container_width=True, caption=f"Gambar {i+1}")
                            except Exception as e:
                                st.warning(f"Gambar tidak ditemukan: {img_path}")

# =============================================================
# HALAMAN: Istilah Penting
# =============================================================
elif st.session_state.page == "Istilah Penting":
    st.title("📗 Istilah Penting")
    st.markdown("Berikut beberapa istilah yang sering muncul dalam praktikum identifikasi senyawa organik.")
    
    glossary = {
        "Endapan": "Fase padat yang terbentuk dari larutan akibat reaksi kimia.",
        "Emulsi": "Campuran dua fase tak saling larut (misal minyak-air) menghasilkan kekeruhan.",
        "Reagen": "Bahan kimia yang digunakan untuk mendeteksi, mengukur, atau memproduksi senyawa tertentu.",
        "Positif": "Ada respon kimia yang konsisten dengan keberadaan gugus fungsi yang diuji.",
        "Negatif": "Tidak ada respon spesifik untuk gugus fungsi tersebut.",
        "Gugus Fungsi": "Kelompok atom dengan sifat kimia khas yang menentukan sifat suatu senyawa.",
        "Senyawa Organik": "Senyawa yang mengandung karbon sebagai unsur utama.",
    }
    
    for term, definition in glossary.items():
        st.markdown(f"**{term}**  \n{definition}")

# =============================================================
# FOOTER
# =============================================================
st.divider()
st.caption("🔬 Aplikasi Identifikasi Senyawa Organik | Dibuat Oleh Kelompok 8 : Dimas Ridho N.A.A (2450153), Hilmy Azry (2460165), Marthin Luther S. (2450178), Nayla Putri Zena (2350194), Zahwa Syahira Alfiliana (2450208)")
st.caption("Sumber : Irawan, C., Putri, I. D., Rahmatia, L., & Utami, A. (2025) Identifikasi secara kimia gugus fungsi senyawa organik. Yogyakarta: Deepublish. | Kartini Afriani, & Utami, A. (2021). Penuntun praktikum kimia organik. Bogor: Politeknik AKA Bogor, Kementerian Perindustrian Republik Indonesia.")
