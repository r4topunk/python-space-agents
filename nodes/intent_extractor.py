from typing import Dict, Any
import re
from langchain_core.runnables import RunnableLambda

async def intent_extractor_logic(state: Dict[str, Any]) -> Dict[str, Any]:
    prompt = state.get("input", "").lower()
    result: Dict[str, Any] = {
        "intent": "create_space",
        "subject": None,
        "fidget_requests": [],
        "theme_hints": {},
        "requested_changes": None,
    }

    if "change" in prompt or "update" in prompt:
        result["intent"] = "edit_fidget"
    elif "theme" in prompt or "background" in prompt:
        result["intent"] = "tweak_theme"

    match = re.search(r"about\s+([a-z0-9.\-@_/]+)", prompt)
    if match:
        result["subject"] = match.group(1)

    if "twitter" in prompt or "x.com" in prompt:
        result["fidget_requests"].append({"type": "feed", "platform": "twitter"})
    if "farcaster" in prompt:
        result["fidget_requests"].append({"type": "feed", "platform": "farcaster"})
    if "video" in prompt or "youtube" in prompt:
        result["fidget_requests"].append({"type": "video"})
    if "gallery" in prompt or "image" in prompt:
        result["fidget_requests"].append({"type": "gallery"})
    if "rss" in prompt or "news" in prompt:
        result["fidget_requests"].append({"type": "rss"})
    if "link" in prompt:
        result["fidget_requests"].append({"type": "links"})

    if "dark" in prompt:
        result["theme_hints"]["vibe"] = "dark"
    if "chill" in prompt:
        result["theme_hints"]["background"] = "chill"
    if "music" in prompt or "song" in prompt:
        result["theme_hints"]["music"] = "true"

    return {
        **state,
        "intent": result,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"🧠 Intent extracted: {result['intent']} for {result['subject']}"
        }]
    }

# 👇 Expose the Runnable
intent_extractor = RunnableLambda(intent_extractor_logic)
