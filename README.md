# Cyclistic Bike-Share Analysis

Goal: Analyze how casual riders and annual members use Cyclistic/Divvy bikes differently, then translate insights into actions that can convert casual riders into members.

This project is an end-to-end, reproducible portfolio piece: data ingestion → cleaning → analysis → visualization → written report.

---

## Data

Source: Public Divvy/Cyclistic trip data (monthly CSVs).

Privacy: Data is anonymized; no personally identifiable information.

How it’s used here: 12 recent months (or a subset) are cleaned into a single Parquet file for fast analysis.

## Tech Stack

Python: duckdb, pandas, pyarrow, matplotlib, seaborn

Engine: DuckDB for fast, memory-safe SQL over CSV/Parquet

Report: Quarto (notebook-style .qmd → clean HTML)

Versioning: git, GitHub

## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Candrews1008/cyclistic-analysis.git
cd cyclistic-analysis
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# OR
.\.venv\Scriptsctivate    # Windows
```

### 3. Install dependencies
```bash
python -m pip install -U pip
pip install -r requirements.txt
```

### 4. Prepare the data
- Download the Cyclistic CSVs from Divvy/Cyclistic trip data.
- Place them under:
```
data/raw/
```

### 5. Clean the data
```bash
python scripts/01_clean.py --raw-dir data/raw --clean-dir data/clean --out trips_clean.parquet --infer-all
```

### 6. Run exploratory analysis
- Open Jupyter:
```bash
jupyter notebook
```
- Launch `notebooks/01_eda.ipynb` (or run the EDA script).
- This will generate plots under:
```
visuals/
```

Example visuals:
- `visuals/avg_duration_by_rider.png`
- `visuals/rides_by_hour.png`

## Results

- Total rides: 5,523,010
- Members: 3,514,081 (63.6%)
- Casual: 2,008,929 (36.4%)

### Ride duration by rider type
– Casual: 20.0 min avg (12.0 min median)
– Member: 11.9 min avg (9.0 min median)
→ Casual trips are ~68% longer on average and 3 min longer at the median.

### Share of total ride-minutes
– Members ≈ 51% | Casual ≈ 49%
→ Even with fewer trips, casual riders consume nearly half of total riding time.

### Hourly patterns (Rides by Hour chart)
– Members: pronounced commute peaks around ~8 AM and ~5–6 PM.
– Casual: gradual build from late morning, broad peak in the afternoon (≈3–6 PM), tapering into evening.
→ Strong commute signal for members; leisure/errand signal for casual riders.

### Weekday vs. weekend (Heatmap)
- Members: highest volumes Mon–Thu/Fri, lower on weekends.
- Casual: largest volumes on Saturday, then Sunday; weekdays markedly lower.
- Casual riding is weekend-skewed; member riding is weekday/commute-skewed.

## What this implies
- Members drive utilization during the workweek; ensure reliability and bike availability around commute windows.
- Casuals are your conversion opportunity on weekends/afternoons; they already ride longer and are more price-insensitive per minute.

## Recommendations
- Weekend → Membership trials: In-app prompts/QR at top casual stations on Sat/Sun afternoons (e.g., “$1 first month” or “3-weekend rides → 1 free month member”).
- Commute perks for members: Morning/evening bike availability guarantees, small e-bike credit 7–10 AM & 4–7 PM, and corporate payroll discounts to deepen weekday use.
- Targeted upsell nudges: When a casual rider logs ≥2 rides in a month or any ride >25 min, trigger a membership offer highlighting cost per minute savings.
---

## Repo Structure
```
cyclistic-analysis/
│
├── data/
│   ├── raw/      # input CSVs
│   └── clean/    # parquet outputs
│
├── scripts/
│   └── 01_clean.py
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── visuals/      # PNG charts
├── requirements.txt
├── .gitignore
└── README.md
```

---
