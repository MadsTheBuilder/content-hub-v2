from pydantic import BaseModel
from typing import Optional


class BrandUpdate(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    font_family: Optional[str] = None
    logo_url: Optional[str] = None
    watermark_enabled: Optional[bool] = None
    watermark_text: Optional[str] = None
    custom_font: Optional[str] = None          # Google Fonts name e.g. "Inter", "Montserrat"
    slide_template: Optional[str] = None       # "default" | "dark_minimalist" | "vibrant_high_energy"
    transition_style: Optional[str] = None     # "dynamic" | "minimal" | "bold" | "smooth"
    reference_creators: Optional[list[str]] = None  # Creator handles for style reference
