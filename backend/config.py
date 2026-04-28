from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str = ""
    # .env uses SUPABASE_KEY for the anon/publishable key
    supabase_anon_key: str = Field(default="", alias="SUPABASE_KEY", validation_alias="SUPABASE_KEY")
    # .env uses SUPABASE_SERVICE_KEY for service role key
    supabase_service_role_key: str = Field(default="", alias="SUPABASE_SERVICE_KEY", validation_alias="SUPABASE_SERVICE_KEY")
    # JWT secret for decoding Supabase tokens
    supabase_jwt_secret: str = Field(default="", alias="SUPABASE_JWT_SECRET", validation_alias="SUPABASE_JWT_SECRET")
    google_ai_studio_key: str = ""
    anthropic_api_key: str = ""
    # .env uses APIFY_API_TOKEN — also accept APIFY_API_KEY
    apify_api_key: str = Field(default="", alias="APIFY_API_TOKEN", validation_alias="APIFY_API_TOKEN")
    remotion_url: str = "http://localhost:3100"
    remotion_secret: str = ""
    environment: str = "development"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "populate_by_name": True,
    }


settings = Settings()
