# Tunisian Startup & CNSS Legal Dataset

## Overview

A structured, multilingual (Arabic/French) dataset of **official Tunisian government legal documents** covering **startup creation** and **CNSS (social security) procedures**. Built for the **AI-Based Multilingual Backend System for Tunisian Startup Creation and CNSS Procedures** academic project.

**62 documents** extracted from 11 source files, normalized into a unified bilingual schema with simplified plain-language summaries.

---

## Dataset Scope

### Included Topics

| Category | Documents | Description |
|----------|-----------|-------------|
| `startup` | 26 | Startup creation, Label Startup, Startup Act 2018, financial incentives, government programs |
| `cnss_employee` | 23 | Pensions (retirement, disability, survivor), healthcare, labor code (CDD/CDI, dismissal) |
| `cnss_employer` | 6 | Employer CNSS registration, contribution obligations, worker affiliation |
| `legal_registration` | 7 | Company registration (RNE), document filing, sanctions, transitional provisions |

### Source Documents

| File | Content | Type |
|------|---------|------|
| `entry1.json` | Company creation procedures (PV, SARL) | Guide API |
| `entry2.json` | Company registration law (Articles 21-64) | Loi |
| `entry3.json` | API Guichet Unique procedures | Guide administratif |
| `entry4.json` | CNSS social security law (Articles 6-38) | Loi |
| `entry5.json` | Employment/Labor code (Articles 6-20) | Code du travail |
| `entry6.json` | Startup Law 2018 — detailed structure (Arabic) | Loi |
| `entry7.json` | Startup Law 2018 — bilingual articles | Loi |
| `entry8.json` | Guide Startups Tunisie | Guide officiel |
| `entry9.json` | Startup ecosystem structured data | Données structurées |
| `entry10.json` | Programme Startup Tunisia | Programme gouvernemental |
| `entry11.json` | Government Order 840/2018 | Décret gouvernemental |
| `metadata.json` | Law 20/2018 metadata | Métadonnées |

### Excluded Topics
- Tax declaration details
- Accounting or financial management
- Legal decision-making or legal advice

---

## Schema

Every document in `full_dataset.json` follows this structure:

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | `int` | Unique numeric identifier |
| `title` | `{ar, fr}` | Document title in Arabic and French |
| `date` | `string` | Publication date (DD-MM-YYYY) |
| `author` | `{ar, fr}` | Author/ministry in Arabic and French |
| `type` | `string` | Document type (Loi, Décret, Guide, etc.) |
| `law_number` | `string` | Official law/order reference number |
| `related_laws` | `string[]` | List of related law references |
| `summary` | `{ar, fr}` | Short summary in Arabic and French |
| `sections` | `Section[]` | Array of structured sections (see below) |
| `keywords` | `Keyword[]` | Keywords in Arabic and French |
| `startup_law_2018` | `bool` | Whether document relates to Startup Act 2018 |
| `procedure_category` | `string` | One of: `startup`, `cnss_employer`, `cnss_employee`, `legal_registration` |
| `simplified_text` | `string` | Plain-language English summary for search & QA |
| `source_document` | `string` | Original source filename for traceability |

### Section Object

```json
{
  "section_id": 1,
  "title": { "ar": "...", "fr": "..." },
  "content": { "ar": "...", "fr": "..." }
}
```

### Example Entry

```json
{
  "document_id": 1,
  "title": {
    "ar": "",
    "fr": "Procès-Verbal de nomination et formalités de création d'entreprise"
  },
  "date": "",
  "author": { "ar": "", "fr": "" },
  "type": "Procédure administrative",
  "law_number": "Guide du Guichet Unique de l'API, pages 15-22",
  "related_laws": [],
  "summary": {
    "ar": "",
    "fr": "Procédures pour nommer un dirigeant et accomplir les démarches légales pour créer une société en Tunisie."
  },
  "sections": [
    {
      "section_id": 1,
      "title": { "ar": "", "fr": "Étape 1" },
      "content": { "ar": "", "fr": "Rédiger un procès-verbal de nomination..." }
    }
  ],
  "keywords": [{ "ar": [], "fr": ["startup", "company_creation"] }],
  "startup_law_2018": false,
  "procedure_category": "startup",
  "simplified_text": "To create a company in Tunisia: 1) Draft minutes naming the manager...",
  "source_document": "entry1.json"
}
```

