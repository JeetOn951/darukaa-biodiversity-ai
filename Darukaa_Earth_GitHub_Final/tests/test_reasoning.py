from app.core.models import EnvironmentalInput
from app.services.reasoning import deterministic_analysis, missing_fields

def test_missing_fields():
    env = EnvironmentalInput(soil_organic_carbon=0.3, rainfall="low", land_use="monoculture", region="semi-arid")
    missing = missing_fields(env)
    assert "biodiversity indicator (e.g., species richness or habitat diversity)" in missing

def test_multi_metric_recommendation():
    env = EnvironmentalInput(
        soil_organic_carbon=0.3, rainfall="low", land_use="monoculture wheat",
        biodiversity="low", region="semi-arid"
    )
    result = deterministic_analysis(env, [])
    assert len(result.recommendations) >= 1
    assert len(result.recommendations[0].impacted_metrics) >= 3
