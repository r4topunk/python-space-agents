"""
Builder agent implementation.
"""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools.conversion_tools import convert_matrix_to_config
from tools.validation_tools import (
    validate_config,
    validate_design_implementation,
    validate_config_grid_utilization,
)


"""
Builder agent implementation with performance optimizations.
"""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import structlog

from tools.conversion_tools import convert_matrix_to_config
from tools.validation_tools import (
    validate_config,
    validate_design_implementation,
    validate_config_grid_utilization,
)
from utils.performance import performance_monitor

logger = structlog.get_logger()


# Optimized builder prompt focused on tool usage and efficiency
BUILDER_PROMPT = """You are a space configuration builder for the Blank Space platform. Your role is to convert design matrices into complete, valid space configurations using AUTOMATED TOOLS for maximum efficiency and accuracy.

## INPUT
You receive a design matrix from the designer with:
- width/height: Grid dimensions (12×8)
- cells: 2D array where each cell contains a fidget ID or null
- fidgets: Array of fidget specifications with types and settings

## OPTIMIZED PROCESS (CRITICAL - FOLLOW EXACTLY)
1. **AUTOMATIC CONVERSION**: Use convert_matrix_to_config tool immediately with the design matrix
2. **VALIDATION**: Use validate_config_grid_utilization tool to verify 75%+ coverage
3. **QUALITY CHECK**: Use validate_config tool to ensure format correctness
4. **FINAL OUTPUT**: Provide the complete JSON configuration in your response

## PERFORMANCE ADVANTAGES
- ✅ **90% Faster**: Automated matrix→config conversion eliminates manual JSON creation
- ✅ **Zero Errors**: Tool-based approach prevents JSON formatting mistakes
- ✅ **Consistent Quality**: Automated layout calculations ensure perfect grid alignment
- ✅ **Validation Built-in**: Tools include error checking and optimization suggestions

## SUCCESS CRITERIA
1. **Tool Usage**: MUST use convert_matrix_to_config as first step
2. **Grid Coverage**: Target 75%+ utilization (validated automatically)
3. **JSON Completeness**: All required fields populated correctly
4. **Format Validation**: Configuration passes all validation checks

## CRITICAL: OUTPUT FORMAT
After tool validation succeeds, your final response must include:

```json
{
  "fidgetInstanceDatums": { ... },
  "layoutID": "layout-...",
  "layoutDetails": { ... },
  "isEditable": true,
  "fidgetTrayContents": [],
  "theme": { ... }
}
```

## ERROR HANDLING
- If conversion fails: Report specific issue and request design corrections
- If validation fails: Use suggestions to optimize configuration
- If coverage is low: Recommend specific improvements to achieve 75%+ target

## EFFICIENCY TARGETS
- Complete configuration generation in 1-2 tool calls maximum
- Achieve 75%+ grid utilization on first attempt
- Provide complete working JSON configuration immediately

Use tools strategically and provide the complete configuration as your final output."""


@performance_monitor.time_operation("create_builder_agent")
def create_builder_agent(llm: ChatOpenAI):
    """
    Create and return the optimized builder agent.
    
    Args:
        llm: Pre-configured language model to use for the agent
        
    Returns:
        Builder agent instance with performance monitoring
    """
    logger.info("Creating builder agent", model=llm.model_name)
    
    # Create agent with optimized tool set
    agent = create_react_agent(
        llm,
        tools=[
            convert_matrix_to_config,
            validate_config,
            validate_design_implementation,
            validate_config_grid_utilization,
        ],
        name="builder",
        prompt=SystemMessage(content=BUILDER_PROMPT),
    )
    
    logger.info("Builder agent created successfully")
    return agent
