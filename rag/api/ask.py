# api/ask.py
# =============================================================
# HOW TunBERT IS USED HERE:
#
# TunBERT (extractive QA) and gemma2 (generative QA) work differently:
#   - gemma2:   reads context → generates a fluent answer in Darija
#   - TunBERT:  reads context → extracts the EXACT span from the text
#
# TunBERT does NOT generate — it only copies words already in the document.
# This means zero hallucination but answers may be in French (the doc language).
#
# HOW TO KNOW IF TunBERT IS HELPING:
#   Send request with "compare_tunbert": true
#   Response includes both answers + TunBERT confidence score
#   If tunbert_score > 0.50 → TunBERT found a strong answer in the docs
#   If tunbert_score < 0.15 → TunBERT failed (question not in docs)
#
# WHEN TunBERT helps more than gemma2:
#   ✅ Exact factual questions: "قداش عندي وقت؟" → TunBERT extracts "60 jours"
#   ✅ When gemma2 hallucinates or returns fallback
#
# WHEN gemma2 helps more:
#   ✅ "كيفاش نعمل شركة خطوة بخطوة؟" → needs synthesis, not extraction
#   ✅ When answer requires combining info from multiple docs
#   ✅ When answer needs to be in Darija (TunBERT returns French text)
# =============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import traceback

from core.vector_store   import retrieve_with_threshold
from core.prompts        import get_prompt, format_context
from core.llm            import get_llm
from core.answer import clean_answer
from utils.language      import detect_language
from analytics.tracker   import log_query
from config.settings     import FALLBACK_MESSAGES

router = APIRouter()


class QueryRequest(BaseModel):
    question:        str
    lang:            str = "auto"
    evaluate:        bool = False
    reference:       Optional[str] = None
    run_bertscore:   bool = False
    compare_tunbert: bool = False   # set true to see TunBERT vs gemma2 side-by-side


def _run_ask(req: QueryRequest) -> dict:
    """Core QA pipeline used by both /ask and /ask/evaluate."""
    from main import vector_store

    # 1. Detect language
    if req.lang == "auto" or req.lang not in ["en", "fr", "darija", "ar"]:
        detected_lang = detect_language(req.question)
    else:
        detected_lang = req.lang

    # 2. Retrieve relevant documents from FAISS
    docs = retrieve_with_threshold(vector_store, req.question, detected_lang)
    categories = list(set(d.metadata.get("category", "") for d in docs))

    # 3. No docs found → return fallback immediately
    if not docs:
        log_query(req.question, detected_lang, 0, [], False)
        return {
            "question":          req.question,
            "detected_language": detected_lang,
            "answer":            FALLBACK_MESSAGES.get(detected_lang, FALLBACK_MESSAGES["en"]),
            "sources":           [],
            "grounded":          False,
            "docs":              [],
        }

    # 4. Build prompt and call gemma2
    context     = format_context(docs)
    prompt_text = get_prompt(detected_lang).format(context=context, question=req.question)
    raw_answer  = get_llm().invoke(prompt_text).content.strip()

    # 5. Validate language (reject Egyptian Arabic, heavy French leak, etc.)
    answer, is_valid = clean_answer(raw_answer, detected_lang, question=req.question)

    # 6. Hallucination guard
    hallucination_signals = [
        "as an ai", "i don't have access", "generally speaking",
        "based on my training", "en général", "عموما", "في الغالب",
    ]
    if any(s in answer.lower() for s in hallucination_signals):
        answer, is_valid = FALLBACK_MESSAGES.get(detected_lang, FALLBACK_MESSAGES["en"]), False

    grounded = is_valid and len(answer) >= 15
    log_query(req.question, detected_lang, len(docs), categories, grounded)

    sources = [
        {
            "title":    d.metadata.get("title", ""),
            "source":   d.metadata.get("source", ""),
            "category": d.metadata.get("category", ""),
            "lang":     d.metadata.get("lang", ""),
        }
        for d in docs
    ]

    return {
        "question":          req.question,
        "detected_language": detected_lang,
        "answer":            answer,
        "sources":           sources,
        "grounded":          grounded,
        "docs":              docs,
    }


def _run_tunbert(question: str, docs: list, lang: str) -> dict:
    """
    Run TunBERT extractive QA on the same docs.
    Returns answer + confidence score.

    HOW TO INTERPRET:
      score > 0.70 → TunBERT very confident, answer is in the docs
      score 0.30-0.70 → partial match, answer might be correct
      score < 0.15 → TunBERT found nothing reliable
    """
    try:
        from core.tunbert_qa import answer_with_tunbert
        result = answer_with_tunbert(question, docs, lang)
        return {
            "tunbert_answer":     result["answer"],
            "tunbert_score":      result["score"],
            "tunbert_grounded":   result["grounded"],
            "tunbert_source":     result.get("source", {}).get("title", "") if result.get("source") else "",
            "tunbert_note": (
                "🟢 High confidence — answer found in documents" if result["score"] > 0.50 else
                "🟡 Medium confidence" if result["score"] > 0.15 else
                "🔴 Low confidence — not found in documents"
            ),
        }
    except Exception as e:
        return {
            "tunbert_answer":   None,
            "tunbert_score":    0.0,
            "tunbert_grounded": False,
            "tunbert_error":    str(e),
            "tunbert_note":     "TunBERT unavailable — run: pip install transformers torch",
        }


