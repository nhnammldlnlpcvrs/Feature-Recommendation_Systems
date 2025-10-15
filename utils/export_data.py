from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "fp_growth_mba",
    "user": "postgres",
    "password": "abc123"
}

OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(exist_ok=True)

MODELS = ["transaction_fpgrowth", "user_item_dl"]

def export_models():
    conn_str = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    engine = create_engine(conn_str)

    for model in MODELS:
        print(f"Exporting {model}...")

        df = pd.read_sql(f"SELECT * FROM {model};", engine)

        output_file = OUTPUT_DIR / f"{model}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")

if __name__ == "__main__":
    export_models()
