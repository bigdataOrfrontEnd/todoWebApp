from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NarratoAI Backend"
    API_V1_STR: str = "/api/v1"

    # --- 数据库配置 ---
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "narrato_db"
    DB_PORT: int = 3306
    
    # SQLAlchemy 异步连接 URL
    # 使用 asyncmy 驱动: mysql+asyncmy://USER:PASSWORD@HOST:PORT/NAME
    DATABASE_URL: str = (
        f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    class Config:
        env_file = ".env" # 允许从 .env 文件加载配置

settings = Settings()