"""
Example usage and demonstration script.
"""

import asyncio
import json
from main import create_space
from utils.pretty_print import pretty_print_json, pretty_print_step


async def run_example():
    """Run an example space creation."""
    
    # Example request for a dog community
    dog_community_request = (
        "Create a space for a community of dog lovers who are active on Farcaster "
        "and interested in dog training, sharing photos of their pets, and connecting "
        "with other dog enthusiasts. Include social feeds, photo galleries, and "
        "resources for training tips."
    )
    
    pretty_print_step("Example 1", "Dog Community Space")
    
    try:
        result = await create_space(dog_community_request)
        
        # Extract the final configuration if available
        for message in reversed(result):
            content = str(message.content) if hasattr(message, 'content') else str(message)
            if '{' in content and 'fidgetInstanceDatums' in content:
                # Try to extract and display JSON
                try:
                    # Find JSON in the content
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start >= 0 and end > start:
                        json_str = content[start:end]
                        config = json.loads(json_str)
                        pretty_print_json(config, "Final Space Configuration")
                        break
                except json.JSONDecodeError:
                    pass
                    
    except Exception as e:
        print(f"Error in example: {e}")


def run_sync_example():
    """Run the example synchronously."""
    asyncio.run(run_example())


if __name__ == "__main__":
    run_sync_example()
