from app.core.models import EnvironmentalInput
from app.services.reasoning import build_reasoning
def test_reasoning_smoke():
    x=EnvironmentalInput(soil_organic_carbon_pct=.3,rainfall_mm=500,crop_system="monoculture wheat",query="improve biodiversity")
    r=build_reasoning(x)
    assert r["recommendations"] and r["metrics"]
