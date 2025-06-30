"""
Researcher agent implementation.
"""

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# from tools.validation_tools import validate_research
# from tools.image_tools import imageResearcher


# Researcher prompt
RESEARCHER_PROMPT = """You are a research expert specialized in gathering information for space creation on the Blank Space platform.

## YOUR ROLE
Research the user's request and gather comprehensive information needed to build a relevant space for their community or project.

## REQUIRED OUTPUT FORMAT
You MUST respond with a JSON object containing exactly these fields:
{
  "summary": "Brief 2-3 sentence summary of the community/topic",
  "keyTopics": ["topic1", "topic2", "topic3"],
  "socialAccounts": {
    "farcaster": ["@username1", "@username2"],
    "twitter": ["@handle1", "@handle2"]
  },
  "relevantLinks": [
    {"title": "Website Name", "url": "https://example.com", "type": "official"},
    {"title": "Resource Name", "url": "https://example.com", "type": "resource"}
  ],
  "contentSuggestions": [
    {"type": "feed", "source": "farcaster", "filter": "keyword", "value": "dogs"},
    {"type": "links", "purpose": "social", "content": "community links"},
    {"type": "text", "purpose": "welcome", "content": "welcome message"}
  ],
  "colors": {
    "primary": "#hex",
    "secondary": "#hex"
  }
}

## RESEARCH PRIORITIES
1. Find official social media accounts and communities
2. Identify key topics, hashtags, and keywords
3. Locate relevant websites, resources, and tools
4. Understand the community's interests and needs
5. Suggest appropriate content types for the space

Be thorough but concise. Focus on actionable information that will help create an engaging space for the Blank Space platform."""


def create_researcher_agent(llm: ChatOpenAI):
    """
    Create and return the researcher agent.
    
    Args:
        llm: Language model to use for the agent
        
    Returns:
        Researcher agent instance
    """
    # Initialize tools
    # image_researcher = tool(imageResearcher)
    # validate_research_tool = tool(validate_research)
    # rss_researcher = tool(rssResearcher)  # Ensure rssResearcher is defined
    # social_network_researcher = tool(socialNetworkResearcher)  # Ensure socialNetworkResearcher is defined
    
    # Create the agent with tools
    return create_react_agent(
        llm,
        tools=[
            # image_researcher, validate_research_tool, rss_researcher, social_network_researcher
            ],
        name="researcher",
        prompt=SystemMessage(content=RESEARCHER_PROMPT),  # Keep this line
        # prompt=SystemMessage(content=RESEARCHER_PROMPT),  # Remove this line
    )
