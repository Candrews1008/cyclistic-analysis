# cyclistic-analysis

## Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Clean
python scripts/01_clean.py --raw-dir data/raw --clean-dir data/clean --out trips_clean.parquet --infer-all

## EDA
Open `notebooks/01_eda.ipynb` → Run All → see PNGs in `visuals/`.
