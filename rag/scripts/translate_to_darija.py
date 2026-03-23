# scripts/translate_to_darija.py
# LOCATION: C:\Users\pc\Documents\dataset\rag\scripts\translate_to_darija.py
# Run from rag/ folder: python scripts/translate_to_darija.py

import json, time, re, os
from langchain_community.chat_models import ChatOllama

INPUT_PATH  = r"C:\Users\pc\Documents\dataset\datasets\rag_dataset.json"
OUTPUT_PATH = r"C:\Users\pc\Documents\dataset\datasets\rag_dataset_darija.json"
MODEL       = "llama3.2"

llm = ChatOllama(model=MODEL, temperature=0.1, num_predict=300, num_ctx=768)

DARIJA_MARKERS = [
    "لازم", "نجم", "باش", "كيفاش", "برشا", "موش", "وقتاش",
    "قداش", "شنية", "هاذا", "هاذي", "عندك", "تجيب", "تمشي",
]
EGYPTIAN_WORDS = ["هقوللك", "بتاع", "عايز", "دلوقتي", "بقى", "شبهة", "هنا", "كمان"]

# Preambles gemma2 likes to add — strip them before validation
PREAMBLE_PATTERNS = [
    r"^(للمرة الأولى،?\s*)?سأقوم بترجمة[^:]*:\s*",
    r"^النص[^:]*:\s*",
    r"^الدارجة[^:]*:\s*",
    r"^ترجمة[^:]*:\s*",
    r"^الجواب[^:]*:\s*",
    r"^أنا متعلم[^.]*\.\s*",
    r"^إليك الترجمة[^:]*:\s*",
    r"^هذا هو[^:]*:\s*",
    r"^قواعد صارمة.*?الدارجة:\s*",  # strips leaked system prompt
]

# Minimum useful text length — skip "bureau 1", "مكتب 1" etc.
MIN_SOURCE_LENGTH = 30


def strip_preamble(text: str) -> str:
    """Remove common LLM preambles that appear before the actual translation."""
    for pattern in PREAMBLE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.DOTALL).strip()
    # Also strip if model repeated the source language tag
    text = re.sub(r"^\[src:[^\]]+\]\s*", "", text).strip()
    return text


def is_valid_darija(text: str) -> tuple[bool, str]:
    if not text or len(text.strip()) < 10:
        return False, "too short"
    if not re.search(r"[\u0600-\u06FF]", text):
        return False, "no Arabic script"
    for w in EGYPTIAN_WORDS:
        if w in text:
            return False, f"Egyptian Arabic: {w}"
    fr_words = re.findall(
        r"\b(le|la|les|de|du|des|un|une|pour|dans|avec|est|sont|doit)\b",
        text, re.IGNORECASE
    )
    if len(fr_words) > 3:
        return False, f"French leakage: {fr_words[:3]}"
    if not any(m in text for m in DARIJA_MARKERS):
        return False, "no Tunisian markers"
    return True, "ok"


# ============================================================
# KEY FIX: Prompt now uses imperative + shows output format explicitly
# "أكتب فقط الترجمة" = "write ONLY the translation"
# This prevents the "للمرة الأولى، سأقوم..." preamble
# ============================================================
FEW_SHOT = """مثال 1:
النص: "Pour créer une entreprise, vous devez rédiger les statuts et ouvrir un compte bancaire."
الترجمة: باش تعمل شركة، لازم تكتب عقد التأسيس وتفتح حساب بنكي.

مثال 2:
النص: "L'enregistrement doit être effectué dans les 60 jours à la Recette des Finances."
الترجمة: لازم تسجل في قباضة المالية في ظرف 60 يوم.

مثال 3:
النص: "Fournir les documents suivants: CIN, statuts signés, contrat de location."
الترجمة: لازم تجيب: بطاقة التعريف، العقد التأسيسي موقع، وعقد الكراء.

مثال 4:
النص: "La déclaration à la CNSS est obligatoire pour tout employeur."
الترجمة: التصريح في الكناس إجباري لكل صاحب عمل."""


def build_prompt(text: str, attempt: int) -> str:
    if attempt == 1:
        return f"""ترجم للدارجة التونسية. أكتب فقط الترجمة بدون أي مقدمة أو شرح.

{FEW_SHOT}

النص: {text}
الترجمة:"""
    elif attempt == 2:
        # Simpler, more direct
        return f"""دارجة تونسية فقط. بدون مقدمة.

"{text}"

الترجمة بالدارجة:"""
    else:
        # Last resort: force-start the answer
        return f"""اكمل هاذي الجملة بالدارجة التونسية:
"{text[:200]}"
→ بالدارجة: لازم"""


