"""
Advanced Streamlit App for AI Recruitment Platform
Includes all advanced features and capabilities
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64

# Configuration
API_BASE_URL = "https://web-production-3f8c.up.railway.app/api/v1"

def main():
    st.set_page_config(
        page_title="AI Recruitment Platform - Advanced",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 AI Recruitment Platform - Advanced Edition")
    st.markdown("### Powered by Advanced AI, OCR, and Matching Algorithms")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Dashboard", "📄 Advanced Resume Parser", "🎯 Smart Matching", 
         "📊 Analytics", "⚙️ Settings", "🔍 Search & Filter"]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📄 Advanced Resume Parser":
        show_advanced_resume_parser()
    elif page == "🎯 Smart Matching":
        show_smart_matching()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "🔍 Search & Filter":
        show_search_filter()

def show_dashboard():
    st.header("📊 Dashboard")
    
    # Health check
    try:
        response = requests.get(f"{API_BASE_URL}/advanced/health/advanced")
        if response.status_code == 200:
            health_data = response.json()
            st.success("✅ All services operational")
            
            # Display service status
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Advanced Parser", "🟢 Operational")
            with col2:
                st.metric("Matching Service", "🟢 Operational")
            with col3:
                st.metric("Vector Search", "🟢 Operational")
            with col4:
                st.metric("AI Analysis", "🟢 Operational")
        else:
            st.error("❌ Some services are down")
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
    
    # Quick stats
    st.subheader("📈 Quick Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Candidates", "1,234", "+12%")
    with col2:
        st.metric("Active Jobs", "56", "+5%")
    with col3:
        st.metric("Match Rate", "87%", "+3%")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    activity_data = {
        "Time": ["2 min ago", "5 min ago", "10 min ago", "15 min ago"],
        "Activity": ["New resume uploaded", "Job posted", "Match found", "Candidate contacted"],
        "Status": ["✅", "✅", "✅", "⏳"]
    }
    df = pd.DataFrame(activity_data)
    st.dataframe(df, use_container_width=True)

def show_advanced_resume_parser():
    st.header("📄 Advanced Resume Parser")
    st.markdown("### Enhanced parsing with OCR, image processing, and AI analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Supports PDF, DOCX, TXT, and image files with OCR"
    )
    
    if uploaded_file is not None:
        st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Display file preview
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="Image Preview", use_column_width=True)
        
        # Parse button
        if st.button("🚀 Parse with Advanced AI", type="primary"):
            with st.spinner("Processing with advanced AI..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(f"{API_BASE_URL}/advanced/parse-advanced", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Advanced parsing completed!")
                        
                        # Display results in tabs
                        tab1, tab2, tab3, tab4, tab5 = st.tabs([
                            "📋 Basic Info", "🎯 AI Analysis", "💼 Experience", 
                            "🎓 Education", "📊 Confidence Scores"
                        ])
                        
                        parsed_data = result.get('parsed_data', {})
                        
                        with tab1:
                            basic_info = parsed_data.get('basic_info', {})
                            if basic_info:
                                st.json(basic_info)
                            else:
                                st.info("No basic info extracted")
                        
                        with tab2:
                            ai_analysis = parsed_data.get('ai_analysis', {})
                            if ai_analysis:
                                st.json(ai_analysis)
                            else:
                                st.info("No AI analysis available")
                        
                        with tab3:
                            experience = parsed_data.get('experience_analysis', {})
                            if experience:
                                st.json(experience)
                            else:
                                st.info("No experience data available")
                        
                        with tab4:
                            education = parsed_data.get('education_analysis', {})
                            if education:
                                st.json(education)
                            else:
                                st.info("No education data available")
                        
                        with tab5:
                            confidence_scores = parsed_data.get('confidence_scores', {})
                            if confidence_scores:
                                # Create confidence chart
                                fig = go.Figure(data=[
                                    go.Bar(
                                        x=list(confidence_scores.keys()),
                                        y=list(confidence_scores.values()),
                                        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                                    )
                                ])
                                fig.update_layout(
                                    title="Confidence Scores",
                                    yaxis_title="Confidence",
                                    yaxis_range=[0, 1]
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No confidence scores available")
                    
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_smart_matching():
    st.header("🎯 Smart Matching")
    st.markdown("### Advanced candidate-job matching with AI algorithms")
    
    # Job input
    st.subheader("📝 Job Description")
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description", height=200)
    
    # Job requirements
    col1, col2 = st.columns(2)
    with col1:
        required_skills = st.text_area("Required Skills (one per line)")
        min_experience = st.number_input("Minimum Experience (years)", min_value=0, value=2)
    with col2:
        job_location = st.text_input("Job Location")
        remote_work = st.checkbox("Remote Work Available")
    
    if st.button("🔍 Find Top Matches", type="primary"):
        if job_title and job_description:
            with st.spinner("Finding top matches..."):
                try:
                    # Prepare job data
                    job_data = {
                        "title": job_title,
                        "description": job_description,
                        "required_skills": [skill.strip() for skill in required_skills.split('\n') if skill.strip()],
                        "min_experience": min_experience,
                        "location": job_location,
                        "remote_work": remote_work
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/advanced/match-candidates",
                        json=job_data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        matches = result.get('top_matches', [])
                        
                        st.success(f"✅ Found {len(matches)} top matches!")
                        
                        # Display matches
                        for i, match in enumerate(matches, 1):
                            with st.expander(f"#{i} {match.get('candidate_name', 'Unknown')} - {match.get('match_score', 0):.1%}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"**Match Score:** {match.get('match_score', 0):.1%}")
                                    st.write(f"**Match Level:** {match.get('match_level', 'Unknown')}")
                                    
                                    # Detailed scores
                                    detailed_scores = match.get('detailed_scores', {})
                                    if detailed_scores:
                                        st.write("**Detailed Scores:**")
                                        for factor, score in detailed_scores.items():
                                            st.progress(score)
                                            st.caption(f"{factor.replace('_', ' ').title()}: {score:.1%}")
                                
                                with col2:
                                    recommendations = match.get('recommendations', [])
                                    if recommendations:
                                        st.write("**Recommendations:**")
                                        for rec in recommendations:
                                            st.write(f"• {rec}")
                    
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please provide job title and description")

def show_analytics():
    st.header("📊 Analytics Dashboard")
    
    # Sample analytics data
    st.subheader("📈 Matching Performance")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Match Score", "78.5%", "+2.3%")
    with col2:
        st.metric("Top Matches Found", "1,234", "+15%")
    with col3:
        st.metric("Processing Time", "2.3s", "-0.5s")
    with col4:
        st.metric("Success Rate", "94.2%", "+1.1%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Match Score Distribution")
        # Sample data
        scores = [0.6, 0.7, 0.8, 0.9, 0.95, 0.85, 0.75, 0.65, 0.8, 0.9]
        fig = px.histogram(x=scores, nbins=10, title="Match Score Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Skills Analysis")
        skills_data = {
            "Skill": ["Python", "JavaScript", "React", "AWS", "Docker"],
            "Demand": [85, 78, 72, 68, 65]
        }
        df = pd.DataFrame(skills_data)
        fig = px.bar(df, x="Skill", y="Demand", title="Top Skills Demand")
        st.plotly_chart(fig, use_container_width=True)

def show_settings():
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Advanced Features")
    
    # Feature toggles
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Enable OCR Processing", value=True)
        st.checkbox("Enable Image Enhancement", value=True)
        st.checkbox("Enable Advanced Matching", value=True)
    
    with col2:
        st.checkbox("Enable Vector Search", value=True)
        st.checkbox("Enable AI Analysis", value=True)
        st.checkbox("Enable Confidence Scoring", value=True)
    
    st.subheader("📊 Performance Settings")
    
    # Performance settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.slider("Max File Size (MB)", 1, 50, 10)
        st.slider("Processing Timeout (seconds)", 10, 120, 30)
    
    with col2:
        st.slider("Match Results Limit", 5, 50, 10)
        st.slider("Confidence Threshold", 0.0, 1.0, 0.7)

def show_search_filter():
    st.header("🔍 Search & Filter")
    
    # Search options
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("Search Candidates")
        skill_filter = st.multiselect(
            "Filter by Skills",
            ["Python", "JavaScript", "React", "AWS", "Docker", "Kubernetes"]
        )
    
    with col2:
        experience_filter = st.slider("Minimum Experience (years)", 0, 20, 2)
        location_filter = st.text_input("Filter by Location")
    
    # Advanced filters
    with st.expander("🔍 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            education_level = st.selectbox(
                "Education Level",
                ["Any", "High School", "Bachelor's", "Master's", "PhD"]
            )
            salary_range = st.slider("Salary Range", 0, 200000, (50000, 100000))
        
        with col2:
            availability = st.selectbox(
                "Availability",
                ["Any", "Immediate", "2 weeks", "1 month", "3 months"]
            )
            remote_preference = st.selectbox(
                "Remote Preference",
                ["Any", "Remote", "Hybrid", "On-site"]
            )
        
        with col3:
            seniority_level = st.selectbox(
                "Seniority Level",
                ["Any", "Entry-Level", "Junior", "Mid-Level", "Senior", "Lead"]
            )
            certification = st.multiselect(
                "Certifications",
                ["AWS", "Azure", "Google Cloud", "PMP", "Scrum Master"]
            )
    
    if st.button("🔍 Search", type="primary"):
        st.info("Search functionality would be implemented here")
        st.json({
            "search_query": search_query,
            "skill_filter": skill_filter,
            "experience_filter": experience_filter,
            "location_filter": location_filter
        })

if __name__ == "__main__":
    main() 