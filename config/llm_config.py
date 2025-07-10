# llm_config.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# ─── PROVIDER MAPPINGS ─────────────────────────────────────
PROVIDERS = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("OPENAI_BASE_URL"),
    },
    "anthropic": {
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "base_url": os.getenv("ANTHROPIC_BASE_URL"),
    },
    "venice": {
        "api_key": os.getenv("VENICE_API_KEY"),
        "base_url": os.getenv("VENICE_BASE_URL"),
    },
}

# ─── TASK-TO-MODEL MAP ─────────────────────────────────────
LLM_CONFIG = {
    "intent_extractor": {"provider": "openai", "model": os.getenv("LLM_MODEL_INTENT_EXTRACTOR", "gpt-3.5-turbo")},
    "planner":          {"provider": "openai", "model": os.getenv("LLM_MODEL_PLANNER", "gpt-3.5-turbo")},
    "designer":         {"provider": "openai", "model": os.getenv("LLM_MODEL_DESIGNER", "gpt-4o")},
    "builder":          {"provider": "openai", "model": os.getenv("LLM_MODEL_BUILDER", "gpt-4o")},
    "default":          {"provider": "openai", "model": "gpt-3.5-turbo"},
}
