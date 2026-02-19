"""
LLM factory — returns a LangChain chat model based on config.
"""

from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(config: dict):
    """
    Create and return a LangChain chat model based on the user's config.

    Supports:
      - groq   → ChatGroq  (requires groq_api_key)
      - gemini → ChatGoogleGenerativeAI (requires gemini_api_key)
      - ollama → ChatOllama (requires local Ollama server running)
    """
    provider = config.get("llm_provider", "").lower()
    model = config.get("llm_model", "")

    if provider == "groq":
        api_key = config.get("groq_api_key", "")
        if not api_key:
            raise ValueError(
                "Groq API key is not configured. Run 'gitbot onboard' first."
            )
        return ChatGroq(
            model=model,
            api_key=api_key,
            temperature=0,
        )

    elif provider == "gemini":
        api_key = config.get("gemini_api_key", "")
        if not api_key:
            raise ValueError(
                "Gemini API key is not configured. Run 'gitbot onboard' first."
            )
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0,
        )

    elif provider == "ollama":
        base_url = config.get("ollama_base_url", "http://localhost:11434")
        return ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0,
        )

    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider}'. Run 'gitbot onboard' first."
        )
