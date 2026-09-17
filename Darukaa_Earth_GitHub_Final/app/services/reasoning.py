from typing import List, Dict
from app.core.models import EnvironmentalInput, Recommendation, AnalysisResponse

def missing_fields(env: EnvironmentalInput) -> List[str]:
    missing = []
    if env.soil_organic_carbon is None:
        missing.append("soil organic carbon (%)")
    if env.rainfall is None and env.rainfall_mm is None:
        missing.append("rainfall pattern or annual rainfall (mm)")
    if env.land_use is None:
        missing.append("land use / land cover")
    if env.biodiversity is None and env.species_richness is None and env.habitat_diversity is None:
        missing.append("biodiversity indicator (e.g., species richness or habitat diversity)")
    if env.region is None:
        missing.append("region / ecological zone")
    return missing

def _has(text, terms):
    t = (text or "").lower()
    return any(x in t for x in terms)

def deterministic_analysis(env: EnvironmentalInput, sources: List[Dict]) -> AnalysisResponse:
    missing = missing_fields(env)
    recs = []
    trace = []

    low_soc = env.soil_organic_carbon is not None and env.soil_organic_carbon < 1.0
    low_rain = _has(env.rainfall, ["low", "dry", "semi-arid", "arid"]) or (
        env.rainfall_mm is not None and env.rainfall_mm < 600
    )
    mono = _has(env.land_use, ["monoculture", "single crop", "intensive"])
    low_bio = _has(env.biodiversity, ["low", "declining", "poor"]) or (
        env.species_richness is not None and env.species_richness < 10
    )
    fragmentation = _has(env.land_use, ["fragment", "cleared", "converted", "urban", "plantation"])

    if low_soc:
        trace.append("Low soil organic carbon increases the priority of practices that add/retain organic matter.")
    if low_rain:
        trace.append("Low water availability makes residual-moisture and water-regulating practices more relevant.")
    if mono:
        trace.append("Monoculture reduces structural and crop diversity, so diversification can address both habitat and soil functions.")
    if low_bio:
        trace.append("A low biodiversity signal increases the value of habitat and resource diversification.")
    if fragmentation:
        trace.append("Land-use fragmentation/clearing makes connectivity and habitat structure relevant.")

    if low_soc and low_rain and mono:
        recs.append(Recommendation(
            action="Introduce a drought-tolerant legume cover/intercrop and retain plant residues rather than leaving bare soil.",
            rationale="The combination of low soil carbon, water limitation and monoculture points to a coupled soil–water–biodiversity constraint. Cover/intercrops add organic inputs, diversify rooting niches and use residual moisture while reducing bare-soil exposure.",
            impacted_metrics=["soil organic carbon", "soil moisture retention", "soil biodiversity", "crop/habitat diversity"],
            time_horizon={"short_term": "1 growing season", "medium_term": "2–3 years", "long_term": "3–5+ years"},
            confidence="Medium–High",
            evidence=[{"title": s["title"], "source": s["source"], "url": s["url"]} for s in sources[:3]]
        ))

    if low_bio or mono:
        recs.append(Recommendation(
            action="Add small, connected native vegetation strips or agroforestry elements along field edges and water-flow pathways.",
            rationale="Increasing vertical and horizontal habitat structure can diversify resources for insects and other organisms. Connecting patches is also relevant where land-use change has reduced habitat connectivity.",
            impacted_metrics=["habitat diversity", "species richness", "ecological connectivity", "water regulation"],
            time_horizon={"short_term": "6–12 months for establishment planning", "medium_term": "2–5 years", "long_term": "5+ years"},
            confidence="Medium",
            evidence=[{"title": s["title"], "source": s["source"], "url": s["url"]} for s in sources[1:4]]
        ))

    if not recs:
        recs.append(Recommendation(
            action="Collect the missing baseline metrics and implement a small monitored diversification trial before scaling the intervention.",
            rationale="The available evidence is insufficient for a site-specific recommendation. A baseline enables the system to connect soil, land-use, water and biodiversity indicators rather than relying on a single metric.",
            impacted_metrics=["soil organic carbon", "soil moisture", "land-use diversity", "biodiversity indicator"],
            time_horizon={"short_term": "0–3 months", "medium_term": "1 year", "long_term": "2–3 years"},
            confidence="Low–Medium",
            evidence=[{"title": s["title"], "source": s["source"], "url": s["url"]} for s in sources[:2]]
        ))

    summary = (
        "The system identified a multi-metric environmental pattern and generated recommendations "
        "using retrieved scientific evidence. " +
        ("Additional inputs are needed for stronger site-specific reasoning." if missing else "The supplied inputs are sufficient for the current rule-based analysis.")
    )

    return AnalysisResponse(
        summary=summary,
        missing_information=missing,
        recommendations=recs,
        retrieved_sources=[{"title": s["title"], "source": s["source"], "url": s["url"]} for s in sources],
        reasoning_trace=trace
    )
