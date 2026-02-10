import json
import os

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
_next_id = 1

def next_id():
    global _next_id
    v = _next_id
    _next_id += 1
    return v

def bi(ar="", fr=""):
    return {"ar": ar, "fr": fr}

def make_doc(*, title_fr="", title_ar="", date="", author_fr="", author_ar="",
             doc_type="", law_number="", related_laws=None, summary_fr="",
             summary_ar="", sections=None, keywords_fr=None, keywords_ar=None,
             startup_law_2018=False, procedure_category="",
             simplified_text="", source_document=""):
    return {
        "document_id": next_id(),
        "title": bi(title_ar, title_fr),
        "date": date,
        "author": bi(author_ar, author_fr),
        "type": doc_type,
        "law_number": law_number,
        "related_laws": related_laws or [],
        "summary": bi(summary_ar, summary_fr),
        "sections": sections or [],
        "keywords": [{"ar": keywords_ar or [], "fr": keywords_fr or []}],
        "startup_law_2018": startup_law_2018,
        "procedure_category": procedure_category,
        "simplified_text": simplified_text,
        "source_document": source_document,
    }

def make_section(sid, title_fr="", title_ar="", content_fr="", content_ar=""):
    return {
        "section_id": sid,
        "title": bi(title_ar, title_fr),
        "content": bi(content_ar, content_fr)
    }

# ─────────────────────────────────────────────
# Process each entry file
# ─────────────────────────────────────────────
all_docs = []

# ============================================================
# entry1.json  (startup company creation procedures)
# ============================================================
with open("datasets/entry1.json", encoding="utf-8") as f:
    data = json.load(f)

simplified_map_e1 = {
    "startup_001": (
        "To create a company in Tunisia: 1) Draft minutes naming the manager. "
        "2) Open a bank account in the company name. 3) Register statutes at "
        "the tax office within 60 days. 4) Register at the RNE to get your "
        "company extract. 5) Declare to CNSS for social coverage. 6) Get a "
        "company stamp."
    ),
    "startup_002": (
        "To register a SARL: 1) Get data_existence certificate and tax ID. "
        "2) Fill the RNE registration form. 3) Provide rental contract or "
        "property title. 4) Provide company name reservation certificate. "
        "5) Submit signed statutes and ID copies. 6) Pay ~50 dinars registration fee. "
        "7) Receive your RNE extract."
    ),
}

for item in data:
    sections = []
    for i, step in enumerate(item.get("steps_or_rules", []), 1):
        sections.append(make_section(i, title_fr=f"Etape {i}", content_fr=step))
    all_docs.append(make_doc(
        title_fr=item.get("title", ""),
        doc_type="Procedure administrative",
        law_number=item.get("legal_source", ""),
        summary_fr=item.get("description", ""),
        sections=sections,
        keywords_fr=[item.get("domain", ""), item.get("category", "")],
        procedure_category="startup",
        simplified_text=simplified_map_e1.get(item.get("id", ""), item.get("description", "")),
        source_document="entry1.json",
    ))

# ============================================================
# entry2.json  (company registration law articles)
# ============================================================
with open("datasets/entry2.json", encoding="utf-8") as f:
    data = json.load(f)

cat_map_e2 = {
    "reg_001": "legal_registration",
    "reg_002": "legal_registration",
    "reg_003": "legal_registration",
    "reg_004": "legal_registration",
    "reg_005": "legal_registration",
    "reg_006": "legal_registration",
}

simplified_map_e2 = {
    "reg_001": "When registering a company, you must submit all required documents (ID, company name certificate, statutes, etc). The office records your application and gives you a receipt immediately.",
    "reg_002": "Any changes to your company must be reported within one month. This includes stopping activity, death of the owner, or guardianship changes.",
    "reg_003": "Companies must submit their financial statements within 7 months after the end of the fiscal year. Any changes to directors or headquarters must also be reported.",
    "reg_004": "The registration center publishes all company operations in an official bulletin. Companies must show their registration number on all commercial documents.",
    "reg_005": "Late registration: penalty of half the fee per month late. False declarations: up to 5 years prison and 50,000 dinars fine. Forgery of official documents: up to 15 years and 100,000 dinars.",
    "reg_006": "Courts and other institutions must transfer all company files to the new registration center within 3 months. Existing companies must update their data within 6 months.",
}

