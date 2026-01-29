
import csv
import re
import html
import shutil
import sys
from pathlib import Path

csv.field_size_limit(2**30)

def normalize_text(text: str) -> str:
    """Normalize special characters and clean text."""
    if not text:
        return ""
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Normalize quotes (Smart quotes to straight quotes)
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace('`', "'")
    text = text.replace('″', '"').replace('′', "'")
    
    # Normalize dashes (preserve semantic difference if possible, but standardizing often safer for NLP)
    # text = text.replace('—', '--').replace('–', '-') # Optional: keep dashes as is if preferred
    
    # Normalize ellipsis
    text = text.replace('…', '...')
    
    # Normalize special spaces
    text = text.replace('\u00a0', ' ').replace('\u2003', ' ')
    text = text.replace('\u2002', ' ').replace('\u200b', '')
    
    # Strip garbage control characters but allow newlines/tabs if they are semantic (csv handles them)
    # Removing null bytes and other non-printable chars
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    return text.strip()

def clean_dataset_file():
    script_dir = Path(__file__).parent
    input_file = script_dir / "2026-01 HuggingFace SEP Philo Dataset_cleaned.csv"
    temp_file = script_dir / "sep_cleaned_temp.csv"
    
    print(f"Cleaning: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8-sig', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8-sig', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        row_count = 0
        
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if v:
                    clean_row[k] = normalize_text(v)
                else:
                    clean_row[k] = v
            
            writer.writerow(clean_row)
            row_count += 1
            if row_count % 1000 == 0:
                print(f"Processed {row_count} rows...", end='\r')
                
    print(f"\nFinished cleaning {row_count} rows.")
    
    # Verify we didn't lose rows (simple check)
    print("Replacing original file...")
    
    import time
    import os
    
    max_retries = 3
    for i in range(max_retries):
        try:
            # Try atomic replace first
            if os.path.exists(input_file):
                os.remove(input_file)
            os.rename(temp_file, input_file)
            print("Done.")
            break
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                time.sleep(1)
            else:
                print("Could not overwrite file. Cleaned data is in sep_cleaned_temp.csv")

if __name__ == "__main__":
    clean_dataset_file()