def _evaluate(question, answer, docs, lang, grounded, reference=None):
    """Inline evaluation metrics — no external module needed."""
    import re

    context_text = " ".join(getattr(d, "page_content", "") for d in docs) if docs else ""

    def faithfulness(ans, ctx):
        if not ans or not ctx:
            return 0.0
        ctx_lower = ctx.lower()
        phrases = re.split(r'[.،؟!\n]+', ans)
        phrases = [p.strip() for p in phrases if len(p.strip()) > 5]
        if not phrases:
            return 0.0
        supported = sum(
            1 for p in phrases
            if sum(1 for w in p.split() if len(w) > 3 and w.lower() in ctx_lower)
               / max(len([w for w in p.split() if len(w) > 3]), 1) >= 0.40
        )
        return round(supported / len(phrases), 4)

    def lang_score(ans, expected):
        arabic  = len(re.findall(r'[\u0600-\u06FF]', ans))
        total   = max(len(ans.replace(" ", "")), 1)
        ar_r    = arabic / total
        fr_w    = re.findall(
            r'\b(le|la|les|de|du|des|un|une|pour|dans|avec|est|doit'
            r'|statuts|employeur|entreprise)\b', ans, re.IGNORECASE)
        fr_r    = len(fr_w) / max(len(ans.split()), 1)
        if expected in ["darija", "ar"]:
            correct = ar_r > 0.4 and fr_r < 0.25
            score   = max(0.0, ar_r - fr_r)
        elif expected == "fr":
            correct = ar_r < 0.2
            score   = 1.0 - ar_r
        else:
            correct = ar_r < 0.1
            score   = 1.0 - ar_r
        return {"score": round(min(1.0, max(0.0, score)), 4),
                "correct": correct, "arabic_ratio": round(ar_r, 4),
                "french_leak": round(fr_r, 4)}

    def rouge(hyp, ref):
        if not hyp or not ref:
            return {}
        try:
            from rouge_score import rouge_scorer
            sc = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
            s  = sc.score(ref, hyp)
            return {"rouge1_f": round(s["rouge1"].fmeasure, 4),
                    "rouge2_f": round(s["rouge2"].fmeasure, 4),
                    "rougeL_f": round(s["rougeL"].fmeasure, 4)}
        except ImportError:
            return {"note": "pip install rouge-score"}

    def bleu(hyp, ref):
        if not hyp or not ref:
            return {}
        try:
            import nltk
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
            try:
                nltk.data.find("tokenizers/punkt")
            except LookupError:
                nltk.download("punkt", quiet=True)
            sm = SmoothingFunction().method1
            r, h = ref.split(), hyp.split()
            return {
                "bleu1": round(sentence_bleu([r], h, (1,0,0,0), smoothing_function=sm), 4),
                "bleu2": round(sentence_bleu([r], h, (.5,.5,0,0), smoothing_function=sm), 4),
                "bleu4": round(sentence_bleu([r], h, (.25,.25,.25,.25), smoothing_function=sm), 4),
            }
        except ImportError:
            return {"note": "pip install nltk"}

    faith   = faithfulness(answer, context_text)
    lang_r  = lang_score(answer, lang)
    r_ctx   = rouge(answer, context_text)
    r_ref   = rouge(answer, reference) if reference else {}
    b_ref   = bleu(answer, reference)  if reference else {}

    is_fallback = any(f in answer for f in [
        "موش موجودة", "not available", "n'est pas disponible", "غير موجودة"
    ])

    overall = (
        faith           * 0.30 +
        lang_r["score"] * 0.25 +
        (1.0 if grounded else 0.0) * 0.20 +
        (0.0 if is_fallback else 1.0) * 0.15 +
        r_ctx.get("rouge1_f", 0) * 0.10
    )

    return {
        "overall_score":      round(overall, 4),
        "grade":              "🟢 Good" if overall >= 0.70 else ("🟡 Fair" if overall >= 0.45 else "🔴 Poor"),
        "is_fallback":        is_fallback,
        "faithfulness":       faith,
        "language_check":     lang_r,
        "rouge_vs_context":   r_ctx,
        "rouge_vs_reference": r_ref,
        "bleu_vs_reference":  b_ref,
        "word_count":         len(answer.split()),
    }


# ============================================================
# ROUTES
# ============================================================

@router.post("/ask")
def ask_question(req: QueryRequest):
    try:
        result = _run_ask(req)
        docs   = result.pop("docs", [])

        # Optional: compare TunBERT vs gemma2
        if req.compare_tunbert:
            result["tunbert_comparison"] = _run_tunbert(
                req.question, docs, result["detected_language"]
            )

        return result
    except Exception as e:
        print(f"ERROR /ask:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@router.post("/ask/evaluate")
def ask_and_evaluate(req: QueryRequest):
    try:
        result = _run_ask(req)
        docs   = result.pop("docs", [])

        ref = req.reference if req.reference and req.reference != "string" else None
        result["evaluation"] = _evaluate(
            question  = req.question,
            answer    = result["answer"],
            docs      = docs,
            lang      = result["detected_language"],
            grounded  = result["grounded"],
            reference = ref,
        )

        # Optional: compare TunBERT vs gemma2
        if req.compare_tunbert:
            result["tunbert_comparison"] = _run_tunbert(
                req.question, docs, result["detected_language"]
            )

        return result
    except Exception as e:
        print(f"ERROR /ask/evaluate:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")