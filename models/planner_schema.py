from pydantic import BaseModel, Field
from typing import List, Dict

class Fidget(BaseModel):
    id: str
    type: str
    title: str
    config: Dict

class PlannerOutput(BaseModel):
    fidgets: List[Fidget]
