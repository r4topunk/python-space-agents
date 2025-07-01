from typing import Dict, Any
import json

def run_builder_node(state: Dict[str, Any]) -> Dict[str, Any]:
    designed = state["designed_fidgets"] if "designed_fidgets" in state else []
    grid = state["grid"] if "grid" in state else {"w": 12, "h": 8}

    final_config = {
        "grid": grid,
        "fidgets": designed,
    }

    return {
        **state,
        "reply": {
            "type": "Reply",
            "name": "Space Builder",
            "message": json.dumps(final_config, indent=2)
        }
    }
