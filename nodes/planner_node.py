from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any

# Define state shape
class PlannerState(TypedDict):
    messages: Annotated[Sequence[Any], lambda x: x[-8:]]  # keep last 8
    input: Optional[str]
    plan: Optional[Dict[str, Any]]

def planner_logic(state: PlannerState) -> PlannerState:
    last_message = state["messages"][-1]
    user_input = last_message.content if isinstance(last_message, HumanMessage) else None
    if not user_input:
        return state

    print("🧠 Planning based on:", user_input)
    plan = {
        "grid_size": "12x10",
        "fidget_count": 4,
        "fidgets": ["rss", "image", "info", "social"]
    }
    new_message = AIMessage(content=f"Planned grid with {plan['fidget_count']} fidgets")

    return {
        **state,
        "messages": state["messages"] + [new_message],
        "plan": plan,
    }

from typing import Dict, Any
from . import planner_node  # assuming planner_node is defined in the same file

async def run_planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    return planner_node.invoke(state)


# Create node
planner_node = RunnableLambda(planner_logic)

# For testing
if __name__ == "__main__":
    test_state = {
        "input": "Create a space about skateboarding culture",
        "messages": [HumanMessage(content="Create a space about skateboarding culture")]
    }
    result = planner_node.invoke(test_state)
    print("\n🧾 Plan Result:", result)
