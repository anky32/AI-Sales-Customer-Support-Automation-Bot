import streamlit as st
import pandas as pd

from chatbot import ask_bot
from email_generator import generate_email
from lead_qualifier import qualify_lead
from crm import save_lead, get_all_leads
from database import create_database

# Initialize Database
create_database()

# Page Config
st.set_page_config(
    page_title="AI Sales & Support Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Sales & Customer Support Automation Bot")

st.markdown(
    """
    AI-powered Sales Automation, Lead Qualification,
    CRM Management and Customer Support Platform.
    """
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💬 Chatbot",
        "🎯 Lead Qualification",
        "📧 Email Generator",
        "📊 CRM Dashboard"
    ]
)

# =====================================================
# CHATBOT
# =====================================================

with tab1:

    st.subheader("Customer Support Chatbot")

    question = st.text_input(
        "Ask a Question"
    )

    if st.button("Chat"):

        if question:

            with st.spinner("Thinking..."):

                answer = ask_bot(question)

            st.success("Response")

            st.write(answer)

        else:

            st.warning(
                "Please enter a question."
            )

# =====================================================
# LEAD QUALIFICATION
# =====================================================

with tab2:

    st.subheader("Lead Qualification Form")

    name = st.text_input(
        "Full Name",
        key="lead_name"
    )

    email = st.text_input(
        "Email",
        key="lead_email"
    )

    company = st.text_input(
        "Company",
        key="lead_company"
    )

    budget = st.number_input(
        "Budget ($)",
        min_value=0,
        step=100,
        value=0,
        key="lead_budget"
    )

    requirement = st.text_area(
        "Project Requirement",
        key="lead_requirement"
    )

    if st.button(
        "Save Lead",
        key="save_lead_btn"
    ):

        # Validation
        if len(name.strip()) == 0:
            st.error("Please enter Name")

        elif len(email.strip()) == 0:
            st.error("Please enter Email")

        elif len(company.strip()) == 0:
            st.error("Please enter Company")

        elif len(requirement.strip()) == 0:
            st.error("Please enter Project Requirement")

        else:

            try:

                score = qualify_lead(budget)

                save_lead(
                    name=name,
                    email=email,
                    company=company,
                    budget=budget,
                    requirement=requirement,
                    score=score
                )

                if score >= 80:
                    category = "🔥 HOT LEAD"

                elif score >= 60:
                    category = "🟡 WARM LEAD"

                else:
                    category = "🔴 COLD LEAD"

                st.success(
                    f"""
                    Lead Saved Successfully!

                    Lead Score: {score}

                    Category: {category}
                    """
                )

            except Exception as e:

                st.error(
                    f"Database Error: {str(e)}"
                )

                
# =====================================================
# EMAIL GENERATOR
# =====================================================

with tab3:

    st.subheader(
        "AI Sales Email Generator"
    )

    client_name = st.text_input(
        "Client Name"
    )

    client_requirement = st.text_area(
        "Client Requirement"
    )

    if st.button(
        "Generate Email"
    ):

        if client_name and client_requirement:

            with st.spinner(
                "Generating Email..."
            ):

                email_text = generate_email(
                    client_name,
                    client_requirement
                )

            st.success(
                "Email Generated"
            )

            st.text_area(
                "Generated Email",
                value=email_text,
                height=350
            )

        else:

            st.warning(
                "Please fill all fields."
            )

# =====================================================
# CRM DASHBOARD
# =====================================================

with tab4:

    st.subheader("CRM Dashboard")

    df = get_all_leads()

    if not df.empty:

        total_leads = len(df)

        hot_leads = len(
            df[df["score"] >= 80]
        )

        warm_leads = len(
            df[
                (df["score"] >= 60)
                &
                (df["score"] < 80)
            ]
        )

        cold_leads = len(
            df[df["score"] < 60]
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Leads",
            total_leads
        )

        col2.metric(
            "🔥 Hot Leads",
            hot_leads
        )

        col3.metric(
            "🟡 Warm Leads",
            warm_leads
        )

        col4.metric(
            "🔴 Cold Leads",
            cold_leads
        )

        st.divider()

        st.subheader("Lead Database")

        def classify(score):

            if score >= 80:
                return "Hot"

            elif score >= 60:
                return "Warm"

            return "Cold"

        df["Lead Status"] = df[
            "score"
        ].apply(classify)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Export Leads CSV",
            data=csv,
            file_name="crm_leads.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No leads found in CRM."
        )