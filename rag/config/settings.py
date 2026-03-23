# config/settings.py
DATASET_PATH = r"C:\Users\pc\Documents\dataset\datasets\rag_dataset.json"
INDEX_PATH   = r"C:\Users\pc\Documents\dataset\datasets\rag_faiss_index"

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL   = "llama3.2"

# Dataset has "fr" and "en" (ar is null in most entries)
SUPPORTED_LANGS = ["fr", "en", "ar"]

# Darija → search BOTH fr and en, pick best
SEARCH_LANG_MAP = {
    "darija": "fr",
    "ar":     "fr",
    "fr":     "fr",
    "en":     "en",
}

TOP_K = 6                  # increased from 5 — more context for Darija
SIMILARITY_THRESHOLD = 500  # scores are 300-460

FALLBACK_MESSAGES = {
    "darija": "المعلومة هاذي موش موجودة في الوثائق المتوفرة.",
    "ar":     "هذه المعلومة غير موجودة في الوثائق المتاحة.",
    "fr":     "Cette information n'est pas disponible dans les documents fournis.",
    "en":     "This information is not available in the provided documents."
}

STRICT_GROUNDING_INSTRUCTION = """قواعد أساسية / Règles fondamentales:
1. أجب فقط بناءً على المعلومات الموجودة في الوثائق أدناه / Réponds UNIQUEMENT avec les infos du contexte
2. لا تخترع معلومات / N'invente aucune information
3. لا تستخدم معرفتك العامة / N'utilise pas tes connaissances générales"""