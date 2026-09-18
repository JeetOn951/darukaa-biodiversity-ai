def build_reasoning(data):
    v=data.model_dump(); findings=[]; rec=[]; metrics=[]; horizons=[]
    soc=v.get("soil_organic_carbon_pct"); rain=v.get("rainfall_mm")
    crop=(v.get("crop_system") or "").lower()
    land=(v.get("land_use") or "").lower()
    pollution=(v.get("pollution") or "").lower()
    deforest=(v.get("deforestation") or "").lower()
    if soc is not None and soc < 1:
        findings.append("Low soil organic carbon suggests reduced soil organic matter and weaker soil biological function.")
        rec.append("Increase organic inputs through compost, residue retention, cover crops, or diversified planting.")
        metrics += ["soil organic carbon","soil biological activity"]; horizons.append("1–3 years")
    if rain is not None and rain < 700:
        findings.append("Low rainfall increases water limitation and can constrain plant and soil-organism survival.")
        rec.append("Use mulching, residue cover, infiltration measures, and drought-tolerant diversified crops.")
        metrics += ["soil moisture","water availability","species survival"]; horizons.append("1–3 seasons")
    if "monoculture" in crop or "monoculture" in land:
        findings.append("Monoculture reduces crop and habitat diversity and can increase ecological vulnerability.")
        rec.append("Introduce intercropping, crop rotation, flowering strips, or agroforestry where locally appropriate.")
        metrics += ["habitat diversity","pollinator resources","ecosystem resilience"]; horizons.append("1–5 years")
    if "high" in pollution:
        findings.append("High pollution pressure can reduce habitat quality and biodiversity.")
        rec.append("Identify the pollution source, reduce the relevant input, and use vegetated buffer zones where appropriate.")
        metrics += ["pollution load","habitat quality","biodiversity"]
    if "high" in deforest:
        findings.append("High deforestation pressure can increase habitat loss and fragmentation.")
        rec.append("Prioritize native vegetation retention, ecological corridors, and restoration of degraded habitat patches.")
        metrics += ["habitat connectivity","vegetation cover","species persistence"]
    if not rec: rec.append("Collect additional soil, climate, land-use, and biodiversity measurements before making a site-specific intervention.")
    return {"findings":list(dict.fromkeys(findings)),"recommendations":list(dict.fromkeys(rec)),
            "metrics":list(dict.fromkeys(metrics)),"horizons":list(dict.fromkeys(horizons)) or ["Site-dependent"]}
