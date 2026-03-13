from core.industries import get_industry_weights


# ── KONSTANTA BOBOT ───────────────────────────────────────────────
# Impact Risk weights (harus total = 1.0)
IMPACT_WEIGHTS = {
    "biodiversity":       0.30,  # seberapa kaya wilayahnya
    "protected_area":     0.30,  # apakah kawasan lindung
    "industry":           0.25,  # jenis industri perusahaan
    "operation_size":     0.15,  # luas area operasi
}

# Dependency Risk weights (harus total = 1.0)
DEPENDENCY_WEIGHTS = {
    "industry":           0.40,  # jenis industri = proxy utama ketergantungan
    "needs_water":        0.20,  # butuh air bersih dari wilayah?
    "needs_land":         0.20,  # butuh tanah/hasil hutan?
    "climate_sensitive":  0.20,  # terpengaruh iklim lokal?
}


# ── HELPER: OPERATION SIZE ────────────────────────────────────────
def _operation_size_score(hectares: float) -> float:
    """
    Konversi luas area operasi (hektar) ke skor 0-1.
    
    Referensi skala:
        < 10 ha      → kecil (kantor, toko)
        10 - 100 ha  → menengah (pabrik kecil, kebun kecil)
        100 - 1000 ha → besar (perkebunan, tambang kecil)
        > 1000 ha    → sangat besar (tambang besar, HPH)
    """
    if hectares < 10:    return 0.1
    if hectares < 100:   return 0.3
    if hectares < 1000:  return 0.6
    if hectares < 10000: return 0.85
    return 1.0


# ── IMPACT RISK ───────────────────────────────────────────────────
def calculate_impact_risk(
    biodiversity_score: float,
    is_protected_area: bool,
    industry_name: str,
    operation_hectares: float,
) -> dict:
    """
    Hitung Impact Risk — seberapa besar potensi perusahaan merusak alam.

    Args:
        biodiversity_score:  skor 0-100 dari calculate_biodiversity_score()
        is_protected_area:   True jika wilayah adalah/dekat kawasan lindung
        industry_name:       nama industri dari dropdown
        operation_hectares:  luas area operasi dalam hektar

    Returns:
        dict dengan skor intermediate + skor akhir + label + penjelasan
    """
    weights = get_industry_weights(industry_name)

    # Normalisasi setiap komponen ke 0-1
    bio_component       = (biodiversity_score / 100)
    protected_component = 1.0 if is_protected_area else 0.2
    industry_component  = weights["impact_weight"]
    size_component      = _operation_size_score(operation_hectares)

    # Hitung skor gabungan
    raw_score = (
        bio_component       * IMPACT_WEIGHTS["biodiversity"]   +
        protected_component * IMPACT_WEIGHTS["protected_area"] +
        industry_component  * IMPACT_WEIGHTS["industry"]       +
        size_component      * IMPACT_WEIGHTS["operation_size"]
    )

    score = round(raw_score * 100, 1)

    return {
        "impact_score":              score,
        "label":                     _risk_label(score),
        "components": {
            "biodiversity_component":  round(bio_component * 100, 1),
            "protected_area":          is_protected_area,
            "industry_component":      round(industry_component * 100, 1),
            "operation_size_ha":       operation_hectares,
        },
        "explanation": _impact_explanation(score, is_protected_area, industry_name),
    }