for item in data:
    rid = item.get("id", "")
    sections = []
    for i, step in enumerate(item.get("steps_or_rules", []), 1):
        sections.append(make_section(i, title_fr=f"Regle {i}", content_fr=step))
    all_docs.append(make_doc(
        title_fr=item.get("title", ""),
        doc_type="Loi / Reglementation",
        law_number=item.get("legal_source", ""),
        summary_fr=item.get("description", ""),
        sections=sections,
        keywords_fr=[item.get("domain", ""), item.get("category", "")],
        procedure_category=cat_map_e2.get(rid, "legal_registration"),
        simplified_text=simplified_map_e2.get(rid, item.get("description", "")),
        source_document="entry2.json",
    ))

# ============================================================
# entry3.json  (API Guichet Unique procedures)
# ============================================================
with open("datasets/entry3.json", encoding="utf-8") as f:
    data = json.load(f)

simplified_map_e3 = [
    "Create a company (SA) online via the API website in 24 hours. No paper documents needed. Steps go through tax office, court registry, and official gazette automatically.",
    "Use the one-stop-shop (Guichet Unique) to create any company type (SARL, SUARL, SA) in 24 hours. One person handles all steps for you: taxes, court, customs, social security.",
    "To increase capital of a SA: register the documents at the tax office, court registry, and publish in the official gazette. Done in 24 hours.",
    "Get your customs identification number at the API one-stop-shop. Done immediately on the spot.",
    "Register your company with CNSS social security at the API office. Done immediately on the spot.",
    "If you are a founder, manager, or CEO, you must register as a non-salaried worker with CNSS. Done immediately.",
    "Foreign employers and workers can get a work permit exemption certificate. Takes 3 days.",
    "Foreign investors can get a residence permit at the API office. Receipt given immediately, card delivered within 1 month.",
    "Publish your company formation documents in the official gazette (JORT). Done immediately.",
    "The API provides information about investment opportunities, tax advantages, customs, social security, and employment procedures in Tunisia.",
    "Companies requiring a specifications booklet (cahier des charges) can declare their activity at the API. Done immediately.",
]

for idx, item in enumerate(data):
    sections = []
    for i, bureau in enumerate(item.get("bureaux_intervenants", []), 1):
        sections.append(make_section(i, title_fr=f"Bureau {i}", content_fr=bureau))
    # Determine category
    title = item.get("title", "").lower()
    if "cnss" in title or "securite sociale" in title or "affiliation" in title:
        cat = "cnss_employer"
    elif "carte de sejour" in title or "attestation" in title:
        cat = "legal_registration"
    else:
        cat = "startup"
    all_docs.append(make_doc(
        title_fr=item.get("title", ""),
        doc_type="Procedure Guichet Unique",
        summary_fr=f"Eligibilite: {item.get('eligibility', '')}. Delai: {item.get('delai_global', '')}.",
        sections=sections,
        keywords_fr=["Guichet Unique", "API", item.get("title", "")],
        procedure_category=cat,
        simplified_text=simplified_map_e3[idx] if idx < len(simplified_map_e3) else "",
        source_document="entry3.json",
    ))

# ============================================================
# entry4.json  (CNSS social security law articles)
# ============================================================
with open("datasets/entry4.json", encoding="utf-8") as f:
    data = json.load(f)

