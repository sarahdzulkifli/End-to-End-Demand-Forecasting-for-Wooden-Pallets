from pydantic import BaseModel, Field
from typing import Optional

class PredictionRequest(BaseModel):
    """Request schema for predictions."""
    periods: int = Field(default=6, ge=1, le=12, description="Number of months to forecast")
    last_quantity: float = Field(..., description="Last known quantity")
    current_month: int = Field(..., ge=1, le=12, description="Current month")
    rate: Optional[float] = Field(default=0.0, description="Current rate")
    freight_cost: Optional[float] = Field(default=0.0, description="Freight cost")

class PredictionResponse(BaseModel):
    """Response schema for predictions."""
    date: str
    predicted_quantity: float
    model: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str
    version: str