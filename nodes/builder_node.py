import asyncio
from typing import Dict, Any, AsyncGenerator
from langchain_core.runnables import RunnableLambda
from utils.message_helpers import make_log, make_message
from utils.pretty_print import print_grid_layout

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
        f["id"]: {
            "id": f["id"],
            "fidgetType": f["type"],
            "config": {
                "editable": True,
                "settings": f.get("settings", {}),
                "data": {}
            }
        }
        for f in fidgets
    }

async def builder_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")
    fidgets = state.get("designed_fidgets", [])
    layout = state.get("layout", {}).get("layout", [])
    layout_id = state.get("layoutID", "custom-space")

    yield make_log("builder", "start", f"🔧 Builder starting for: {prompt}")
    await asyncio.sleep(0.5)

    fidget_map = build_fidget_map(fidgets)

    final_config = {
        "layoutID": layout_id,
        "layoutDetails": {
            "layoutFidget": layout_id,
            "layoutConfig": {
                "layout": layout
            }
        },
        "fidgetInstanceDatums": fidget_map,
        "theme": DEFAULT_THEME,
        "isEditable": True,
        "fidgetTrayContents": []
    }

    # 📦 Server-side Grid Render
    print("🔍 Rendering layout on server side:")
    print_grid_layout(layout)

    message = f"✅ Final layout generated with {len(fidgets)} fidgets"
    yield make_message(message)
    yield make_log("builder", "end", f"✅ Builder finished for: {prompt}")

    yield {
        **state,
        "output": final_config,
        "messages": state.get("messages", []) + [{"type": "message", "content": message}]
    }

run_builder_node = RunnableLambda(builder_logic)
