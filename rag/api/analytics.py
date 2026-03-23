# =============================
# api/analytics.py
# =============================
from fastapi import APIRouter, Query
from analytics.tracker import (
    get_overview,
    get_procedure_stats,
    get_language_stats,
    get_keyword_stats,
    get_recent_queries,
)

router = APIRouter(prefix="/analytics", tags=["Analytics / BI"])


@router.get("/overview")
def analytics_overview():
    """High-level BI summary: total queries, answer rate, language breakdown."""
    return get_overview()


@router.get("/procedures")
def analytics_procedures():
    """Most requested procedure categories."""
    return get_procedure_stats()


@router.get("/languages")
def analytics_languages():
    """Distribution of queries per language (EN / FR / Darija)."""
    return get_language_stats()


@router.get("/keywords")
def analytics_keywords(top: int = Query(default=20, ge=1, le=100)):
    """Top N most frequent keywords across all queries."""
    return get_keyword_stats(top_n=top)


@router.get("/queries")
def analytics_recent_queries(limit: int = Query(default=20, ge=1, le=100)):
    """Recent query log (for admin/debugging use)."""
    return {"recent_queries": get_recent_queries(limit=limit)}