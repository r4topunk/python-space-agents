#!/usr/bin/env python3
"""
Setup and installation script for Python Space Agents.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def setup_environment():
    """Set up environment configuration."""
    print("🔧 Setting up environment...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        # Copy example to .env
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from .env.example")
        print("📝 Please edit .env file with your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example file found")


def validate_setup():
    """Validate the setup by running basic imports."""
    print("🧪 Validating setup...")
    
    try:
        # Test imports
        import langchain
        import langchain_openai
        import langgraph
        import pydantic
        print("✅ Core dependencies imported successfully")
        
        # Test models
        from models.agent_types import FidgetType, ResearchData
        print("✅ Models imported successfully")
        
        # Test tools
        from tools.validation_tools import validate_research
        print("✅ Tools imported successfully")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Try running: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🚀 Setting up Python Space Agents...")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    setup_environment()
    
    if validate_setup():
        print("=" * 50)
        print("✅ Setup completed successfully!")
        print("\n📚 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python main.py")
        print("3. Or run the example: python example.py")
        print("\n🧪 Run tests with: python -m pytest tests/")
    else:
        print("❌ Setup validation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
