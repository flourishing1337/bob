from .scraper import hitta_foretag, hitta_allabolag
from .ai_analysis import analyze_website
from .social_analysis import get_instagram_data
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal

def main(keyword, location):
    db = SessionLocal()

    # Steg 1: Skrapa data från hitta.se och allabolag
    hitta_data = hitta_foretag(location, keyword)
    allabolag_data = hitta_allabolag(keyword, location)

    combined_data = hitta_data + allabolag_data

    profiles_saved = []

    for company in combined_data:
        # Steg 2: AI analys på hemsida
        website_url = company.get('website', '')
        ai_data = analyze_website(website_url) if website_url else {}

        # Steg 3: Social media analys
        instagram_username = ai_data.get('instagram', '')
        instagram_data = get_instagram_data(instagram_username) if instagram_username else {}

        # Skapa och spara komplett företagsprofil i databasen
        profile = models.CompanyProfile(
            name=company.get('name'),
            address=company.get('address'),
            website=website_url,
            email=ai_data.get('email', ''),
            phone=ai_data.get('phone', ''),
            instagram=instagram_username,
            instagram_followers=instagram_data.get('followers'),
            instagram_following=instagram_data.get('following'),
            instagram_posts=instagram_data.get('posts_count'),
            facebook=ai_data.get('facebook', ''),
            linkedin=ai_data.get('linkedin', ''),
            industry=ai_data.get('industry', ''),
            video_need_assessment=ai_data.get('video_need_assessment', '')
        )

        db.add(profile)
        profiles_saved.append(profile)

    db.commit()

    return profiles_saved
