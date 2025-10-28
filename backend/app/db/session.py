from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# ✅ Get database URL from environment
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in environment variables.")

# ✅ Ensure correct driver and SSL mode
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# ✅ Create engine with SSL required (important for Supabase)
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"}, pool_pre_ping=True)

# ✅ Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
