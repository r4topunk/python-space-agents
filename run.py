"""
Simplified main script that works without all dependencies installed.
"""

import os
import sys
import json
from typing import List, Dict, Any


def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   {var}")
        print("\n📝 Please set them in your .env file or environment")
        return False
    return True


def simple_demo():
    """Run a simple demo without the full workflow."""
    print("🎯 Python Space Agents Demo")
    print("=" * 50)
    
    # Example input
    user_request = (
        "Create a space for a community of dog lovers who are active on Farcaster "
        "and interested in dog training, sharing photos of their pets, and connecting "
        "with other dog enthusiasts."
    )
    
    print(f"📝 User Request: {user_request}")
    print("\n🔄 Processing would involve:")
    print("1. 🔍 Researcher Agent: Gathering information about dog communities")
    print("2. 🎨 Designer Agent: Creating optimal grid layout with fidgets")
    print("3. ⚙️ Builder Agent: Generating final JSON configuration")
    
    # Mock example output structure
    example_output = {
        "fidgetInstanceDatums": {
            "fidget:welcome": {
                "config": {
                    "editable": True,
                    "settings": {
                        "title": "Welcome Dog Lovers!",
                        "text": "Join our community of dog enthusiasts!",
                        "fontColor": "var(--user-theme-font-color)"
                    },
                    "data": {}
                },
                "fidgetType": "text",
                "id": "fidget:welcome"
            },
            "fidget:feed": {
                "config": {
                    "editable": True,
                    "settings": {
                        "feedType": "farcaster",
                        "feedFilter": "dogs",
                        "title": "Dog Community Feed"
                    },
                    "data": {}
                },
                "fidgetType": "feed", 
                "id": "fidget:feed"
            }
        },
        "layoutDetails": {
            "layoutFidget": "grid",
            "layoutConfig": {
                "layout": [
                    {
                        "i": "fidget:welcome",
                        "x": 0,
                        "y": 0,
                        "w": 6,
                        "h": 2,
                        "minW": 3,
                        "maxW": 36,
                        "minH": 2,
                        "maxH": 36,
                        "moved": False,
                        "static": False
                    },
                    {
                        "i": "fidget:feed",
                        "x": 6,
                        "y": 0,
                        "w": 6,
                        "h": 4,
                        "minW": 4,
                        "maxW": 36,
                        "minH": 2,
                        "maxH": 36,
                        "moved": False,
                        "static": False
                    }
                ]
            }
        },
        "theme": {
            "id": "default-theme",
            "name": "Dog Community Theme",
            "properties": {
                "font": "Inter",
                "fontColor": "#ffffff",
                "background": "linear-gradient(45deg, #2d1b69 0%, #11253d 50%, #0f3460 100%)"
            }
        }
    }
    
    print(f"\n✅ Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    
    print("\n🚀 To run the full system:")
    print("1. Install dependencies: pip install -r requirements.txt")  
    print("2. Set up API keys in .env file")
    print("3. Run: python main.py")


def main():
    """Main entry point."""
    # Load .env file if it exists
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Check if we have dependencies installed
    try:
        import langchain
        import langgraph
        from main import create_space
        
        print("✅ Full dependencies available - running complete system")
        
        if not check_environment():
            return
            
        # Run the actual system
        import asyncio
        
        example_request = (
            "Create a space for a community of dog lovers who are active on Farcaster "
            "and interested in dog training, sharing photos of their pets, and connecting "
            "with other dog enthusiasts."
        )
        
        result = asyncio.run(create_space(example_request))
        print(f"\n✅ Generated {len(result)} workflow steps")
        
    except ImportError:
        print("⚠️  Some dependencies not installed - running demo mode")
        simple_demo()


if __name__ == "__main__":
    main()
