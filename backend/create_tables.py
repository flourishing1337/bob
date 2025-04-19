# create_tables.py
from database import engine, Base
import models

# Detta kommando skapar alla definierade tabeller i databasen.
Base.metadata.create_all(bind=engine)