# ── DEPENDENCY RISK ───────────────────────────────────────────────
def calculate_dependency_risk(
    industry_name: str,
    needs_water: bool,
    needs_land: bool,
    climate_sensitive: bool,
) -> dict:
    """
    Hitung Dependency Risk — seberapa besar perusahaan bergantung pada alam.

    Args:
        industry_name:     nama industri dari dropdown
        needs_water:       apakah operasi butuh air bersih dari wilayah?
        needs_land:        apakah operasi butuh tanah/hasil hutan?
        climate_sensitive: apakah operasi terpengaruh perubahan iklim lokal?

    Returns:
        dict dengan skor intermediate + skor akhir + label + penjelasan
    """
    weights = get_industry_weights(industry_name)

    industry_component = weights["dependency_weight"]
    water_component    = 1.0 if needs_water else 0.0
    land_component     = 1.0 if needs_land else 0.0
    climate_component  = 1.0 if climate_sensitive else 0.0

    raw_score = (
        industry_component * DEPENDENCY_WEIGHTS["industry"]          +
        water_component    * DEPENDENCY_WEIGHTS["needs_water"]       +
        land_component     * DEPENDENCY_WEIGHTS["needs_land"]        +
        climate_component  * DEPENDENCY_WEIGHTS["climate_sensitive"]
    )

    score = round(raw_score * 100, 1)

    return {
        "dependency_score": score,
        "label":            _risk_label(score),
        "components": {
            "industry_dependency":  round(industry_component * 100, 1),
            "needs_water":          needs_water,
            "needs_land":           needs_land,
            "climate_sensitive":    climate_sensitive,
        },
        "explanation": _dependency_explanation(score, needs_water, needs_land, climate_sensitive),
    }


# ── LABEL & PENJELASAN ────────────────────────────────────────────
def _risk_label(score: float) -> str:
    if score >= 75: return "Critical"
    if score >= 50: return "High"
    if score >= 25: return "Medium"
    return "Low"


def _impact_explanation(score: float, is_protected: bool, industry: str) -> str:
    protected_text = "berada di/dekat kawasan lindung" if is_protected else "tidak di kawasan lindung"
    if score >= 75:
        return f"Risiko dampak sangat tinggi. Operasi {industry} yang {protected_text} berpotensi merusak ekosistem secara signifikan. Mitigasi mendesak diperlukan sesuai GRI 304-2."
    if score >= 50:
        return f"Risiko dampak tinggi. {industry} di wilayah ini perlu program mitigasi biodiversitas yang jelas sesuai GRI 304-1."
    if score >= 25:
        return f"Risiko dampak moderat. Monitoring berkala terhadap dampak operasi disarankan sesuai GRI 304-3."
    return f"Risiko dampak rendah. Tetap lakukan monitoring standar sesuai GRI 304."


def _dependency_explanation(score: float, water: bool, land: bool, climate: bool) -> str:
    deps = []
    if water:   deps.append("air bersih")
    if land:    deps.append("lahan/hasil hutan")
    if climate: deps.append("stabilitas iklim lokal")
    dep_text = ", ".join(deps) if deps else "sumber daya alam"

    if score >= 75:
        return f"Ketergantungan sangat tinggi pada {dep_text}. Kerusakan ekosistem di wilayah ini akan langsung mengganggu operasi bisnis. Sesuai TNFD: Dependency disclosure wajib."
    if score >= 50:
        return f"Ketergantungan tinggi pada {dep_text}. Perlu strategi mitigasi risiko supply chain alam."
    if score >= 25:
        return f"Ketergantungan moderat pada {dep_text}. Monitor kondisi ekosistem secara berkala."
    return "Ketergantungan rendah pada ekosistem lokal."


# ── TEST MANUAL ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Impact Risk: Tambang di Kalimantan ===")
    impact = calculate_impact_risk(
        biodiversity_score=87.0,
        is_protected_area=True,
        industry_name="Pertambangan (Batu Bara, Nikel, dll)",
        operation_hectares=5000,
    )
    print(f"  Score: {impact['impact_score']} → {impact['label']}")
    print(f"  {impact['explanation']}")

    print("\n=== Dependency Risk: Perikanan di Maluku ===")
    dep = calculate_dependency_risk(
        industry_name="Perikanan & Akuakultur Industri",
        needs_water=True,
        needs_land=False,
        climate_sensitive=True,
    )
    print(f"  Score: {dep['dependency_score']} → {dep['label']}")
    print(f"  {dep['explanation']}")
