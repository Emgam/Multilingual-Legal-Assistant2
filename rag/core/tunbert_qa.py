# =============================================================
# core/tunbert_qa.py
# Extractive QA using CAMeL-Lab Arabic BERT (TunBERT-compatible)
# Finds exact answer spans from your documents — zero hallucination
# =============================================================

from transformers import pipeline
from config.settings import FALLBACK_MESSAGES

# ✅ FIXED: points to a MODEL FOLDER, not a .py file
# Before fine-tuning → uses base Arabic dialect BERT from HuggingFace
# After fine-tuning  → change this to your trained model folder
FINETUNED_MODEL_PATH = r"C:\Users\pc\Documents\dataset\models\tunbert-qa-finetuned"
BASE_MODEL           = "CAMeL-Lab/bert-base-arabic-camelbert-da"

# Minimum confidence to trust TunBERT's answer
# Below this → return fallback message
MIN_CONFIDENCE = 0.15

_qa_pipeline = None


def get_qa_pipeline():
    """Load the QA pipeline once at startup and reuse."""
    global _qa_pipeline
    if _qa_pipeline is None:
        import os
        import torch

        # Use fine-tuned model if it exists, otherwise use base model
        if os.path.isdir(FINETUNED_MODEL_PATH):
            model_path = FINETUNED_MODEL_PATH
            print(f"🔄 Loading fine-tuned TunBERT from: {model_path}")
        else:
            model_path = BASE_MODEL
            print(f"🔄 Loading base Arabic BERT from HuggingFace: {model_path}")
            print(f"   (Fine-tune first for better Darija results)")

        _qa_pipeline = pipeline(
            "question-answering",
            model=model_path,
            tokenizer=model_path,
            device=0 if torch.cuda.is_available() else -1,  # GPU if available, else CPU
        )
        print("✅ QA pipeline ready")
    return _qa_pipeline


def answer_with_tunbert(question: str, docs: list, lang: str) -> dict:
    """
    Extractive QA: finds the exact answer span inside retrieved documents.
    The answer MUST exist in the documents — no generation, no hallucination.

    Args:
        question: user's question (any language)
        docs:     list of LangChain Document objects from FAISS retrieval
        lang:     detected language for fallback message selection

    Returns:
        dict with answer, confidence score, source metadata, grounded flag
    """
    fallback = FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["en"])

    if not docs:
        return {
            "answer":   fallback,
            "score":    0.0,
            "source":   None,
            "grounded": False,
        }

    qa          = get_qa_pipeline()
    best_result = None
    best_score  = 0.0
    best_doc    = None

    for doc in docs:
        context = (doc.page_content or "").strip()
        if not context:
            continue

        try:
            result = qa(
                question=question,
                context=context,
                max_answer_len=250,
                handle_impossible_answer=True,  # returns empty string if no answer found
            )

            score  = result.get("score", 0.0)
            answer = result.get("answer", "").strip()

            if answer and score > best_score:
                best_score  = score
                best_result = answer
                best_doc    = doc

        except Exception as e:
            print(f"   ⚠️  TunBERT error on doc '{doc.metadata.get('title','')}': {e}")
            continue

    # Confidence check
    if not best_result or best_score < MIN_CONFIDENCE:
        print(f"   ⚠️  TunBERT confidence too low ({best_score:.4f}) — returning fallback")
        return {
            "answer":   fallback,
            "score":    float(best_score),
            "source":   None,
            "grounded": False,
        }

    print(f"   ✅ TunBERT answer (confidence={best_score:.4f}): {best_result[:80]}")
    return {
        "answer":   best_result,
        "score":    float(best_score),
        "source":   best_doc.metadata if best_doc else None,
        "grounded": True,
    }