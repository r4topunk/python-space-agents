from typing import List, Dict, Any
import random

def layout_fidgets(fidgets: List[Dict[str, Any]], grid_width: int = 12, grid_height: int = 8) -> List[Dict[str, Any]]:
    """
    Assigns position (x, y) and dimensions (w, h) to each fidget in the grid.
    Ensures no overlap by using simple greedy placement.
    """
    used_positions = set()
    placed = []

    for f in fidgets:
        for _ in range(100):  # Try 100 random positions max
            w, h = random.choice([(3, 3), (4, 2), (2, 2), (6, 4)])
            x = random.randint(0, grid_width - w)
            y = random.randint(0, grid_height - h)
            coords = {(x + dx, y + dy) for dx in range(w) for dy in range(h)}

            if not coords & used_positions:
                used_positions |= coords
                placed.append({**f, "x": x, "y": y, "w": w, "h": h})
                break
        else:
            # Failed to place it
            print(f"⚠️ Could not place fidget: {f['type']}")

    return placed

def run_designer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    fidgets = state["fidgets"] if "fidgets" in state else []
    grid_size = state["grid"] if "grid" in state else {"w": 12, "h": 8}
    designed = layout_fidgets(fidgets, grid_size["w"], grid_size["h"])
    return {**state, "designed_fidgets": designed}
