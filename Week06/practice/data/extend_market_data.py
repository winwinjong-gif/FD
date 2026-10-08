"""Build the Week05 offline market_data.db fixture from the approved FDR window."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import FinanceDataReader as fdr
import pandas as pd


START = "2024-06-25"
END = "2026-06-24"
CODES = [
    "000270",
    "000660",
    "005380",
    "005930",
    "009150",
    "010950",
    "011170",
    "035420",
    "051910",
    "055550",
    "105560",
    "207940",
]


def build_database(output_db: Path, source_db: Path | None) -> None:
    output_db.parent.mkdir(parents=True, exist_ok=True)
    if output_db.exists():
        raise FileExistsError(f"Refusing to overwrite existing database: {output_db}")

    with sqlite3.connect(output_db) as out:
        if source_db and source_db.exists():
            with sqlite3.connect(source_db) as source:
                for table in ("companies", "financials"):
                    frame = pd.read_sql_query(f"SELECT * FROM {table}", source)
                    frame.to_sql(table, out, index=False, if_exists="replace")

        returns: list[pd.DataFrame] = []
        for code in CODES:
            prices = fdr.DataReader(code, START, END).reset_index()
            prices = prices[["Date", "Close"]].rename(
                columns={"Date": "date", "Close": "close"}
            )
            prices["code"] = code
            prices["date"] = prices["date"].dt.strftime("%Y-%m-%d")
            prices["daily_return"] = prices["close"].pct_change()
            returns.append(prices[["code", "date", "close", "daily_return"]])

        pd.concat(returns, ignore_index=True).to_sql(
            "returns", out, index=False, if_exists="replace"
        )

        summary = pd.read_sql_query(
            "SELECT COUNT(*) AS rows, COUNT(DISTINCT code) AS codes, "
            "MIN(date) AS start, MAX(date) AS end FROM returns",
            out,
        ).iloc[0]
        print(
            f"rows={int(summary['rows'])} codes={int(summary['codes'])} "
            f"period={summary['start']}..{summary['end']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-db", type=Path, required=True)
    parser.add_argument("--source-db", type=Path)
    args = parser.parse_args()
    build_database(args.output_db, args.source_db)


if __name__ == "__main__":
    main()
