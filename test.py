import json
import os
from pymongo import MongoClient

# -----------------------------
# Config
# -----------------------------
json_files = [
    "datasets/entry1.json",
    "datasets/entry2.json",
    "datasets/entry3.json",
    "datasets/entry4.json",
    "datasets/entry5.json",
    "datasets/entry6.json",
    "datasets/entry7.json",
    "datasets/entry8.json",
    "datasets/entry9.json",
    "datasets/entry10.json",
    "datasets/entry11.json",
    "datasets/metadata.json"
]

mandatory_fields = [
    "document_id", "title", "date", "author", "type", "law_number",
    "related_laws", "summary", "sections", "keywords", "startup_law_2018"
]

# -----------------------------
# Load JSON files
# -----------------------------
all_data = []

for file_path in json_files:
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"Warning: {file_path} is missing or empty, skipping.")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_path}: {e}")

print(f"Loaded {len(all_data)} entries from JSON files.")

# -----------------------------
# Validation
# -----------------------------
document_ids = set()
errors = []

for i, doc in enumerate(all_data, 1):
    # 1. Check missing fields
    for field in mandatory_fields:
        if field not in doc:
            errors.append(f"[Entry {i}] Missing field: {field}")

    # 2. Check bilingual fields (title, summary, sections)
    for field in ["title", "summary"]:
        if field in doc:
            if not isinstance(doc[field], dict) or "ar" not in doc[field] or "fr" not in doc[field]:
                errors.append(f"[Entry {i}] Bilingual missing in field '{field}'")

    if "sections" in doc and isinstance(doc["sections"], list):
        for sec_index, sec in enumerate(doc["sections"], 1):
            for subfield in ["title", "content"]:
                if subfield in sec:
                    if "ar" not in sec[subfield] or "fr" not in sec[subfield]:
                        errors.append(f"[Entry {i}] Section {sec_index} missing AR/FR in '{subfield}'")
                else:
                    errors.append(f"[Entry {i}] Section {sec_index} missing '{subfield}' field")

    # 3. Numeric limits
    if "staff" in doc and isinstance(doc["staff"], int) and doc["staff"] > 100:
        errors.append(f"[Entry {i}] Staff exceeds 100: {doc['staff']}")
    if "assets" in doc and isinstance(doc["assets"], (int, float)) and doc["assets"] > 15_000_000:
        errors.append(f"[Entry {i}] Assets exceed 15M TND: {doc['assets']}")

    # 4. Duplicate document_id
    if "document_id" in doc:
        if doc["document_id"] in document_ids:
            errors.append(f"[Entry {i}] Duplicate document_id: {doc['document_id']}")
        else:
            document_ids.add(doc["document_id"])

# -----------------------------
# Report
# -----------------------------
if errors:
    print(f"\nValidation completed with {len(errors)} issue(s):")
    for e in errors:
        print(e)
else:
    print("\nValidation passed! No issues found.")

# -----------------------------
# Optional: Insert into MongoDB if valid
# -----------------------------
if not errors and all_data:
    client = MongoClient("localhost:27017")
    db = client.datasets
    collection = db.datasets_law
    collection.insert_many(all_data)
    print(f"\nInserted {len(all_data)} documents into MongoDB successfully!")
