from pydantic import BaseModel


class ContentGenerateRequest(BaseModel):
    workflow_id: str
    content_type: str
    platform: str
    topic: str
    skip_refinement: bool = False


class ContentEditRequest(BaseModel):
    edited_script: str


class SynthesizeRequest(BaseModel):
    workflow_id: str
    selected_post_ids: list[str]
    platform: str


class StrategyGenerateRequest(BaseModel):
    workflow_id: str
    strategy: dict
    original_strategy: dict | None = None
    user_notes: str = ""
    content_type: str = "short_form"
    skip_refinement: bool = False


class ReviseStrategyRequest(BaseModel):
    workflow_id: str
    current_strategy: dict
    rejection_notes: str = ""
    selected_post_ids: list[str] = []
