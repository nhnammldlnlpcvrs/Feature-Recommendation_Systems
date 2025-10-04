import psycopg2
import pandas as pd
from pathlib import Path

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "db_postgres",
    "user": "nhnammldlnlpcvrs",
    "password": "abc123"
}

OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(exist_ok=True)

MODELS = ["transaction_fpgrowth", "user_item_dl"]

def export_models():
    conn = psycopg2.connect(**DB_CONFIG)

    for model in MODELS:
        print(f"Exporting {model}...")

        df = pd.read_sql_query(f"SELECT * FROM {model};", conn)

        output_file = OUTPUT_DIR / f"{model}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")

    conn.close()

if __name__ == "__main__":
    export_models()
