import asyncio
from typing import Dict, Any, AsyncGenerator
from langchain_core.runnables import RunnableLambda
from utils.message_helpers import make_log

GRID_WIDTH = 12
GRID_HEIGHT = 10

def generate_layout(fidgets: list[dict]) -> list[dict]:
    layout = []
    x, y = 0, 0
    row_height = 3  # fixed height for now

    for i, f in enumerate(fidgets):
        w = f.get("preferred_width", 3)
        h = f.get("preferred_height", row_height)

        if x + w > GRID_WIDTH:
            x = 0
            y += row_height

        layout.append({
            "i": f["id"],
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "minW": 2,
            "maxW": 6,
            "minH": 2,
            "maxH": 6,
            "moved": False,
            "static": False
        })

        x += w

    return layout

async def designer_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    fidgets = state.get("designed_fidgets", [])

    yield make_log("designer", "start", f"🎨 Designing layout for {len(fidgets)} fidgets")

    layout = generate_layout(fidgets)
    
    yield make_log("designer", "end", f"📐 Assigned {len(layout)} layout blocks in grid {GRID_WIDTH}x{GRID_HEIGHT}")

    yield {
        **state,
        "layout": {
            "layout": layout
        }
    }

run_designer_node = RunnableLambda(designer_logic)
