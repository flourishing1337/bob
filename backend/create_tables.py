from .database import engine, Base
from .models import CompanyProfile  # Ensure this import exists

def init_db():
    print("Dropping all tables explicitly...")
    Base.metadata.drop_all(bind=engine)  # explicitly drops existing tables
    print("Creating all tables explicitly...")
    Base.metadata.create_all(bind=engine)  # explicitly creates tables
    print("Database schema synced successfully!")

if __name__ == "__main__":
    init_db()
