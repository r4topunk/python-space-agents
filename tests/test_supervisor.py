import asyncio
from agents.supervisor import create_supervisor_workflow
from langchain_core.messages import HumanMessage

async def test_workflow():
    workflow = create_supervisor_workflow()
    user_input = "Design a space to explore skateboarding news and YouTube clips"

    print("🚀 Running space-builder supervisor workflow...\n")

    async for step in workflow.astream(
        {"messages": [HumanMessage(content=user_input)]},
        stream_mode="values",
        config={"recursion_limit": 50}
    ):
        if "messages" in step:
            for m in step["messages"]:
                print(f"📨 {m.type}: {m.content}\n")

asyncio.run(test_workflow())
