"""
Centralized LLM configuration and factory for performance optimization.
"""

from typing import Optional, Dict, Any
from functools import lru_cache
from langchain_openai import ChatOpenAI
import structlog

from config.app_config import get_config

logger = structlog.get_logger()


class LLMConfig:
    """Centralized LLM configuration management."""
    
    # Temperature settings by agent type (optimized for performance vs quality)
    AGENT_TEMPERATURES = {
        "researcher": 0.3,    # Some creativity for finding diverse sources
        "designer": 0.1,      # Low for consistent layout decisions
        "builder": 0.05,      # Very low for JSON accuracy
        "supervisor": 0.1,    # Low for consistent routing
    }
    
    # Token limits by agent type
    AGENT_TOKEN_LIMITS = {
        "researcher": 2000,   # Moderate - structured research output
        "designer": 3000,     # Higher - complex matrix descriptions
        "builder": 4000,      # Highest - complete JSON configs
        "supervisor": 1000,   # Lowest - simple routing decisions
    }
    
    # Performance optimization settings
    PERFORMANCE_SETTINGS = {
        "request_timeout": None,  # Will be set from config
        "max_retries": None,      # Will be set from config  
        "streaming": False,       # Disable for better caching
    }
    
    @classmethod
    def get_performance_settings(cls) -> Dict[str, Any]:
        """Get performance settings from app config."""
        config = get_config()
        return {
            "request_timeout": config.performance.request_timeout,
            "max_retries": config.performance.max_retries,
            "streaming": False,
        }


@lru_cache(maxsize=8)
def get_llm_instance(agent_type: str) -> ChatOpenAI:
    """
    Get a cached LLM instance for the specified agent type.
    
    Args:
        agent_type: Type of agent (researcher, designer, builder, supervisor)
        
    Returns:
        Configured ChatOpenAI instance
    """
    config = get_config()
    
    # Get model from configuration
    model = config.get_model_for_agent(agent_type)
    temperature = LLMConfig.AGENT_TEMPERATURES.get(agent_type, 0.1)
    max_tokens = LLMConfig.AGENT_TOKEN_LIMITS.get(agent_type, 2000)
    
    logger.info(
        "Creating LLM instance",
        agent_type=agent_type,
        model=model,
        temperature=temperature,
        tier=config.models.tier.value
    )
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        **LLMConfig.get_performance_settings()
    )


def get_optimized_llm(agent_type: str, custom_config: Optional[Dict[str, Any]] = None) -> ChatOpenAI:
    """
    Get an optimized LLM instance with optional custom configuration.
    
    Args:
        agent_type: Type of agent
        custom_config: Optional custom configuration overrides
        
    Returns:
        Configured ChatOpenAI instance
    """
    if custom_config:
        # Create a new instance for custom configs (don't cache)
        config = get_config()
        
        base_settings = {
            "model": config.get_model_for_agent(agent_type),
            "temperature": LLMConfig.AGENT_TEMPERATURES.get(agent_type, 0.1),
            "max_completion_tokens": LLMConfig.AGENT_TOKEN_LIMITS.get(agent_type, 2000),
            **LLMConfig.get_performance_settings()
        }
        
        # Override with custom config
        merged_config = {**base_settings, **custom_config}
        
        return ChatOpenAI(**merged_config)
    
    return get_llm_instance(agent_type)


def clear_llm_cache():
    """Clear the LLM instance cache."""
    get_llm_instance.cache_clear()
    logger.info("LLM cache cleared")


def get_llm_stats() -> Dict[str, Any]:
    """Get LLM cache statistics."""
    cache_info = get_llm_instance.cache_info()
    config = get_config()
    
    return {
        "cache_hits": cache_info.hits,
        "cache_misses": cache_info.misses,
        "cache_size": cache_info.currsize,
        "max_cache_size": cache_info.maxsize,
        "hit_rate": cache_info.hits / (cache_info.hits + cache_info.misses) * 100 
                   if (cache_info.hits + cache_info.misses) > 0 else 0,
        "current_tier": config.models.tier.value,
        "caching_enabled": config.performance.enable_caching
    }
