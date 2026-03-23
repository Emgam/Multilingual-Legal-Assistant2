# =============================
# main.py  —  Entry point
# =============================
from fastapi import FastAPI
from langchain_community.embeddings import OllamaEmbeddings

from config.settings import EMBED_MODEL
from core.vector_store import load_vector_store

from api.ask        import router as ask_router
from api.procedures import router as procedures_router
from api.analytics  import router as analytics_router
from api.voice      import router as voice_router

# =============================
# STARTUP: load embeddings + vector store once
# =============================
print("🔄 Initializing embeddings model...")
embeddings = OllamaEmbeddings(model=EMBED_MODEL)

print("🔄 Loading vector store...")
vector_store = load_vector_store(embeddings)
print("✅ System ready.\n")

# =============================
# APP
# =============================
app = FastAPI(
    title="Multilingual Tunisian RAG API",
    description=(
        "AI-powered backend for Tunisian startup creation and CNSS procedures. "
        "Supports English, French, and Tunisian Arabic dialect (Darija)."
    ),
    version="2.0.0",
)

# Register routers
app.include_router(ask_router,        tags=["QA"])
app.include_router(procedures_router)
app.include_router(analytics_router)
app.include_router(voice_router)

@app.get("/debug/search")
def debug_search(q: str, lang: str = "darija"):
    from config.settings import SIMILARITY_THRESHOLD, SEARCH_LANG_MAP
    
    # Apply the same lang mapping as real /ask endpoint
    search_lang = SEARCH_LANG_MAP.get(lang, "en")
    
    results_mapped = vector_store.similarity_search_with_score(q, k=10, filter={"lang": search_lang})
    results_all = vector_store.similarity_search_with_score(q, k=10)

    return {
        "query": q,
        "user_lang": lang,
        "searching_lang": search_lang,   # shows darija→fr mapping
        "current_threshold": SIMILARITY_THRESHOLD,
        "with_mapped_lang_filter": [
            {
                "score": float(score),
                "passes_threshold": float(score) < SIMILARITY_THRESHOLD,
                "title": doc.metadata.get("title", ""),
                "lang":  doc.metadata.get("lang", ""),
                "content_preview": doc.page_content[:120]
            }
            for doc, score in results_mapped
        ],
        "without_filter_top5": [
            {
                "score": float(score),
                "lang":  doc.metadata.get("lang", ""),
                "title": doc.metadata.get("title", ""),
            }
            for doc, score in results_all[:5]
        ],
        "index_total_docs": int(vector_store.index.ntotal),
    }


@app.get("/debug/index-stats")
def debug_index_stats():
    sample = vector_store.similarity_search("startup CNSS", k=50)
    lang_counts: dict = {}
    cat_counts: dict = {}
    titles = []
    for doc in sample:
        l = doc.metadata.get("lang", "unknown")
        c = doc.metadata.get("category", "unknown")
        lang_counts[l] = lang_counts.get(l, 0) + 1
        cat_counts[c] = cat_counts.get(c, 0) + 1
        titles.append(doc.metadata.get("title", "")[:60])

    return {
        "total_vectors_in_index":        int(vector_store.index.ntotal),
        "sampled":                        len(sample),
        "lang_distribution_in_sample":   lang_counts,
        "category_distribution_in_sample": cat_counts,
        "sample_titles":                  titles[:10],
    }


@app.get("/", tags=["Health"])
def root():
    return {
        "status":  "RAG API running",
        "version": "2.0.0",
        "endpoints": {
            "ask_text":             "POST /ask",
            "ask_voice":            "POST /ask/voice",
            "startup_procedures":   "GET  /procedures/startup",
            "cnss_procedures":      "GET  /procedures/cnss",
            "all_procedures":       "GET  /procedures/all",
            "analytics_overview":   "GET  /analytics/overview",
            "analytics_procedures": "GET  /analytics/procedures",
            "analytics_languages":  "GET  /analytics/languages",
            "analytics_keywords":   "GET  /analytics/keywords",
            "analytics_queries":    "GET  /analytics/queries",
            "docs":                 "GET  /docs",
        },
    }

@app.get("/debug/json-keys")
def debug_json_keys():
    import json
    path = r"C:\Users\pc\Documents\dataset\datasets\rag_dataset.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    first = data[0] if data else {}
    simplified = first.get("simplified_text") or {}
    
    return {
        "total_entries": len(data),
        "first_entry_keys": list(first.keys()),
        "simplified_text_keys": list(simplified.keys()),   # ← THIS is what we need
        "sample_simplified": {k: str(v)[:80] for k, v in simplified.items()}
    }