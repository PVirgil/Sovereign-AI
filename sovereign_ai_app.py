# sovereign_ai_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# General LLM agent

def run_agent(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Sovereign AI, the CFO AI system for private funds, automating legal, financial, treasury, and LP tasks."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Agents

def capital_accounts_agent(df: pd.DataFrame) -> str:
    prompt = f"Prepare capital account summaries for LPs based on this data: {df.head(3).to_dict()}"
    return run_agent(prompt)

def audit_compliance_agent(text: str) -> str:
    prompt = f"Draft a GAAP audit memo and ESG compliance checklist for this fund: {text}"
    return run_agent(prompt)

def lp_relations_agent(question: str, context: str) -> str:
    prompt = f"LP asks: {question}\nContext: {context}\nRespond with a clear, professional LP communication."
    return run_agent(prompt)

def treasury_agent(df: pd.DataFrame) -> str:
    prompt = f"Analyze this fund flow data for treasury insights and optimization: {df.head(3).to_dict()}"
    return run_agent(prompt)

def filing_agent(form_type: str, context: str) -> str:
    prompt = f"Generate a {form_type} filing draft for this fund description: {context}"
    return run_agent(prompt)

def performance_analyst_agent(df: pd.DataFrame) -> str:
    prompt = f"Analyze fund performance from this dataset: {df.head(3).to_dict()}. Report IRR, MOIC, DPI."
    return run_agent(prompt)

def cfo_copilot_agent(question: str, context: str) -> str:
    prompt = f"Context: {context}\nCFO asks: {question}\nReply with a confident, insightful response."
    return run_agent(prompt)

# UI

def main():
    st.set_page_config("Sovereign AI – CFO Copilot", page_icon="🧠", layout="wide")
    st.title("🧠 Sovereign AI – Autonomous CFO Copilot for Fund Ops")
    st.markdown("Automate compliance, treasury, LP relations, filings, and analytics.")

    uploaded_file = st.file_uploader("Upload fund data (CSV)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
    else:
        df = pd.DataFrame()

    tabs = st.tabs([
        "📋 Capital Accounts",
        "📑 Audit & ESG",
        "💬 LP Relations",
        "💰 Treasury",
        "📝 SEC / K-1 Filings",
        "📊 Performance Analyst",
        "💼 CFO Copilot"
    ])

    with tabs[0]:
        st.subheader("📋 Capital Accounts")
        if st.button("Generate Summaries"):
            if df.empty:
                st.error("Please upload data.")
            else:
                result = capital_accounts_agent(df)
                st.text_area("Capital Account Output", result, height=400)

    with tabs[1]:
        st.subheader("📑 Audit & ESG")
        text = st.text_area("Describe fund operations, ESG policies, etc.")
        if st.button("Generate Audit Memo"):
            if not text:
                st.error("Enter context.")
            else:
                result = audit_compliance_agent(text)
                st.text_area("Audit & ESG Output", result, height=400)

    with tabs[2]:
        st.subheader("💬 LP Relations")
        context = st.text_area("Fund summary or prior LP notes")
        q = st.text_input("Enter LP question")
        if st.button("Answer LP"):
            if not q or not context:
                st.error("Provide question and context.")
            else:
                result = lp_relations_agent(q, context)
                st.text_area("LP Response", result, height=300)

    with tabs[3]:
        st.subheader("💰 Treasury Optimizer")
        if st.button("Run Treasury Analysis"):
            if df.empty:
                st.error("Upload fund data first.")
            else:
                result = treasury_agent(df)
                st.text_area("Treasury Analysis", result, height=300)

    with tabs[4]:
        st.subheader("📝 Filing Assistant")
        form = st.selectbox("Select Filing Type", ["K-1", "Form D", "ADV", "ESG Report"])
        info = st.text_area("Fund Info / Context")
        if st.button("Draft Filing"):
            if not info:
                st.error("Provide fund description.")
            else:
                result = filing_agent(form, info)
                st.text_area("Draft Filing", result, height=400)

    with tabs[5]:
        st.subheader("📊 Performance Analytics")
        if st.button("Analyze Fund Performance"):
            if df.empty:
                st.error("Upload performance data.")
            else:
                result = performance_analyst_agent(df)
                st.text_area("Performance Report", result, height=300)

    with tabs[6]:
        st.subheader("💼 CFO Copilot")
        context = st.text_area("Describe fund ops situation")
        q = st.text_input("Ask your CFO AI anything")
        if st.button("Ask Copilot"):
            if not context or not q:
                st.error("Enter both context and question.")
            else:
                result = cfo_copilot_agent(q, context)
                st.text_area("AI Response", result, height=300)

if __name__ == "__main__":
    main()
