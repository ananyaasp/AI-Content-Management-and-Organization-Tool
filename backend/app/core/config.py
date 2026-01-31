from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Content Organizer"
    host: str = "0.0.0.0"
    port: int = 8000
    ingest_dir: str = "./data/incoming"
    storage_dir: str = "./data/storage"
    faiss_index_path: str = "./data/faiss.index"
    jwt_secret: str = "change-this-secret-in-prod"
    jwt_exp_minutes: int = 60

settings = Settings()
