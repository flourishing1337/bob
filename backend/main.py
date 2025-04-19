from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import models
from database import SessionLocal
import os
import json
from scraper import hitta_foretag, hitta_allabolag
from ai_analysis import analyze_website
from social_analysis import get_instagram_data
from pipeline import full_pipeline

load_dotenv()

app = FastAPI()

@app.post("/generate-profiles")
def generate_profiles(keyword: str, location: str):
    saved_profiles = full_pipeline(keyword, location)
    return {"created_profiles": len(saved_profiles)}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/instagram-data")
def instagram(username: str):
    return get_instagram_data(username)

@app.post("/analyze-website")
def analyze_company_website(url: str):
    data = analyze_website(url)
    return data

@app.post("/save-company-profile")
def save_company_profile(profile: dict, db: Session = Depends(get_db)):
    company = CompanyProfile(**profile)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@app.get("/combined-search")
def combined_search(sokord: str, plats: str):
    results_hitta = hitta_foretag(plats, sokord)
    results_allabolag = hitta_allabolag(sokord, plats)

    combined_results = []

    for r in results_hitta:
        combined_results.append({
            "name": r["name"],
            "address": r["address"],
            "source": "hitta.se",
            "link": f"https://www.hitta.se/sök?vad={r['name'].replace(' ', '%20')}&var={plats}",
            "outreach_status": "Ej kontaktad",
            "priority": "Normal",
            "notes": ""
        })

    for r in results_allabolag:
        combined_results.append({
            "name": r["name"],
            "address": plats,
            "source": "allabolag.se",
            "link": r["link"],
            "outreach_status": "Ej kontaktad",
            "priority": "Hög",
            "notes": ""
        })

    return combined_results

@app.get("/hitta-se")
def hitta(stad: str, sokord: str):
    return hitta_foretag(stad, sokord)

@app.get("/allabolag-se")
def allabolag(sokord: str, plats: str):
    return hitta_allabolag(sokord, plats)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chat_model = ChatOpenAI(model="gpt-4-turbo")

class OutreachRequest(BaseModel):
    customer_name: str
    customer_interest: str
    platform: str

# Dependency som öppnar/stänger databas-sessions automatiskt
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate-message")
async def generate_outreach_message(request: OutreachRequest, db: Session = Depends(get_db)):
    prompt_template = ChatPromptTemplate.from_template("""
        Skriv ett personligt och engagerande outreach-meddelande från HappyFeet till kunden.

        Kundens namn: {customer_name}
        Kundens intresse: {customer_interest}
        Plattform: {platform}

        Meddelandet ska vara kort, vänligt, och uppmana till respons.
    """)

    prompt = prompt_template.format_messages(
        customer_name=request.customer_name,
        customer_interest=request.customer_interest,
        platform=request.platform
    )

    try:
        response = chat_model.invoke(prompt)
        generated_message = response.content.strip()

        # Skapa ny logg i databasen
        log_entry = models.OutreachLog(
            customer_name=request.customer_name,
            customer_interest=request.customer_interest,
            platform=request.platform,
            generated_message=generated_message
        )

        # Lägg till i databasen
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        # Returnera meddelandet
        return {"message": generated_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages")
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.OutreachLog).order_by(models.OutreachLog.created_at.desc()).all()
    return messages
