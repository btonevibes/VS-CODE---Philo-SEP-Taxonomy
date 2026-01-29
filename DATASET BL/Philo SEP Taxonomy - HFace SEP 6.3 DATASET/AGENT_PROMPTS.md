
# Agent Commands Cheat Sheet

Use these prompts to quickly trigger the workflows we've set up for the SEP dataset.

## 1. Process New Descriptions

To have the agent analyze the next set of rows and write definitions:

> "Run the batch process for the next **[N]** descriptions. Extract them, generate the definitions yourself using the style guide (concise, declarative, no fluff), and apply them to the CSV."

**Recommended Batch Size:** 20-50

## 2. Clean the Dataset

To fix encoding, quotes, or formatting issues:

> "Run the `clean_dataset.py` script to normalize the CSV text."

## 3. Verify Progress

To check how many have been done or look for issues:

> "Check the CSV and tell me how many descriptions are currently populated vs empty."

## Style Guide Refresher (Optional)

If the agent needs a reminder of the specific definition rules:

> "Remember the rules:
>
> 1. **Length**: 2-3 sentences. (Never 1).
> 2. **Declarative**: Start immediately with the definition. No 'In philosophy' or 'This term refers to'.
> 3. **Biographical**: For people, use 'Full Name (Year-Year) was...'."
