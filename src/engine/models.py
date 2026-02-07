from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class Outcome(BaseModel):
    name: str
    probability: float = Field(..., ge=0, le=1.0)
    value: float

class StrategyNode(BaseModel):
    name: str
    node_type: str = "chance"  # "decision" or "chance"
    # The | operator replaces Union
    children: List[StrategyNode | Outcome] = Field(default_factory=list)
    expected_value: Optional[float] = None
    probability: float = 1.0  # Default for root or nested nodes