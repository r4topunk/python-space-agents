"""
Main execution script for the Python Space Agents system with performance optimizations.
"""

import asyncio
import os
import sys
import time
from typing import List, Dict, Any, cast
from langchain_core.messages import AnyMessage
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.info("python-dotenv not available, using environment variables directly")
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
    from utils.performance import performance_monitor, simple_cache
    from config.llm_config import clear_llm_cache
    DEPENDENCIES_AVAILABLE = True
    logger.info("All dependencies loaded successfully")
except ImportError as e:
    logger.error("Import error", error=str(e))
    print(f"❌ Import error: {e}")
    print("💡 Try running: ./venv/bin/pip install -r requirements.txt")
    print("💡 Or use: python run.py for demo mode")
    DEPENDENCIES_AVAILABLE = False


@performance_monitor.time_operation("create_space")
async def create_space(user_request: str) -> List[Dict[str, Any]]:
    """
    Create a space configuration based on user request with performance monitoring.
    
    Args:
        user_request: Natural language description of the space to create
        
    Returns:
        List of messages from the workflow execution
    """
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Required dependencies not available. Please install them first.")
    
    start_time = time.time()
    logger.info("Starting space creation", request=user_request[:100])
    
    try:
        pretty_print_step("Initializing", "Setting up the optimized supervisor workflow...")
        
        # Create the supervisor workflow
        workflow = create_supervisor_workflow()
        
        pretty_print_step("Processing", f"Creating space for: {user_request}")
        
        # Execute the workflow with performance monitoring
        result = []
        step_count = 0
        
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
                step_count += 1
        
        duration = time.time() - start_time
        
        # Log performance metrics
        cache_stats = simple_cache.get_stats()
        performance_report = performance_monitor.get_report()
        
        logger.info(
            "Space creation completed",
            duration=round(duration, 2),
            steps=step_count,
            cache_hit_rate=cache_stats["hit_rate"],
            total_operations=performance_report["summary"]["total_operations"]
        )
        
        pretty_print_success(f"Space creation completed in {duration:.2f}s with {step_count} steps!")
        
        # Print performance summary
        if cache_stats["hit_rate"] > 0:
            pretty_print_step("Performance", f"Cache hit rate: {cache_stats['hit_rate']}%")
        
        return result
        
    except Exception as error:
        duration = time.time() - start_time
        logger.error("Space creation failed", error=str(error), duration=round(duration, 2))
        pretty_print_error(f"Error creating space: {str(error)}")
        raise error


def main():
    """Main entry point for the application with performance optimizations."""
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
    
    logger.info("Starting application")
    
    # Example usage with enhanced prompt
    example_request = (
        "Create a space for a community of dog lovers who are active on Farcaster "
        "and interested in dog training, sharing photos of their pets, and connecting "
        "with other dog enthusiasts. Include feeds for dog-related content, links to "
        "training resources, and a welcoming community atmosphere."
    )
    
    try:
        start_time = time.time()
        result = asyncio.run(create_space(example_request))
        total_time = time.time() - start_time
        
        pretty_print_step("Completed", f"Generated {len(result)} workflow steps in {total_time:.2f}s")
        
        # Show performance summary
        performance_report = performance_monitor.get_report()
        cache_stats = simple_cache.get_stats()
        
        if performance_report["summary"]["total_operations"] > 0:
            pretty_print_step("Performance Summary", 
                f"Operations: {performance_report['summary']['total_operations']} | "
                f"Cache hits: {cache_stats['hits']} | "
                f"Slowest: {performance_report['summary']['slowest_operation']}"
            )
        
        # Clear caches for next run
        clear_llm_cache()
        
    except Exception as e:
        logger.error("Application error", error=str(e))
        pretty_print_error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
