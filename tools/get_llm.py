# tools/get_llm.py or similar
from langchain_openai import ChatOpenAI
from config.llm_config import LLM_CONFIG, PROVIDERS

def get_llm(worker: str) -> ChatOpenAI:
    config = LLM_CONFIG.get(worker, LLM_CONFIG["default"])
    provider = config["provider"]
    model = config["model"]

    return ChatOpenAI(
        model=model,
        api_key=PROVIDERS[provider]["api_key"],
        base_url=PROVIDERS[provider]["base_url"],
        temperature=0.3,
    )

from typing import Type
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

async def chat_with_schema(model: ChatOpenAI, system_prompt: str, user_prompt: str, schema: BaseModel):
    response = await model.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    
    # print("🔍 RAW RESPONSE FROM LLM:", response.content)  # ← Debug

    try:
        return schema.model_validate_json(response.content)
    except Exception as e:
        print("❌ Validation error:", e)
        raise