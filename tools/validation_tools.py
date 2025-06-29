"""
Validation tools for agent outputs and configurations.
"""

import json
from typing import Any, Dict, List, Optional, Set
from langchain_core.tools import tool

from models.agent_types import (
    ResearchData,
    DesignMatrix,
    FidgetType,
    FIDGET_MIN_SIZES,
    SpaceConfig,
)


@tool
def validate_research(data: str) -> str:
    """
    Validates research output format and content.
    
    Args:
        data: JSON string containing research data
        
    Returns:
        Validation result message
    """
    try:
        parsed_data = json.loads(data)
        research_data = ResearchData(**parsed_data)
        
        # Basic validation checks
        if not research_data.summary or len(research_data.summary.strip()) < 10:
            return "❌ Summary is too short. Please provide a meaningful 2-3 sentence summary."
        
        if len(research_data.key_topics) < 2:
            return "❌ Please provide at least 2 key topics."
            
        if not research_data.relevant_links:
            return "❌ Please provide at least one relevant link."
            
        return "✅ Research data is valid and properly formatted."
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON format: {str(e)}"
    except Exception as e:
        return f"❌ Validation error: {str(e)}"


@tool
def validate_matrix_design(data: str) -> str:
    """
    Fast validation of matrix design format and coverage.
    
    Args:
        data: JSON string containing design matrix
        
    Returns:
        Validation result message
    """
    try:
        parsed_data = json.loads(data)
        matrix = DesignMatrix(**parsed_data)
        
        GRID_WIDTH = 12
        GRID_HEIGHT = 8
        TOTAL_CELLS = GRID_WIDTH * GRID_HEIGHT
        
        # Validate grid dimensions
        if matrix.width != GRID_WIDTH or matrix.height != GRID_HEIGHT:
            return f"❌ Invalid grid dimensions: {matrix.width}×{matrix.height}. Must be {GRID_WIDTH}×{GRID_HEIGHT}."
        
        # Validate matrix structure
        if len(matrix.cells) != GRID_HEIGHT:
            return f"❌ Matrix has {len(matrix.cells)} rows, expected {GRID_HEIGHT}."
        
        for i, row in enumerate(matrix.cells):
            if not row or len(row) != GRID_WIDTH:
                return f"❌ Row {i} has {len(row) if row else 0} columns, expected {GRID_WIDTH}."
        
        # Extract fidget regions and validate
        fidget_regions: Dict[str, Dict[str, int]] = {}
        fidget_ids: Set[str] = set()
        occupied_cells = 0
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_value = matrix.cells[y][x]
                if cell_value:
                    occupied_cells += 1
                    fidget_ids.add(cell_value)
                    
                    if cell_value not in fidget_regions:
                        fidget_regions[cell_value] = {
                            "min_x": x, "max_x": x, "min_y": y, "max_y": y
                        }
                    else:
                        region = fidget_regions[cell_value]
                        region["min_x"] = min(region["min_x"], x)
                        region["max_x"] = max(region["max_x"], x)
                        region["min_y"] = min(region["min_y"], y)
                        region["max_y"] = max(region["max_y"], y)
        
        # Validate that all fidgets in the spec exist in the matrix
        spec_fidget_ids = {f.id for f in matrix.fidgets}
        for fidget_id in fidget_ids:
            if fidget_id not in spec_fidget_ids:
                return f"❌ Fidget '{fidget_id}' found in matrix but not in fidgets spec."
        
        # Validate fidget minimum sizes
        for fidget_id, region in fidget_regions.items():
            fidget_spec = next((f for f in matrix.fidgets if f.id == fidget_id), None)
            if not fidget_spec:
                continue
            
            width = region["max_x"] - region["min_x"] + 1
            height = region["max_y"] - region["min_y"] + 1
            min_size = FIDGET_MIN_SIZES.get(fidget_spec.type)
            
            if min_size and (width < min_size.width or height < min_size.height):
                return f"❌ Fidget '{fidget_id}' size {width}×{height} is below minimum {min_size.width}×{min_size.height}."
            
            # Validate fidget forms a proper rectangle
            for y in range(region["min_y"], region["max_y"] + 1):
                for x in range(region["min_x"], region["max_x"] + 1):
                    if matrix.cells[y][x] != fidget_id:
                        return f"❌ Fidget '{fidget_id}' doesn't form a proper rectangle at ({x}, {y})."
        
        # Calculate coverage
        coverage_percentage = (occupied_cells / TOTAL_CELLS) * 100
        
        if coverage_percentage < 60:
            return f"❌ Coverage too low: {coverage_percentage:.1f}% (target: 70%+). Fill more cells."
        
        if coverage_percentage < 70:
            needed = int(TOTAL_CELLS * 0.70) - occupied_cells
            return f"⚠️ Coverage: {coverage_percentage:.1f}%. Add ~{needed} more cells to reach 70% target."
        
        return f"✅ Matrix design valid: {coverage_percentage:.1f}% coverage, {len(fidget_ids)} fidgets, proper rectangles."
        
    except json.JSONDecodeError as e:
        return f"❌ JSON parsing error: {str(e)}"
    except Exception as e:
        return f"❌ Validation error: {str(e)}"


