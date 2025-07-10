from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from typing import Dict, Any

from nodes.intent_extractor import intent_extractor          # ✅ NEW
from nodes.planner_node import run_planner_node
from nodes.researcher_node import run_researcher_node
from nodes.designer_node import run_designer_node
from nodes.builder_node import run_builder_node

async def create_supervisor_workflow() -> Runnable:
    workflow = StateGraph(Dict[str, Any])
    workflow.add_node("intent_extractor", intent_extractor)
    workflow.add_node("researcher", run_researcher_node)
    workflow.add_node("planner", run_planner_node)
    workflow.add_node("designer", run_designer_node)
    workflow.add_node("builder", run_builder_node)

    workflow.set_entry_point("intent_extractor")
    workflow.add_edge("intent_extractor", "researcher")
    workflow.add_edge("researcher", "planner")
    workflow.add_edge("planner", "designer")
    workflow.add_edge("designer", "builder")
    workflow.add_edge("builder", END)
    
    return workflow.compile()