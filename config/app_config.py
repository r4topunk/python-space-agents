"""
Configuration management for the Python Space Agents system.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
import json
from dataclasses import dataclass, field, asdict
from enum import Enum


class LogLevel(str, Enum):
    """Available log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ModelTier(str, Enum):
    """Model performance tiers."""
    FAST = "fast"  # Use faster, cheaper models
    BALANCED = "balanced"  # Balance speed and quality
    QUALITY = "quality"  # Use best models for highest quality


@dataclass
class PerformanceConfig:
    """Performance-related configuration."""
    enable_caching: bool = True
    cache_dir: str = ".agent_cache"
    max_cache_size: int = 1000
    request_timeout: int = 60
    max_retries: int = 3
    parallel_requests: bool = False  # Future: enable parallel LLM calls


@dataclass
class ModelConfig:
    """Model configuration for different tiers."""
    tier: ModelTier = ModelTier.BALANCED
    
    def __post_init__(self):
        """Initialize model mappings."""
        # Model mappings by tier
        self.TIER_MODELS: Dict[ModelTier, Dict[str, str]] = {
            ModelTier.FAST: {
                "researcher": "gpt-4o-mini",
                "designer": "gpt-4o-mini", 
                "builder": "gpt-4o-mini",
                "supervisor": "gpt-4o-mini"
            },
            ModelTier.BALANCED: {
                "researcher": "gpt-4o-mini",
                "designer": "gpt-4o",
                "builder": "gpt-4o",
                "supervisor": "gpt-4o-mini"
            },
            ModelTier.QUALITY: {
                "researcher": "gpt-4o",
                "designer": "gpt-4o",
                "builder": "gpt-4o",
                "supervisor": "gpt-4o"
            }
        }
    
    def get_model_for_agent(self, agent_type: str) -> str:
        """Get the model name for a specific agent type."""
        if not hasattr(self, 'TIER_MODELS'):
            self.__post_init__()
        return self.TIER_MODELS[self.tier].get(agent_type, "gpt-4o-mini")


@dataclass
class ValidationConfig:
    """Validation configuration."""
    enable_strict_validation: bool = True
    min_grid_coverage: float = 0.75  # 75% minimum coverage
    max_validation_retries: int = 2
    enable_design_validation: bool = True
    enable_config_validation: bool = True


@dataclass
class AppConfig:
    """Main application configuration."""
    log_level: LogLevel = LogLevel.INFO
    environment: str = "production"
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    models: ModelConfig = field(default_factory=ModelConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    
    # API Configuration
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        # Override from environment
        log_level_env = os.getenv("LOG_LEVEL")
        if log_level_env:
            try:
                self.log_level = LogLevel(log_level_env.upper())
            except ValueError:
                pass
                
        model_tier_env = os.getenv("MODEL_TIER")
        if model_tier_env:
            try:
                self.models.tier = ModelTier(model_tier_env.lower())
            except ValueError:
                pass
                
        if os.getenv("ENVIRONMENT"):
            self.environment = os.getenv("ENVIRONMENT", "production")
            
        # Performance overrides
        enable_caching_env = os.getenv("ENABLE_CACHING")
        if enable_caching_env:
            self.performance.enable_caching = enable_caching_env.lower() == "true"
            
        min_coverage_env = os.getenv("MIN_GRID_COVERAGE")
        if min_coverage_env:
            try:
                self.validation.min_grid_coverage = float(min_coverage_env)
            except ValueError:
                pass
    
    @classmethod
    def load_from_file(cls, config_path: str) -> "AppConfig":
        """Load configuration from a JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            return cls()  # Return default config
            
        with config_file.open() as f:
            config_data = json.load(f)
            
        # Create config with nested objects
        config = cls()
        
        if "performance" in config_data:
            config.performance = PerformanceConfig(**config_data["performance"])
        if "models" in config_data:
            config.models = ModelConfig(**config_data["models"])
        if "validation" in config_data:
            config.validation = ValidationConfig(**config_data["validation"])
            
        # Update top-level fields
        for key, value in config_data.items():
            if key not in ["performance", "models", "validation"] and hasattr(config, key):
                setattr(config, key, value)
                
        return config
    
    def save_to_file(self, config_path: str):
        """Save configuration to a JSON file."""
        config_file = Path(config_path)
        config_file.parent.mkdir(exist_ok=True)
        
        with config_file.open("w") as f:
            json.dump(asdict(self), f, indent=2)
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment in ["development", "dev", "local"]
    
    def get_model_for_agent(self, agent_type: str) -> str:
        """Get the configured model for a specific agent."""
        return self.models.get_model_for_agent(agent_type)


# Global configuration instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load configuration from file or environment."""
    global config
    
    if config_path:
        config = AppConfig.load_from_file(config_path)
    else:
        # Look for config file in common locations
        for config_file in ["config.json", ".config.json", "config/app.json"]:
            if Path(config_file).exists():
                config = AppConfig.load_from_file(config_file)
                break
        else:
            # Use environment-based config
            config = AppConfig()
    
    return config


def create_example_config():
    """Create an example configuration file."""
    example_config = AppConfig(
        log_level=LogLevel.INFO,
        environment="development",
        performance=PerformanceConfig(
            enable_caching=True,
            cache_dir=".agent_cache",
            max_cache_size=1000,
            request_timeout=60
        ),
        models=ModelConfig(tier=ModelTier.BALANCED),
        validation=ValidationConfig(
            min_grid_coverage=0.75,
            enable_strict_validation=True
        )
    )
    
    example_config.save_to_file("config.example.json")
    print("📁 Example configuration saved to config.example.json")
    print("💡 Copy to config.json and modify as needed")


if __name__ == "__main__":
    create_example_config()