---

## Usage

### Generate the Dataset

```bash
python merge_dataset.py
```

This reads all 11 entry files + `metadata.json`, normalizes them into the unified schema, and outputs `datasets/full_dataset.json`.

### Validate the Dataset

```bash
python test.py
```

Checks all 11 mandatory fields, bilingual structure, duplicate IDs, and numeric limits.

### Load into MongoDB

```bash
python create_dataset.py
```

Inserts all documents into MongoDB (`datasets.datasets_law` collection).

### Query the Dataset (Python)

```python
import json

with open("datasets/full_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Filter by category
startup_docs = [d for d in dataset if d["procedure_category"] == "startup"]
cnss_docs = [d for d in dataset if d["procedure_category"].startswith("cnss")]

# Search simplified text
query = "how to register"
results = [d for d in dataset if query.lower() in d["simplified_text"].lower()]
```

---

## Project Integration

This dataset is designed for the **AI-Based Multilingual Backend System** FastAPI project:

| Project Requirement | Dataset Support |
|---------------------|-----------------|
| **FR1** – Document Collection | 62 documents from 7 official source types |
| **FR2** – Procedure Extraction | `procedure_category` field enables direct filtering |
| **FR3** – Multilingual Search | Bilingual `title`/`summary`/`sections` + English `simplified_text` |
| **FR4** – Simplification | `simplified_text` provides plain-language explanations |
| **FR5** – Question Answering | `source_document` enables source attribution |
| **FR7** – Business Intelligence | Category counts, keyword frequency, document type distribution |

### Suggested API Mapping

```
GET /procedures/startup      → procedure_category == "startup"
GET /procedures/cnss         → procedure_category in ("cnss_employer", "cnss_employee")
POST /ask                    → semantic search over simplified_text + sections
GET /analytics/procedures    → aggregate by procedure_category
GET /analytics/overview      → total counts, category distribution
```

---

## Legal References

| Reference | Description |
|-----------|-------------|
| Loi N°2018-20 du 17 avril 2018 | Startup Act — legal framework for startups |
| Décret N°2018-840 du 11 octobre 2018 | Implementation decree for Label Startup |
| Circulaires BCT N°2019-01 et N°2019-02 | Central Bank circulars for startup finance |
| Code de la sécurité sociale (Loi 30/1960) | CNSS social security framework |
| Code du travail (Loi 51/2007) | Employment and labor law |

---

## Project Structure

```
dataset/
├── datasets/
│   ├── entry1.json  ... entry11.json   # Source documents
│   ├── metadata.json                   # Law metadata
│   └── full_dataset.json               # ← Merged & normalized output
├── docs/                               # Supporting documentation
├── merge_dataset.py                    # Dataset merge & normalization script
├── create_dataset.py                   # MongoDB insertion script
├── check_dataset.py                    # MongoDB validation script
├── test.py                             # Schema validation script
└── readme.md                           # This file
```

---

## Constraints

- **Academic use only** — informational, not legal advice
- **Public documents only** — sourced from JORT, API guides, CNSS documentation
- **Small-scale dataset** — 7 source documents, 62 structured entries
- **No legal liability** — simplified texts preserve meaning but are not official interpretations

---

## Languages

- **French** — primary legal language for Tunisian law
- **Arabic** — official language, especially for Startup Act 2018
- **English** — simplified summaries for multilingual search and QA
- **Tunisian Dialect** — supported at the NLP/application layer, not in raw data
