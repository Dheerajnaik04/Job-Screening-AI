import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import os

# Configure the page
st.set_page_config(
    page_title="Job Screening AI",
    page_icon="🤖",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

def main():
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
    st.title("🤖 Job Screening AI Dashboard")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Jobs", "5")
    with col2:
        st.metric("Total Candidates", "25")
    with col3:
        st.metric("Pending Matches", "12")
    with col4:
        st.metric("Scheduled Interviews", "8")
    
    # Recent activity
    st.subheader("Recent Activity")
    activity_data = {
        "Time": ["2 hours ago", "3 hours ago", "5 hours ago", "1 day ago"],
        "Activity": [
            "New job posted: Senior Python Developer",
            "CV uploaded: John Doe",
            "Match found: 85% match score",
            "Interview scheduled: Technical Round"
        ]
    }
    st.table(pd.DataFrame(activity_data))

def show_post_job():
    st.title("📝 Post a New Job")
    
    with st.form("job_form"):
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description", height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            required_skills = st.text_area("Required Skills (one per line)")
            experience = st.text_input("Required Experience")
        with col2:
            preferred_skills = st.text_area("Preferred Skills (one per line)")
            education = st.text_input("Required Education")
        
        submitted = st.form_submit_button("Post Job")
        
        if submitted:
            try:
                response = requests.post(
                    f"{API_URL}/analyze-job",
                    params={"job_description": job_description}
                )
                if response.status_code == 200:
                    st.success("Job posted successfully!")
                    st.json(response.json())
                else:
                    st.error("Error posting job. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_upload_cv():
    st.title("📄 Upload CV")
    
    uploaded_file = st.file_uploader("Choose a CV file", type=['pdf'])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp_cv.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        try:
            response = requests.post(
                f"{API_URL}/analyze-cv",
                params={"cv_path": "temp_cv.pdf"}
            )
            if response.status_code == 200:
                st.success("CV analyzed successfully!")
                st.json(response.json())
            else:
                st.error("Error analyzing CV. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists("temp_cv.pdf"):
                os.remove("temp_cv.pdf")

def show_matches():
    st.title("🎯 View Matches")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        job_filter = st.selectbox("Filter by Job", ["All Jobs", "Python Developer", "Data Scientist"])
    with col2:
        score_filter = st.slider("Minimum Match Score", 0, 100, 70)
    
    # Sample matches data
    matches_data = {
        "Candidate": ["John Doe", "Jane Smith", "Mike Johnson"],
        "Job": ["Python Developer", "Data Scientist", "Python Developer"],
        "Match Score": [85, 92, 78],
        "Status": ["Pending", "Matched", "Interview Scheduled"]
    }
    st.table(pd.DataFrame(matches_data))

def show_interviews():
    st.title("📅 Schedule Interviews")
    
    # Sample interviews data
    interviews_data = {
        "Candidate": ["John Doe", "Jane Smith"],
        "Job": ["Python Developer", "Data Scientist"],
        "Date": ["2024-04-10", "2024-04-12"],
        "Time": ["10:00 AM", "2:00 PM"],
        "Status": ["Scheduled", "Pending"]
    }
    st.table(pd.DataFrame(interviews_data))
    
    # Schedule new interview
    st.subheader("Schedule New Interview")
    with st.form("interview_form"):
        candidate = st.selectbox("Select Candidate", ["John Doe", "Jane Smith", "Mike Johnson"])
        job = st.selectbox("Select Job", ["Python Developer", "Data Scientist"])
        date = st.date_input("Interview Date")
        time = st.time_input("Interview Time")
        
        submitted = st.form_submit_button("Schedule Interview")
        if submitted:
            st.success("Interview scheduled successfully!")

if __name__ == "__main__":
    main() 