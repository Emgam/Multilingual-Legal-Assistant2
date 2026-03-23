# =============================
# api/procedures.py
# =============================
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/procedures", tags=["Procedures"])


def _search_procedures(store, category: str, lang: str, query: str):
    """Helper: search vector store filtered by category and language."""
    results = store.similarity_search(
        query,
        k=10,
        filter={"category": category, "lang": lang}
    )
    return [
        {
            "title":       d.metadata.get("title", ""),
            "source":      d.metadata.get("source", ""),
            "domain":      d.metadata.get("domain", ""),
            "content":     d.page_content,
        }
        for d in results
    ]


@router.get("/startup")
def get_startup_procedures(
    lang: str = Query(default="en", description="Language: en / fr / darija")
):
    """Return all startup creation procedures in the requested language."""
    from main import vector_store
    procedures = _search_procedures(
        store=vector_store,
        category="Startup",
        lang=lang,
        query="startup creation registration steps legal"
    )
    return {
        "category": "Startup",
        "lang":     lang,
        "count":    len(procedures),
        "procedures": procedures,
    }


@router.get("/cnss")
def get_cnss_procedures(
    lang:     str = Query(default="en", description="Language: en / fr / darija"),
    sub_type: Optional[str] = Query(default=None, description="employer / employee / all")
):
    """Return CNSS registration and declaration procedures."""
    from main import vector_store

    # Decide query and category based on sub_type
    if sub_type == "employer":
        query    = "CNSS employer registration declaration cotisation"
        category = "CNSS Employer"
    elif sub_type == "employee":
        query    = "CNSS employee declaration social security"
        category = "CNSS Employee"
    else:
        # Return both — search broadly
        employer_docs = _search_procedures(vector_store, "CNSS Employer", lang, "CNSS employer")
        employee_docs = _search_procedures(vector_store, "CNSS Employee", lang, "CNSS employee")
        return {
            "category": "CNSS",
            "lang":     lang,
            "employer_procedures": employer_docs,
            "employee_procedures": employee_docs,
        }

    procedures = _search_procedures(
        store=vector_store,
        category=category,
        lang=lang,
        query=query,
    )
    return {
        "category": category,
        "lang":     lang,
        "count":    len(procedures),
        "procedures": procedures,
    }


@router.get("/all")
def get_all_procedures(
    lang: str = Query(default="en", description="Language: en / fr / darija")
):
    """Return all available procedures grouped by category."""
    from main import vector_store
    startup = _search_procedures(vector_store, "Startup",       lang, "startup")
    employer = _search_procedures(vector_store, "CNSS Employer", lang, "CNSS employer")
    employee = _search_procedures(vector_store, "CNSS Employee", lang, "CNSS employee")
    return {
        "lang": lang,
        "startup":         startup,
        "cnss_employer":   employer,
        "cnss_employee":   employee,
    }