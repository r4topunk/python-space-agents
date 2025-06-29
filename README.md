# Python Space Agents V2 - High-Performance Blank Space Builder

A sophisticated multi-agent system for automatically generating space configurations for the Blank Space platform using Python LangChain and OpenAI.

## 🏗️ Architecture

The system uses a **supervised multi-agent architecture** with three specialized agents:

1. **🔍 Researcher Agent**: Gathers comprehensive information about the requested community/topic
2. **🎨 Designer Agent**: Creates optimal grid layouts using available fidgets (widgets)  
3. **⚙️ Builder Agent**: Generates final JSON configuration for the space

## 🚀 Key Improvements (Python Best Practices Applied)

### 1. **Structured Output Formats**
- All agents use **strict Pydantic models** for consistent data exchange
- Clear input/output specifications reduce hallucinations
- Validation tools ensure data quality at each step

### 2. **Optimized Prompts**
- **Token-efficient** prompts with essential information only
- **Specific constraints** and validation rules
- **Clear examples** and templates for each agent
- **Consistent terminology** across all agents

### 3. **Type Safety & Validation**
- Full Python type hints and Pydantic model definitions
- Runtime validation tools for each agent's output
- Fidget size constraints and type validation
- Unique ID enforcement

### 4. **Performance Optimizations**
- Lower temperature (0.1) for consistent structured output
- Maximum token limits to prevent runaway generation
- Efficient prompt structure with minimal redundancy
- Parallel validation where possible

### 5. **Error Handling**
- Comprehensive error catching and reporting
- Validation at each agent handoff
- Clear error messages for debugging
- Graceful failure handling

## 📁 Project Structure

```
python-space-agents/
├── agents/
│   ├── __init__.py
│   ├── researcher.py        # Research agent implementation
│   ├── designer.py          # Design agent implementation
│   ├── builder.py           # Builder agent implementation
│   └── supervisor.py        # Supervisor workflow
├── models/
│   ├── __init__.py
│   ├── agent_types.py       # Pydantic model definitions
│   └── fidget_types.py      # Fidget configuration models
├── tools/
│   ├── __init__.py
│   ├── validation_tools.py  # Validation utilities
│   └── conversion_tools.py  # Matrix conversion tools
├── utils/
│   ├── __init__.py
│   └── pretty_print.py      # Output formatting
├── main.py                  # Main execution script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Usage

```python
from main import create_space

# Create a space with a descriptive request
result = await create_space(
    "Create a space for dog lovers who share photos and training tips"
)
```

## 🔧 Agent Specifications

### Researcher Agent
- **Input**: User request (natural language)
- **Output**: Structured Pydantic model with research findings
- **Tools**: TavilySearch, validation
- **Focus**: Social accounts, keywords, resources, color schemes

### Designer Agent  
- **Input**: Research data Pydantic model
- **Output**: Layout plan with fidget positioning
- **Tools**: Design validation
- **Focus**: Grid layout, fidget selection, user experience

### Builder Agent
- **Input**: Design plan Pydantic model
- **Output**: Final space configuration JSON
- **Tools**: Configuration validation
- **Focus**: Proper JSON structure, settings validation

## 🎨 Available Fidgets

The system supports 16+ fidget types including:
- **Content**: text, gallery, Video, Rss
- **Social**: feed, cast, Chat, links  
- **Finance**: Swap, Portfolio, Market
- **Governance**: SnapShot, governance
- **Utility**: iframe, frame, FramesV2

Each fidget has specific minimum size requirements and configuration options.

## 🚀 Performance Features

- **Fast execution** with optimized prompts
- **Consistent results** through structured output
- **Error resilience** with validation at each step
- **Type safety** throughout the pipeline
- **Extensible architecture** for adding new fidgets

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📊 Example Output

The system generates a complete space configuration like:

```json
{
  "fidgetInstanceDatums": {
    "fidget:welcome": {
      "config": {
        "editable": true,
        "settings": {
          "title": "Welcome Dog Lovers!",
          "text": "Join our community of dog enthusiasts!"
        },
        "data": {}
      },
      "fidgetType": "text",
      "id": "fidget:welcome"
    }
  },
  "layoutDetails": {
    "layoutFidget": "grid",
    "layoutConfig": {
      "layout": [...]
    }
  }
}
```

This refactored Python system delivers **high-performance LLM interactions** with reliable, structured outputs for space generation on the Blank Space platform.

## Installation & Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
export OPENAI_API_KEY="your_openai_key"
export TAVILY_API_KEY="your_tavily_key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your_langsmith_key"  # Optional
```

3. Run the application:

```bash
python main.py
```

## 🌟 New Python Features

- **Async/await support** for better performance
- **Rich console output** with colored formatting
- **Comprehensive logging** with structured logs
- **Configuration management** with environment variables
- **Professional error handling** with custom exceptions
- **Unit tests** with pytest framework
- **Code formatting** with black and isort
- **Type checking** with mypy
