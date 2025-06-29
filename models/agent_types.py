"""
Pydantic models for agent data structures and space configuration.
"""

from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import BaseModel, Field
from enum import Enum


class FidgetType(str, Enum):
    """Valid fidget types for validation."""
    TEXT = "text"
    GALLERY = "gallery" 
    VIDEO = "Video"
    FEED = "feed"
    CAST = "cast"
    CHAT = "Chat"
    IFRAME = "iframe"
    LINKS = "links"
    RSS = "Rss"
    SWAP = "Swap"
    PORTFOLIO = "Portfolio"
    MARKET = "Market"
    GOVERNANCE = "governance"
    SNAPSHOT = "SnapShot"
    FRAME = "frame"
    FRAMES_V2 = "FramesV2"


class FidgetMinSize(BaseModel):
    """Minimum size requirements for a fidget type."""
    width: int = Field(..., ge=1, le=12)
    height: int = Field(..., ge=1, le=8)


# Minimum size requirements for each fidget type
FIDGET_MIN_SIZES: Dict[FidgetType, FidgetMinSize] = {
    FidgetType.TEXT: FidgetMinSize(width=3, height=2),
    FidgetType.GALLERY: FidgetMinSize(width=2, height=2),
    FidgetType.VIDEO: FidgetMinSize(width=2, height=2),
    FidgetType.FEED: FidgetMinSize(width=4, height=2),
    FidgetType.CAST: FidgetMinSize(width=3, height=1),
    FidgetType.CHAT: FidgetMinSize(width=3, height=2),
    FidgetType.IFRAME: FidgetMinSize(width=2, height=2),
    FidgetType.LINKS: FidgetMinSize(width=2, height=2),
    FidgetType.RSS: FidgetMinSize(width=3, height=2),
    FidgetType.SWAP: FidgetMinSize(width=3, height=3),
    FidgetType.PORTFOLIO: FidgetMinSize(width=3, height=3),
    FidgetType.MARKET: FidgetMinSize(width=3, height=2),
    FidgetType.GOVERNANCE: FidgetMinSize(width=4, height=3),
    FidgetType.SNAPSHOT: FidgetMinSize(width=4, height=3),
    FidgetType.FRAME: FidgetMinSize(width=2, height=2),
    FidgetType.FRAMES_V2: FidgetMinSize(width=2, height=2),
}


class SocialAccounts(BaseModel):
    """Social media accounts for a community."""
    farcaster: List[str] = Field(default_factory=list, description="Farcaster usernames")
    twitter: List[str] = Field(default_factory=list, description="Twitter handles")


class RelevantLink(BaseModel):
    """A relevant link with metadata."""
    title: str = Field(..., description="Title of the link")
    url: str = Field(..., description="URL of the link")
    type: Literal["official", "resource", "community"] = Field(..., description="Type of link")


class ContentSuggestion(BaseModel):
    """Content suggestion for a fidget."""
    type: str = Field(..., description="Type of content/fidget")
    source: Optional[str] = Field(None, description="Content source")
    filter: Optional[str] = Field(None, description="Content filter")
    value: Optional[str] = Field(None, description="Content value")
    purpose: Optional[str] = Field(None, description="Purpose of the content")
    content: Optional[str] = Field(None, description="Actual content")


class Colors(BaseModel):
    """Color scheme for the space."""
    primary: str = Field(..., description="Primary color (hex code)")
    secondary: str = Field(..., description="Secondary color (hex code)")


class ResearchData(BaseModel):
    """Research data gathered by the researcher agent."""
    summary: str = Field(..., description="Brief 2-3 sentence summary")
    key_topics: List[str] = Field(..., alias="keyTopics", description="Key topics related to the community")
    social_accounts: SocialAccounts = Field(..., alias="socialAccounts")
    relevant_links: List[RelevantLink] = Field(..., alias="relevantLinks")
    content_suggestions: List[ContentSuggestion] = Field(..., alias="contentSuggestions")
    colors: Colors = Field(..., description="Suggested color scheme")

    class Config:
        populate_by_name = True


class FidgetPosition(BaseModel):
    """Position and size of a fidget in the grid."""
    x: int = Field(..., ge=0, lt=12, description="X position in grid")
    y: int = Field(..., ge=0, lt=8, description="Y position in grid")
    width: int = Field(..., ge=1, le=12, description="Width in grid units")
    height: int = Field(..., ge=1, le=8, description="Height in grid units")


class FidgetDesign(BaseModel):
    """Design specification for a fidget."""
    id: str = Field(..., description="Unique fidget identifier")
    type: FidgetType = Field(..., description="Type of fidget")
    position: FidgetPosition = Field(..., description="Position in grid")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Fidget-specific settings")


class DesignPlan(BaseModel):
    """Design plan output from the designer agent."""
    fidgets: List[FidgetDesign] = Field(..., description="List of fidgets to place")
    grid_layout: List[List[Optional[str]]] = Field(..., alias="gridLayout", description="2D grid layout matrix")
    rationale: str = Field(..., description="Explanation of design choices")

    class Config:
        populate_by_name = True


