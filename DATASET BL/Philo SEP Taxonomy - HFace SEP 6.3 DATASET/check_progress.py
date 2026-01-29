import os
from pathlib import Path

import pandas as pd

script_dir = Path(__file__).parent
csv_file = script_dir / "2026-01 HuggingFace SEP Philo Dataset_cleaned.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    total_rows = len(df)
    
    # Check for empty strings or NaN in 'Description' column
    empty_mask = df["Description"].isna() | (df["Description"] == "")
    empty_count = empty_mask.sum()
    
    print(f"Total rows in CSV: {total_rows}")
    print(f"Rows with empty 'Description': {empty_count}")
    print(f"Rows with populated description: {total_rows - empty_count}")
else:
    print(f"File not found: {csv_file}")
