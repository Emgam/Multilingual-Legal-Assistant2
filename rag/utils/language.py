# =============================
# utils/language.py
# =============================
import re
from config.settings import SUPPORTED_LANGS, FALLBACK_MESSAGES
from config.settings import SEARCH_LANG_MAP


# Comprehensive Tunisian Darija word list
DARIJA_WORDS = [
    "علاش", "كيفاش", "نجم", "باش", "وين", "فاما", "يزي", "برشا",
    "نحب", "تعمل", "نعمل", "شنية", "احنا", "هوما", "هي", "هو",
    "نمشي", "تمشي", "يمشي", "وقتاش", "قداش", "بالله", "يسر",
    "تخدم", "نخدم", "يخدم", "لازم", "ما نجمش", "ما فماش",
    "عندي", "عندك", "عنده", "موش", "ماكش", "فيش", "عليش",
    "نبدا", "تبدا", "يبدا", "صاحبي", "خويا", "ختي",
]

FRENCH_WORDS = [
    "comment", "pourquoi", "entreprise", "créer", "création",
    "inscription", "quelle", "quels", "obtenir", "déclarer",
    "enregistrer", "procédure", "startup", "déclaration",
    "employeur", "salarié", "cotisation", "registre", "formulaire",
    "quoi", "peut", "dois", "faut", "besoin",
]



def detect_language(text: str) -> str:
    if re.search(r'[\u0600-\u06FF]', text):
        return "darija"   # will be remapped via LANG_KEY_MAP before FAISS query
    text_lower = text.lower()
    if any(w in text_lower for w in FRENCH_WORDS):
        return "fr"
    return "en"

def get_fallback(lang: str) -> str:
    return FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["en"])


def safe_lang(lang: str) -> str:
    """Return lang if supported, else default to 'en'."""
    return lang if lang in SUPPORTED_LANGS else "en"