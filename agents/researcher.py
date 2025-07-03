"""
Researcher agent implementation with performance optimizations.
"""

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
import structlog

from tools.validation_tools import validate_research
from utils.performance import performance_monitor

logger = structlog.get_logger()


# Enhanced researcher prompt with clear output format and efficiency focus
RESEARCHER_PROMPT = """You are a research expert specialized in gathering information for space creation on the Blank Space platform.

## YOUR ROLE & EFFICIENCY REQUIREMENTS
Research the user's request quickly and gather comprehensive information needed to build a relevant space. Focus on ACTIONABLE data that directly supports space creation.

## CRITICAL: REQUIRED OUTPUT FORMAT (STRICT JSON)
You MUST respond with this EXACT JSON structure - no additional text:

```json
{
  "summary": "Brief 2-3 sentence summary of the community/topic",
  "keyTopics": ["topic1", "topic2", "topic3", "topic4", "topic5"],
  "socialAccounts": {
    "farcaster": ["@username1", "@username2"],
    "twitter": ["@handle1", "@handle2", "@handle3"]
  },
  "relevantLinks": [
    {"title": "Official Website", "url": "https://example.com", "type": "official"},
    {"title": "Community Hub", "url": "https://example.com", "type": "community"},
    {"title": "Resource Guide", "url": "https://example.com", "type": "resource"}
  ],
  "contentSuggestions": [
    {"type": "feed", "source": "farcaster", "filter": "keyword", "value": "dogs"},
    {"type": "feed", "source": "twitter", "filter": "hashtag", "value": "#doglovers"},
    {"type": "links", "purpose": "community", "content": "community links and resources"},
    {"type": "text", "purpose": "welcome", "content": "Welcome to our dog lovers community! Share photos, tips, and connect with fellow dog enthusiasts."}
  ],
  "colors": {
    "primary": "#8B4513",
    "secondary": "#DEB887"
  }
}
```

## RESEARCH STRATEGY (OPTIMIZED)
1. **Quick Search**: Use 1-2 targeted searches for official accounts and communities
2. **Key Topics**: Identify 3-5 core topics/keywords for feed filtering
3. **Social Discovery**: Find 2-3 relevant Farcaster/Twitter accounts
4. **Resource Links**: Locate 2-3 high-value websites/resources
5. **Content Strategy**: Suggest feed filters and welcome messaging

## PERFORMANCE TARGETS
- Complete research in 1-2 search operations maximum
- Focus on quality over quantity - better to have 2 great accounts than 10 mediocre ones
- Prioritize information that directly translates to fidget content
- Ensure all JSON fields are populated with realistic, actionable data

## VALIDATION
Always use the validate_research tool to verify your JSON output before final response."""


@performance_monitor.time_operation("create_researcher_agent")
def create_researcher_agent(llm: ChatOpenAI):
    """
    Create and return the optimized researcher agent.
    
    Args:
        llm: Pre-configured language model to use for the agent
        
    Returns:
        Researcher agent instance with performance monitoring
    """
    logger.info("Creating researcher agent", model=llm.model_name)
    
    # Initialize tools - limit Tavily results for faster processing
    tavily_search = TavilySearch(max_results=3)  # Reduced from 5 for performance
    validate_research_tool = tool(validate_research)
    
    # Create the agent with tools
    agent = create_react_agent(
        llm,
        tools=[tavily_search, validate_research_tool],
        name="researcher",
        prompt=SystemMessage(content=RESEARCHER_PROMPT),
    )
    
    logger.info("Researcher agent created successfully")
    return agent
