from pydantic import BaseModel
from typing import List, Dict, Any
from uuid import uuid4

class PlanStep(BaseModel):
    id: str
    action: str
    params: Dict[str, Any]
    verify: str

class Plan(BaseModel):
    plan_id: str
    steps: List[PlanStep]

def new_plan_id():
    return str(uuid4())
