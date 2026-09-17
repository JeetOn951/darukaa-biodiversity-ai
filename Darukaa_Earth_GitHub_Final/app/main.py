import json
import streamlit as st
from core.models import EnvironmentalInput
from app.rag.store import KnowledgeStore
from app.services.llm import analyze_with_llm, llm_enabled

st.set_page_config(page_title="Darukaa.Earth Biodiversity Intelligence", page_icon="🌱", layout="wide")
st.title("🌱 Darukaa.Earth — Biodiversity Intelligence")
st.caption("Evidence-grounded environmental reasoning across soil, water, land use, climate and biodiversity.")

@st.cache_resource
def get_store():
    return KnowledgeStore()

store = get_store()

with st.sidebar:
    st.header("Environmental inputs")
    st.info("For a strong assessment demo, enter at least soil carbon + rainfall + land use + biodiversity + region.")
    soil_soc = st.number_input("Soil organic carbon (%)", min_value=0.0, value=0.3, step=0.1)
    soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.2, step=0.1)
    soil_moisture = st.number_input("Soil moisture (%)", min_value=0.0, value=18.0, step=1.0)
    rainfall = st.text_input("Rainfall pattern", "low / semi-arid")
    temperature = st.number_input("Temperature (°C)", value=31.0)
    land_use = st.text_input("Land use / land cover", "monoculture wheat")
    biodiversity = st.text_input("Biodiversity indicator", "low")
    habitat_diversity = st.text_input("Habitat diversity", "low")
    pollution = st.text_input("Pollution", "unknown")
    region = st.text_input("Region / ecological zone", "semi-arid")
    crop = st.text_input("Crop", "wheat")
    water = st.text_input("Water availability", "low")

    run = st.button("Analyze ecosystem", type="primary", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

if run:
    env = EnvironmentalInput(
        soil_organic_carbon=soil_soc, soil_ph=soil_ph, soil_moisture=soil_moisture,
        rainfall=rainfall, temperature_c=temperature, land_use=land_use,
        biodiversity=biodiversity, habitat_diversity=habitat_diversity,
        pollution=pollution, region=region, crop=crop, water_availability=water
    )
    query = f"""soil organic carbon {soil_soc} rainfall {rainfall} land use {land_use}
    biodiversity {biodiversity} habitat diversity {habitat_diversity} region {region}
    water {water} climate {temperature} crop {crop}"""
    sources = store.search(query, k=5)
    result = analyze_with_llm(env, sources)
    st.session_state.history.append({"input": env.model_dump(), "result": result.model_dump()})

if st.session_state.history:
    latest = st.session_state.history[-1]
    result = latest["result"]

    st.subheader("Assessment")
    st.write(result["summary"])

    if result["missing_information"]:
        st.warning("Clarifying information requested: " + ", ".join(result["missing_information"]))

    for i, rec in enumerate(result["recommendations"], 1):
        st.markdown(f"### Recommendation {i}")
        st.markdown(f"**What to do:** {rec['action']}")
        st.markdown(f"**Why it works:** {rec['rationale']}")
        st.markdown("**Impacted metrics:** " + ", ".join(rec["impacted_metrics"]))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Short term", rec["time_horizon"].get("short_term","—"))
        c2.metric("Medium term", rec["time_horizon"].get("medium_term","—"))
        c3.metric("Long term", rec["time_horizon"].get("long_term","—"))
        c4.metric("Confidence", rec["confidence"])
        st.markdown("**Evidence:**")
        for e in rec["evidence"]:
            st.markdown(f"- [{e['title']}]({e['url']}) — {e['source']}")

    with st.expander("Multi-metric reasoning trace"):
        for step in result["reasoning_trace"]:
            st.write("• " + step)

    with st.expander("Retrieved knowledge"):
        for s in latest["result"]["retrieved_sources"]:
            st.markdown(f"- [{s['title']}]({s['url']}) — {s['source']}")

    with st.expander("Structured JSON input/output"):
        st.code(json.dumps({"input": latest["input"], "output": result}, indent=2), language="json")

else:
    st.markdown("""
### Demo scenario
The prefilled example represents a semi-arid wheat system with low soil organic carbon,
low rainfall, monoculture and low biodiversity. Click **Analyze ecosystem** to demonstrate:

- RAG retrieval from a scientific knowledge base
- Multi-variable environmental reasoning
- Clarifying questions for incomplete inputs
- Evidence-backed recommendations
- Time horizons and confidence
- Structured JSON input/output
""")

st.divider()
st.caption("Knowledge sources include FAO, IPCC and IPBES materials. This prototype is decision-support software, not a substitute for field sampling or ecological assessment.")
