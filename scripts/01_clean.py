from __future__ import annotations

import argparse
import glob
import os
from pathlib import Path
import sys

import duckdb


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Clean Cyclistic trips CSVs to Parquet.")
    p.add_argument(
        "--raw-dir",
        default=os.environ.get("RAW_DIR", "data/raw"),
        help="Directory containing monthly CSV files (default: data/raw)",
    )
    p.add_argument(
        "--clean-dir",
        default=os.environ.get("CLEAN_DIR", "data/clean"),
        help="Directory to write cleaned outputs (default: data/clean)",
    )
    p.add_argument(
        "--pattern",
        default="*.csv",
        help="Glob pattern for input files within raw-dir (default: *.csv)",
    )
    p.add_argument(
        "--out",
        default="trips_clean.parquet",
        help="Output Parquet filename placed under clean-dir (default: trips_clean.parquet)",
    )
    p.add_argument(
        "--infer-all",
        action="store_true",
        help="Use sample_size=-1 for CSV type inference (slower, more accurate).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    raw_dir = Path(args.raw_dir).expanduser().resolve()
    clean_dir = Path(args.clean_dir).expanduser().resolve()
    parquet_out = clean_dir / args.out

    if not raw_dir.exists():
        sys.exit(f"[ERROR] Raw directory not found: {raw_dir}")

    clean_dir.mkdir(parents=True, exist_ok=True)

    # Collect CSVs
    csv_glob = str(raw_dir / args.pattern)
    csvs = sorted(glob.glob(csv_glob))
    if not csvs:
        sys.exit(f"[ERROR] No CSVs found with pattern {csv_glob}")

    print(f"[INFO] Found {len(csvs)} CSV files under {raw_dir}")

    # Connect in-memory (adjust if you want persistence)
    con = duckdb.connect(database=":memory:")
    try:
        # Build relation from CSVs
        rel_kwargs = {
            "filename": True,             # add _filename column
            "hive_partitioning": False,
        }
        if args.infer_all:
            rel_kwargs["sample_size"] = -1

        rel_raw = con.read_csv(csvs, **rel_kwargs)
        rel_raw.create_view("trips_raw", replace=True)

        # Optional peek
        n_rows = con.sql("SELECT COUNT(*)::UBIGINT AS n FROM trips_raw").fetchone()[0]
        print(f"[INFO] trips_raw row count: {n_rows}")

        # Clean & type (safe, Cyclistic-friendly)
        clean_sql = """
            WITH typed AS (
                SELECT
                    ride_id,
                    rideable_type,
                    TRY_CAST(started_at AS TIMESTAMP) AS started_at,
                    TRY_CAST(ended_at   AS TIMESTAMP) AS ended_at,
                    start_station_name,
                    start_station_id,
                    end_station_name,
                    end_station_id,
                    TRY_CAST(start_lat AS DOUBLE) AS start_lat,
                    TRY_CAST(start_lng AS DOUBLE) AS start_lng,
                    TRY_CAST(end_lat   AS DOUBLE) AS end_lat,
                    TRY_CAST(end_lng   AS DOUBLE) AS end_lng,
                    LOWER(TRIM(member_casual)) AS member_casual,
                    filename
                FROM trips_raw
            ),
            enriched AS (
                SELECT
                    *,
                    DATE_DIFF('minute', started_at, ended_at) AS duration_min
                FROM typed
            ),
            filtered AS (
                SELECT *
                FROM enriched
                WHERE ride_id IS NOT NULL
                  AND started_at IS NOT NULL
                  AND ended_at   IS NOT NULL
                  AND duration_min IS NOT NULL
                  AND duration_min >= 1
                  AND duration_min <= 1440
            )
            SELECT * FROM filtered
        """

        # Materialize the cleaned relation
        rel_clean = con.sql(clean_sql)

        # Write Parquet via Relation API (avoids COPY parameter issues)
        print(f"[INFO] Writing cleaned Parquet -> {parquet_out}")
        rel_clean.write_parquet(str(parquet_out))  # compression defaults are fine

        # Quick verification: read back and report rows
        n_clean = con.execute(
            "SELECT COUNT(*)::UBIGINT FROM read_parquet(?)",
            [str(parquet_out)],
        ).fetchone()[0]
        print(f"[INFO] Wrote {n_clean} cleaned rows to {parquet_out}")

    finally:
        con.close()


if __name__ == "__main__":
    main()