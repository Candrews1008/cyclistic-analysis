# Cyclistic Bike-Share Analysis

This project analyzes Cyclistic bike-share data to uncover usage patterns, differences between member and casual riders, and insights for marketing strategies.

---

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

---

## Tools Used
- **Python** (pandas, DuckDB, matplotlib, pyarrow)
- **Jupyter Notebook** for EDA
- **Tableau** for interactive dashboards

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
