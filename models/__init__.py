"""
Init file for models package.
"""

from .agent_types import (
    FidgetType,
    FidgetMinSize,
    FIDGET_MIN_SIZES,
    SocialAccounts,
    RelevantLink,
    ContentSuggestion,
    Colors,
    ResearchData,
    FidgetPosition,
    FidgetDesign,
    DesignPlan,
    FidgetSpec,
    DesignMatrix,
    FidgetConfig,
    FidgetInstanceDatum,
    LayoutItem,
    LayoutConfig,
    LayoutDetails,
    ThemeProperties,
    Theme,
    SpaceConfig,
    SpaceConfigList,
)

import os
from models.agent_types import AGENT_MODELS

def load_model_settings():
    for agent, config in AGENT_MODELS.items():
        provider = config["provider"]
        if provider == "openai":
            config["api_key"] = os.getenv("OPENAI_API_KEY", "")
            config["base_url"] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        elif provider == "anthropic":
            config["api_key"] = os.getenv("ANTHROPIC_API_KEY", "")
            config["base_url"] = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1/")
        elif provider == "venice":
            config["api_key"] = os.getenv("VENICE_API_KEY", "")
            config["base_url"] = os.getenv("VENICE_BASE_URL", "https://api.venice.ai/api/v1")


__all__ = [
    "FidgetType",
    "FidgetMinSize", 
    "FIDGET_MIN_SIZES",
    "SocialAccounts",
    "RelevantLink",
    "ContentSuggestion",
    "Colors",
    "ResearchData",
    "FidgetPosition",
    "FidgetDesign",
    "DesignPlan",
    "FidgetSpec",
    "DesignMatrix",
    "FidgetConfig",
    "FidgetInstanceDatum",
    "LayoutItem",
    "LayoutConfig",
    "LayoutDetails",
    "ThemeProperties",
    "Theme",
    "SpaceConfig",
    "SpaceConfigList",
]
