# =============================
# analytics/tracker.py
# =============================
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# In-memory query log — replace with SQLite/PostgreSQL for production
# ---------------------------------------------------------------------------
_query_log: List[Dict[str, Any]] = []
_procedure_hit_counter: Dict[str, int] = defaultdict(int)
_keyword_counter: Dict[str, int] = defaultdict(int)


def log_query(
    question: str,
    lang: str,
    docs_found: int,
    categories: List[str],
    answered: bool,
):
    """Log every incoming query for BI analytics."""
    _query_log.append({
        "timestamp":  datetime.utcnow().isoformat(),
        "question":   question,
        "lang":       lang,
        "docs_found": docs_found,
        "categories": categories,
        "answered":   answered,
    })

    # Count procedure category hits
    for cat in categories:
        if cat:
            _procedure_hit_counter[cat] += 1

    # Simple keyword extraction (split on spaces, filter short words)
    for word in question.lower().split():
        if len(word) > 3:
            _keyword_counter[word] += 1


def get_overview() -> Dict[str, Any]:
    total = len(_query_log)
    answered = sum(1 for q in _query_log if q["answered"])
    lang_counts = defaultdict(int)
    for q in _query_log:
        lang_counts[q["lang"]] += 1

    return {
        "total_queries":    total,
        "answered_queries": answered,
        "unanswered_queries": total - answered,
        "answer_rate":      round(answered / total * 100, 1) if total else 0,
        "by_language":      dict(lang_counts),
    }


def get_procedure_stats() -> Dict[str, Any]:
    return {
        "procedure_hits": dict(
            sorted(_procedure_hit_counter.items(), key=lambda x: x[1], reverse=True)
        )
    }


def get_language_stats() -> Dict[str, Any]:
    lang_counts = defaultdict(int)
    for q in _query_log:
        lang_counts[q["lang"]] += 1
    return {"language_distribution": dict(lang_counts)}


def get_keyword_stats(top_n: int = 20) -> Dict[str, Any]:
    top = sorted(_keyword_counter.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return {"top_keywords": dict(top)}


def get_recent_queries(limit: int = 20) -> List[Dict]:
    return _query_log[-limit:][::-1]