class FidgetSpec(BaseModel):
    """Specification for a fidget in the matrix design."""
    id: str = Field(..., description="Unique fidget identifier")
    type: FidgetType = Field(..., description="Type of fidget")
    purpose: str = Field(..., description="Purpose of this fidget")
    priority: Literal["high", "medium", "low"] = Field(..., description="Priority level")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Fidget-specific settings")


class DesignMatrix(BaseModel):
    """Matrix-based design plan for improved performance."""
    width: int = Field(12, description="Grid width (always 12)")
    height: int = Field(8, description="Grid height (always 8)")
    cells: List[List[Optional[str]]] = Field(..., description="Matrix where each cell contains fidget ID or null")
    fidgets: List[FidgetSpec] = Field(..., description="List of fidgets with their types and settings")
    rationale: str = Field(..., description="Explanation of design choices")


class FidgetConfig(BaseModel):
    """Configuration for a fidget instance."""
    editable: bool = Field(True, description="Whether the fidget is editable")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Fidget-specific settings")
    data: Dict[str, Any] = Field(default_factory=dict, description="Fidget data")


class FidgetInstanceDatum(BaseModel):
    """A complete fidget instance in the space configuration."""
    config: FidgetConfig = Field(..., description="Fidget configuration")
    fidget_type: str = Field(..., alias="fidgetType", description="Type of fidget")
    id: str = Field(..., description="Unique fidget identifier")

    class Config:
        populate_by_name = True


class LayoutItem(BaseModel):
    """Layout item for the grid layout."""
    i: str = Field(..., description="Item identifier")
    x: int = Field(..., ge=0, description="X position")
    y: int = Field(..., ge=0, description="Y position")
    w: int = Field(..., ge=1, description="Width")
    h: int = Field(..., ge=1, description="Height")
    min_w: int = Field(..., alias="minW", description="Minimum width")
    max_w: int = Field(36, alias="maxW", description="Maximum width")
    min_h: int = Field(..., alias="minH", description="Minimum height")
    max_h: int = Field(36, alias="maxH", description="Maximum height")
    moved: bool = Field(False, description="Whether item has been moved")
    static: bool = Field(False, description="Whether item is static")

    class Config:
        populate_by_name = True


class LayoutConfig(BaseModel):
    """Layout configuration for the space."""
    layout: List[LayoutItem] = Field(..., description="List of layout items")


class LayoutDetails(BaseModel):
    """Layout details for the space."""
    layout_fidget: str = Field("grid", alias="layoutFidget", description="Type of layout")
    layout_config: LayoutConfig = Field(..., alias="layoutConfig", description="Layout configuration")

    class Config:
        populate_by_name = True


class ThemeProperties(BaseModel):
    """Theme properties for the space."""
    font: str = Field("Inter", description="Primary font")
    font_color: str = Field("#ffffff", alias="fontColor", description="Font color")
    headings_font: str = Field("Roboto", alias="headingsFont", description="Headings font")
    headings_font_color: str = Field("#00ffff", alias="headingsFontColor", description="Headings font color")
    background: str = Field(
        "linear-gradient(45deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)", 
        description="Background CSS"
    )
    background_html: str = Field("", alias="backgroundHTML", description="Background HTML")
    music_url: str = Field("", alias="musicURL", description="Background music URL")
    fidget_background: str = Field(
        "rgba(30, 100, 150, 0.95)", 
        alias="fidgetBackground", 
        description="Fidget background"
    )
    fidget_border_width: str = Field("1px", alias="fidgetBorderWidth", description="Fidget border width")
    fidget_border_color: str = Field("#00ffff", alias="fidgetBorderColor", description="Fidget border color")
    fidget_shadow: str = Field(
        "0 0 20px rgba(0, 255, 255, 0.5)", 
        alias="fidgetShadow", 
        description="Fidget shadow"
    )
    fidget_border_radius: str = Field("12px", alias="fidgetBorderRadius", description="Fidget border radius")
    grid_spacing: str = Field("16", alias="gridSpacing", description="Grid spacing")

    class Config:
        populate_by_name = True


class Theme(BaseModel):
    """Theme configuration for the space."""
    id: str = Field("default-theme", description="Theme identifier")
    name: str = Field("Default Theme", description="Theme name")
    properties: ThemeProperties = Field(..., description="Theme properties")


class SpaceConfig(BaseModel):
    """Complete space configuration."""
    fidget_instance_datums: Dict[str, FidgetInstanceDatum] = Field(
        ..., 
        alias="fidgetInstanceDatums", 
        description="Map of fidget instances"
    )
    layout_id: str = Field(..., alias="layoutID", description="Layout identifier")
    layout_details: LayoutDetails = Field(..., alias="layoutDetails", description="Layout details")
    is_editable: bool = Field(True, alias="isEditable", description="Whether space is editable")
    fidget_tray_contents: List[Any] = Field(
        default_factory=list, 
        alias="fidgetTrayContents", 
        description="Fidget tray contents"
    )
    theme: Theme = Field(..., description="Theme configuration")

    class Config:
        populate_by_name = True


# Type aliases for backward compatibility
SpaceConfigList = List[FidgetInstanceDatum]
