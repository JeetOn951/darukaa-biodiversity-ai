# Darukaa.Earth — Biodiversity Intelligence AI

An evidence-grounded conversational environmental decision-support prototype for the Darukaa.Earth AI Biodiversity Intelligence Challenge.

## What it demonstrates

- Retrievable scientific knowledge layer using ChromaDB + sentence-transformer embeddings
- Environmental variables: soil carbon, pH, moisture, rainfall, temperature, land use, biodiversity, habitat diversity, pollution, water availability
- Clarifying questions for incomplete environmental inputs
- Multi-turn session memory through Streamlit session state
- Multi-metric reasoning across soil ↔ biodiversity, water ↔ survival/resilience, and land use ↔ habitat/connectivity
- Evidence-backed recommendations with source links
- Structured JSON input/output
- Optional LLM reasoning through OpenAI API; deterministic reasoning fallback keeps the demo runnable without an API key
- Unit tests

## Architecture

```text
Streamlit UI
    ↓
EnvironmentalInput (Pydantic)
    ↓
Query construction
    ↓
SentenceTransformer embedding
    ↓
ChromaDB retrieval
    ↓
Reasoning engine
    ├── deterministic fallback
    └── optional LLM JSON reasoning
    ↓
Recommendation + metrics + time horizon + confidence + evidence
```

## Database/schema

ChromaDB collection: `environmental_knowledge`

Metadata fields:
- `title`
- `source`
- `url`
- `topics`

Document field:
- scientific evidence text

## Local setup

Python 3.10+ is recommended.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd darukaa-biodiversity-ai

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

streamlit run app/main.py
```

On first run, the sentence-transformer model is downloaded and the ChromaDB collection is populated.

## Optional LLM

Add an API key to `.env`:

```text
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

Without a key, the application uses the transparent deterministic reasoning engine.

## Tests

```bash
pytest -q
```

## CI/CD

GitHub Actions runs the test suite on every push and pull request. See `.github/workflows/ci.yml`.

## Assessment demo

Use the prefilled example:
- Soil organic carbon: 0.3%
- Rainfall: low / semi-arid
- Land use: monoculture wheat
- Biodiversity: low
- Region: semi-arid
- Water availability: low

Then click **Analyze ecosystem** and show:
1. Retrieved sources
2. Multi-metric reasoning trace
3. Recommendations
4. Impacted metrics
5. Time horizon
6. Evidence links
7. Structured JSON

## Evidence sources

- FAO — Soil organic cover: https://www.fao.org/conservation-agriculture/in-practice/soil-organic-cover/en/
- FAO — Agroforestry: https://www.fao.org/americas/priorities/agricultura-sostenible/agrofesteria/en
- FAO — Recarbonizing global soils: https://www.fao.org/family-farming/detail/en/c/1678078/
- FAO — Soil biodiversity: https://www.fao.org/4/y4810e/y4810e06.htm
- IPCC — Climate Change and Land: https://www.ipcc.ch/srccl/
- IPBES — Spatial planning and connectivity: https://www.ipbes.net/spatial-planning-assessment
