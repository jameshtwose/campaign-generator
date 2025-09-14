from pydantic_settings import BaseSettings

class ClickUpSettings(BaseSettings):
    clickup_api_key: str
    clickup_team_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"