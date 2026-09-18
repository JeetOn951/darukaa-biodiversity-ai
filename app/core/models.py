from typing import Optional
from pydantic import BaseModel, Field

class EnvironmentalInput(BaseModel):
    soil_ph: Optional[float] = Field(None, ge=0, le=14)
    soil_organic_carbon_pct: Optional[float] = Field(None, ge=0)
    soil_moisture_pct: Optional[float] = Field(None, ge=0, le=100)
    rainfall_mm: Optional[float] = Field(None, ge=0)
    temperature_c: Optional[float] = None
    land_use: Optional[str] = None
    crop_system: Optional[str] = None
    biodiversity_indicator: Optional[str] = None
    pollution: Optional[str] = None
    deforestation: Optional[str] = None
    location: Optional[str] = None
    query: str = ""
