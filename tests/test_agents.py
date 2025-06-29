"""
Test suite for the Python Space Agents system.
"""

import pytest
import json
from unittest.mock import Mock, patch

from models.agent_types import (
    ResearchData,
    DesignMatrix,
    FidgetType,
    FidgetSpec,
    Colors,
    SocialAccounts,
)


class TestResearchData:
    """Test cases for ResearchData model."""
    
    def test_research_data_creation(self):
        """Test creating a valid ResearchData instance."""
        data = {
            "summary": "A community for dog lovers sharing photos and tips.",
            "keyTopics": ["dogs", "training", "photos"],
            "socialAccounts": {
                "farcaster": ["@doglovers"],
                "twitter": ["@dogcommunity"]
            },
            "relevantLinks": [
                {
                    "title": "Dog Training Guide",
                    "url": "https://example.com/training",
                    "type": "resource"
                }
            ],
            "contentSuggestions": [
                {
                    "type": "feed",
                    "source": "farcaster", 
                    "filter": "keyword",
                    "value": "dogs"
                }
            ],
            "colors": {
                "primary": "#ff0000",
                "secondary": "#00ff00"
            }
        }
        
        research = ResearchData(**data)
        assert research.summary == "A community for dog lovers sharing photos and tips."
        assert len(research.key_topics) == 3
        assert research.colors.primary == "#ff0000"


class TestDesignMatrix:
    """Test cases for DesignMatrix model."""
    
    def test_design_matrix_creation(self):
        """Test creating a valid DesignMatrix instance."""
        data = {
            "width": 12,
            "height": 8,
            "cells": [
                ["welcome", "welcome", "welcome", None, None, None, None, None, None, None, None, None],
                ["welcome", "welcome", "welcome", None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
            ],
            "fidgets": [
                {
                    "id": "welcome",
                    "type": "text",
                    "purpose": "Welcome message",
                    "priority": "high",
                    "settings": {
                        "title": "Welcome",
                        "text": "Hello!"
                    }
                }
            ],
            "rationale": "Simple welcome message layout"
        }
        
        matrix = DesignMatrix(**data)
        assert matrix.width == 12
        assert matrix.height == 8
        assert len(matrix.fidgets) == 1
        assert matrix.fidgets[0].type == FidgetType.TEXT


@pytest.mark.asyncio
class TestValidationTools:
    """Test cases for validation tools."""
    
    def test_validate_research_valid_data(self):
        """Test validation with valid research data."""
        from tools.validation_tools import validate_research
        
        valid_data = {
            "summary": "A community for dog lovers sharing photos and tips.",
            "keyTopics": ["dogs", "training"],
            "socialAccounts": {
                "farcaster": ["@doglovers"],
                "twitter": ["@dogcommunity"]
            },
            "relevantLinks": [
                {
                    "title": "Dog Training Guide",
                    "url": "https://example.com/training",
                    "type": "resource"
                }
            ],
            "contentSuggestions": [
                {
                    "type": "feed",
                    "source": "farcaster"
                }
            ],
            "colors": {
                "primary": "#ff0000",
                "secondary": "#00ff00"
            }
        }
        
        result = validate_research.invoke({"data": json.dumps(valid_data)})
        assert "✅" in result
        assert "valid and properly formatted" in result
    
    def test_validate_research_invalid_json(self):
        """Test validation with invalid JSON."""
        from tools.validation_tools import validate_research
        
        result = validate_research.invoke({"data": "invalid json"})
        assert "❌" in result
        assert "Invalid JSON format" in result


class TestConversionTools:
    """Test cases for conversion tools."""
    
    def test_convert_matrix_to_config(self):
        """Test matrix to configuration conversion."""
        from tools.conversion_tools import convert_matrix_to_config
        
        matrix_data = {
            "width": 12,
            "height": 8,
            "cells": [
                ["welcome", "welcome", "welcome", None, None, None, None, None, None, None, None, None],
                ["welcome", "welcome", "welcome", None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
            ],
            "fidgets": [
                {
                    "id": "welcome",
                    "type": "text",
                    "purpose": "Welcome message",
                    "priority": "high",
                    "settings": {
                        "title": "Welcome",
                        "text": "Hello!"
                    }
                }
            ],
            "rationale": "Simple welcome message layout"
        }
        
        result = convert_matrix_to_config.invoke({"data": json.dumps(matrix_data)})
        assert "✅" in result
        assert "Configuration generated successfully" in result
        assert "fidgetInstanceDatums" in result


if __name__ == "__main__":
    pytest.main([__file__])
