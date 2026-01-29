
import csv
import json
import shutil
import sys
import argparse
from pathlib import Path

csv.field_size_limit(2**30)

SCRIPT_DIR = Path(__file__).parent
CSV_FILE = SCRIPT_DIR / "2026-01 HuggingFace SEP Philo Dataset_cleaned.csv"
PENDING_FILE = SCRIPT_DIR / "pending_descriptions.json"

def extract_batch(batch_size=5):
    """Extracts the next N rows with empty descriptions."""
    print(f"Extracting batch of {batch_size}...")
    
    batch = []
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('Description'):
                # Grab text preview
                text_preview = row.get('text_1', '')[:500]
                batch.append({
                    'category': row['category'],
                    'text_preview': text_preview,
                    'generated_description': "" # Placeholder for AI
                })
                if len(batch) >= batch_size:
                    break
    
    if not batch:
        print("No empty descriptions found!")
        return
        
    with open(PENDING_FILE, 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2)
        
    print(f"Exported {len(batch)} items to {PENDING_FILE}")
    print("Instructions: Open this JSON, fill in 'generated_description', then run with --import")

def apply_batch(json_file_path):
    """Applies descriptions from a JSON file to the CSV."""
    json_path = Path(json_file_path)
    if not json_path.exists():
        print(f"Error: File {json_path} not found.")
        return

    print(f"Applying descriptions from {json_path}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        updates = json.load(f)
        
    # Create lookup map
    update_map = {item['category']: item['generated_description'] for item in updates if item.get('generated_description')}
    
    if not update_map:
        print("No descriptions found in JSON (generated_description field empty?)")
        return

    # Validate sentence counts
    print("Validating descriptions...")
    for cat, desc in update_map.items():
        # A rough heuristic for sentence count: count periods followed by space or end of string
        # This isn't perfect (e.g. "Mr.", "i.e.") but good enough for a sanity check warning
        sentence_count = desc.count('. ') + (1 if desc.endswith('.') else 0)
        
        if sentence_count < 2:
            print(f"WARNING: Description for '{cat}' is too short ({sentence_count} sentences). Aim for 2-3.")
        elif sentence_count > 3:
            print(f"WARNING: Description for '{cat}' might be too long ({sentence_count} sentences). Aim for 2-3.")
        
    temp_file = SCRIPT_DIR / "sep_cleaned_temp_update.csv"
    
    updated_count = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8-sig', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            cat = row['category']
            if cat in update_map:
                row['Description'] = update_map[cat]
                updated_count += 1
            writer.writerow(row)
            
    print(f"Updated {updated_count} rows.")
    print(f"Updated {updated_count} rows.")
    
    import time
    import os
    
    max_retries = 3
    for i in range(max_retries):
        try:
            if os.path.exists(CSV_FILE):
                os.remove(CSV_FILE)
            os.rename(temp_file, CSV_FILE)
            print("CSV updated successfully.")
            return
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                time.sleep(1)
            else:
                print("Could not overwrite file. Check permissions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process SEP descriptions")
    parser.add_argument('--extract', type=int, help="Extract N rows for processing")
    parser.add_argument('--apply', type=str, help="Apply descriptions from JSON file")
    
    args = parser.parse_args()
    
    if args.extract:
        extract_batch(args.extract)
    elif args.apply:
        apply_batch(args.apply)
    else:
        parser.print_help()
