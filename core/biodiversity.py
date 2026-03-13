import math
from collections import Counter


# ── KONSTANTA ────────────────────────────────────────────────────
# Bobot gabungan Biodiversity Score (harus total = 1.0)
WEIGHT_SHANNON   = 0.5   # keberagaman spesies
WEIGHT_RICHNESS  = 0.5   # jumlah spesies unik

# Nilai maksimum referensi untuk normalisasi
# Shannon max ~4.5 untuk ekosistem hutan tropis Indonesia
# Richness max ~600 spesies per provinsi (estimasi data GBIF Indonesia)
MAX_SHANNON  = 4.5
MAX_RICHNESS = 600


# ── KALKULASI DASAR ───────────────────────────────────────────────

def calculate_shannon(species_list: list) -> float:
    """
    Hitung Shannon-Wiener Diversity Index.
    H' = -Σ(pi × ln(pi))

    Makin tinggi = makin beragam = lebih banyak jenis berbeda.
    Makin rendah = satu jenis mendominasi = ekosistem kurang sehat.

    Args:
        species_list: list nama spesies (boleh duplikat = jumlah individu)
                      contoh: ["Panthera tigris", "Panthera tigris", "Pongo pygmaeus"]

    Returns:
        float antara 0.0 (tidak beragam) sampai ~4.5 (sangat beragam)
    """
    if not species_list:
        return 0.0

    counts  = Counter(species_list)
    total   = sum(counts.values())
    shannon = -sum((n / total) * math.log(n / total) for n in counts.values())
    return round(shannon, 4)


def calculate_richness(species_list: list) -> int:
    """
    Hitung species richness — jumlah spesies unik.

    Args:
        species_list: list nama spesies (boleh duplikat)

    Returns:
        int jumlah spesies unik
    """
    return len(set(species_list))


def normalize(value: float, max_value: float) -> float:
    """
    Normalisasi nilai ke skala 0-100.
    Nilai di atas max_value di-cap di 100.
    """
    return min(round((value / max_value) * 100, 1), 100.0)


# ── BIODIVERSITY SCORE ────────────────────────────────────────────

def calculate_biodiversity_score(species_list: list) -> dict:
    """
    Hitung Biodiversity Score gabungan (0-100).

    Formula:
        Biodiversity Score = (Shannon normalized × 50%) + (Richness normalized × 50%)

    Args:
        species_list: list nama spesies dari data GBIF wilayah tersebut

    Returns:
        dict berisi semua angka intermediate + skor akhir:
        {
            "shannon_raw":        float,   # angka Shannon mentah
            "richness_raw":       int,     # jumlah spesies unik
            "shannon_normalized": float,   # 0-100
            "richness_normalized":float,   # 0-100
            "biodiversity_score": float,   # 0-100 (skor akhir)
            "label":              str,     # Very High / High / Medium / Low / Critical
        }
    """
    shannon_raw  = calculate_shannon(species_list)
    richness_raw = calculate_richness(species_list)

    shannon_norm  = normalize(shannon_raw,  MAX_SHANNON)
    richness_norm = normalize(richness_raw, MAX_RICHNESS)

    score = (shannon_norm  * WEIGHT_SHANNON) + \
            (richness_norm * WEIGHT_RICHNESS)
    score = round(score, 1)

    return {
        "shannon_raw":         shannon_raw,
        "richness_raw":        richness_raw,
        "shannon_normalized":  shannon_norm,
        "richness_normalized": richness_norm,
        "biodiversity_score":  score,
        "label":               _biodiversity_label(score),
    }


def _biodiversity_label(score: float) -> str:
    """Konversi skor numerik ke label teks."""
    if score >= 80: return "Very High"
    if score >= 60: return "High"
    if score >= 40: return "Medium"
    if score >= 20: return "Low"
    return "Critical"


# ── TEST MANUAL ───────────────────────────────────────────────────
if __name__ == "__main__":
    # Simulasi data spesies Kalimantan (kaya biodiversitas)
    kalimantan = [
        "Pongo pygmaeus", "Panthera tigris", "Elephas borneensis",
        "Pongo pygmaeus", "Helarctos malayanus", "Nasalis larvatus",
        "Nasalis larvatus", "Presbytis rubicunda", "Macaca nemestrina",
        "Buceros rhinoceros", "Buceros rhinoceros", "Argusianus argus",
    ] * 5  # kali 5 untuk simulasi data lebih banyak

    # Simulasi data Jakarta (biodiversitas rendah)
    jakarta = [
        "Corvus splendens", "Corvus splendens", "Corvus splendens",
        "Passer montanus", "Passer montanus",
        "Columba livia", "Columba livia", "Columba livia",
    ]

    print("=== Kalimantan Tengah ===")
    result = calculate_biodiversity_score(kalimantan)
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\n=== DKI Jakarta ===")
    result = calculate_biodiversity_score(jakarta)
    for k, v in result.items():
        print(f"  {k}: {v}")