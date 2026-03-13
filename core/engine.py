from core.biodiversity import calculate_biodiversity_score
from core.risk import calculate_impact_risk, calculate_dependency_risk


def analyze(
    # ── Input wilayah ──────────────────────────────
    province_name: str,
    species_list: list,
    is_protected_area: bool,

    # ── Input perusahaan ───────────────────────────
    company_name: str,
    industry_name: str,
    operation_hectares: float,

    # ── Pertanyaan dependency ──────────────────────
    needs_water: bool,
    needs_land: bool,
    climate_sensitive: bool,
) -> dict:
    """
    Analisis lengkap BioESG untuk satu perusahaan di satu wilayah.

    Returns:
        dict lengkap berisi semua skor, label, komponen, dan penjelasan.
        Struktur ini yang dikirim ke UI dan ke report generator.
    """

    # Tahap 1: Biodiversity
    bio = calculate_biodiversity_score(species_list)

    # Tahap 2A: Impact Risk
    impact = calculate_impact_risk(
        biodiversity_score=bio["biodiversity_score"],
        is_protected_area=is_protected_area,
        industry_name=industry_name,
        operation_hectares=operation_hectares,
    )

    # Tahap 2B: Dependency Risk
    dependency = calculate_dependency_risk(
        industry_name=industry_name,
        needs_water=needs_water,
        needs_land=needs_land,
        climate_sensitive=climate_sensitive,
    )

    return {
        "meta": {
            "company_name":      company_name,
            "province":          province_name,
            "industry":          industry_name,
            "operation_ha":      operation_hectares,
            "is_protected_area": is_protected_area,
        },
        "biodiversity": bio,
        "impact":       impact,
        "dependency":   dependency,
        "summary": {
            "biodiversity_score": bio["biodiversity_score"],
            "biodiversity_label": bio["label"],
            "impact_score":       impact["impact_score"],
            "impact_label":       impact["label"],
            "dependency_score":   dependency["dependency_score"],
            "dependency_label":   dependency["label"],
        }
    }


# ── TEST MANUAL ───────────────────────────────────────────────────
if __name__ == "__main__":
    # Simulasi: perusahaan tambang di Kalimantan
    result = analyze(
        province_name="Kalimantan Tengah",
        species_list=[
            "Pongo pygmaeus", "Panthera tigris", "Elephas borneensis",
            "Pongo pygmaeus", "Helarctos malayanus", "Nasalis larvatus",
            "Buceros rhinoceros", "Argusianus argus", "Presbytis rubicunda",
        ] * 10,
        is_protected_area=True,
        company_name="PT Contoh Tambang",
        industry_name="Pertambangan (Batu Bara, Nikel, dll)",
        operation_hectares=3000,
        needs_water=True,
        needs_land=True,
        climate_sensitive=False,
    )

    print("=" * 50)
    print(f"  {result['meta']['company_name']}")
    print(f"  {result['meta']['province']} | {result['meta']['industry']}")
    print("=" * 50)
    print(f"  🌿 Biodiversity Score : {result['summary']['biodiversity_score']}/100  → {result['summary']['biodiversity_label']}")
    print(f"  ⚠️  Impact Risk        : {result['summary']['impact_score']}/100  → {result['summary']['impact_label']}")
    print(f"  🏭 Dependency Risk    : {result['summary']['dependency_score']}/100  → {result['summary']['dependency_label']}")
    print()
    print(f"  Impact:     {result['impact']['explanation']}")
    print(f"  Dependency: {result['dependency']['explanation']}")
