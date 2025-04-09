# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logger import logger

DATABASE_URL = settings.DATABASE_URL

logger.info(f"Database URL: {DATABASE_URL}")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG, # Log SQL queries if DEBUG is True
    future=True
)

# Create sessionmaker
# expire_on_commit=False prevents attributes from expiring after commit
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for declarative models
Base = declarative_base()

async def init_models():
    """Initialize the database models (create tables)."""
    async with engine.begin() as conn:
        logger.info("Dropping and creating database tables...")
        # Drop all tables (useful for development, disable in production)
        # await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created.")

async def get_db() -> AsyncSession:
    """FastAPI dependency to get a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rollback due to exception: {e}")
            raise
        finally:
            await session.close() 