import asyncio
import json
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable
from utils.message_helpers import make_log, make_message

def render_terminal_grid(layout, grid_width=12, grid_height=10):
    grid = [[" . " for _ in range(grid_width)] for _ in range(grid_height)]
    legend = []

    for idx, item in enumerate(layout, 1):
        i = item.get("i", "?")
        x = item.get("x", 0)
        y = item.get("y", 0)
        w = item.get("w", 1)
        h = item.get("h", 1)

        if x + w > grid_width or y + h > grid_height:
            print(f"❌ Invalid position/size for: {i}")
            continue

        label = f"F{idx}"
        for dy in range(h):
            for dx in range(w):
                if dy == 0 and dx == 0:
                    grid[y + dy][x + dx] = f"{label:>3}"
                else:
                    grid[y + dy][x + dx] = " ░ "

        legend.append(f"{label} = {i} @ ({x},{y}) [{w}x{h}]")

    print("\n🧱 Grid Layout Preview:\n")
    for row in grid:
        print("".join(row))
    print("\n📘 Legend:")
    for l in legend:
        print("  ", l)
    print()


async def builder_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")
    yield make_log("builder", "start", f"🔧 Builder starting for: {prompt}")

    await asyncio.sleep(2.5)

    layout_items = state.get("designed_fidgets", [])
    layout = {
        "layoutID": "auto-generated",
        "layoutDetails": {
            "layoutFidget": "generated-layout",
            "layoutConfig": {
                "layout": layout_items
            }
        }
    }

    # 👇 Render the grid layout in the server console
    print("\n🔍 Rendering layout on server side:")
    render_terminal_grid(layout_items)

    # Send layout JSON as message for client use
    yield make_message(json.dumps(layout, indent=2))

    yield make_log("builder", "end", f"✅ Builder finished for: {prompt}")

    yield {
        **state,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"✅ Final layout generated with {len(layout_items)} fidgets"
        }],
        "output": layout
    }

run_builder_node: Runnable = builder_logic
