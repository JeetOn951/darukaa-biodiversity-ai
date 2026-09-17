import os, json
from typing import List, Dict
from dotenv import load_dotenv
from app.core.models import EnvironmentalInput, AnalysisResponse
from app.services.reasoning import deterministic_analysis

load_dotenv()

def llm_enabled():
    return bool(os.getenv("OPENAI_API_KEY"))

def analyze_with_llm(env: EnvironmentalInput, sources: List[Dict]) -> AnalysisResponse:
    if not llm_enabled():
        return deterministic_analysis(env, sources)

    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    context = "\n\n".join(
        f"SOURCE: {s['title']}\nURL: {s['url']}\nCONTENT: {s['text']}" for s in sources
    )
    system = """You are Darukaa.Earth Biodiversity Intelligence, an environmental decision-support assistant.
Use only the retrieved evidence for scientific claims. Do not invent numerical impact estimates.
Connect at least three environmental variables whenever the data permits.
If required information is missing, explicitly ask for it.
Return JSON matching this structure:
{
 "summary": "...",
 "missing_information": ["..."],
 "recommendations": [{
   "action":"...",
   "rationale":"...",
   "impacted_metrics":["..."],
   "time_horizon":{"short_term":"...","medium_term":"...","long_term":"..."},
   "confidence":"Low|Medium|High",
   "evidence":[{"title":"...","source":"...","url":"..."}]
 }],
 "retrieved_sources":[{"title":"...","source":"...","url":"..."}],
 "reasoning_trace":["..."]
}"""
    prompt = f"ENVIRONMENTAL INPUT:\n{env.model_dump_json(indent=2)}\n\nRETRIEVED KNOWLEDGE:\n{context}"
    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}]
    )
    data = json.loads(resp.choices[0].message.content)
    return AnalysisResponse.model_validate(data)
