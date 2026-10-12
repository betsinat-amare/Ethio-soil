from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class FarmInput(BaseModel):
    kebele_name: str = Field(..., description="Name of the Kebele or location")
    farm_size_hectares: float = Field(..., gt=0, description="Size of the farm in hectares")
    
    # Optional GPS coordinates for automatic SoilGrids fetching
    latitude: Optional[float] = Field(None, description="Farm Latitude")
    longitude: Optional[float] = Field(None, description="Farm Longitude")
    
    # Soil test parameters
    soil_ph: Optional[float] = Field(6.0, ge=0, le=14, description="Soil pH level")
    nitrogen_n: float = Field(50.0, ge=0, description="Nitrogen (N) level")
    phosphorus_p: float = Field(20.0, ge=0, description="Phosphorus (P) level")
    potassium_k: float = Field(100.0, ge=0, description="Potassium (K) level")
    rainfall: float = Field(1000.0, ge=0, description="Rainfall in mm")
    language: Optional[str] = Field("en", description="Language preference: 'en', 'am', or 'om'")

class RecommendationResponse(BaseModel):
    success: bool
    data: Dict[str, Any]