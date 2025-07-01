"""
Supervisor agent implementation using LangGraph.
"""

import asyncio
from typing import List, Literal, Set
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command

from agents.researcher import create_researcher_agent
from agents.designer import create_designer_agent
from agents.builder import create_builder_agent

# Supervisor prompt
SUPERVISOR_PROMPT = """You are the supervisor of a space creation team for the Blank Space platform with three specialists:

1. **RESEARCHER**: Gathers information and provides structured research data
2. **DESIGNER**: Creates layout plans with optimal grid coverage and fidget positioning
3. **BUILDER**: Generates final JSON configuration and validates design implementation

## ENHANCED WORKFLOW
1. Start with RESEARCHER to gather comprehensive information
2. Pass research results to DESIGNER to create layout plan
3. DESIGNER must validate their design meets grid coverage requirements (60%+ coverage)
4. Pass design plan to BUILDER to generate final configuration
5. BUILDER must validate that their implementation matches the design exactly
6. BUILDER must output the complete JSON configuration in their final response
7. Use FINISH only when both design validation, implementation validation pass, AND the JSON is provided

## QUALITY CONTROL
- Designer validates grid coverage and space utilization
- Builder validates design implementation fidelity
- Each agent has specialized validation tools
- Ensure designs fill the grid effectively (no large empty spaces)
- Verify final output matches design specifications exactly
- CRITICAL: The final response must contain the complete JSON configuration
"""

def get_next_node(last_message: BaseMessage, current_node: str) -> str:
    """Determine the next node based on the last message content."""
    # Log the last message to WebSocket clients
    from websocket import create_connection, WebSocket  # Import WebSocket for usage

    # Initialize the websocket connection
    websocket = create_connection("ws://your_websocket_url")  # Replace with actual URL
    log_to_websocket(last_message['content'], websocket)
    content = str(last_message.content).lower()
    
    # Check for completion indicators
    if any(phrase in content for phrase in ["final answer", "complete json configuration", "✅ configuration generated"]):
        return END
    
    # Follow the workflow sequence
    if current_node == "researcher":
        return "designer"
    elif current_node == "designer":
        return "builder"
    else:
        return END

async def research_node(state: MessagesState, websocket: web.WebSocketResponse) -> Command[Literal["designer", END]]:
    """Research node that gathers information about the community/topic."""
    # Create researcher agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4000)
    research_agent = create_researcher_agent(llm)
    
    # Execute research
    result = research_agent.invoke(state)
    await send_log_to_clients(f"Research result: {result}", websocket)  # Log research result
    goto = get_next_node(result["messages"][-1], "researcher")
    
    # Format the last message as human message for next agent
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="researcher"
    )
    
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )

def design_node(state: MessagesState, websocket: web.WebSocketResponse) -> Command[Literal["builder", "END"]]:
    """Design node that creates the layout plan."""
    # Create designer agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4000)
    design_agent = create_designer_agent(llm)
    
async def execute_design(state, design_agent):  # Pass design_agent as an argument
    # Execute design
    result = design_agent.invoke(state)
    await send_log_to_clients(f"Design result: {result}", websocket)  # Log design result
    goto = get_next_node(result["messages"][-1], "designer")
    
    # Format the last message as human message for next agent
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="designer"
    )
    
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )

def build_node(state: MessagesState) -> Command[Literal[END]]:
    """Build node that generates the final configuration."""
    # Create builder agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4000)
    build_agent = create_builder_agent(llm)
    
    # Execute build
    result = build_agent.invoke(state)
    
    # Format the last message as human message
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content,
        name="builder"
    )
    
    return Command(
        update={"messages": result["messages"]},
        goto=END,
    )

def create_supervisor_workflow():
    """
    Create and return the supervisor workflow.
    
    Returns:
        Compiled workflow graph
    """
    # Create the workflow graph
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("researcher", research_node)
    workflow.add_node("designer", design_node)
    workflow.add_node("builder", build_node)
    
    # Add edges
    workflow.add_edge(START, "researcher")
    
    # Compile the workflow
    return workflow.compile()

import logging
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to send logs to WebSocket clients
async def send_log_to_clients(message: str, clients: Set[web.WebSocketResponse]):
    for client in clients:
        await client.send_str(message)
        logger.info(f"Sent log to client: {message}")

def log_to_websocket(message: str, websocket: web.WebSocketResponse):
    logger.info(message)
    asyncio.create_task(websocket.send_str(message))
