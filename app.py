import streamlit as st
import sys
import os

# explicitly set backend path
sys.path.append(os.path.abspath("backend"))

from pipeline import main as pipeline_main

st.set_page_config(page_title="Bob Outreach Tool", layout="centered")

st.title("🚀 Bob - Outreach & Analysis Tool")

st.markdown("Click the button below to execute the full pipeline and analyze your data.")

if st.button("🔍 Run Analysis"):
    with st.spinner("Executing pipeline, please wait..."):
        try:
            pipeline_main()
            st.success("🎉 Pipeline executed successfully!")
        except Exception as e:
            st.exception(f"⚠️ An error occurred: {e}")
