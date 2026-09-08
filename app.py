import streamlit as st
import pandas as pd

from chatbot import ask_bot
from email_generator import generate_email
from lead_qualifier import qualify_lead
from crm import save_lead, get_all_leads, delete_lead
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
st.markdown("AI-powered Sales Automation, Lead Qualification, CRM Management and Customer Support Platform.")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chatbot",
    "🎯 Lead Qualification",
    "📧 Email Generator",
    "📊 CRM Dashboard"
])

# =====================================================
# TAB 1 — CHATBOT
# =====================================================

with tab1:

    st.subheader("💬 Customer Support Chatbot")
    st.caption("Ask anything about our services, pricing, refunds or support.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your question here...")

    if user_input:

        # Show user message
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_bot(user_input)
            st.write(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# =====================================================
# TAB 2 — LEAD QUALIFICATION
# =====================================================

with tab2:

    st.subheader("🎯 Lead Qualification Form")
    st.caption("Fill in the lead details. AI will score and categorize the lead automatically.")

    with st.form("lead_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            company = st.text_input("Company *")

        with col2:
            budget = st.number_input("Budget ($) *", min_value=0, step=100, value=0)
            requirement = st.text_area("Project Requirement *", height=130)

        submitted = st.form_submit_button("🚀 Qualify & Save Lead", use_container_width=True)

    if submitted:

        errors = []

        if not name.strip():
            errors.append("Full Name is required.")
        if not email.strip():
            errors.append("Email is required.")
        elif "@" not in email:
            errors.append("Please enter a valid email address.")
        if not company.strip():
            errors.append("Company is required.")
        if not requirement.strip():
            errors.append("Project Requirement is required.")

        if errors:
            for err in errors:
                st.error(err)

        else:

            with st.spinner("Analyzing lead with AI..."):
                score = qualify_lead(budget, requirement)

            try:
                save_lead(
                    name=name.strip(),
                    email=email.strip(),
                    company=company.strip(),
                    budget=budget,
                    requirement=requirement.strip(),
                    score=score
                )

                if score >= 80:
                    category = "🔥 HOT LEAD"
                    color = "success"
                elif score >= 60:
                    category = "🟡 WARM LEAD"
                    color = "warning"
                else:
                    category = "🔴 COLD LEAD"
                    color = "error"

                st.success(f"✅ Lead saved successfully!")

                r1, r2 = st.columns(2)
                r1.metric("AI Lead Score", f"{score} / 100")
                r2.metric("Lead Category", category)

            except Exception as e:
                st.error(f"Database Error: {str(e)}")

# =====================================================
# TAB 3 — EMAIL GENERATOR
# =====================================================

with tab3:

    st.subheader("📧 AI Sales Email Generator")
    st.caption("Generate a professional, personalized sales email in seconds.")

    client_name = st.text_input("Client Name", key="email_name")
    client_requirement = st.text_area("Client Requirement", key="email_req", height=120)

    if st.button("✉️ Generate Email", use_container_width=True):

        if not client_name.strip():
            st.warning("Please enter the client name.")

        elif not client_requirement.strip():
            st.warning("Please enter the client requirement.")

        else:

            with st.spinner("Generating email..."):
                email_text = generate_email(client_name.strip(), client_requirement.strip())

            st.success("Email generated!")
            st.text_area("Generated Email", value=email_text, height=400, key="email_output")

            st.download_button(
                label="📥 Download Email as .txt",
                data=email_text,
                file_name=f"sales_email_{client_name.strip().replace(' ', '_')}.txt",
                mime="text/plain"
            )

# =====================================================
# TAB 4 — CRM DASHBOARD
# =====================================================

with tab4:

    st.subheader("📊 CRM Dashboard")

    df = get_all_leads()

    if df.empty:
        st.info("No leads found in CRM. Start by adding leads in the Lead Qualification tab.")

    else:

        total_leads = len(df)
        hot_leads   = len(df[df["score"] >= 80])
        warm_leads  = len(df[(df["score"] >= 60) & (df["score"] < 80)])
        cold_leads  = len(df[df["score"] < 60])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📋 Total Leads", total_leads)
        c2.metric("🔥 Hot Leads",   hot_leads)
        c3.metric("🟡 Warm Leads",  warm_leads)
        c4.metric("🔴 Cold Leads",  cold_leads)

        st.divider()

        # Add lead status column
        def classify(score):
            if score >= 80:
                return "🔥 Hot"
            elif score >= 60:
                return "🟡 Warm"
            return "🔴 Cold"

        df["Status"] = df["score"].apply(classify)

        # Filter controls
        col_filter, col_sort = st.columns([2, 2])

        with col_filter:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "🔥 Hot", "🟡 Warm", "🔴 Cold"],
                key="crm_filter"
            )

        with col_sort:
            sort_by = st.selectbox(
                "Sort by",
                ["Newest First", "Score (High to Low)", "Score (Low to High)"],
                key="crm_sort"
            )

        filtered_df = df.copy()

        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]

        if sort_by == "Newest First":
            filtered_df = filtered_df.sort_values("id", ascending=False)
        elif sort_by == "Score (High to Low)":
            filtered_df = filtered_df.sort_values("score", ascending=False)
        else:
            filtered_df = filtered_df.sort_values("score", ascending=True)

        st.dataframe(
            filtered_df[["id", "name", "email", "company", "budget", "requirement", "score", "Status", "created_at"]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # Export and Delete
        export_col, delete_col = st.columns([3, 1])

        with export_col:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export All Leads as CSV",
                data=csv,
                file_name="crm_leads.csv",
                mime="text/csv"
            )

        with delete_col:
            lead_ids = df["id"].tolist()
            del_id = st.selectbox("Delete Lead by ID", ["Select..."] + lead_ids, key="del_id")

            if st.button("🗑️ Delete Lead", key="del_btn"):
                if del_id != "Select...":
                    delete_lead(int(del_id))
                    st.success(f"Lead #{del_id} deleted.")
                    st.rerun()
                else:
                    st.warning("Please select a lead ID to delete.")
