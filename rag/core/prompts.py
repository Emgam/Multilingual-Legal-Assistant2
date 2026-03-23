# core/prompts.py
from langchain_core.prompts import PromptTemplate
from config.settings import FALLBACK_MESSAGES, STRICT_GROUNDING_INSTRUCTION

# ============================================================
# SYSTEM PROMPTS — language rule repeated before AND after context
# ============================================================

SYSTEM_PROMPTS = {
    "darija": """أنت مساعد إداري تونسي متخصص.
قواعد صارمة جداً:
- اكتب بالدارجة التونسية فقط — مش مصرية، مش فصحى، مش فرنسية
- الدارجة التونسية تستعمل: لازم، نجم، تمشي، تجيب، تعمر، باش، كيفاش، برشا، موش، وقتاش، قداش، شنية، عندي، بعد كاش، ماكش
- المصطلحات الرسمية تبقى كما هي: RNE، CNSS، SARL، SA، API
- ممنوع تكتب كلمة واحدة بالفرنسية أو العربية الفصحى أو المصرية""",

    "ar": """أنت مساعد إداري تونسي متخصص.
قواعد صارمة:
- اكتب باللغة العربية الفصحى فقط
- ممنوع استخدام الفرنسية أو الدارجة""",

    "fr": """Tu es un assistant administratif tunisien spécialisé.
Règles strictes:
- Écris UNIQUEMENT en français standard
- Interdit d'utiliser l'arabe ou l'anglais""",

    "en": """You are a specialized Tunisian administrative assistant.
Strict rules:
- Write ONLY in English
- No Arabic or French words allowed""",
}

# ============================================================
# FEW-SHOT EXAMPLES — show exact Tunisian Darija style expected
# ============================================================

FEW_SHOT = {
    "darija": """
=== أمثلة على الدارجة التونسية الصحيحة ===

مثال 1:
السياق: "Pour créer une entreprise: 1) Rédiger les statuts. 2) Ouvrir un compte bancaire. 3) S'immatriculer au RNE dans les 60 jours."
السؤال: كيفاش نعمل شركة؟
الجواب الصحيح بالدارجة: باش تعمل شركة، لازم:
1) تكتب عقد التأسيس
2) تفتح حساب بنكي باسم الشركة
3) تسجل في RNE في ظرف 60 يوم

مثال 2:
السياق: "L'enregistrement des statuts doit être effectué à la Recette des Finances dans les 60 jours."
السؤال: قداش عندي وقت باش نسجل العقد؟
الجواب الصحيح بالدارجة: حسب الوثائق، عندك 60 يوم باش تسجل العقد في قباضة المالية.

مثال 3:
السياق: "La déclaration à la CNSS est obligatoire pour tout employeur dès le premier recrutement."
السؤال: وقتاش لازم نصرح في الكناس؟
الجواب الصحيح بالدارجة: حسب الوثائق، لازم تصرح في الكناس من أول ما تعمل الشركة وقبل ما تخدم أي واحد.

مثال 4:
السياق: "Documents requis: CIN, certificat de réservation, statuts signés, contrat de location."
السؤال: شنية الوثائق المطلوبة؟
الجواب الصحيح بالدارجة: لازم تجيب: بطاقة التعريف، شهادة حجز الاسم، العقد التأسيسي موقع، وعقد الكراء.

=== نهاية الأمثلة ===
""",

    "ar": """
=== أمثلة ===
السياق: "Pour créer une entreprise: rédiger les statuts, ouvrir un compte, s'immatriculer au RNE."
السؤال: كيف أنشئ شركة في تونس؟
الجواب: وفقاً للوثائق، لإنشاء شركة يجب: 1) إعداد عقد التأسيس. 2) فتح حساب مصرفي. 3) التسجيل في RNE.
=== نهاية ===
""",

    "fr": """
=== Exemples ===
Contexte: "Pour créer une entreprise: rédiger les statuts, ouvrir un compte bancaire, s'immatriculer au RNE."
Question: Comment créer une entreprise?
Réponse: Selon les documents, pour créer une entreprise: 1) Rédiger les statuts. 2) Ouvrir un compte bancaire. 3) S'immatriculer au RNE.
=== Fin ===
""",

    "en": """
=== Examples ===
Context: "To create a company: draft statutes, open a bank account, register at the RNE."
Question: How to create a company?
Answer: According to the documents: 1) Draft the statutes. 2) Open a bank account. 3) Register at the RNE.
=== End ===
""",
}

# Reminder placed AFTER context so model follows it at generation time
LANG_REMINDER = {
    "darija": "\nتذكير مهم: اكتب جوابك بالدارجة التونسية فقط — مش مصرية، مش فرنسية، مش فصحى.\n",
    "ar":     "\nتذكير: اكتب باللغة العربية الفصحى فقط.\n",
    "fr":     "\nRappel: écris UNIQUEMENT en français.\n",
    "en":     "\nReminder: write ONLY in English.\n",
}


def get_prompt(lang: str) -> PromptTemplate:
    if lang not in SYSTEM_PROMPTS:
        lang = "en"

    fallback  = FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["en"])
    system    = SYSTEM_PROMPTS[lang]
    examples  = FEW_SHOT[lang]
    reminder  = LANG_REMINDER[lang]

    if lang == "darija":
        q_label = "السؤال بالدارجة"
        a_label = "الجواب بالدارجة التونسية فقط"
        fallback_instruction = f'إذا الجواب موش موجود في السياق، قل فقط: "{fallback}"'
    elif lang == "ar":
        q_label = "السؤال"
        a_label = "الجواب بالعربية الفصحى"
        fallback_instruction = f'إذا لم تجد الإجابة في السياق، قل فقط: "{fallback}"'
    elif lang == "fr":
        q_label = "Question"
        a_label = "Réponse en français uniquement"
        fallback_instruction = f'Si la réponse n\'est pas dans le contexte, dis exactement: "{fallback}"'
    else:
        q_label = "Question"
        a_label = "Answer in English only"
        fallback_instruction = f'If the answer is not in the context, say exactly: "{fallback}"'

    template = f"""{system}

{STRICT_GROUNDING_INSTRUCTION}

{fallback_instruction}

{examples}

=== الوثائق الرسمية / Documents officiels ===
{{context}}
=== نهاية الوثائق ===
{reminder}
{q_label}: {{question}}

{a_label}:"""

    return PromptTemplate(input_variables=["context", "question"], template=template)


def format_context(docs) -> str:
    """Format docs — include section content for richer context."""
    sections = []
    for i, doc in enumerate(docs, 1):
        meta   = doc.metadata
        header = f"[{i}] {meta.get('title', 'N/A')} | {meta.get('category', 'N/A')}"
        sections.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)