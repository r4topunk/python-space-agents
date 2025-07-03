"""
Supervisor agent implementation using LangGraph with performance optimizations.
"""

from typing import List, Literal
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
import structlog

from agents.researcher import create_researcher_agent
from agents.designer import create_designer_agent  
from agents.builder import create_builder_agent
from config.llm_config import get_optimized_llm
from utils.performance import performance_monitor

logger = structlog.get_logger()


# Enhanced supervisor prompt with better workflow control
SUPERVISOR_PROMPT = """You are the supervisor of a space creation team for the Blank Space platform with three specialists:

1. **RESEARCHER**: Gathers information and provides structured research data with specific JSON format
2. **DESIGNER**: Creates optimized layout plans with matrix-based grid coverage (70%+ required)
3. **BUILDER**: Generates final JSON configuration using automated tools for accuracy

## OPTIMIZED WORKFLOW (Critical Performance Requirements)
1. **RESEARCHER**: Must output structured JSON research data immediately - no multiple iterations
2. **DESIGNER**: Must create matrix design with 70%+ grid coverage - validate before proceeding  
3. **BUILDER**: Must use conversion tools to generate final configuration - validate implementation
4. **Quality Gates**: Each agent has validation tools - use them to prevent workflow failures

## PERFORMANCE OPTIMIZATIONS
- Each agent specializes with optimized prompts and focused LLM configurations
- Matrix design approach reduces JSON generation complexity by 60%
- Automated validation prevents expensive re-work loops
- Structured output formats eliminate parsing errors

## SUCCESS CRITERIA
- Research: Valid JSON with all required fields (summary, keyTopics, socialAccounts, etc.)
- Design: Matrix with 70%+ coverage, proper fidget sizing, rectangular regions
- Build: Complete space configuration JSON that validates successfully
- CRITICAL: Final response must contain complete working JSON configuration

Delegate efficiently and ensure quality gates pass before proceeding to next stage."""


@performance_monitor.time_operation("get_next_node")
def get_next_node(last_message: BaseMessage, current_node: str) -> str:
    """Determine the next node based on the last message content with performance logging."""
    content = str(last_message.content).lower()
    
    # Check for completion indicators
    if any(phrase in content for phrase in [
        "final answer", "complete json configuration", "✅ configuration generated",
        "configuration generated successfully"
    ]):
        logger.info("Workflow completion detected", current_node=current_node)
        return END
    
    # Follow the optimized workflow sequence
    if current_node == "researcher":
        logger.info("Routing to designer", previous_node=current_node)
        return "designer"
    elif current_node == "designer":
        logger.info("Routing to builder", previous_node=current_node)
        return "builder"
    else:
        logger.info("Workflow complete", previous_node=current_node)
        return END


@performance_monitor.time_operation("research_node")
def research_node(state: MessagesState) -> Command:
    """Research node that gathers information about the community/topic."""
    logger.info("Starting research phase")
    
    # Use optimized LLM for research
    llm = get_optimized_llm("researcher")
    research_agent = create_researcher_agent(llm)
    
    # Execute research
    result = research_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "researcher")
    
    # Format the last message as human message for next agent
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="researcher"
    )
    
    logger.info("Research phase completed", next_node=goto)
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )


@performance_monitor.time_operation("design_node")
def design_node(state: MessagesState) -> Command:
    """Design node that creates the layout plan."""
    logger.info("Starting design phase")
    
    # Use optimized LLM for design
    llm = get_optimized_llm("designer")
    design_agent = create_designer_agent(llm)
    
    # Execute design
    result = design_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "designer")
    
    # Format the last message as human message for next agent
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="designer"
    )
    
    logger.info("Design phase completed", next_node=goto)
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )


@performance_monitor.time_operation("build_node")
def build_node(state: MessagesState) -> Command:
    """Build node that generates the final configuration."""
    logger.info("Starting build phase")
    
    # Use optimized LLM for building
    llm = get_optimized_llm("builder")
    build_agent = create_builder_agent(llm)
    
    # Execute build
    result = build_agent.invoke(state)
    
    # Format the last message as human message
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="builder"
    )
    
    logger.info("Build phase completed")
    return Command(
        update={"messages": result["messages"]},
        goto=END,
    )


@performance_monitor.time_operation("create_supervisor_workflow")
def create_supervisor_workflow():
    """
    Create and return the optimized supervisor workflow.
    
    Returns:
        Compiled workflow graph with performance monitoring
    """
    logger.info("Creating optimized supervisor workflow")
    
    # Create the workflow graph
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("researcher", research_node)
    workflow.add_node("designer", design_node)
    workflow.add_node("builder", build_node)
    
    # Add edges - simplified linear flow for better performance
    workflow.add_edge(START, "researcher")
    
    # Compile the workflow
    compiled_workflow = workflow.compile()
    
    logger.info("Supervisor workflow created successfully")
    return compiled_workflow
