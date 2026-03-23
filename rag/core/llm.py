# core/llm.py
from langchain_community.chat_models import ChatOllama
from config.settings import LLM_MODEL, FALLBACK_MESSAGES

_llm_instance = None


def get_llm() -> ChatOllama:
    """Return a single shared Ollama LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatOllama(
            model=LLM_MODEL,
            temperature=0,
            num_predict=800,    # ← increased from 500 to get complete answers
            repeat_penalty=1.1,
            num_ctx=2048,       # ← enough context to read all retrieved docs
        )
    return _llm_instance


def generate_answer(prompt_text: str, lang: str, docs: list) -> str:
    """Call LLM and apply hallucination guard."""
    llm = get_llm()
    response = llm.invoke(prompt_text)
    answer = response.content.strip()

    hallucination_signals = [
        "as an ai", "i don't have access", "i cannot provide",
        "generally speaking", "based on my training", "in general",
        "typically", "usually", "en général", "généralement",
        "عموما", "في الغالب",
    ]

    if len(answer) < 20 or any(s in answer.lower() for s in hallucination_signals):
        return FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["en"])

    return answer