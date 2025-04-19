from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func

# Try different import paths to work in both contexts
try:
    # When imported as part of the backend package
    from backend.database import Base
except ImportError:
    try:
        # When imported directly in the backend directory
        from database import Base
    except ImportError:
        # When imported with relative imports
        from .database import Base


class OutreachLog(Base):
    __tablename__ = "outreach_logs"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    customer_interest = Column(String, index=True)
    platform = Column(String, index=True)
    generated_message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    instagram_followers = Column(Integer, nullable=True)
    instagram_following = Column(Integer, nullable=True)
    instagram_posts = Column(Integer, nullable=True)
    facebook = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    video_need_assessment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
