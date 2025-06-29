# Python Space Agents - Quick Start Guide

## 🚀 Quick Start

### Option 1: Full Automated Setup
```bash
cd python-space-agents
./start.sh
```

### Option 2: Manual Setup
```bash
cd python-space-agents

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

### Option 3: Demo Mode (No Dependencies)
```bash
cd python-space-agents
python run.py
```

## 📋 Required API Keys

1. **OpenAI API Key** (Required)
   - Get from: https://platform.openai.com/api-keys
   - Set in .env: `OPENAI_API_KEY=sk-...`

2. **Tavily API Key** (Required for research)
   - Get from: https://tavily.com/
   - Set in .env: `TAVILY_API_KEY=tvly-...`

3. **LangSmith API Key** (Optional - for monitoring)
   - Get from: https://smith.langchain.com/
   - Set in .env: `LANGCHAIN_API_KEY=ls__...`

## 🎯 Usage Examples

### Basic Usage
```python
from main import create_space

result = await create_space(
    "Create a space for crypto traders sharing market analysis"
)
```

### Custom Request Examples
```python
# NFT Community
await create_space(
    "Build a space for NFT collectors with galleries, marketplace feeds, and trading discussions"
)

# Developer Community  
await create_space(
    "Create a developer community space with code sharing, job postings, and technical discussions"
)

# Gaming Community
await create_space(
    "Design a gaming community with tournament feeds, leaderboards, and strategy guides"
)
```

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🔍 Researcher  │───▶│   🎨 Designer   │───▶│   ⚙️ Builder    │
│                 │    │                 │    │                 │
│ • Tavily Search │    │ • Grid Layout   │    │ • JSON Config   │
│ • Social Accounts│    │ • Fidget Types  │    │ • Validation    │
│ • Key Topics    │    │ • Size Rules    │    │ • Final Output  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎨 Available Fidgets

| Type | Min Size | Purpose |
|------|----------|---------|
| `text` | 3×2 | Welcome messages, announcements |
| `feed` | 4×2 | Social media feeds (Farcaster/X) |
| `gallery` | 2×2 | Images, NFTs, visual content |
| `cast` | 3×1 | Individual Farcaster posts |
| `Chat` | 3×2 | Real-time messaging |
| `links` | 2×2 | Link collections |
| `Video` | 2×2 | YouTube/Vimeo embeds |
| `Rss` | 3×2 | RSS feed readers |
| `Swap` | 3×3 | Token trading widgets |
| `Portfolio` | 3×3 | Crypto portfolio tracking |
| `Market` | 3×2 | Market data displays |
| `governance` | 4×3 | DAO proposals/voting |
| `SnapShot` | 4×3 | Snapshot governance |
| `iframe` | 2×2 | External website embeds |
| `frame` | 2×2 | Frame widgets |
| `FramesV2` | 2×2 | Enhanced frame widgets |

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agents.py::TestResearchData

# Run with verbose output
python -m pytest tests/ -v
```

## 🔧 Development

### Code Formatting
```bash
# Format code
black .
isort .

# Type checking  
mypy .
```

### Project Structure
```
python-space-agents/
├── agents/           # Agent implementations
├── models/           # Pydantic data models
├── tools/            # Validation & conversion tools
├── utils/            # Pretty printing utilities
├── tests/            # Test suite
├── main.py           # Main application
├── run.py            # Demo runner
└── requirements.txt  # Dependencies
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   source venv/bin/activate  # Make sure venv is active
   ```

2. **API Key Errors**
   ```bash
   # Check .env file exists and has correct keys
   cat .env
   ```

3. **Permission Errors**
   ```bash
   chmod +x start.sh
   ```

### Debug Mode
```python
# Enable debug logging
import os
os.environ["LOG_LEVEL"] = "DEBUG"
```

## 📊 Performance Tips

1. **Token Limits**: Adjust `MAX_TOKENS` in .env for larger/smaller outputs
2. **Temperature**: Lower values (0.1) for consistent results
3. **Grid Coverage**: Aim for 70%+ grid utilization for best layouts
4. **Validation**: Always validate outputs with built-in tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Format code: `black . && isort .`
5. Run tests: `pytest`
6. Submit pull request

## 📝 License

This project is part of the Nounspace ecosystem. See the main repository for license details.

---

🎉 **Happy Building!** Create amazing spaces for your communities!
