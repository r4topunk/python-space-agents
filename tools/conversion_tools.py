"""
Matrix conversion tools for transforming design matrices into configurations.
"""

import json
from typing import Dict, Any
from datetime import datetime
from langchain_core.tools import tool

from models.agent_types import DesignMatrix, SpaceConfig, FidgetInstanceDatum, FidgetConfig


@tool
def convert_matrix_to_config(data: str) -> str:
    """
    Converts a design matrix into a complete space configuration object.
    
    Args:
        data: JSON string containing design matrix
        
    Returns:
        Success message with complete configuration JSON
    """
    try:
        matrix_data = json.loads(data)
        matrix = DesignMatrix(**matrix_data)
        
        # Extract fidget positions from matrix
        fidget_positions: Dict[str, Dict[str, int]] = {}
        
        for fidget_spec in matrix.fidgets:
            fidget_id = fidget_spec.id
            min_x = matrix.width
            max_x = -1
            min_y = matrix.height
            max_y = -1
            
            # Find bounds of this fidget in the matrix
            for y in range(matrix.height):
                for x in range(matrix.width):
                    if y < len(matrix.cells) and x < len(matrix.cells[y]):
                        if matrix.cells[y][x] == fidget_id:
                            min_x = min(min_x, x)
                            max_x = max(max_x, x)
                            min_y = min(min_y, y)
                            max_y = max(max_y, y)
            
            if max_x >= 0 and max_y >= 0:
                fidget_positions[fidget_id] = {
                    "x": min_x,
                    "y": min_y,
                    "width": max_x - min_x + 1,
                    "height": max_y - min_y + 1
                }
        
        # Generate configuration object
        layout_id = f"layout-{int(datetime.now().timestamp())}"
        
        # Initialize fidget instance datums
        fidget_instance_datums: Dict[str, Any] = {}
        layout_items = []
        
        # Generate fidget instances and layout items
        for fidget_spec in matrix.fidgets:
            position = fidget_positions.get(fidget_spec.id)
            if not position:
                continue
            
            fidget_id = f"fidget:{fidget_spec.id}"
            
            # Create fidget instance
            fidget_instance = FidgetInstanceDatum(
                config=FidgetConfig(
                    editable=True,
                    settings={
                        **fidget_spec.settings,
                        # Use theme variables for colors
                        "fontColor": fidget_spec.settings.get("fontColor", "var(--user-theme-font-color)"),
                        "headingColor": fidget_spec.settings.get("headingColor", "var(--user-theme-headings-font-color)")
                    },
                    data={}
                ),
                fidget_type=fidget_spec.type.value,
                id=fidget_id
            )
            
            fidget_instance_datums[fidget_id] = fidget_instance.dict(by_alias=True)
            
            # Add to layout
            layout_items.append({
                "i": fidget_id,
                "x": position["x"],
                "y": position["y"],
                "w": position["width"],
                "h": position["height"],
                "minW": position["width"],
                "maxW": 36,
                "minH": position["height"],
                "maxH": 36,
                "moved": False,
                "static": False
            })
        
        # Create complete configuration
        config = {
            "fidgetInstanceDatums": fidget_instance_datums,
            "layoutID": layout_id,
            "layoutDetails": {
                "layoutFidget": "grid",
                "layoutConfig": {
                    "layout": layout_items
                }
            },
            "isEditable": True,
            "fidgetTrayContents": [],
            "theme": {
                "id": "default-theme",
                "name": "Default Theme",
                "properties": {
                    "font": "Inter",
                    "fontColor": "#ffffff",
                    "headingsFont": "Roboto",
                    "headingsFontColor": "#00ffff",
                    "background": "linear-gradient(45deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
                    "backgroundHTML": "",
                    "musicURL": "",
                    "fidgetBackground": "rgba(30, 100, 150, 0.95)",
                    "fidgetBorderWidth": "1px",
                    "fidgetBorderColor": "#00ffff",
                    "fidgetShadow": "0 0 20px rgba(0, 255, 255, 0.5)",
                    "fidgetBorderRadius": "12px",
                    "gridSpacing": "16"
                }
            }
        }
        
        return f"✅ Configuration generated successfully with {len(matrix.fidgets)} fidgets.\n\n{json.dumps(config, indent=2)}"
        
    except json.JSONDecodeError as e:
        return f"❌ JSON parsing error: {str(e)}"
    except Exception as e:
        return f"❌ Error converting matrix to config: {str(e)}"
