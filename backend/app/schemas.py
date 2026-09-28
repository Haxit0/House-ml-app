from pydantic import BaseModel, Field


class HouseInput(BaseModel):
    area_sqft: float = Field(..., gt=0)
    bedrooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    location_score: float = Field(..., ge=1, le=10)
    age_years: int = Field(..., ge=0)


class PredictionResponse(BaseModel):
    predicted_price: float


class FeedbackInput(HouseInput):
    actual_price: float = Field(..., gt=0)
    predicted_price: float = Field(..., gt=0)
