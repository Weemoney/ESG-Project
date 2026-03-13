import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.biodiversity import calculate_biodiversity_score

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Sehat Alam Indonesia",
    page_icon="🌿",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E8F5E9;
        margin-bottom: 1rem;
        height: 100%;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .card-body {
        font-size: 0.88rem;
        color: #444;
        line-height: 1.7;
    }
    .verdict {
        font-size: 1rem;
        font-weight: 500;
        padding: 0.85rem 1.25rem;
        border-radius: 10px;
        margin: 0.5rem 0 1rem 0;
    }
    .verdict-baik   { background: #E8F5E9; color: #1B5E20; border-left: 4px solid #43A047; }
    .verdict-sedang { background: #FFF8E1; color: #E65100; border-left: 4px solid #FFA000; }
    .verdict-kritis { background: #FFEBEE; color: #B71C1C; border-left: 4px solid #E53935; }
</style>
""", unsafe_allow_html=True)

# ── Data provinsi ─────────────────────────────────────────────────
PROVINCE_DATA = {
    "Papua": {
        "species": ["Sp_A"]*50+["Sp_B"]*30+["Sp_C"]*20+["Sp_D"]*15+["Sp_E"]*10+["Sp_F"]*8+["Sp_G"]*5,
        "air_note": "Sungai-sungai besar Papua seperti Mamberamo dan Digul masih sangat bersih karena hutan di sekitarnya belum banyak terganggu. Air ini adalah sumber kehidupan jutaan warga dan ekosistem unik yang tidak ditemukan di tempat lain di dunia.",
        "udara_note": "Tutupan hutan Papua yang masih sangat luas berperan sebagai paru-paru yang menyerap karbon dan menghasilkan oksigen. Kualitas udara di sini termasuk terbaik di Indonesia — jauh dari polusi industri dan kendaraan.",
        "tanah_note": "Tanah Papua kaya mineral dan organik karena ribuan tahun akumulasi humus hutan hujan. Ini yang membuat pertanian tradisional masyarakat adat bisa bertahan tanpa pupuk kimia sejak lama.",
    },
    "Kalimantan Tengah": {
        "species": ["Sp_A"]*45+["Sp_B"]*35+["Sp_C"]*25+["Sp_D"]*12+["Sp_E"]*8,
        "air_note": "Sungai Kahayan dan Barito masih menjadi urat nadi kehidupan warga. Namun ekspansi perkebunan sawit di hulu mulai mengancam kualitas air — sedimentasi meningkat dan beberapa anak sungai mulai keruh.",
        "udara_note": "Kebakaran gambut yang berulang setiap musim kemarau — sebagian besar dipicu pembukaan lahan — membuat kualitas udara turun drastis dan merugikan kesehatan jutaan warga setiap tahunnya.",
        "tanah_note": "Lahan gambut Kalimantan Tengah adalah salah satu penyimpan karbon terbesar di dunia. Ketika dikonversi ke perkebunan, gambut mengering, mudah terbakar, dan melepaskan karbon dalam jumlah besar.",
    },
    "DKI Jakarta": {
        "species": ["Sp_A"]*8+["Sp_B"]*6+["Sp_C"]*3,
        "air_note": "Jakarta hampir tidak punya sumber air bersih mandiri. Sekitar 40% warga masih bergantung pada air tanah yang kualitasnya terus memburuk akibat intrusi air laut dan kontaminasi limbah.",
        "udara_note": "Jakarta konsisten masuk daftar kota dengan kualitas udara terburuk di dunia. Hilangnya ruang hijau, kepadatan kendaraan, dan aktivitas industri membuat udara Jakarta berbahaya terutama bagi anak-anak dan lansia.",
        "tanah_note": "Jakarta mengalami penurunan tanah hingga 25 cm per tahun di beberapa titik — salah satu tercepat di dunia. Ini terjadi karena pengambilan air tanah berlebihan akibat minimnya sumber air permukaan yang sehat.",
    },
    "Jawa Barat": {
        "species": ["Sp_A"]*20+["Sp_B"]*15+["Sp_C"]*8+["Sp_D"]*4,
        "air_note": "DAS Citarum yang melayani jutaan orang sempat masuk daftar sungai paling tercemar di dunia. Hutan di pegunungan selatan yang menampung air hujan terus menyusut karena alih fungsi lahan.",
        "udara_note": "Dengan kepadatan industri dan kendaraan yang sangat tinggi, kualitas udara di kawasan industri Jawa Barat termasuk yang paling buruk di Indonesia.",
        "tanah_note": "Tanah pertanian Jawa Barat mengalami degradasi akibat penggunaan pupuk kimia jangka panjang dan erosi. Beberapa wilayah yang dulunya sawah produktif kini berubah menjadi kawasan industri.",
    },
    "Aceh": {
        "species": ["Sp_A"]*30+["Sp_B"]*22+["Sp_C"]*14,
        "air_note": "Hutan Leuser yang membentang di Aceh adalah salah satu sumber air terpenting di Sumatera. Sungai-sungai yang mengalir dari Leuser menghidupi pertanian dan kebutuhan sehari-hari jutaan warga.",
        "udara_note": "Aceh masih memiliki kualitas udara yang relatif baik berkat luasnya Kawasan Ekosistem Leuser yang menyerap jutaan ton karbon per tahun.",
        "tanah_note": "Tanah di kawasan sekitar Leuser sangat subur dan mendukung pertanian kopi, kakao, dan padi. Deforestasi di batas kawasan mulai menyebabkan erosi dan banjir di hilir.",
    },
    "Bali": {
        "species": ["Sp_A"]*14+["Sp_B"]*10+["Sp_C"]*5,
        "air_note": "Sistem subak Bali yang diakui UNESCO bergantung sepenuhnya pada mata air dari hutan di pegunungan tengah. Pariwisata massal mengancam ketersediaan air karena hotel dan resort menyedot air tanah berlebihan.",
        "udara_note": "Kualitas udara Bali terus memburuk seiring pertumbuhan kendaraan dan konstruksi. Ironis karena wisatawan datang justru untuk menikmati keindahan alam yang perlahan hilang.",
        "tanah_note": "Alih fungsi sawah untuk pembangunan villa dan hotel menghancurkan lanskap pertanian Bali yang ikonik dan mengancam ketahanan pangan serta tradisi bertani yang sudah berumur ribuan tahun.",
    },
    "Maluku": {
        "species": ["Sp_A"]*28+["Sp_B"]*20+["Sp_C"]*12+["Sp_D"]*6,
        "air_note": "Kepulauan Maluku dikelilingi laut yang masih relatif sehat dengan terumbu karang yang kaya. Air laut yang bersih ini adalah fondasi kehidupan nelayan dan budidaya laut yang menjadi tulang punggung ekonomi lokal.",
        "udara_note": "Maluku memiliki kualitas udara yang sangat baik berkat minimnya industri berat dan masih luasnya tutupan hutan. Angin laut yang segar menciptakan iklim mikro yang nyaman.",
        "tanah_note": "Tanah Maluku subur dan cocok untuk rempah-rempah yang secara historis membuat kepulauan ini diperebutkan bangsa-bangsa dunia. Pertanian rempah tradisional yang ramah lingkungan masih menjaga kesuburan tanah.",
    },
    "Nusa Tenggara Timur": {
        "species": ["Sp_A"]*15+["Sp_B"]*11+["Sp_C"]*5,
        "air_note": "NTT adalah salah satu wilayah paling kering di Indonesia. Deforestasi yang terus berlanjut memperparah kekeringan karena tidak ada lagi hutan yang menampung air hujan. Krisis air bersih di NTT adalah krisis kemanusiaan yang nyata.",
        "udara_note": "Kebakaran hutan dan lahan yang terjadi tiap tahun menghasilkan asap yang mengganggu kesehatan dan pertanian warga NTT.",
        "tanah_note": "Tanah NTT yang sudah kering semakin rentan terhadap erosi akibat minimnya tutupan vegetasi. Lahan pertanian produktif terus menyusut, memaksa banyak warga bermigrasi ke kota.",
    },
    "Sulawesi Tengah": {
        "species": ["Sp_A"]*32+["Sp_B"]*22+["Sp_C"]*14+["Sp_D"]*7,
        "air_note": "Danau Poso dan Danau Lindu adalah ekosistem air tawar unik dengan spesies endemik yang tidak ada di tempat lain di dunia. Kesehatan hutan di sekitarnya langsung mempengaruhi kualitas air bagi warga.",
        "udara_note": "Sulawesi Tengah masih memiliki tutupan hutan yang cukup baik di wilayah pedalaman. Namun aktivitas pertambangan nikel yang berkembang pesat mulai mengancam kualitas udara di beberapa kabupaten.",
        "tanah_note": "Penambangan nikel yang masif meninggalkan lahan gundul yang sulit dipulihkan dan rentan terhadap longsor saat musim hujan.",
    },
    "Sumatera Utara": {
        "species": ["Sp_A"]*28+["Sp_B"]*20+["Sp_C"]*12,
        "air_note": "Danau Toba — danau vulkanik terbesar di dunia — adalah sumber air dan identitas Sumatera Utara. Aktivitas budidaya ikan keramba yang berlebihan mulai menurunkan kualitas air danau.",
        "udara_note": "Kualitas udara di Medan dan sekitarnya cukup tercemar oleh kendaraan dan industri. Sementara wilayah pegunungan Batak masih memiliki udara segar yang menjadi daya tarik wisata.",
        "tanah_note": "Konversi hutan menjadi perkebunan sawit dan karet skala besar telah mengubah struktur tanah secara signifikan. Tanah yang dulunya kaya humus kini bergantung pada pupuk kimia.",
    },
}

DEFAULT_DATA = {
    "species": ["Sp_A"]*15+["Sp_B"]*10+["Sp_C"]*5,
    "air_note": "Data detail untuk wilayah ini sedang dalam pengembangan.",
    "udara_note": "Data detail untuk wilayah ini sedang dalam pengembangan.",
    "tanah_note": "Data detail untuk wilayah ini sedang dalam pengembangan.",
}

ALL_PROVINCES = sorted([
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi",
    "Sumatera Selatan", "Bengkulu", "Lampung",
    "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan",
    "Kalimantan Timur", "Kalimantan Utara",
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara",
    "Jawa Barat", "Jawa Tengah", "Jawa Timur", "DKI Jakarta",
    "DI Yogyakarta", "Banten",
    "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur",
    "Maluku", "Maluku Utara", "Papua", "Papua Barat",
])

# ── Helpers ───────────────────────────────────────────────────────
def kondisi(score):
    if score >= 70: return "Baik", "🟢", "verdict-baik"
    if score >= 40: return "Perlu Perhatian", "🟡", "verdict-sedang"
    return "Kritis", "🔴", "verdict-kritis"

def indikator_alam(bio_score):
    air   = round(min(bio_score * 1.05, 100), 1)
    udara = round(min(bio_score * 0.98, 100), 1)
    tanah = round(min(bio_score * 1.02, 100), 1)
    return air, udara, tanah

# ── Header ────────────────────────────────────────────────────────
st.markdown("## 🌿 Seberapa Sehat Alam Indonesia?")
st.markdown(
    "Pilih sebuah wilayah dan lihat kondisi air, udara, dan tanahnya — "
    "serta apa artinya bagi kehidupan masyarakat di sana."
)
st.divider()

# ── Province selector ─────────────────────────────────────────────
province = st.selectbox(
    "Pilih wilayah yang ingin kamu jelajahi:",
    ALL_PROVINCES,
    index=ALL_PROVINCES.index("Kalimantan Tengah"),
)

data = PROVINCE_DATA.get(province, DEFAULT_DATA)
bio  = calculate_biodiversity_score(data["species"])
score = bio["biodiversity_score"]
air_s, udara_s, tanah_s = indikator_alam(score)

# ── Overall verdict ───────────────────────────────────────────────
label, emoji, css = kondisi(score)
st.markdown(f"""
<div class="verdict {css}">
    {emoji} Kondisi alam <strong>{province}</strong>: <strong>{label}</strong>
    &nbsp;·&nbsp; Skor keberagaman hayati: <strong>{score}/100</strong>
</div>
""", unsafe_allow_html=True)

# ── Tiga kartu ────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

for col, icon, label_ind, score_ind, note in [
    (col1, "🌊", "Air",   air_s,   data["air_note"]),
    (col2, "💨", "Udara", udara_s, data["udara_note"]),
    (col3, "🌱", "Tanah", tanah_s, data["tanah_note"]),
]:
    lbl, emj, _ = kondisi(score_ind)
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{icon} {label_ind} &nbsp; {emj} {lbl} &nbsp;
                <span style="color:#888;font-weight:400;font-size:0.85rem">{score_ind}/100</span>
            </div>
            <div class="card-body">{note}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Narasi dampak ─────────────────────────────────────────────────
st.markdown("#### Apa artinya ini bagi kehidupan di sana?")

if score >= 70:
    st.success(
        f"Alam {province} masih dalam kondisi yang relatif sehat. "
        f"Artinya air yang diminum warga, udara yang dihirup, dan tanah yang ditanami "
        f"masih terjaga dengan baik. Ini bukan sesuatu yang bisa dianggap remeh — "
        f"banyak wilayah lain di Indonesia sudah kehilangan fondasi alam ini."
    )
elif score >= 40:
    st.warning(
        f"Alam {province} sedang dalam tekanan. Beberapa indikator menunjukkan tanda-tanda "
        f"degradasi yang perlu segera diperhatikan. Kalau tidak ada tindakan, "
        f"kualitas air, udara, dan tanah akan terus memburuk — dan dampaknya "
        f"paling dirasakan oleh masyarakat yang hidupnya paling bergantung pada alam."
    )
else:
    st.error(
        f"Alam {province} dalam kondisi kritis. Fondasi ekologis wilayah ini sudah sangat "
        f"terganggu. Ini bukan hanya masalah lingkungan — ini masalah keberlangsungan "
        f"hidup masyarakat yang bergantung pada air bersih, udara sehat, "
        f"dan tanah yang masih bisa ditanami."
    )

st.divider()

# ── Angka di balik layar ──────────────────────────────────────────
with st.expander("📊 Angka di balik layar"):
    st.caption(
        "Dashboard ini menggunakan keberagaman spesies sebagai cerminan kesehatan ekosistem. "
        "Semakin beragam makhluk hidup di suatu wilayah, semakin sehat air, udara, dan tanahnya."
    )
    c1, c2 = st.columns(2)
    c1.metric("Indeks Keberagaman Spesies", f"{bio['shannon_raw']:.2f}")
    c1.metric("Jumlah Jenis Makhluk Hidup", bio['richness_raw'])
    c2.metric("Skor Keberagaman", f"{bio['shannon_normalized']:.1f}/100")
    c2.metric("Skor Kelimpahan", f"{bio['richness_normalized']:.1f}/100")
    st.caption("⚠️ Data spesies saat ini masih simulasi. Data GBIF nyata akan segera diintegrasikan.")

# ── Footer ────────────────────────────────────────────────────────
st.divider()
st.caption("🌿 Sehat Alam Indonesia · Open source · Data: GBIF · Dibuat untuk edukasi publik")