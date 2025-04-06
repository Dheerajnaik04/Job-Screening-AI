import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Job Screening AI Dashboard",
    page_icon="🎯",
    layout="wide"
)

# Constants
API_URL = "http://localhost:8000"

def main():
    st.title("Job Screening AI Dashboard")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Post Job", "Upload CV", "View Matches", "Schedule Interviews"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Post Job":
        show_post_job()
    elif page == "Upload CV":
        show_upload_cv()
    elif page == "View Matches":
        show_matches()
    elif page == "Schedule Interviews":
        show_interviews()

def show_dashboard():
    st.header("Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Jobs", "15")
    with col2:
        st.metric("Total Candidates", "156")
    with col3:
        st.metric("Pending Matches", "45")
    with col4:
        st.metric("Scheduled Interviews", "12")
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_data = {
        "Date": ["2024-04-06", "2024-04-06", "2024-04-05"],
        "Activity": [
            "New job posted: Senior Python Developer",
            "5 new candidates matched",
            "Interview scheduled with John Doe"
        ]
    }
    st.table(pd.DataFrame(recent_data))

def show_post_job():
    st.header("Post a New Job")
    
    with st.form("job_form"):
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        required_skills = st.text_input("Required Skills (comma-separated)")
        experience = st.number_input("Years of Experience Required", min_value=0, max_value=20)
        preferred_skills = st.text_input("Preferred Skills (comma-separated)")
        education = st.selectbox("Minimum Education", 
                               ["High School", "Bachelor's", "Master's", "PhD"])
        
        if st.form_submit_button("Post Job"):
            try:
                response = requests.post(
                    f"{API_URL}/jobs/",
                    json={
                        "title": title,
                        "description": description,
                        "required_skills": required_skills.split(","),
                        "experience": experience,
                        "preferred_skills": preferred_skills.split(","),
                        "education": education
                    }
                )
                if response.status_code == 200:
                    st.success("Job posted successfully!")
                else:
                    st.error("Failed to post job.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_upload_cv():
    st.header("Upload CV")
    
    uploaded_file = st.file_uploader("Choose a CV file", type=["pdf", "docx"])
    if uploaded_file is not None:
        if st.button("Process CV"):
            try:
                # Here you would process the CV file and send it to the API
                st.success("CV processed successfully!")
            except Exception as e:
                st.error(f"Error processing CV: {str(e)}")

def show_matches():
    st.header("View Matches")
    
    # Filter options
    job_id = st.selectbox("Select Job", ["Senior Python Developer", "Data Scientist", "ML Engineer"])
    min_score = st.slider("Minimum Match Score", 0, 100, 70)
    
    # Display matches
    matches_data = {
        "Candidate": ["John Doe", "Jane Smith", "Bob Johnson"],
        "Match Score": [95, 88, 82],
        "Experience": ["5 years", "3 years", "4 years"],
        "Status": ["Pending", "Interviewed", "Scheduled"]
    }
    st.dataframe(pd.DataFrame(matches_data))

def show_interviews():
    st.header("Schedule Interviews")
    
    with st.form("interview_form"):
        candidate = st.selectbox("Select Candidate", ["John Doe", "Jane Smith", "Bob Johnson"])
        job = st.selectbox("Select Job", ["Senior Python Developer", "Data Scientist", "ML Engineer"])
        date = st.date_input("Interview Date")
        time = st.time_input("Interview Time")
        
        if st.form_submit_button("Schedule Interview"):
            try:
                st.success(f"Interview scheduled with {candidate} for {date} at {time}")
            except Exception as e:
                st.error(f"Error scheduling interview: {str(e)}")

if __name__ == "__main__":
    main() 