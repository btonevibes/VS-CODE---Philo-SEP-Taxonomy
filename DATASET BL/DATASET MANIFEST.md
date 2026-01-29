DATASET MANIFEST
Purpose
- This folder contains the master working dataset plus source-specific pipelines.
- The HFace SEP 6.3 dataset is a newer SEP-derived description source, kept separate until merged.
- If you return after time away: start with the master file, then review the HFace 6.3 folder for its own workflow and scripts.

Master dataset
- File: DATASET BL/2025-12-31 TEMP Gemini GPT SEP+IEP Merge 2 TEMP.enriched.csv
- Current usage: Loaded by index.html for the UI.
- Notes: This is the active working dataset; changes here affect the UI and downstream analysis.

Source: SEP (Stanford Encyclopedia of Philosophy) - Hugging Face pipeline (6.3)
- Folder: DATASET BL/Philo SEP Taxonomy - HFace SEP 6.3 DATASET
- Raw input: Hugging Face stanford-encyclopedia-philosophy.csv (2026-01-26)
- Cleaned output: 2026-01 HuggingFace SEP Philo Dataset_cleaned.csv (2026-01-27)
- Backup: 2026-01 HuggingFace SEP Philo Dataset_cleaned BACKUP.csv
- Scripts: clean_dataset.py, batch_process_descriptions.py, check_progress.py
- Why it exists: Potential replacement or companion to the existing "6.2 Description SEP" column.
- Intended new column: "6.21 Description SEP" (HFace pipeline).

Schema highlights (used by scripts)
- category
- Description
- text_1 (used for preview in batch extraction)

Integration into master
- Status: Not yet merged; stored for future integration.
- When resuming later: confirm column names and row alignment before merging.

Quick workflow reminders (HFace 6.3)
- clean_dataset.py: normalizes/cleans text in-place for the cleaned CSV.
- batch_process_descriptions.py: exports missing Description rows to JSON, then imports filled descriptions.
- check_progress.py: prints missing Description counts for the cleaned CSV.
