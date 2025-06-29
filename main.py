"""
Main execution script for the Python Space Agents system.
"""

import asyncio
import os
import sys
from typing import List, Dict, Any, cast
from langchain_core.messages import AnyMessage

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not available, using environment variables directly")
    # Try to load .env manually if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

try:
    from langchain_core.messages import HumanMessage
    from agents.supervisor import create_supervisor_workflow
    from utils.pretty_print import (
        pretty_print_message,
        pretty_print_step,
        pretty_print_error,
        pretty_print_success,
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try running: ./venv/bin/pip install -r requirements.txt")
    print("💡 Or use: python run.py for demo mode")
    DEPENDENCIES_AVAILABLE = False


async def create_space(user_request: str) -> List[Dict[str, Any]]:
    """
    Create a space configuration based on user request.
    
    Args:
        user_request: Natural language description of the space to create
        
    Returns:
        List of messages from the workflow execution
    """
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Required dependencies not available. Please install them first.")
    
    try:
        pretty_print_step("Initializing", "Setting up the supervisor workflow...")
        
        # Create the supervisor workflow
        workflow = create_supervisor_workflow()
        
        pretty_print_step("Processing", f"Creating space for: {user_request}")
        
        # Execute the workflow
        result = []
        async for step in workflow.astream(
            {"messages": cast(List[AnyMessage], [HumanMessage(content=user_request)])},
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            if "messages" in step and step["messages"]:
                last_message = step["messages"][-1]
                pretty_print_message(last_message)
                print("─" * 50)
                result.append(last_message)
        
        pretty_print_success("Space creation completed successfully!")
        return result
        
    except Exception as error:
        pretty_print_error(f"Error creating space: {str(error)}")
        raise error


def main():
    """Main entry point for the application."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Required dependencies not available.")
        print("🔧 Please run: ./venv/bin/pip install -r requirements.txt")
        print("💡 Or use: python run.py for demo mode")
        return
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pretty_print_error(f"Missing required environment variables: {', '.join(missing_vars)}")
        pretty_print_step("Setup", "Please set the following environment variables:")
        for var in missing_vars:
            print(f"  export {var}='your_key_here'")
        return
    
    # Example usage
    example_request = (
        "Create a space for a community of dog lovers who are active on Farcaster "
        "and interested in dog training, sharing photos of their pets, and connecting "
        "with other dog enthusiasts."
    )
    
    try:
        result = asyncio.run(create_space(example_request))
        pretty_print_step("Completed", f"Generated {len(result)} workflow steps")
    except Exception as e:
        pretty_print_error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
