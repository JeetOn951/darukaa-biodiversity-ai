import json
import streamlit as st
from app.core.models import EnvironmentalInput
from app.rag.store import KnowledgeStore
from app.services.reasoning import build_reasoning


@st.cache_resource
def get_store():
    return KnowledgeStore()


def main():
    st.set_page_config(
        page_title="Darukaa.Earth Biodiversity Intelligence",
        page_icon="🌿",
        layout="wide",
    )

    st.title("🌿 Darukaa.Earth — Biodiversity Intelligence")
    st.caption("Evidence-grounded, multi-metric environmental reasoning")

    with st.sidebar:
        st.header("Environmental Inputs")

        ph = st.number_input(
            "Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1
        )
        soc = st.number_input(
            "Soil Organic Carbon (%)", min_value=0.0, value=0.3, step=0.1
        )
        moisture = st.number_input(
            "Soil Moisture (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
        )
        rainfall = st.number_input(
            "Annual Rainfall (mm)", min_value=0.0, value=500.0, step=50.0
        )
        temp = st.number_input("Temperature (°C)", value=28.0, step=0.5)
        land = st.text_input("Land use / land cover", "semi-arid farmland")
        crop = st.text_input("Crop system", "monoculture wheat")
        bio = st.text_input("Biodiversity indicator", "low pollinator diversity")
        pollution = st.text_input("Pollution pressure", "low")
        deforest = st.text_input("Deforestation pressure", "low")
        location = st.text_input("Location (optional)", "")

    query = st.text_area(
        "Ask an environmental question",
        "How can I improve soil health and biodiversity under these conditions?",
    )

    if st.button("Analyze", type="primary", use_container_width=True):
        try:
            data = EnvironmentalInput(
                soil_ph=ph,
                soil_organic_carbon_pct=soc,
                soil_moisture_pct=moisture,
                rainfall_mm=rainfall,
                temperature_c=temp,
                land_use=land,
                crop_system=crop,
                biodiversity_indicator=bio,
                pollution=pollution,
                deforestation=deforest,
                location=location,
                query=query,
            )

            with st.spinner(
                "Retrieving knowledge and generating recommendations..."
            ):
                docs = get_store().query(
                    json.dumps(data.model_dump()) + " " + query
                )
                result = build_reasoning(data)

            st.success("Analysis completed")

            st.subheader("Recommendation")
            for item in result["recommendations"]:
                st.write("• " + item)

            st.subheader("Impacted Metrics")
            st.write(
                ", ".join(result["metrics"])
                or "Additional measurements required"
            )

            st.subheader("Time Horizon")
            st.write(", ".join(result["horizons"]))

            st.subheader("Scientific Reasoning")
            for item in result["findings"]:
                st.write("• " + item)

            st.subheader("Evidence / Retrieved Knowledge")
            if docs:
                for doc in docs:
                    st.markdown(f"**{doc['title']}** — {doc['source']}")
                    st.write(doc["text"])
            else:
                st.info("No matching knowledge records were retrieved.")

            with st.expander("Structured JSON"):
                st.json(
                    {
                        "recommendation": result["recommendations"],
                        "impacted_metrics": result["metrics"],
                        "time_horizon": result["horizons"],
                        "confidence": "medium",
                        "retrieved_sources": [doc["title"] for doc in docs],
                    }
                )

        except Exception as error:
            st.error("Analysis failed.")
            st.exception(error)
    else:
        st.info("Adjust the environmental variables, then click Analyze.")


if __name__ == "__main__":
    main()
