"""
transform_dataset.py
====================
Transforms full_dataset.json into a RAG-optimized multilingual dataset.

Transformations applied:
  1. Normalize empty strings → null
  2. Normalize dates → ISO YYYY-MM-DD or null
  3. Nullable author (null if both ar/fr are empty)
  4. Multilingual simplified_text → {ar, fr, en}
  5. Flatten keywords from [{ar:[], fr:[]}] → {ar:[], fr:[]}
  6. Add domain field (startup / cnss / labor)
  7. Add document_type field (law / decree / guide / procedure / metadata)
  8. Generate unified text field for RAG embedding
  9. Remove startup_law_2018 boolean (redundant)
"""

import json
import re
import os
from datetime import datetime

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
INPUT_PATH = os.path.join("datasets", "full_dataset.json")
OUTPUT_PATH = os.path.join("datasets", "rag_dataset.json")

# ─────────────────────────────────────────────
# 1. Normalize empty strings → null (recursive)
# ─────────────────────────────────────────────
def normalize_nulls(obj):
    """Replace empty strings with None recursively. Keep empty lists as-is."""
    if isinstance(obj, str):
        return None if obj.strip() == "" else obj
    elif isinstance(obj, dict):
        return {k: normalize_nulls(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_nulls(item) for item in obj]
    return obj


# ─────────────────────────────────────────────
# 2. Normalize dates → ISO YYYY-MM-DD
# ─────────────────────────────────────────────
def normalize_date(date_val):
    """Convert DD-MM-YYYY → YYYY-MM-DD. Return None for empty/null."""
    if not date_val:
        return None
    date_val = str(date_val).strip()
    if not date_val:
        return None

    # Already ISO format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
        return date_val

    # DD-MM-YYYY format
    m = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', date_val)
    if m:
        day, month, year = m.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # DD/MM/YYYY format
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', date_val)
    if m:
        day, month, year = m.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Return as-is if unrecognized (shouldn't happen)
    return date_val


# ─────────────────────────────────────────────
# 3. Nullable author
# ─────────────────────────────────────────────
def normalize_author(author):
    """If both ar and fr are null/empty, return None. Else return cleaned dict."""
    if author is None:
        return None
    if isinstance(author, dict):
        ar = author.get("ar")
        fr = author.get("fr")
        if not ar and not fr:
            return None
        return {"ar": ar, "fr": fr}
    return None


# ─────────────────────────────────────────────
# 4. Multilingual simplified_text
# ─────────────────────────────────────────────
# Pre-built French translations keyed by document_id
# These are derived directly from the legal content in each document.
SIMPLIFIED_FR = {
    1: "Pour créer une entreprise en Tunisie : 1) Rédiger un PV de nomination du dirigeant. 2) Ouvrir un compte bancaire au nom de la société. 3) Enregistrer les statuts à la Recette des Finances dans les 60 jours. 4) S'immatriculer au RNE pour obtenir l'extrait. 5) Déclarer à la CNSS pour la couverture sociale. 6) Obtenir un cachet d'entreprise.",
    2: "Pour immatriculer une SARL : 1) Obtenir la déclaration d'existence et la carte fiscale. 2) Remplir le formulaire d'immatriculation au RNE. 3) Fournir le contrat de location ou titre de propriété. 4) Fournir le certificat de réservation de dénomination. 5) Soumettre les statuts signés et copies CIN. 6) Payer ~50 dinars de frais. 7) Recevoir l'extrait RNE.",
    3: "Lors de l'immatriculation, vous devez soumettre tous les documents requis (CIN, certificat de dénomination, statuts, etc). Le bureau enregistre votre demande et vous délivre un récépissé immédiatement.",
    4: "Toute modification de votre société doit être déclarée dans le mois. Cela inclut la cessation d'activité, le décès du propriétaire ou les changements de tutelle.",
    5: "Les entreprises doivent déposer leurs états financiers dans les 7 mois suivant la clôture de l'exercice. Tout changement de dirigeants ou de siège doit aussi être déclaré.",
    6: "Le centre d'enregistrement publie toutes les opérations dans un bulletin officiel. Les entreprises doivent indiquer leur numéro d'immatriculation sur tous les documents commerciaux.",
    7: "Retard d'immatriculation : pénalité de la moitié des frais par mois de retard. Fausses déclarations : jusqu'à 5 ans de prison et 50 000 dinars d'amende. Falsification de documents : jusqu'à 15 ans et 100 000 dinars.",
    8: "Les tribunaux et institutions doivent transférer tous les dossiers au nouveau centre d'enregistrement dans les 3 mois. Les entreprises existantes doivent mettre à jour leurs données dans les 6 mois.",
    9: "Créer une SA en ligne via le site de l'API en 24 heures. Pas besoin de documents papier. Les étapes passent automatiquement par le bureau fiscal, le greffe et le JORT.",
    10: "Utiliser le Guichet Unique pour créer tout type de société (SARL, SUARL, SA) en 24 heures. Un interlocuteur unique s'occupe de toutes les démarches : impôts, greffe, douane, CNSS.",
    11: "Pour augmenter le capital d'une SA : enregistrer les documents à la Recette des Finances, au greffe du tribunal et publier au JORT. Fait en 24 heures.",
    12: "Obtenir votre numéro d'identification en douane au Guichet Unique de l'API. Fait immédiatement sur place.",
    13: "Inscrire votre société à la CNSS pour la sécurité sociale au bureau de l'API. Fait immédiatement sur place.",
    14: "Si vous êtes fondateur, gérant ou PDG, vous devez vous inscrire comme travailleur non salarié à la CNSS. Fait immédiatement.",
    15: "Les employeurs et travailleurs étrangers peuvent obtenir une attestation de non-soumission au visa du contrat de travail. Délai : 3 jours.",
    16: "Les investisseurs étrangers peuvent obtenir une carte de séjour au bureau de l'API. Récépissé immédiat, carte livrée dans le mois.",
    17: "Publier les documents de constitution de votre société au Journal Officiel (JORT). Fait immédiatement.",
    18: "L'API fournit des informations sur les opportunités d'investissement, les avantages fiscaux, douaniers, la sécurité sociale et les procédures d'emploi en Tunisie.",
    19: "Les entreprises nécessitant un cahier des charges peuvent déclarer leur activité à l'API. Fait immédiatement.",
    20: "Tout employeur doit inscrire ses salariés à la CNSS. Les travailleurs indépendants doivent également s'inscrire. Les règles d'inscription sont fixées par décret.",
    21: "Le taux de cotisation est de 7,5% des 2/3 du salaire minimum. L'employeur paie 2/3 de la cotisation, le salarié 1/3. Les indépendants paient la totalité.",
    22: "Les modalités de recouvrement des cotisations de sécurité sociale sont déterminées par décret.",
    23: "Si un employeur oublie de déduire les cotisations, il ne peut pas récupérer l'argent auprès du travailleur par la suite. L'employeur doit compenser tout préjudice causé par son retard.",
    24: "La couverture santé de la CNSS couvre : l'assuré, le conjoint, les enfants mineurs, les enfants adultes handicapés, les filles non mariées sans revenus et les parents à charge.",
    25: "Toutes les personnes listées à l'article 10 bénéficient des prestations de santé fournies par la CNSS.",
    26: "Seules les périodes de cotisation effectives comptent pour le calcul des droits à la retraite.",
    27: "Pour obtenir une pension de retraite : avoir au moins 65 ans, avoir au moins 120 mois de cotisations et ne pas exercer d'emploi rémunéré.",
    28: "Pension minimale de retraite : 30% du salaire minimum. Les cotisations supplémentaires au-delà de 120 mois ajoutent 0,5% par trimestre, jusqu'à un maximum de 80% du salaire.",
    29: "La pension d'invalidité est pour les travailleurs ayant perdu au moins 2/3 de leur capacité de travail pour des causes non professionnelles.",
    30: "Pour obtenir une pension d'invalidité : ne pas avoir atteint l'âge de la retraite et avoir au moins 60 mois de cotisations.",
    31: "Pension d'invalidité : 30% du salaire minimum, plus 0,5% par trimestre supplémentaire de cotisations, jusqu'à un maximum de 80%.",
    32: "Si une personne invalide a besoin d'aide pour les actes quotidiens, sa pension est augmentée de 20%.",
    33: "Le conjoint survivant reçoit une pension si le défunt remplissait les conditions de retraite ou d'invalidité.",
    34: "La pension de survivant est égale à 50% de la pension de retraite ou d'invalidité du défunt.",
    35: "Les demandes de pension doivent être soumises à la CNSS dans les 5 ans suivant l'âge de la retraite, l'arrêt de travail ou le décès. Les demandes tardives perdent les paiements antérieurs.",
    36: "La pension commence le 1er jour du mois suivant l'arrêt de travail, la reconnaissance d'invalidité ou le décès. Les paiements cessent si les conditions ne sont plus remplies.",
    37: "La CNSS reprend automatiquement les droits de la victime ou des héritiers pour récupérer les frais médicaux causés par un accident ou une blessure.",
    38: "Les petits agriculteurs, pêcheurs et artisans peuvent demander la sécurité sociale dans l'année suivant l'entrée en vigueur de la loi.",
    39: "Un contrat de travail existe lorsqu'une personne travaille sous l'autorité d'un employeur contre rémunération. Il peut être écrit ou verbal.",
    40: "Les contrats à durée déterminée (CDD) ne sont autorisés que pour un surcroît temporaire d'activité, le remplacement d'un salarié absent ou un travail saisonnier. Durée maximale : 4 ans.",
    41: "Si un CDD dépasse la durée légale ou est renouvelé illégalement, il devient automatiquement un contrat à durée indéterminée (CDI).",
    42: "Les salariés en CDD doivent recevoir le même salaire et les mêmes conditions de travail que les salariés permanents.",
    43: "Une période d'essai peut être incluse dans le contrat de travail. Chaque partie peut y mettre fin sans indemnité mais doit respecter le préavis.",
    44: "Le contrat de travail est suspendu (non résilié) en cas de maladie, accident ou congé maternité. Le salarié a le droit de reprendre son poste après.",
    45: "Le licenciement doit être justifié par une cause réelle et sérieuse. L'employeur doit respecter le préavis légal.",
    46: "Un licenciement sans justification légale ou factuelle est abusif. L'employeur peut devoir verser des dommages et intérêts au salarié.",
}

# Arabic simplified texts for Startup Law 2018 documents (entry6)
SIMPLIFIED_AR = {
    47: "علامة المؤسسة الناشئة صالحة لمدة 8 سنوات. تنظر لجنة في الطلبات. للحصول عليها يجب أن تكون شركتك مبتكرة ذات إمكانات نمو عالية. يمكن سحب العلامة إذا لم تعد الشروط مستوفاة.",
    48: "يمكن للمؤسسين الحصول على عطلة لمدة سنة من عملهم لإنشاء مؤسسة ناشئة (قابلة للتجديد مرة واحدة). يمكن لما يصل إلى 3 مؤسسين الحصول على منحة شهرية. يمكن لحاملي الشهادات الجدد تأجيل برامج التشغيل لمدة 3 سنوات.",
    49: "تساعد الدولة المؤسسات الناشئة في تسجيل براءات الاختراع وطنياً ودولياً. يأتي التمويل من صندوق تنمية الاتصالات وتكنولوجيات المعلومات.",
    50: "تحصل المؤسسات الناشئة على إعفاءات ضريبية وتغطية اجتماعية وحوافز استثمارية. صناديق متخصصة تدعم مراحل البذر والمبكرة والمتأخرة.",
    51: "يمكن للمؤسسات الناشئة فتح حسابات بالعملة الأجنبية واستخدامها بحرية للمساهمات في رأس المال وتسبقات الشركاء.",
    52: "صندوق ضمان المؤسسات الناشئة، تديره الشركة التونسية للضمان، يؤمّن الاستثمارات في المؤسسات الناشئة. يموّل من صندوق تنمية الاتصالات.",
    53: "تعتبر المؤسسات الناشئة الحاصلة على العلامة تلقائياً متعاملين اقتصاديين معتمدين لأغراض الجمارك.",
}

def normalize_simplified_text(doc):
    """Convert simplified_text string → {ar, fr, en} object."""
    doc_id = doc.get("document_id")
    current = doc.get("simplified_text")

    if isinstance(current, dict):
        # Already transformed (shouldn't happen, but handle gracefully)
        return current

    en_text = current if current else None
    fr_text = SIMPLIFIED_FR.get(doc_id)
    ar_text = SIMPLIFIED_AR.get(doc_id)

    return {
        "ar": ar_text,
        "fr": fr_text,
        "en": en_text,
    }


# ─────────────────────────────────────────────
# 5. Flatten keywords
# ─────────────────────────────────────────────
def flatten_keywords(keywords):
    """Transform [{ar:[], fr:[]}] → {ar:[], fr:[]}. Merge if multiple entries."""
    if not keywords:
        return {"ar": [], "fr": []}

    if isinstance(keywords, dict):
        # Already flat
        return {
            "ar": keywords.get("ar", []),
            "fr": keywords.get("fr", []),
        }

    if isinstance(keywords, list):
        merged_ar = []
        merged_fr = []
        for entry in keywords:
            if isinstance(entry, dict):
                for k in entry.get("ar", []):
                    if k and k not in merged_ar:
                        merged_ar.append(k)
                for k in entry.get("fr", []):
                    if k and k not in merged_fr:
                        merged_fr.append(k)
        return {"ar": merged_ar, "fr": merged_fr}

    return {"ar": [], "fr": []}


# ─────────────────────────────────────────────
# 6. Add domain field
# ─────────────────────────────────────────────
TYPE_TO_DOMAIN = {
    "Code du travail": "labor",
}

def infer_domain(doc):
    """Infer domain from procedure_category and type."""
    cat = doc.get("procedure_category")
    doc_type = doc.get("type", "")

    if doc_type in TYPE_TO_DOMAIN:
        return TYPE_TO_DOMAIN[doc_type]

    if cat in ("cnss_employer", "cnss_employee"):
        return "cnss"
    if cat == "startup":
        return "startup"
    if cat == "legal_registration":
        return "startup"  # legal registration is part of startup creation domain

    return "startup"


# ─────────────────────────────────────────────
# 7. Add document_type field
# ─────────────────────────────────────────────
TYPE_MAPPING = {
    "Loi / Reglementation": "law",
    "Loi securite sociale": "law",
    "Code du travail": "law",
    "Loi Startup 2018": "decree",
    "Arrêté gouvernemental / Government Order": "decree",
    "Guide officiel": "guide",
    "Donnees structurees": "guide",
    "Programme gouvernemental": "guide",
    "Procedure administrative": "procedure",
    "Procedure Guichet Unique": "procedure",
    "Metadonnees": "metadata",
}

def infer_document_type(doc):
    """Map existing type field to normalized document_type."""
    raw_type = doc.get("type", "")
    if raw_type in TYPE_MAPPING:
        return TYPE_MAPPING[raw_type]
    # Fallback: check for keywords
    if raw_type and "loi" in raw_type.lower():
        return "law"
    if raw_type and ("arrêté" in raw_type.lower() or "décret" in raw_type.lower()):
        return "decree"
    if raw_type and "guide" in raw_type.lower():
        return "guide"
    if raw_type and "procedure" in raw_type.lower():
        return "procedure"
    return "law"  # safe default


# ─────────────────────────────────────────────
# 8. Generate unified text field for RAG embedding
# ─────────────────────────────────────────────
def safe_str(val):
    """Return string or empty string for None."""
    return val if val else ""

def generate_text_field(doc):
    """Merge relevant content into one searchable text field."""
    parts = []

    # Title
    title = doc.get("title", {})
    if isinstance(title, dict):
        t_fr = safe_str(title.get("fr"))
        t_ar = safe_str(title.get("ar"))
        if t_fr or t_ar:
            parts.append(f"{t_fr} | {t_ar}".strip(" |"))

    # Summary
    summary = doc.get("summary", {})
    if isinstance(summary, dict):
        s_fr = safe_str(summary.get("fr"))
        s_ar = safe_str(summary.get("ar"))
        combined = f"{s_fr} {s_ar}".strip()
        if combined:
            parts.append(combined)

    # Section contents
    sections = doc.get("sections", [])
    for sec in sections:
        content = sec.get("content", {})
        if isinstance(content, dict):
            c_fr = safe_str(content.get("fr"))
            c_ar = safe_str(content.get("ar"))
            combined = f"{c_fr} {c_ar}".strip()
            if combined:
                parts.append(combined)
        elif isinstance(content, str) and content:
            parts.append(content)

    # Simplified text (after transformation to multilingual object)
    simp = doc.get("simplified_text", {})
    if isinstance(simp, dict):
        for lang in ("en", "fr", "ar"):
            val = simp.get(lang)
            if val:
                parts.append(val)

    return "\n".join(parts)


# ─────────────────────────────────────────────
# Main transformation pipeline
# ─────────────────────────────────────────────
def transform_document(doc):
    """Apply all transformations to a single document."""

    # 1. Normalize empty strings → null
    doc = normalize_nulls(doc)

    # 2. Normalize date
    doc["date"] = normalize_date(doc.get("date"))

    # 3. Nullable author
    doc["author"] = normalize_author(doc.get("author"))

    # 4. Multilingual simplified_text
    doc["simplified_text"] = normalize_simplified_text(doc)

    # 5. Flatten keywords
    doc["keywords"] = flatten_keywords(doc.get("keywords"))

    # 6. Add domain
    doc["domain"] = infer_domain(doc)

    # 7. Add document_type
    doc["document_type"] = infer_document_type(doc)

    # 8. Generate text field (must be after simplified_text transform)
    doc["text"] = generate_text_field(doc)

    # 9. Remove redundant field
    doc.pop("startup_law_2018", None)

    # Ensure consistent field ordering
    ordered = {
        "document_id": doc.get("document_id"),
        "title": doc.get("title"),
        "date": doc.get("date"),
        "author": doc.get("author"),
        "type": doc.get("type"),
        "law_number": doc.get("law_number"),
        "related_laws": doc.get("related_laws", []),
        "procedure_category": doc.get("procedure_category"),
        "domain": doc.get("domain"),
        "document_type": doc.get("document_type"),
        "source_document": doc.get("source_document"),
        "summary": doc.get("summary"),
        "simplified_text": doc.get("simplified_text"),
        "keywords": doc.get("keywords"),
        "sections": doc.get("sections", []),
        "text": doc.get("text"),
    }
    return ordered


def main():
    # Load
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"[INFO] Loaded {len(dataset)} documents from {INPUT_PATH}")

    # Transform
    transformed = [transform_document(doc) for doc in dataset]

    # Write
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)

    print(f"[OK] Wrote {len(transformed)} documents to {OUTPUT_PATH}")

    # Summary stats
    from collections import Counter
    domains = Counter(d["domain"] for d in transformed)
    doc_types = Counter(d["document_type"] for d in transformed)

    print(f"\n--- Domain distribution ---")
    for k, v in domains.most_common():
        print(f"  {k}: {v}")

    print(f"\n--- Document type distribution ---")
    for k, v in doc_types.most_common():
        print(f"  {k}: {v}")

    with_text = sum(1 for d in transformed if d.get("text"))
    with_simplified = sum(1 for d in transformed if d.get("simplified_text", {}).get("en"))
    null_authors = sum(1 for d in transformed if d.get("author") is None)
    null_dates = sum(1 for d in transformed if d.get("date") is None)

    print(f"\n--- Field coverage ---")
    print(f"  text field present:       {with_text}/{len(transformed)}")
    print(f"  simplified_text.en:       {with_simplified}/{len(transformed)}")
    print(f"  author is null:           {null_authors}/{len(transformed)}")
    print(f"  date is null:             {null_dates}/{len(transformed)}")


if __name__ == "__main__":
    main()
