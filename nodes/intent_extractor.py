from typing import Dict, Any
from langchain_core.runnables import RunnableLambda
from tools.get_llm import get_llm, chat_with_schema
from models.intent_schema import IntentSchema
from utils.message_helpers import make_message

INTENT_SYSTEM_PROMPT = """
You are a helpful assistant extracting structured user intent from a prompt.

Return a JSON object with the following structure:

{
  "intent": "create_space" | "edit_fidget" | "tweak_theme",
  "subject": string,
  "fidget_requests": [
    {"type": "gallery" | "video" | "rss" | "feed" | "links", "platform": optional string}
  ],
  "theme_hints": {
    "vibe": optional string,
    "background": optional string,
    "music": optional string
  },
  "requested_changes" should be a dictionary (e.g., {"summary": "..."}) or null.
}
"""


async def intent_extractor_logic(state: Dict[str, Any]) -> Dict[str, Any]:
    prompt = state.get("input", "")
    print("prompt: " + prompt)

    llm = get_llm("intent_extractor")

    parsed_intent = await chat_with_schema(
        model=llm,
        system_prompt=INTENT_SYSTEM_PROMPT,
        user_prompt=prompt,
        schema=IntentSchema
    )

    return {
        **state,
        "intent": parsed_intent.model_dump(),
        "messages": state.get("messages", []) + [
            make_message(f"🧠 Intent extracted: {parsed_intent.intent} for {parsed_intent.subject}")
        ]
    }

intent_extractor = RunnableLambda(intent_extractor_logic)