# Articles 6-9: employer obligations; 10+: employee benefits
simplified_map_e4 = {
    6: "Every employer must register their employees with CNSS. Self-employed workers must also register. Registration rules are set by decree.",
    7: "Social security contributions are 7.5% of 2/3 of the minimum wage. Employers pay 2/3 of the contribution, employees pay 1/3. Self-employed pay the full amount.",
    8: "The methods for collecting social security contributions are determined by decree.",
    9: "If an employer forgets to deduct contributions, they cannot recover the money from the worker later. The employer must compensate any harm caused by their delay.",
    10: "Social security healthcare covers: the insured person, their spouse, minor children, disabled adult children, unmarried daughters without income, and dependent parents.",
    11: "All persons listed in Article 10 benefit from healthcare services provided by CNSS.",
    12: "Only actual contribution periods count when calculating pension rights.",
    13: "To get a retirement pension: be at least 65 years old, have at least 120 months of contributions, and not be working in a paid job.",
    14: "Minimum retirement pension: 30% of the minimum wage. Extra contributions beyond 120 months add 0.5% per quarter, up to a maximum of 80% of salary.",
    15: "Disability pension is for workers who lose at least 2/3 of their working capacity due to non-work-related causes.",
    16: "To get a disability pension: you must not have reached retirement age and must have at least 60 months of contributions.",
    17: "Disability pension: 30% of minimum wage, plus 0.5% per extra quarter of contributions, up to 80% maximum.",
    18: "If a disabled person needs help with daily activities, their pension is increased by 20%.",
    21: "The surviving spouse receives a pension if the deceased met the conditions for retirement or disability pension.",
    23: "Survivor's pension equals 50% of the deceased's retirement or disability pension.",
    29: "Pension applications must be submitted to CNSS within 5 years of reaching retirement age, stopping work, or death. Late applications lose past payments.",
    30: "Pension starts on the 1st day of the month after stopping work, disability recognition, or death. Payments stop if conditions are no longer met.",
    35: "CNSS automatically takes over the victim's or heirs' rights to recover medical expenses caused by an accident or injury.",
    38: "Small farmers, fishermen, and artisans can apply for social security within one year after the law takes effect.",
}

for item in data:
    art = item.get("article", 0)
    ch = item.get("chapter", "")
    sec = item.get("section", "")
    sub = item.get("subsection", "")
    sections = [make_section(1, title_fr=item.get("title", ""), content_fr=item.get("content", ""))]

    if art <= 9:
        cat = "cnss_employer"
    else:
        cat = "cnss_employee"

    all_docs.append(make_doc(
        title_fr=f"Article {art} - {item.get('title', '')}",
        doc_type="Loi securite sociale",
        law_number=f"Loi CNSS - Article {art}",
        summary_fr=f"{ch}. {sec}. {sub}".strip(". "),
        sections=sections,
        keywords_fr=["CNSS", "securite sociale", ch],
        procedure_category=cat,
        simplified_text=simplified_map_e4.get(art, item.get("content", "")),
        source_document="entry4.json",
    ))

# ============================================================
# entry5.json  (Employment/Labor code articles)
# ============================================================
with open("datasets/entry5.json", encoding="utf-8") as f:
    data = json.load(f)

simplified_map_e5 = {
    "6": "An employment contract exists when someone works under the authority of an employer for pay. It can be written or verbal.",
    "6-2": "Fixed-term contracts (CDD) are only for temporary work increases, replacing absent workers, or seasonal work. Maximum total duration: 4 years.",
    "6-3": "If a CDD exceeds the legal limit or is renewed illegally, it automatically becomes a permanent contract (CDI).",
    "6-4": "CDD employees must receive the same salary and working conditions as permanent employees.",
    "18": "A trial period can be included in an employment contract. Either party can end it without compensation, but must respect the notice period.",
    "20": "An employment contract is paused (not ended) during illness, accident, or maternity leave. The employee has the right to return to their job afterward.",
    "14": "Firing an employee must be justified by a real and serious reason. The employer must respect the legal notice period.",
    "14 bis": "A dismissal without legal or factual justification is abusive. The employer may have to pay damages to the employee.",
}

for item in data:
    art = str(item.get("article", ""))
    sections = [make_section(1, title_fr=item.get("title", ""), content_fr=item.get("content", ""))]
    kw = ["Code du travail", item.get("section", "")]
    if item.get("importance"):
        kw.append(item["importance"])
    all_docs.append(make_doc(
        title_fr=f"Article {art} - {item.get('title', '')}",
        doc_type="Code du travail",
        law_number=f"Code du travail - Article {art}",
        summary_fr=item.get("content", "")[:200],
        sections=sections,
        keywords_fr=kw,
        procedure_category="cnss_employee",
        simplified_text=simplified_map_e5.get(art, item.get("content", "")),
        source_document="entry5.json",
    ))

