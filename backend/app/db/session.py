from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 异步数据库引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 异步 Session 工厂
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 基础模型
Base = declarative_base()

# 依赖注入函数：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session