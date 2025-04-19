from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set, use SQLite with a file in the backend directory
if not DATABASE_URL:
    # Get the directory where this file is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Create the database file in the backend directory
    sqlite_db_path = os.path.join(BASE_DIR, "app.db")
    DATABASE_URL = f"sqlite:///{sqlite_db_path}"
    print(f"Using SQLite database at: {sqlite_db_path}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