# ============================================================
# entry6.json  (Startup Law 2018 detailed - Arabic)
# ============================================================
with open("datasets/entry6.json", encoding="utf-8") as f:
    data = json.load(f)
law = data.get("startup_law_2018", {})

simplified_map_e6 = {
    "startup_mark": "The Startup Label is valid for 8 years. A committee reviews applications. To get it, your company must be innovative with high growth potential. The label can be withdrawn if conditions are no longer met.",
    "founder_rights": "Founders can take 1-year leave from their job to create a startup (renewable once). Up to 3 founders can get a monthly grant. Fresh graduates can defer employment programs for 3 years.",
    "ip_support": "The state helps startups register patents nationally and internationally. Funding comes from the ICT Development Fund.",
    "financial_incentives": "Startups get tax exemptions, social security coverage, and investment incentives. Specialized funds support seed, early, and late-stage startups.",
    "foreign_currency_account": "Startups can open foreign currency accounts and use them freely for capital contributions and shareholder advances.",
    "startup_guarantee": "A Startup Guarantee Fund, managed by the Tunisian Guarantee Company, secures investments in startups. Funded by the ICT Development Fund.",
    "customs_status": "Labeled startups are automatically considered authorized economic operators for customs purposes.",
}

for key, val in law.items():
    if not isinstance(val, dict):
        continue
    art = val.get("article_number", "")
    kw_ar = val.get("keywords", [])
    text_ar = val.get("text", "")
    content_parts = []
    for k2, v2 in val.items():
        if k2 in ("article_number", "keywords", "text"):
            continue
        if isinstance(v2, dict):
            for k3, v3 in v2.items():
                content_parts.append(f"{k3}: {v3}")
        elif isinstance(v2, list):
            content_parts.append(", ".join(str(x) for x in v2))
        else:
            content_parts.append(f"{k2}: {v2}")
    sections = [make_section(1, title_ar=key, content_ar="\n".join(content_parts))]
    all_docs.append(make_doc(
        title_ar=key,
        title_fr=f"Startup Law 2018 - {key}",
        doc_type="Loi Startup 2018",
        law_number=f"2018-20 Article {art}",
        summary_ar=text_ar[:200] if text_ar else "",
        sections=sections,
        keywords_ar=kw_ar if isinstance(kw_ar, list) else [],
        keywords_fr=["Startup", key],
        startup_law_2018=True,
        procedure_category="startup",
        simplified_text=simplified_map_e6.get(key, ""),
        source_document="entry6.json",
    ))

# ============================================================
# entry7.json  (Startup Law 2018 bilingual articles)
# ============================================================
with open("datasets/entry7.json", encoding="utf-8") as f:
    data = json.load(f)

simplified_map_e7 = {
    "startup_law_2018_20_001": "This law creates a framework to encourage startups in Tunisia based on creativity, innovation, and new technologies, aiming for national and international competitiveness.",
    "startup_law_2018_20_002": "A Startup is any commercial company that has obtained the official Startup Label according to this law's requirements.",
    "startup_law_2018_20_003": "To get the Startup Label: company must be under 8 years old, under 100 employees, revenue under 15M dinars, 2/3 owned by individuals or investors, innovative business model, and high growth potential.",
    "startup_law_2018_20_004": "Anyone wanting to create a startup can get a Pre-Label for 6 months if they meet innovation and growth criteria. The full label requires actually creating the company.",
}

for item in data:
    sections = [make_section(1,
        title_fr=item.get("title", ""),
        content_fr=item.get("text_fr", ""),
        content_ar=item.get("text_ar", "")
    )]
    all_docs.append(make_doc(
        title_fr=item.get("title", ""),
        doc_type="Loi Startup 2018",
        law_number=f"2018-20 {item.get('article_number', '')}",
        summary_fr=item.get("text_fr", "")[:200],
        summary_ar=item.get("text_ar", "")[:200],
        sections=sections,
        keywords_fr=item.get("keywords", []),
        startup_law_2018=True,
        procedure_category="startup",
        simplified_text=simplified_map_e7.get(item.get("id", ""), ""),
        source_document="entry7.json",
    ))

