import asyncio
from typing import Dict, Any, AsyncGenerator
from langchain_core.runnables import RunnableLambda
from utils.message_helpers import make_log, make_message
from utils.pretty_print import print_grid_layout
import uuid
import json

DEFAULT_THEME = {
    "id": "default",
    "name": "Default Theme",
    "properties": {
        "font": "Inter",
        "fontColor": "#000000",
        "headingsFont": "Poppins",
        "headingsFontColor": "#333333",
        "background": "#ffffff",
        "fidgetBackground": "#f5f5f5",
        "fidgetBorderColor": "#dddddd",
        "fidgetShadow": "none",
        "fidgetBorderRadius": "8px",
        "gridSpacing": "8"
    }
}

def build_fidget_map(fidgets: list[dict]) -> dict:
    return {
        f.get("id", str(uuid.uuid4())): {
            "id": f.get("id", str(uuid.uuid4())),
            "fidgetType": f["type"],
            "config": {
                "editable": True,
                "settings": f.get("settings", {}),
                "data": f.get("data", {})
            }
        }
        for f in fidgets
    }

async def builder_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    if isinstance(state, list):
        state = state[-1] if state else {}

    prompt = state.get("input", "")
    intent = state.get("intent", {}).get("intent", "")
    fidgets = state.get("designed_fidgets", [])
    layout = state.get("layout", {}).get("layout", [])
    layout_id = state.get("layoutID", "custom-space")
    images = state.get("images", [])

    yield make_log("builder", "start", f"🔧 Builder starting for: {prompt}")

    if intent == "image_search" and images:
        fidget_map = {
            "fidget:0": {
                "id": "fidget:0",
                "fidgetType": "gallery",
                "config": {
                    "editable": True,
                    "settings": {"title": f"Images for {prompt}"},
                    "data": {"images": images}
                }
            }
        }
        layout = [{
            "i": "fidget:0",
            "x": 0,
            "y": 0,
            "w": 12,
            "h": 6,
            "minW": 6,
            "maxW": 12,
            "minH": 4,
            "maxH": 8,
            "moved": False,
            "static": False
        }]
        theme = {"id": "minimal", "name": "Minimal Theme", "properties": {"background": "#ffffff"}}
    else:
        fidget_map = build_fidget_map(fidgets)
        theme = DEFAULT_THEME

    final_config = {
        "layoutID": layout_id,
        "layoutDetails": {
            "layoutFidget": layout_id,
            "layoutConfig": {"layout": layout}
        },
        "fidgetInstanceDatums": fidget_map,
        "theme": theme,
        "isEditable": True,
        "fidgetTrayContents": []
    }

    print("🔍 Rendering layout on server side:")
    print_grid_layout(layout)

    # Send builder_logs as a single JSON object
    yield {"type": "builder_logs", "message": final_config}

    yield make_message(f"✅ Final layout generated with {len(fidget_map)} fidgets")

    yield {
        **state,
        "output": final_config,
        "messages": state.get("messages", []) + [{"type": "builder_logs", "content": final_config}]
    }

run_builder_node = RunnableLambda(builder_logic)