import streamlit as st
import sys
import os
from backend.database import engine, Base
from backend.models import CompanyProfile

Base.metadata.create_all(bind=engine)

# Ensure the app can find the backend package regardless of how it's run
try:
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory (project root)
    project_root = current_dir
    
    # Add the project root to the Python path if it's not already there
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"Added {project_root} to Python path")
except Exception as e:
    st.error(f"Error setting up Python path: {e}")

# Now we can import from the backend package
from backend.pipeline import main as pipeline_main

st.set_page_config(page_title="Bob Outreach Tool", layout="centered")
st.title("🚀 Bob - Outreach & Analysis Tool")

keyword = st.text_input("Enter keyword:", "")
location = st.text_input("Enter location:", "")

if st.button("🔍 Run Analysis"):
    if keyword and location:
        with st.spinner("Executing pipeline, please wait..."):
            try:
                pipeline_main(keyword, location)
                st.success("🎉 Pipeline executed successfully!")
            except Exception as e:
                st.exception(f"⚠️ An error occurred: {e}")
    else:
        st.warning("Please enter both keyword and location.")
