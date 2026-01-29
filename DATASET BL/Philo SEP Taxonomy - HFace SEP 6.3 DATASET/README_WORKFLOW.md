
# SEP Dataset Processing Instructions

This guide documents the workflow for cleaning the dataset and generating descriptions for the SEP Taxonomy project.

## 1. Workspace Cleanup

The workspace should only contain essential files. The following scripts are core to the workflow:

- `clean_dataset.py`: For data hygiene (encoding, quotes, normalization).
- `batch_process_descriptions.py`: For managing the description generation cycle.
- `2026-01 HuggingFace SEP Philo Dataset_cleaned.csv`: The master dataset.

## 2. Data Cleaning

To ensure the dataset is free of malformed text, smart quotes, and encoding artifacts:

```powershell
python clean_dataset.py
```

*Note: This script uses UTF-8-SIG encoding and atomic file replacement.*

## 3. Description Generation Loops

We use a **Batch Processing Workflow** to generate descriptions without manual row-by-row entry.

### workflow

1. **Extract Batch**:

    ```powershell
    python batch_process_descriptions.py --extract 50
    ```

    *This creates `pending_descriptions.json` with the next 50 empty rows.*

2. **Generate Descriptions (AI Agent Step)**:
    - The AI agent reads `pending_descriptions.json`.
    - It generates concise, declarative descriptions (no fluff) for each entry.
    - It saves the updated JSON.

3. **Apply Batch**:

    ```powershell
    python batch_process_descriptions.py --apply pending_descriptions.json
    ```

    *This reads the JSON and updates `2026-01 HuggingFace SEP Philo Dataset_cleaned.csv` only for the matching categories.*

## Description Style Guide

- **Length**: Strict **2-3 sentences**. Never 1 sentence.
  - *Tip*: If it's simple, split the definition into "What it is" and "Why it matters".
- **Declarative**: Start directly with the definition (e.g., "A theory of...").
- **No Fluff**: Avoid generic intros like "In philosophy...", "The term refers to...".
- **Biographical**: For people, always start with: `Full Name (Birth–Death) was...`.
  - Example: `Peter Abelard (1079–1142) was a preeminent medieval philosopher...`

## Troubleshooting

- **File Lock Errors**: If `clean_dataset.py` fails to save, close any apps (like Excel) that might have the CSV open.
- **Empty JSON**: If `--extract` returns 0 items, all rows might already be populated. Check the file or run a manual inspection.