# ============================================================
# entry8.json  (Guide Startups Tunisie)
# ============================================================
with open("datasets/entry8.json", encoding="utf-8") as f:
    data = json.load(f)
sections = []
for i, sec in enumerate(data.get("sections", []), 1):
    content_parts = []
    if sec.get("content"):
        content_parts.append(sec["content"])
    if sec.get("terms"):
        for t in sec["terms"]:
            content_parts.append(f"- {t['term']}: {t['definition']}")
    if sec.get("laws"):
        for l in sec["laws"]:
            content_parts.append(f"- {l['type']}: {l['reference']}")
    if sec.get("criteria"):
        for c in sec["criteria"]:
            content_parts.append(f"- {c['name']}: {c['description']}")
    if sec.get("process"):
        content_parts.extend(sec["process"])
    if sec.get("documents_required"):
        content_parts.extend(sec["documents_required"])
    if sec.get("for_entrepreneurs"):
        content_parts.extend(sec["for_entrepreneurs"])
    sections.append(make_section(i, title_fr=sec.get("section_title", ""), content_fr="\n".join(content_parts)))
all_docs.append(make_doc(
    title_fr=data.get("title", ""),
    doc_type="Guide officiel",
    summary_fr="Guide complet sur les startups en Tunisie: definitions, label, avantages et procedures.",
    sections=sections,
    keywords_fr=["Startup", "Guide", "Label", "Tunisie"],
    startup_law_2018=True,
    procedure_category="startup",
    simplified_text="Complete startup guide for Tunisia: what is a startup, how to get the Label, benefits (monthly grant 1000-5000 DT, tax exemption, patent coverage, leave to create startup), required documents (RNE extract, tax ID, statutes, CNSS attestation), and application process via startupact.tn portal.",
    source_document="entry8.json",
))

# ============================================================
# entry9.json  (Startup ecosystem structured data)
# ============================================================
with open("datasets/entry9.json", encoding="utf-8") as f:
    data = json.load(f)
sections = []
sid = 1
for top_key, top_val in data.items():
    content_lines = []
    if isinstance(top_val, dict):
        for k, v in top_val.items():
            content_lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    elif isinstance(top_val, list):
        for v in top_val:
            content_lines.append(json.dumps(v, ensure_ascii=False))
    else:
        content_lines.append(str(top_val))
    sections.append(make_section(sid, title_fr=top_key, content_fr="\n".join(content_lines)))
    sid += 1
all_docs.append(make_doc(
    title_fr="Ecosysteme Startup Tunisie - Donnees structurees",
    doc_type="Donnees structurees",
    summary_fr="Definition startup, cadre legal, procedure label, avantages financiers/fiscaux, obligations.",
    sections=sections,
    keywords_fr=["Startup", "Label", "Ecosysteme", "Tunisie"],
    startup_law_2018=True,
    procedure_category="startup",
    simplified_text="Tunisia had 1081 startups in 2022. Label conditions: under 8 years old, max 100 employees, max 15M dinars revenue, 2/3 owned by individuals/investors, innovative model. Benefits: 1-year creation leave, monthly grant (1000-5000 DT), patent coverage, tax exemption, foreign currency account (up to 100K DT/year). Growth obligations: 10 employees and 300K DT after 3 years, 30 employees and 1M DT after 5 years.",
    source_document="entry9.json",
))

# ============================================================
# entry10.json  (Programme Startup Tunisia bilingual)
# ============================================================
with open("datasets/entry10.json", encoding="utf-8") as f:
    data = json.load(f)
