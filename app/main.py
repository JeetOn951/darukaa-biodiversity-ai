import json
import streamlit as st
from app.core.models import EnvironmentalInput
from app.rag.store import KnowledgeStore
from app.services.reasoning import build_reasoning
from app.services.llm import analyze_with_llm,llm_enabled
st.set_page_config(page_title="Darukaa.Earth Biodiversity Intelligence",page_icon="🌿",layout="wide")
@st.cache_resource
def get_store(): return KnowledgeStore()
st.title("🌿 Darukaa.Earth — Biodiversity Intelligence")
st.caption("Evidence-grounded, multi-metric environmental reasoning")
with st.sidebar:
    st.header("Environmental Inputs")
    ph=st.number_input("Soil pH",0.,14.,6.5)
    soc=st.number_input("Soil Organic Carbon (%)",0.,value=.3)
    moisture=st.number_input("Soil Moisture (%)",0.,100.,20.)
    rainfall=st.number_input("Annual Rainfall (mm)",0.,value=500.)
    temp=st.number_input("Temperature (°C)",value=28.)
    land=st.text_input("Land use / land cover","semi-arid farmland")
    crop=st.text_input("Crop system","monoculture wheat")
    bio=st.text_input("Biodiversity indicator","low pollinator diversity")
    pollution=st.text_input("Pollution pressure","low")
    deforest=st.text_input("Deforestation pressure","low")
    location=st.text_input("Location (optional)","")
query=st.text_area("Ask an environmental question","How can I improve soil health and biodiversity under these conditions?")
data=EnvironmentalInput(soil_ph=ph,soil_organic_carbon_pct=soc,soil_moisture_pct=moisture,rainfall_mm=rainfall,temperature_c=temp,land_use=land,crop_system=crop,biodiversity_indicator=bio,pollution=pollution,deforestation=deforest,location=location,query=query)
if st.button("Analyze",type="primary"):
    docs=get_store().query(json.dumps(data.model_dump())+" "+query)
    result=build_reasoning(data)
    st.subheader("Recommendation")
    for x in result["recommendations"]: st.write("• "+x)
    st.subheader("Impacted Metrics"); st.write(", ".join(result["metrics"]) or "Additional measurements required")
    st.subheader("Time Horizon"); st.write(", ".join(result["horizons"]))
    st.subheader("Scientific Reasoning")
    for x in result["findings"]: st.write("• "+x)
    st.subheader("Evidence / Retrieved Knowledge")
    for d in docs:
        st.markdown(f"**{d['title']}** — {d['source']}"); st.write(d["text"])
    if llm_enabled():
        try:
            st.subheader("LLM Synthesis"); st.write(analyze_with_llm(data,docs))
        except Exception: st.warning("LLM synthesis unavailable; deterministic reasoning remains available.")
    with st.expander("Structured JSON"):
        st.json({"recommendation":result["recommendations"],"impacted_metrics":result["metrics"],"time_horizon":result["horizons"],"confidence":"medium","retrieved_sources":[d["title"] for d in docs]})
else: st.info("Adjust the environmental variables, then click Analyze.")
