# 🌿 BioESG Indonesia Project
### Biodiversity Index Dashboard for Corporate ESG Reporting

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework: GRI 304](https://img.shields.io/badge/Framework-GRI%20304-brightgreen)](https://www.globalreporting.org/)
[![Framework: TNFD](https://img.shields.io/badge/Framework-TNFD-blue)](https://tnfd.global/)
[![Status: MVP](https://img.shields.io/badge/Status-MVP-orange)]()

---

## 🧭 Overview

**BioESG Indonesia** is an open-source tool that transforms raw biodiversity occurrence data into actionable ESG metrics aligned with **GRI 304** and **TNFD** frameworks — focused on Indonesia's ecosystems.

> 55% of global GDP depends on high-functioning biodiversity (Swiss Re, 2020).  
> Yet less than 25% of at-risk companies disclose their biodiversity impacts (KPMG).  
> This tool helps close that gap.

---

## 🎯 Objectives

- Collect and process species occurrence data across Indonesian provinces
- Calculate standardized biodiversity indices (Shannon, Simpson, species richness)
- Convert ecological data into ESG-compatible scores based on GRI 304 & TNFD
- Provide an interactive dashboard for corporate sustainability reporting

---

## 🗺️ Scope

| Coverage | Detail |
|---|---|
| **Geography** | All 34 provinces of Indonesia |
| **Data Source** | [GBIF](https://www.gbif.org/), [iNaturalist](https://www.inaturalist.org/) |
| **Taxonomic Groups** | Plants, Birds, Mammals, Reptiles, Amphibians |
| **ESG Frameworks** | GRI 304, TNFD, SDG 14 & 15 |

---

## 🏗️ Project Structure

```
biodiversity-esg-indonesia/
│
├── src/
│   ├── collector/          # [Partner] Data fetching from GBIF & iNaturalist
│   │   ├── gbif_fetcher.py
│   │   └── inaturalist_fetcher.py
│   │
│   ├── analyzer/           # [Partner] Biodiversity index calculations
│   │   ├── diversity_index.py
│   │   └── species_classifier.py
│   │
│   └── dashboard/          # [You] ESG scoring + Streamlit UI
│       ├── esg_scorer.py
│       ├── gri304_mapper.py
│       └── app.py
│
├── data/
│   ├── raw/                # Raw occurrence data (gitignored if large)
│   └── processed/          # Cleaned, indexed datasets
│
├── docs/                   # Methodology, framework references
├── tests/                  # Unit tests per module
└── .github/
    ├── ISSUE_TEMPLATE/     # Bug report, feature request templates
    └── workflows/          # CI/CD (future)
```

---

## 👥 Contributors & Responsibilities

| Module | Owner | Domain |
|---|---|---|
| `src/collector/` | Partner | Bioinformatics — API, taxonomy, data parsing |
| `src/analyzer/` | Partner | Bioinformatics — diversity indices, ecology stats |
| `src/dashboard/esg_scorer.py` | You | ESG — scoring model, GRI 304 alignment |
| `src/dashboard/gri304_mapper.py` | You | ESG — framework mapping, reporting output |
| `src/dashboard/app.py` | You | ESG — Streamlit UI, visualization |

---

## 🚀 Roadmap

### v0.1 — MVP *(Semester 2)*
- [ ] GBIF data collector for 5 pilot provinces
- [ ] Shannon Diversity Index calculator
- [ ] Basic ESG score output (3 tiers: Low / Medium / High risk)
- [ ] Streamlit dashboard (province filter + index visualization)

### v0.2 — Expansion *(Semester 3-4)*
- [ ] Full 34 provinces coverage
- [ ] Correlation: biodiversity vs land use change
- [ ] TNFD LEAP approach integration
- [ ] Export to CSV/PDF for reporting

### v1.0 — Research Grade *(Semester 5-6)*
- [ ] Satellite data integration (NDVI via Google Earth Engine)
- [ ] Corporate benchmarking module
- [ ] Peer-reviewed methodology documentation

### v2.0 — Thesis Ready *(Semester 7-8)*
- [ ] Predictive model: biodiversity risk projection
- [ ] Full GRI 304 & TNFD disclosure template generator
- [ ] API endpoint for third-party integration

---

## 📚 Theoretical Background

This project is grounded in:
- **GRI 304: Biodiversity** — global standard for organizational biodiversity impact reporting
- **TNFD LEAP Approach** — Locate, Evaluate, Assess, Prepare framework for nature-related risks
- **Shannon-Wiener Diversity Index** — H' = -Σ(pi × ln(pi))
- **SDG 14 & 15** — Life below water, Life on land

---

## 🛠️ Tech Stack

| Purpose | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Collection | `pygbif`, `requests` |
| Data Processing | `pandas`, `numpy` |
| Ecology Stats | `scipy`, `skbio` |
| Dashboard | `streamlit`, `plotly` |
| Visualization | `folium` (maps), `matplotlib` |

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/biodiversity-esg-indonesia.git
cd biodiversity-esg-indonesia
pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 📖 References

- GRI 304: Biodiversity Standard (2016, revised 2023)
- TNFD Framework v1.0 (2023)
- Swiss Re Institute — Biodiversity and Ecosystem Services (2020)
- GBIF — Global Biodiversity Information Facility