sections = []
for i, sec in enumerate(data.get("sections", []), 1):
    content_fr_parts = []
    content_ar = sec.get("content", "")
    if isinstance(content_ar, dict):
        content_ar = content_ar.get("ar", "")
    for key in ("direct_objectives", "strategic_objectives", "quantitative_objectives", "targets"):
        if key in sec:
            content_fr_parts.extend(sec[key])
    if "pillars" in sec:
        for p in sec["pillars"]:
            content_fr_parts.append(f"{p['name']}: {p['description']}")
    if "enablers" in sec:
        for e in sec["enablers"]:
            content_fr_parts.append(f"{e['name']}: {e['description']}")
    if "references" in sec:
        for r in sec["references"]:
            content_fr_parts.append(f"{r['type']}: {r['reference']}")
    if not content_fr_parts and isinstance(sec.get("content"), str):
        content_fr_parts.append(sec["content"])
    sections.append(make_section(i,
        title_fr=sec.get("section_title", ""),
        content_fr="\n".join(content_fr_parts),
        content_ar=content_ar if isinstance(content_ar, str) else ""
    ))
all_docs.append(make_doc(
    title_fr=data.get("title", ""),
    title_ar="برنامج المؤسسات الناشئة تونس",
    doc_type="Programme gouvernemental",
    summary_fr="Programme Startup Tunisia: objectifs, composantes (Act/Invest/Empower), indicateurs.",
    summary_ar="برنامج المؤسسات الناشئة: الأهداف والمكونات والمؤشرات",
    sections=sections,
    keywords_fr=["Startup Tunisia", "Programme", "Startup Act", "Startup Invest"],
    keywords_ar=["مؤسسة ناشئة", "برنامج", "تونس"],
    startup_law_2018=True,
    procedure_category="startup",
    simplified_text="National program to support startups in Tunisia. Goals: create 1000 startups (200/year), 10,000 jobs, 1 billion DT revenue, and launch a Tunisian unicorn. Three pillars: Startup Act (legal framework), Startup Invest (funding at all stages), Startup Empower (grants and support). All services available at www.startupAct.tn.",
    source_document="entry10.json",
))

# ============================================================
# entry11.json  (Already in target schema - enhance it)
# ============================================================
with open("datasets/entry11.json", encoding="utf-8") as f:
    data = json.load(f)
data["document_id"] = next_id()
data["procedure_category"] = "startup"
data["simplified_text"] = (
    "Government order implementing the 2018 Startup Law. Defines: "
    "1) How to apply for and lose the Startup Label. "
    "2) How the labeling committee works (public and private members). "
    "3) Benefits: creation leave, grants, employment fund support, patent registration. "
    "4) Ministers responsible for enforcement."
)
data["source_document"] = "entry11.json"
all_docs.append(data)

# ============================================================
# metadata.json  (General metadata)
# ============================================================
with open("datasets/metadata.json", encoding="utf-8") as f:
    meta = json.load(f)
sections = [make_section(1, title_fr="Metadonnees", content_fr=meta.get("text", ""))]
kw = meta.get("keywords", [])
all_docs.append(make_doc(
    title_fr=f"Metadonnees - Loi N deg {meta.get('law_number', '')}",
    title_ar="بيانات وصفية - قانون المؤسسات الناشئة",
    date=meta.get("date", ""),
    doc_type="Metadonnees",
    law_number=meta.get("law_number", ""),
    summary_fr=meta.get("text", "")[:200],
    sections=sections,
    keywords_fr=[k for k in kw if not any(c > '\u0600' for c in k)],
    keywords_ar=[k for k in kw if any(c > '\u0600' for c in k)],
    startup_law_2018=meta.get("startup_law_2018", False),
    procedure_category="startup",
    simplified_text="Law 20/2018 from April 17, 2018: The Tunisian Startup Act. Covers the legal framework, tax advantages, financial benefits, and administrative support for startups in Tunisia, including eligibility conditions, labeling, founder rights, IP support, grants, and guarantees.",
    source_document="metadata.json",
))

# ─────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────
output_path = "datasets/full_dataset.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_docs, f, ensure_ascii=False, indent=2)

print(f"[OK] Merged {len(all_docs)} documents into {output_path}")

# Print category summary
from collections import Counter
cats = Counter(d["procedure_category"] for d in all_docs)
print("\nProcedure categories:")
for cat, count in cats.most_common():
    print(f"  {cat}: {count} documents")

print(f"\nDocuments with simplified_text: {sum(1 for d in all_docs if d.get('simplified_text'))}/{len(all_docs)}")
print(f"Documents with source_document: {sum(1 for d in all_docs if d.get('source_document'))}/{len(all_docs)}")
