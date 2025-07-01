from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from typing import Dict, Any

from nodes.planner_node import run_planner_node
from nodes.researcher_node import run_researcher_node
from nodes.designer_node import run_designer_node
from nodes.builder_node import run_builder_node

def create_supervisor_workflow() -> Runnable:
    workflow = StateGraph(Dict[str, Any])

    # Add each step node
    workflow.add_node("researcher", run_researcher_node)
    workflow.add_node("planner", run_planner_node)
    workflow.add_node("designer", run_designer_node)
    workflow.add_node("builder", run_builder_node)

    # Connect the flow
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "planner")
    workflow.add_edge("planner", "designer")
    workflow.add_edge("designer", "builder")
    workflow.add_edge("builder", END)

    # Compile into a LangGraph Runnable
    return workflow.compile()
