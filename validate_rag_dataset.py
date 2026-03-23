"""
validate_rag_dataset.py
=======================
Validates the transformed RAG dataset against all requirements.
Checks 12 criteria and reports pass/fail for each.
"""

import json
import re
import sys
import os
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATASET_PATH = os.path.join("datasets", "rag_dataset.json")
EXPECTED_COUNT = 62

VALID_DOMAINS = {"startup", "cnss", "labor"}
VALID_DOC_TYPES = {"law", "decree", "guide", "procedure", "metadata"}
REQUIRED_FIELDS = [
    "document_id", "title", "date", "author", "type", "law_number",
    "related_laws", "procedure_category", "domain", "document_type",
    "source_document", "summary", "simplified_text", "keywords",
    "sections", "text",
]

ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# ─────────────────────────────────────────────
# Check helpers
# ─────────────────────────────────────────────
results = []

def check(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append((name, status, detail))
    icon = "✓" if passed else "✗"
    msg = f"  [{icon}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def find_empty_strings(obj, path=""):
    """Recursively find empty strings in obj, returning paths."""
    found = []
    if isinstance(obj, str) and obj == "":
        found.append(path or "<root>")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(find_empty_strings(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(find_empty_strings(v, f"{path}[{i}]"))
    return found


# ─────────────────────────────────────────────
# Load dataset
# ─────────────────────────────────────────────
print(f"Validating: {DATASET_PATH}\n")

try:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    check("1. Valid JSON", True, f"Parsed as array of {len(data)} items")
except Exception as e:
    check("1. Valid JSON", False, str(e))
    sys.exit(1)

# ─────────────────────────────────────────────
# 2. Required fields
# ─────────────────────────────────────────────
missing_fields = []
for i, doc in enumerate(data):
    for field in REQUIRED_FIELDS:
        if field not in doc:
            missing_fields.append(f"doc[{i}] (id={doc.get('document_id','?')}) missing: {field}")
check("2. All required fields present", len(missing_fields) == 0,
      f"{len(missing_fields)} missing" if missing_fields else "All 16 fields present in every document")
if missing_fields:
    for m in missing_fields[:10]:
        print(f"     → {m}")

# ─────────────────────────────────────────────
# 3. No empty strings
# ─────────────────────────────────────────────
empty_string_docs = []
for i, doc in enumerate(data):
    empties = find_empty_strings(doc)
    if empties:
        empty_string_docs.append((doc.get("document_id"), empties[:3]))
check("3. No empty strings (null instead)", len(empty_string_docs) == 0,
      f"{len(empty_string_docs)} docs have empty strings" if empty_string_docs else "All empty values are null")
if empty_string_docs:
    for did, paths in empty_string_docs[:5]:
        print(f"     → doc_id={did}: {paths}")

# ─────────────────────────────────────────────
# 4. ISO dates
# ─────────────────────────────────────────────
bad_dates = []
for doc in data:
    d = doc.get("date")
    if d is not None and not ISO_DATE_RE.match(str(d)):
        bad_dates.append((doc.get("document_id"), d))
check("4. Dates are ISO YYYY-MM-DD or null", len(bad_dates) == 0,
      f"{len(bad_dates)} bad dates" if bad_dates else "All dates valid")
if bad_dates:
    for did, d in bad_dates[:5]:
        print(f"     → doc_id={did}: '{d}'")

# ─────────────────────────────────────────────
# 5. simplified_text is {ar, fr, en}
# ─────────────────────────────────────────────
bad_simplified = []
for doc in data:
    st = doc.get("simplified_text")
    if not isinstance(st, dict) or not all(k in st for k in ("ar", "fr", "en")):
        bad_simplified.append(doc.get("document_id"))
check("5. simplified_text is {ar, fr, en} object", len(bad_simplified) == 0,
      f"{len(bad_simplified)} docs wrong format" if bad_simplified else "All multilingual")

# ─────────────────────────────────────────────
# 6. Keywords are flat {ar:[], fr:[]}
# ─────────────────────────────────────────────
bad_keywords = []
for doc in data:
    kw = doc.get("keywords")
    if not isinstance(kw, dict) or "ar" not in kw or "fr" not in kw:
        bad_keywords.append(doc.get("document_id"))
    elif not isinstance(kw["ar"], list) or not isinstance(kw["fr"], list):
        bad_keywords.append(doc.get("document_id"))
check("6. Keywords are flat {ar:[], fr:[]}", len(bad_keywords) == 0,
      f"{len(bad_keywords)} docs wrong format" if bad_keywords else "All flat objects")

# ─────────────────────────────────────────────
# 7. Domain values
# ─────────────────────────────────────────────
bad_domains = [doc.get("document_id") for doc in data if doc.get("domain") not in VALID_DOMAINS]
check("7. Domain in {startup, cnss, labor}", len(bad_domains) == 0,
      f"{len(bad_domains)} invalid" if bad_domains else "All valid")

# ─────────────────────────────────────────────
# 8. Document type values
# ─────────────────────────────────────────────
bad_doc_types = [doc.get("document_id") for doc in data if doc.get("document_type") not in VALID_DOC_TYPES]
check("8. document_type in {law, decree, guide, procedure, metadata}", len(bad_doc_types) == 0,
      f"{len(bad_doc_types)} invalid" if bad_doc_types else "All valid")

# ─────────────────────────────────────────────
# 9. Text field non-empty
# ─────────────────────────────────────────────
empty_text = [doc.get("document_id") for doc in data if not doc.get("text")]
check("9. text field non-empty", len(empty_text) == 0,
      f"{len(empty_text)} empty" if empty_text else "All documents have embedding text")

# ─────────────────────────────────────────────
# 10. Author is null or {ar, fr} with content
# ─────────────────────────────────────────────
bad_authors = []
for doc in data:
    a = doc.get("author")
    if a is None:
        continue  # valid
    if not isinstance(a, dict) or "ar" not in a or "fr" not in a:
        bad_authors.append(doc.get("document_id"))
    elif not a.get("ar") and not a.get("fr"):
        bad_authors.append(doc.get("document_id"))
check("10. Author is null or {ar, fr} with content", len(bad_authors) == 0,
      f"{len(bad_authors)} invalid" if bad_authors else "All valid")

# ─────────────────────────────────────────────
# 11. Unique document_ids
# ─────────────────────────────────────────────
ids = [doc.get("document_id") for doc in data]
unique_ids = set(ids)
check("11. Unique document_ids", len(ids) == len(unique_ids),
      f"{len(ids) - len(unique_ids)} duplicates" if len(ids) != len(unique_ids) else f"All {len(ids)} unique")

# ─────────────────────────────────────────────
# 12. Document count
# ─────────────────────────────────────────────
check("12. Document count matches source", len(data) == EXPECTED_COUNT,
      f"Got {len(data)}, expected {EXPECTED_COUNT}")

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
passed = sum(1 for _, s, _ in results if s == "PASS")
total = len(results)
print(f"\n{'='*50}")
print(f"Results: {passed}/{total} checks passed")
if passed == total:
    print("✓ ALL CHECKS PASSED — Dataset is RAG-ready!")
else:
    print(f"✗ {total - passed} check(s) FAILED — review issues above")
    sys.exit(1)
