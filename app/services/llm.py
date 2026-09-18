import os
from dotenv import load_dotenv
load_dotenv()
def llm_enabled(): return bool(os.getenv("OPENAI_API_KEY"))
def analyze_with_llm(data,retrieved):
    from openai import OpenAI
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    r=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),temperature=.2,
      messages=[{"role":"system","content":"Give concise evidence-grounded environmental reasoning."},
                {"role":"user","content":f"Input: {data.model_dump()}\nEvidence: {retrieved}"}])
    return r.choices[0].message.content
