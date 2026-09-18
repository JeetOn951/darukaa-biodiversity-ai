import json
from pathlib import Path
class KnowledgeStore:
    def __init__(self):
        p=Path(__file__).resolve().parents[2]/"knowledge"/"sources.json"
        self.docs=json.loads(p.read_text(encoding="utf-8"))
    def query(self,text,k=4):
        terms=set(text.lower().split()); scored=[]
        for d in self.docs:
            c=(d["title"]+" "+d["text"]).lower()
            scored.append((sum(1 for t in terms if len(t)>3 and t in c),d))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [d for _,d in scored[:k]]
