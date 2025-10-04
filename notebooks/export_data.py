from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

DB_URI = "postgresql+psycopg2://your_username:your_password@localhost:5432/fp_growth_mba"
engine = create_engine(DB_URI)

OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(exist_ok=True)

MODELS = ["transaction_fpgrowth", "user_item_dl"]

def export_models():
    with engine.connect() as conn:
        for model in MODELS:
            print(f"Exporting {model}...")

            df = pd.read_sql(f"SELECT * FROM {model};", conn)

            output_file = OUTPUT_DIR / f"{model}.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(df)} rows to {output_file}")

if __name__ == "__main__":
    export_models()
