from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class EnvironmentalInput(BaseModel):
    soil_ph: Optional[float] = Field(default=None, ge=0, le=14)
    soil_organic_carbon: Optional[float] = Field(default=None, ge=0)
    soil_moisture: Optional[float] = Field(default=None, ge=0)
    rainfall: Optional[str] = None
    rainfall_mm: Optional[float] = Field(default=None, ge=0)
    temperature_c: Optional[float] = None
    land_use: Optional[str] = None
    biodiversity: Optional[str] = None
    species_richness: Optional[float] = Field(default=None, ge=0)
    habitat_diversity: Optional[str] = None
    pollution: Optional[str] = None
    deforestation: Optional[str] = None
    region: Optional[str] = None
    crop: Optional[str] = None
    water_availability: Optional[str] = None

class Recommendation(BaseModel):
    action: str
    rationale: str
    impacted_metrics: List[str]
    time_horizon: Dict[str, str]
    confidence: str
    evidence: List[Dict[str, str]]

class AnalysisResponse(BaseModel):
    summary: str
    missing_information: List[str]
    recommendations: List[Recommendation]
    retrieved_sources: List[Dict[str, str]]
    reasoning_trace: List[str]
