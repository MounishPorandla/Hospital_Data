#app.py - The Web User Interface

import streamlit as st
import pandas as pd
from agent_loop import run_agent
from tools.read_file import read_file
from utils import logger

#1. Page Configuration and Styling
st.set_page_config(page_title="Hospital Data Cleaning Agent", page_icon="🏥", layout="wide")

st.title("🏥 Autonomous Hospital Data Cleaning Agent")
st.markdown("Uplaod a messy hospital Excel or CSV file. Our AI agent will diagnose layout issues, apply data cleaning workflows, and provide a downloadable clean data ")

st.divider()

#2. File Upload UI Widget Component
uploaded_file = st.file_uploader("Choose a messy data file", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # 3. Read File using your Existing Tool Script
    # Streamlit uploaded files act like file paths automatically

    try:
        raw_df = read_file(uploaded_file)

    except Exception as e:
        st.error(f"Error reading file structures: {str(e)}")
        st.stop()

        #Display preview fof messy data layout layouts
    st.subheader(" Raw Messy Input Preview")
    st.dataframe(raw_df.head(5), use_container_width=True)

    st.divider()

    # 4. Trigger Execution Trigger Button
    if st.button(" Start AI Agent Cleaning Cycle", type="primary"):

        with st.spinner("Brain Agent Active...Executing iterative multi-step tool sequence pipeline..."):
            # Call YOUR existing core execution agent brain function
            cleaned_df, audit_log = run_agent(raw_df)

            st.balloons()
            st.success("Data cleaning process complete!")

            # Create UI side-by-side comparative layout layout frames
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(" Cleaned Final Dataset State")
                st.dataframe(cleaned_df.head(5), use_container_width=True)

                # 5. Provide Download Action for the Final Clean DataFrame
                # 6. Convert Pandas state back to text bits safely
                csv_download_payload = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=" Download Cleaned CSV File",
                    data=csv_download_payload,
                    file_name="cleaned_hospital_records.csv",
                    mime="text/csv"
                    )

            with col2:
                st.subheader("Agent Audit Operational History Trail")
                for step in audit_log:
                    with st.expander(f"Executed Tool: {step['tool']}"):
                        st.json(step['args'])
                        st.caption(f"Execution Result Summary: {step['result']}")