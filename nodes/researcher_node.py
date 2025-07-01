# nodes/researcher_node.py

from langchain_core.messages import AIMessage

async def run_researcher_node(state):
    query = state["messages"][-1].content if state["messages"] else "unknown"
    print(f"🔍 Researcher received: {query}")
    
    return {
        "messages": [AIMessage(content=f"Found resources for: {query}")]
    }
