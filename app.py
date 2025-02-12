import streamlit as st
import pandas as pd

def main():
    # Hide all streamlit elements and github profile
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1rs6os {visibility: hidden;}
        .css-1lsmgbg {display: none;}
        .css-6qob1r {visibility: hidden;}
        .css-erpbk7 {display: none;}
        .stDeployButton {display: none;}
        .viewerBadge_container__1QSob {display: none;}
        .viewerBadge_link__1S137 {display: none;}
        div.stToolbar {display: none;}
        .css-eh5xgm {visibility: hidden;}
        .css-1avcm0n {visibility: hidden;}
        .css-14xtw13 {visibility: hidden;}
        section[data-testid="stSidebar"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.set_page_config(
        page_title="PARSS Calculator",
        page_icon="🏥",
        layout="wide"
    )

    st.title("Post-Adenotonsillectomy Risk Stratification System (PARSS) Calculator")
    st.markdown("### A Clinical Tool for Pediatric Otolaryngologists")

    # Initialize session state for total score if not exists
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Patient Risk Factors")
        
        # Age Category
        age_category = st.radio(
            "Age Category",
            options=["< 5 years", "5-9 years", "≥ 10 years"],
            horizontal=True
        )
        age_score = {"< 5 years": 1, "5-9 years": 2, "≥ 10 years": 0}[age_category]

        # Primary Indication
        indication = st.radio(
            "Primary Indication",
            options=["OSA/Sleep-disordered breathing", "Recurrent tonsillitis", "Adenotonsillar hypertrophy"],
            horizontal=True
        )
        indication_score = {
            "OSA/Sleep-disordered breathing": 2,
            "Recurrent tonsillitis": 0,
            "Adenotonsillar hypertrophy": 1
        }[indication]

        # Tonsil Size
        tonsil_size = st.radio(
            "Tonsil Size",
            options=["Grade 1-2", "Grade 3", "Grade 4"],
            horizontal=True
        )
        tonsil_score = {"Grade 1-2": 0, "Grade 3": 1, "Grade 4": 2}[tonsil_size]

        # Comorbidities (multiple selection)
        comorbidities = st.multiselect(
            "Comorbidities",
            options=["Asthma", "Obesity (BMI > 95th percentile)"],
            help="Select all that apply"
        )
        comorbidity_score = 0
        if "Asthma" in comorbidities:
            comorbidity_score += 2
        if "Obesity (BMI > 95th percentile)" in comorbidities:
            comorbidity_score += 1

        # Sleep Study
        sleep_study = st.radio(
            "Pre-op Sleep Study (if available)",
            options=["AHI > 10", "AHI 5-10", "AHI < 5 or not available"],
            horizontal=True
        )
        sleep_score = {"AHI > 10": 2, "AHI 5-10": 1, "AHI < 5 or not available": 0}[sleep_study]

        # Calculate total score
        total_score = age_score + indication_score + tonsil_score + comorbidity_score + sleep_score

    with col2:
        st.subheader("Risk Assessment")
        st.markdown(f"### Total Risk Score: {total_score}")
        
        # Determine risk level and color
        if total_score <= 2:
            risk_level = "Low Risk"
            color = "green"
        elif total_score <= 5:
            risk_level = "Moderate Risk"
            color = "orange"
        else:
            risk_level = "High Risk"
            color = "red"
        
        st.markdown(f"### Risk Level: :{color}[{risk_level}]")

        # Special alerts
        if "Asthma" in comorbidities and indication == "OSA/Sleep-disordered breathing":
            st.warning("⚠️ Automatic High-Risk: OSA + Asthma combination")
        
        if tonsil_size == "Grade 4" and "Obesity (BMI > 95th percentile)" in comorbidities:
            st.warning("⚠️ Automatic High-Risk: Grade 4 tonsils + Obesity")

    # Recommendations section
    st.markdown("---")
    st.subheader("Recommended Monitoring Protocol")

    if total_score <= 2:
        st.info("""
        📋 Low Risk Protocol:
        - Standard follow-up at 1 week, 1 month, 3 months
        - Weight checks at each visit
        - Basic post-operative care instructions
        """)
    elif total_score <= 5:
        st.warning("""
        📋 Moderate Risk Protocol:
        - Additional visits at 2 weeks and 2 months
        - Monthly weight monitoring for 6 months
        - Consider nutritionist referral
        - Monthly weight tracking
        """)
    else:
        st.error("""
        📋 High Risk Protocol:
        - Weekly weight checks first month
        - Monthly specialist follow-up for 6 months
        - Mandatory nutritionist referral
        - Sleep study follow-up if indicated
        - Comprehensive weight management program
        """)

    # Footer with information
    st.markdown("---")
    st.markdown("""
    *Note: This risk stratification system is based on analysis of 4,987 pediatric adenotonsillectomy cases. 
    Clinical judgment should always be exercised in individual patient management.*
    """)

if __name__ == "__main__":
    main()
