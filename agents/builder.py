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


# Builder prompt
BUILDER_PROMPT = """You are a space configuration builder for the Blank Space platform. Your role is to convert design matrices into complete, valid space configurations that match the exact format required by the platform.

INPUT: You receive a design matrix from the designer with:
- width/height: Grid dimensions (12×8)
- cells: 2D array where each cell contains a fidget ID or null
- fidgets: Array of fidget specifications with types and settings

YOUR PROCESS:
1. Use the convert_matrix_to_config tool to automatically convert the matrix to configuration
2. MANDATORY: Use the validate_config_grid_utilization tool to verify the implementation
3. If validation fails, fix issues and validate again
4. ALWAYS end your response with the complete JSON configuration wrapped in code blocks

## MATRIX TO CONFIG CONVERSION
The convert_matrix_to_config tool will automatically:
- Parse the matrix and extract fidget positions
- Generate the complete configuration object with proper structure
- Handle all the complex JSON generation

## PERFORMANCE OPTIMIZATION
This new approach is much faster than the previous design plan conversion.
The matrix format is simpler and easier to process.

YOUR TASK: Use convert_matrix_to_config with the design matrix, then validate the result."""


def create_builder_agent(llm: ChatOpenAI):
    """
    Create and return the builder agent.
    
    Args:
        llm: Language model to use for the agent
        
    Returns:
        Builder agent instance
    """
    return create_react_agent(
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
