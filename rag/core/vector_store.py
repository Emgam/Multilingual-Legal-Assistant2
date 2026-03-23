# core/vector_store.py
import json
import os
import re
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from config.settings import (
    DATASET_PATH, INDEX_PATH, EMBED_MODEL, SUPPORTED_LANGS,
    TOP_K, SIMILARITY_THRESHOLD, SEARCH_LANG_MAP
)

# -------------------------------------------------------
# Keywords to detect question intent for better retrieval
# -------------------------------------------------------
STARTUP_KEYWORDS = [
    # Arabic / Darija
    "شركة", "تأسيس", "تسجيل", "نعمل شركة", "نفتح شركة", "RNE", "SARL", "SA",
    "عقد التأسيس", "رأس المال", "الجريدة الرسمية",
    # French
    "entreprise", "créer", "création", "startup", "immatriculer", "statuts",
    "capital", "associés", "SARL", "SA", "RNE", "guichet",
    # English
    "company", "startup", "register", "create", "incorporate", "business",
]

CNSS_KEYWORDS = [
    # Arabic / Darija
    "كناس", "CNSS", "تأمين", "ضمان اجتماعي", "خدام", "صاحب عمل",
    "اشتراك", "تصريح", "مستخدم",
    # French
    "cnss", "cotisation", "salarié", "employeur", "déclaration sociale",
    "sécurité sociale", "affiliation",
    # English
    "cnss", "social security", "employee", "employer", "contribution",
    "declaration", "social coverage",
]


def detect_question_category(question: str) -> str | None:
    """
    Detect whether question is about startup creation or CNSS.
    Returns 'startup', 'cnss', or None (search everything).
    """
    q = question.lower()
    startup_score = sum(1 for kw in STARTUP_KEYWORDS if kw.lower() in q)
    cnss_score    = sum(1 for kw in CNSS_KEYWORDS    if kw.lower() in q)

    if startup_score > cnss_score:
        return "startup"
    if cnss_score > startup_score:
        return "cnss"
    return None  # ambiguous — search without category filter


def build_documents(dataset: list) -> List[Document]:
    """
    Convert JSON dataset entries into LangChain Documents.
    Enriches page_content with keywords and sections for better retrieval.
    """
    docs = []
    skipped = 0

    for entry in dataset:
        if not isinstance(entry, dict):
            skipped += 1
            continue

        simplified = entry.get("simplified_text") or {}
        if not isinstance(simplified, dict):
            skipped += 1
            continue

        # Also build richer text from sections if available
        sections = entry.get("sections") or []

        for lang_key in SUPPORTED_LANGS:
            raw_text = simplified.get(lang_key)
            text = (raw_text or "").strip()
            if not text:
                continue

            title = entry.get("title") or {}
            title_text = (title.get(lang_key) or "").strip() if isinstance(title, dict) else str(title).strip()

            # Add section content to enrich the document
            section_texts = []
            for sec in sections:
                sec_content = (sec.get("content") or {}).get(lang_key, "")
                if sec_content:
                    section_texts.append(sec_content.strip())

            # Full text = title + simplified + sections
            parts = [p for p in [title_text, text] + section_texts if p]
            full_text = "\n\n".join(parts)

            category = str(entry.get("procedure_category") or "")

            docs.append(Document(
                page_content=full_text,
                metadata={
                    "document_id": str(entry.get("document_id") or ""),
                    "title":       title_text,
                    "source":      str(entry.get("source_document") or ""),
                    "category":    category,
                    "domain":      str(entry.get("domain") or ""),
                    "lang":        lang_key,
                },
            ))

    if skipped:
        print(f"   ⚠️  Skipped {skipped} malformed entries")
    print(f"   ✅ Built {len(docs)} documents")
    return docs


def load_vector_store(embeddings: OllamaEmbeddings) -> FAISS:
    if os.path.exists(INDEX_PATH):
        print("📂 Loading existing FAISS index...")
        return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    print("🔨 Building FAISS index from dataset...")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"   Loaded {len(data)} dataset entries")

    documents = build_documents(data)
    os.makedirs(INDEX_PATH, exist_ok=True)
    store = FAISS.from_documents(documents, embeddings)
    store.save_local(INDEX_PATH)
    print("✅ FAISS index saved")
    return store


def retrieve_with_threshold(
    store: FAISS,
    question: str,
    lang: str,
    k: int = TOP_K,
    threshold: float = SIMILARITY_THRESHOLD,
) -> List[Document]:
    """
    Smart retrieval:
    1. Maps user language to index language (darija → fr/ar)
    2. Detects question category (startup vs cnss) for better filtering
    3. Falls back to no-category search if filtered results are empty
    """
    search_lang = SEARCH_LANG_MAP.get(lang, "en")
    category    = detect_question_category(question)

    # Try category-filtered search first
    if category:
        cat_filter = {"lang": search_lang, "category": category}
        results = store.similarity_search_with_score(question, k=k, filter=cat_filter)
        passed  = [doc for doc, score in results if score < threshold]
        print(f"   [{lang}→{search_lang}] category={category}: {len(results)} found, {len(passed)} passed")

        # If category filter found good results, use them
        if passed:
            _print_scores(results, threshold)
            return passed

        print(f"   ⚠️  No results with category filter, trying without...")

    # Fallback: search by language only (no category filter)
    results = store.similarity_search_with_score(question, k=k, filter={"lang": search_lang})
    passed  = [doc for doc, score in results if score < threshold]
    print(f"   [{lang}→{search_lang}] no-category: {len(results)} found, {len(passed)} passed")
    _print_scores(results, threshold)

    return passed


def _print_scores(results, threshold):
    for doc, score in results:
        status = "✅" if score < threshold else "❌"
        print(f"     {status} {score:.1f} | {doc.metadata.get('title','')[:55]}")