@tool
def validate_config_grid_utilization(data: str) -> str:
    """
    Fast validation of configuration grid coverage and optimization suggestions.
    
    Args:
        data: JSON string containing space configuration
        
    Returns:
        Validation result message
    """
    try:
        # Try to parse the configuration
        try:
            config_data = json.loads(data)
        except json.JSONDecodeError:
            # Try unescaping if needed
            unescaped_data = data.replace('\\"', '"').replace('\\\\', '\\')
            try:
                config_data = json.loads(unescaped_data)
            except json.JSONDecodeError:
                if '{' in data and not data.strip().endswith('}'):
                    return "❌ Configuration JSON is truncated. Please ensure complete JSON is passed."
                return "❌ JSON parsing failed. Please check JSON formatting."
        
        # Validate structure
        if "layoutDetails" not in config_data or "layoutConfig" not in config_data["layoutDetails"]:
            return "❌ Invalid configuration format. Missing layout details."
        
        layout_items = config_data["layoutDetails"]["layoutConfig"].get("layout", [])
        if not layout_items:
            return "❌ No layout items found in configuration."
        
        GRID_WIDTH = 12
        GRID_HEIGHT = 8
        TOTAL_CELLS = GRID_WIDTH * GRID_HEIGHT
        
        occupied_cells = 0
        max_row_used = 0
        max_col_used = 0
        
        # Simple cell counting
        for item in layout_items:
            x, y, width, height = item["x"], item["y"], item["w"], item["h"]
            
            # Bounds check
            if x < 0 or y < 0 or x + width > GRID_WIDTH or y + height > GRID_HEIGHT:
                return f"❌ {item['i']} exceeds grid bounds: ({x},{y}) {width}×{height}"
            
            occupied_cells += width * height
            max_row_used = max(max_row_used, y + height)
            max_col_used = max(max_col_used, x + width)
        
        coverage_percentage = (occupied_cells / TOTAL_CELLS) * 100
        
        result = f"Grid Analysis: {coverage_percentage:.1f}% coverage ({occupied_cells}/{TOTAL_CELLS} cells)\n"
        
        if coverage_percentage >= 75:
            result += f"✅ GOOD: Grid utilization meets target ({coverage_percentage:.1f}%)"
            if max_row_used < GRID_HEIGHT:
                result += f"\n💡 Could extend to row {GRID_HEIGHT - 1} for even better utilization"
        else:
            result += f"⚠️ NEEDS IMPROVEMENT: {coverage_percentage:.1f}% coverage (target: 75%+)\n"
            result += f"📊 Using {max_row_used}/{GRID_HEIGHT} rows, {max_col_used}/{GRID_WIDTH} columns\n"
            
            missing_cells = int(TOTAL_CELLS * 0.75) - occupied_cells
            if missing_cells > 0:
                result += f"💡 Add ~{missing_cells} more cells of content to reach 75% target"
        
        return result
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def validate_design_implementation(design_data: str, config_data: str) -> str:
    """
    Validates that the builder correctly implemented the designer's plan.
    
    Args:
        design_data: JSON string containing design plan
        config_data: JSON string containing space configuration
        
    Returns:
        Validation result message
    """
    try:
        design = json.loads(design_data)
        config = json.loads(config_data)
        
        # Check if all designed fidgets are implemented
        if "fidgets" not in design:
            return "❌ Design data missing fidgets field."
            
        if "fidgetInstanceDatums" not in config:
            return "❌ Configuration missing fidgetInstanceDatums field."
        
        design_fidget_ids = [f["id"] for f in design["fidgets"]]
        config_fidget_ids = list(config["fidgetInstanceDatums"].keys())
        
        # Check for missing fidgets
        missing_fidgets = [fid for fid in design_fidget_ids if not any(cid.endswith(fid) for cid in config_fidget_ids)]
        if missing_fidgets:
            return f"❌ Missing fidgets in implementation: {', '.join(missing_fidgets)}. All designed fidgets must be included."
        
        # Check layout positions if available
        if "layoutDetails" in config and "layoutConfig" in config["layoutDetails"]:
            layout_items = config["layoutDetails"]["layoutConfig"].get("layout", [])
            
            for design_fidget in design["fidgets"]:
                fidget_id = design_fidget["id"]
                # Find corresponding layout item (may have prefix like "fidget:")
                layout_item = next(
                    (item for item in layout_items if item["i"].endswith(fidget_id)), 
                    None
                )
                
                if not layout_item:
                    return f"❌ Layout missing for fidget: {fidget_id}"
        
        return "✅ Builder implementation matches the design plan. All fidgets are correctly implemented."
        
    except json.JSONDecodeError as e:
        return f"❌ JSON parsing error: {str(e)}"
    except Exception as e:
        return f"❌ Validation error: {str(e)}"


@tool
def validate_config(data: str) -> str:
    """
    Validates final space configuration format and content.
    
    Args:
        data: JSON string containing space configuration
        
    Returns:
        Validation result message
    """
    try:
        config_data = json.loads(data)
        
        # Check if it's the old array format or new object format
        if isinstance(config_data, list):
            # Old format validation
            ids = set()
            for fidget in config_data:
                if not all(key in fidget for key in ["config", "fidgetType", "id"]):
                    return "❌ Each fidget must have config, fidgetType, and id fields."
                
                if fidget["id"] in ids:
                    return f"❌ Duplicate fidget ID: {fidget['id']}"
                ids.add(fidget["id"])
                
                try:
                    fidget_type = FidgetType(fidget["fidgetType"])
                except ValueError:
                    return f"❌ Invalid fidget type: {fidget['fidgetType']}"
        else:
            # New object format validation
            space_config = SpaceConfig(**config_data)
            
            # Check for duplicate IDs
            ids = set()
            for fidget_id, fidget in space_config.fidget_instance_datums.items():
                if fidget.id in ids:
                    return f"❌ Duplicate fidget ID: {fidget.id}"
                ids.add(fidget.id)
                
                try:
                    FidgetType(fidget.fidget_type)
                except ValueError:
                    return f"❌ Invalid fidget type: {fidget.fidget_type}"
        
        return "✅ Configuration is valid and properly formatted."
        
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON format: {str(e)}"
    except Exception as e:
        return f"❌ Validation error: {str(e)}"