def translate(text: str, attempt: int = 1) -> str | None:
    prompt = build_prompt(text, attempt)
    try:
        raw    = llm.invoke(prompt).content.strip()
        result = strip_preamble(raw)

        # Attempt 3 special case: we force-started with "لازم", prepend it back
        if attempt == 3 and not result.startswith("لازم"):
            result = "لازم " + result

        valid, reason = is_valid_darija(result)
        print(f"      [{attempt}] {'✅' if valid else f'⚠️ ({reason})'} → {result[:60]}")
        return result if valid else None
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return None


def translate_with_retry(text: str) -> str:
    for attempt in range(1, 4):
        result = translate(text, attempt)
        if result:
            return result
        time.sleep(0.5)
    # All failed — store original so RAG still has something
    print("      ⚠️  All attempts failed — keeping source text")
    return f"[src] {text[:300]}"


# ============================================================
# SECTION TRANSLATION — skip very short texts (bureau labels etc.)
# ============================================================

def translate_sections(sections: list) -> list:
    for sec in sections:
        content = sec.get("content") or {}
        if not content.get("darija") or str(content["darija"]).startswith("[src]"):
            src  = content.get("fr") or content.get("en") or content.get("ar") or ""
            lang = "fr" if content.get("fr") else ("en" if content.get("en") else "ar")
            if len(src.strip()) < MIN_SOURCE_LENGTH:
                # Too short to translate meaningfully — just copy as-is
                content["darija"] = src
                print(f"      ⏭️  Section too short ({len(src)} chars) — copied as-is")
            else:
                print(f"      📝 Section: {src[:40]}...")
                content["darija"] = translate_with_retry(src)

        # Section title
        title = sec.get("title") or {}
        if not title.get("darija"):
            src = title.get("fr") or title.get("en") or title.get("ar") or ""
            if len(src.strip()) >= MIN_SOURCE_LENGTH:
                title["darija"] = translate_with_retry(src)
            else:
                title["darija"] = src
    return sections


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("Darija Translation — gemma2 (improved prompt)")
    print("=" * 60)

    source = OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else INPUT_PATH
    print(f"{'▶️  Resuming' if os.path.exists(OUTPUT_PATH) else '📂 Loading'}: {source}")
    with open(source, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"   {len(data)} entries\n")

    translated = skipped = failed = sections_done = 0

    for i, doc in enumerate(data):
        simplified = doc.get("simplified_text") or {}
        title_str  = str((doc.get("title") or {}).get("fr") or "")[:50]

        # ── simplified_text ──────────────────────────────────
        existing = simplified.get("darija", "")
        if existing and not str(existing).startswith("[src"):
            print(f"[{i+1}/{len(data)}] ⏭️  {title_str}")
            skipped += 1
        else:
            print(f"\n[{i+1}/{len(data)}] 🔄 {title_str}")
            src = simplified.get("fr") or simplified.get("en") or simplified.get("ar") or ""

            if len(src.strip()) < MIN_SOURCE_LENGTH:
                print(f"      ⚠️  Source too short ({len(src)} chars) — skipping")
                failed += 1
            elif src:
                result = translate_with_retry(src)
                simplified["darija"] = result
                if result.startswith("[src"):
                    failed += 1
                else:
                    translated += 1
            else:
                print("      ⚠️  No source text")
                failed += 1

        # ── sections ─────────────────────────────────────────
        if doc.get("sections"):
            untranslated = [
                s for s in doc["sections"]
                if not (s.get("content") or {}).get("darija")
                or str((s.get("content") or {}).get("darija", "")).startswith("[src")
            ]
            if untranslated:
                print(f"      📂 {len(untranslated)} sections to translate...")
                doc["sections"] = translate_sections(doc["sections"])
                sections_done  += len(untranslated)

        # Save after every entry — resume-safe
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ Done!")
    print(f"   Translated:      {translated}")
    print(f"   Skipped/existed: {skipped}")
    print(f"   Failed:          {failed}")
    print(f"   Sections done:   {sections_done}")
    print(f"   Output: {OUTPUT_PATH}")
    print("""
Next steps after translation completes:
  1. config/settings.py → set:
       DATASET_PATH    = r"...\\rag_dataset_darija.json"
       SUPPORTED_LANGS = ["fr", "en", "darija"]
       SEARCH_LANG_MAP = {"darija": "darija", "fr": "fr", "en": "en"}
  2. Delete rag_faiss_index folder
  3. uvicorn main:app --reload --port 8000
""")


if __name__ == "__main__":
    main()