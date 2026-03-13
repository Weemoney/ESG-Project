INDUSTRIES = {
    # ── VERY HIGH IMPACT ─────────────────────────────────────────
    "Pertambangan (Batu Bara, Nikel, dll)": {
        "impact_weight": 1.0,
        "dependency_weight": 0.7,
        "note": "Ekstraksi langsung mengubah bentang alam dan menghancurkan habitat."
    },
    "Minyak & Gas Bumi": {
        "impact_weight": 0.95,
        "dependency_weight": 0.6,
        "note": "Risiko tumpahan, pencemaran tanah dan air, deforestasi untuk akses."
    },
    "Kehutanan Komersial / HPH": {
        "impact_weight": 0.9,
        "dependency_weight": 0.85,
        "note": "Langsung bergantung pada dan mengubah ekosistem hutan."
    },

    # ── HIGH IMPACT ──────────────────────────────────────────────
    "Perkebunan Skala Besar (Sawit, Karet, dll)": {
        "impact_weight": 0.8,
        "dependency_weight": 0.75,
        "note": "Konversi hutan ke monokultur menghancurkan biodiversitas lokal."
    },
    "Pertanian Industri": {
        "impact_weight": 0.7,
        "dependency_weight": 0.8,
        "note": "Penggunaan pestisida dan air skala besar, bergantung pada tanah subur."
    },
    "Perikanan & Akuakultur Industri": {
        "impact_weight": 0.75,
        "dependency_weight": 0.9,
        "note": "Sangat bergantung pada kesehatan ekosistem laut dan air tawar."
    },

    # ── MEDIUM IMPACT ─────────────────────────────────────────────
    "Konstruksi & Infrastruktur": {
        "impact_weight": 0.6,
        "dependency_weight": 0.4,
        "note": "Fragmentasi habitat, perubahan aliran air, polusi konstruksi."
    },
    "Manufaktur & Industri": {
        "impact_weight": 0.55,
        "dependency_weight": 0.45,
        "note": "Limbah industri dan kebutuhan air bersih untuk proses produksi."
    },
    "Pariwisata & Perhotelan": {
        "impact_weight": 0.4,
        "dependency_weight": 0.7,
        "note": "Bergantung pada keindahan alam, tapi bisa merusaknya jika tidak dikelola."
    },
    "Energi Terbarukan (PLTA, Geothermal)": {
        "impact_weight": 0.45,
        "dependency_weight": 0.65,
        "note": "PLTA mengubah aliran sungai, geothermal butuh kawasan vulkanik."
    },

    # ── LOW IMPACT ────────────────────────────────────────────────
    "Teknologi & Digital": {
        "impact_weight": 0.1,
        "dependency_weight": 0.1,
        "note": "Dampak langsung ke alam minimal, tapi ada jejak karbon dari server."
    },
    "Jasa Keuangan & Perbankan": {
        "impact_weight": 0.05,
        "dependency_weight": 0.05,
        "note": "Dampak tidak langsung melalui investasi ke industri lain."
    },
    "Pendidikan & Penelitian": {
        "impact_weight": 0.05,
        "dependency_weight": 0.1,
        "note": "Dampak langsung ke alam sangat minimal."
    },
    "Kesehatan & Farmasi": {
        "impact_weight": 0.15,
        "dependency_weight": 0.2,
        "note": "Farmasi bergantung pada senyawa alami, tapi limbah medis berisiko."
    },
}

def get_industry_list() -> list:
    """Return daftar nama industri untuk dropdown UI."""
    return list(INDUSTRIES.keys())

def get_industry_weights(industry_name: str) -> dict:
    """
    Return bobot impact dan dependency untuk industri tertentu.
    
    Returns:
        dict dengan keys: impact_weight, dependency_weight, note
    """
    if industry_name not in INDUSTRIES:
        raise ValueError(f"Industri '{industry_name}' tidak ditemukan.")
    return INDUSTRIES[industry_name]