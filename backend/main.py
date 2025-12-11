from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine, Base
from loguru import logger

# 数据库初始化 (创建表)
async def init_db():
    """
    尝试连接数据库并创建所有未创建的表。
    在生产环境中，推荐使用 Alembic 进行数据库迁移，而不是自动创建。
    """
    logger.info("Database startup: Starting connection and checking schema...")
    async with engine.begin() as conn:
        # 如果需要自动创建表，取消下一行的注释。
        # 如果您已经在使用 Alembic 管理迁移，请注释掉这一行。
        # await conn.run_sync(Base.metadata.create_all) 
        pass
    logger.info("Database startup complete.")

# 使用 lifespan 替代 on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用启动和关闭时的生命周期事件处理。
    """
    # 应用启动时执行: 数据库连接初始化、LLM模型加载等
    try:
        await init_db()
    except Exception as e:
        logger.error(f"❌ 数据库连接或初始化失败: {e}")
        # 在实际部署中，通常会在这里选择退出应用

    yield # 应用开始接受请求

    # 应用关闭时执行: 资源清理
    logger.info("Application shutdown: Cleaning up resources...")
    # 例如：关闭数据库连接池 (SQLAlchemy engine 会自动处理)

def create_application() -> FastAPI:
    # 将 lifespan 上下文管理器传递给 FastAPI 构造函数
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan # <--- 传递 lifespan
    )

    @application.get("/")
    def read_root():
        return {"message": "NarratoAI Backend is running!"}

    # TODO: 注册 API 路由

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    # 假设 MySQL 已经运行在本地，且数据库 'narrato_db' 已创建
    logger.info(f"Starting server on http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)