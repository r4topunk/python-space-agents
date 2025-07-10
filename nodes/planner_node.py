from typing import Dict, Any, AsyncGenerator
from langchain_core.runnables import RunnableLambda
from utils.message_helpers import make_log
from tools.get_llm import get_llm, chat_with_schema
from pydantic import BaseModel, Field

# 🧠 SYSTEM PROMPT CONSTANT
PLANNER_SYSTEM_PROMPT = """You are a layout planning agent for personalized digital spaces.
Your job is to decide which content blocks ("fidgets") to include in a layout based on a user's input and detected intent.

Return a JSON response that includes:
{
  "designed_fidgets": [ { ...fidget object... } ],
  "theme_hints": { ...optional theme styling info... }
}"""
# Example fidgets: text block, feed block (e.g. X, Farcaster), image gallery, RSS, video player, etc.

# 🧱 Pydantic Output Schema
class PlannerSchema(BaseModel):
    designed_fidgets: list[dict]
    theme_hints: dict = Field(default_factory=dict)

# 🔧 LLM-based Planner Logic
async def planner_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")
    intent = state.get("intent", {})
    subject = intent.get("subject", "unknown")

    yield make_log("planner", "start", f"📐 Planner analyzing layout for: {prompt}")

    llm = get_llm("planner")

    user_prompt = f"""
User Prompt: {prompt}
Detected Subject: {subject}
Detected Intent: {intent}
"""

    result = await chat_with_schema(llm, PLANNER_SYSTEM_PROMPT, user_prompt, PlannerSchema)

    # ✅ Ensure each fidget has a unique ID
    for i, f in enumerate(result.designed_fidgets):
        f.setdefault("id", f"fidget:{i}")

    yield make_log("planner", "end", f"🧩 Planner selected {len(result.designed_fidgets)} fidgets")

    yield {
        **state,
        "designed_fidgets": result.designed_fidgets,
        "theme_hints": result.theme_hints,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"🧩 Planner prepared {len(result.designed_fidgets)} fidgets for subject: {subject}"
        }]
    }

# 🚀 Export Runnable Node
run_planner_node = RunnableLambda(planner_logic)
