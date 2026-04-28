from pydantic import BaseModel
from typing import Optional


class WorkflowCreate(BaseModel):
    name: str
    template_type: str
    brand_voice: str = ""
    content_pillars: list[str] = []
    platforms: list[str] = []
    posting_cadence: dict = {}
    competitors: list[str] = []
    questionnaire_answers: Optional[dict] = None


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    brand_voice: Optional[str] = None
    content_pillars: Optional[list[str]] = None
    platforms: Optional[list[str]] = None
    posting_cadence: Optional[dict] = None
    competitors: Optional[list[str]] = None
    is_active: Optional[bool] = None
