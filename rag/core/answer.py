# core/answer_cleaner.py
# =============================================================
# PURPOSE: Validate that the LLM answer is in the correct language.
# Called AFTER the LLM responds, BEFORE returning to the user.
#
# Main scenarios it handles:
#   1. LLM answered in Egyptian Arabic instead of Tunisian Darija
#   2. LLM mixed French into a Darija answer
#   3. LLM answered in Arabic when French was expected
#   4. Question itself has French words → be more lenient
# =============================================================

import re
from config.settings import FALLBACK_MESSAGES

# French words that commonly leak into Darija answers
FRENCH_LEAK_PATTERN = re.compile(
    r'\b(le|la|les|de|du|des|un|une|pour|dans|avec|sur|est|sont|vous|nous'
    r'|doit|peut|faut|selon|après|avant|lors|statuts|licenciement|préavis'
    r'|employeur|salarié|entreprise|immatriculation|déclaration|formulaire)\b',
    re.IGNORECASE
)

# Egyptian Arabic words — reject if found in a "Darija" answer
EGYPTIAN_WORDS = [
    "هقوللك", "بتاع", "عايز", "إزيك", "ازيك",
    "دلوقتي", "بقى", "كمان", "أهو", "طب", "شبهة",
]

# Tunisian Darija marker words — a valid answer should have at least one
TUNISIAN_MARKERS = [
    "لازم", "باش", "موش", "كيفاش", "وقتاش", "قداش",
    "شنية", "برشا", "نجم", "تمشي", "هاذا", "هاذي",
    "عندك", "تجيب", "تعمل", "ماكش", "بعد كاش",
]


def question_has_french(question: str) -> bool:
    return bool(FRENCH_LEAK_PATTERN.search(question))


def has_french_leak(text: str, threshold: float = 0.20) -> bool:
    words = text.split()
    if not words:
        return False
    french_count = len(FRENCH_LEAK_PATTERN.findall(text))
    ratio = french_count / len(words)
    if ratio > threshold:
        print(f"   ⚠️  French leak: {french_count}/{len(words)} words ({ratio:.1%})")
        return True
    return False


def has_arabic_script(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))


def is_egyptian_arabic(text: str) -> bool:
    return any(word in text for word in EGYPTIAN_WORDS)


def has_tunisian_markers(text: str) -> bool:
    return any(marker in text for marker in TUNISIAN_MARKERS)


def clean_answer(answer: str, lang: str, question: str = "") -> tuple[str, bool]:
    """
    Validate answer language. Returns (answer, is_valid).
    If invalid → returns (fallback_message, False).
    """
    fallback = FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["en"])

    if not answer or len(answer.strip()) < 10:
        return fallback, False

    if lang == "darija":
        if not has_arabic_script(answer):
            print("   ⚠️  No Arabic script → rejected")
            return fallback, False
        if is_egyptian_arabic(answer):
            print("   ⚠️  Egyptian Arabic detected → rejected")
            return fallback, False
        if len(answer.split()) > 8 and not has_tunisian_markers(answer):
            print("   ⚠️  No Tunisian markers → rejected")
            return fallback, False
        q_has_french     = question_has_french(question)
        french_threshold = 0.40 if q_has_french else 0.20
        if has_french_leak(answer, threshold=french_threshold):
            print("   ⚠️  Too much French → rejected")
            return fallback, False

    elif lang == "ar":
        if not has_arabic_script(answer):
            return fallback, False

    elif lang == "fr":
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', answer))
        total_chars  = max(len(answer.replace(" ", "")), 1)
        if arabic_chars / total_chars > 0.30:
            return fallback, False

    elif lang == "en":
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', answer))
        total_chars  = max(len(answer.replace(" ", "")), 1)
        if arabic_chars / total_chars > 0.15:
            return fallback, False

    return answer.strip(), True