from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class FidgetRequest(BaseModel):
    type: str
    platform: Optional[str] = None

class IntentSchema(BaseModel):
    intent: str  # Allow "image_search"
    subject: Optional[str]
    query: Optional[str] = None
    max_results: Optional[int] = 5
    min_quality_score: Optional[float] = 80.0
    min_resolution: Optional[List[int]] = [1024, 768]
    fidget_requests: List[FidgetRequest] = Field(default_factory=list)
    theme_hints: dict = Field(default_factory=dict)
    requested_changes: Optional[dict] = None