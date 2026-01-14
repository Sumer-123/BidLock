from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Bid(BaseModel):
    job_id: str
    freelancer_id: str
    bid_amount: float
    proposal_text: Optional[str] = None
    timestamp: datetime = datetime.now()

class Job(BaseModel):
    job_id: str
    client_id: str
    title: str
    budget: float
    timestamp: datetime = datetime.now()