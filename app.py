import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Campus Gatekeeper AI", layout="wide")
st.title("🛡️ Smart Gatekeeper System")

tab1, tab2 = st.tabs(["Log New Entry (AI)", "Active Campus Dashboard"])

with tab1:
    st.subheader("Fast Entry Logging")
    st.info("Guards: Just type what the visitor says. The AI will sort it out.")
    raw_input = st.text_input("Raw Entry Details", placeholder="e.g. Suresh is here to meet Amit in Room 402 driving bike DL4S9876")
    
    if st.button("Log Entry"):
        if raw_input:
            with st.spinner("AI is processing and saving to database..."):
                res = requests.post(f"{API_URL}/log-entry", json={"raw_text": raw_input})
                if res.status_code == 200:
                    data = res.json()["data"]
                    st.success(f"Logged! Name: {data['visitor_name']} | Visiting: {data['visiting_student']} | Vehicle: {data['vehicle_number']}")
                else:
                    st.error("Failed to log entry. Is the backend running?")

with tab2:
    st.subheader("Currently on Campus")
    if st.button("Refresh Data"):
        res = requests.get(f"{API_URL}/active-visitors")
        if res.status_code == 200:
            visitors = res.json()
            if visitors:
                df = pd.DataFrame(visitors)
                df = df[["id", "visitor_name", "visiting_student", "vehicle_number", "entry_time"]]
                st.dataframe(df, use_container_width=True)
                
                st.markdown("### Log Exit")
                exit_id = st.number_input("Enter Visitor ID to log exit", min_value=1, step=1)
                if st.button("Confirm Exit"):
                    exit_res = requests.post(f"{API_URL}/log-exit/{exit_id}")
                    if exit_res.status_code == 200:
                        st.success("Exit logged successfully! Refresh data to update.")
                    else:
                        st.error("Could not log exit.")
            else:
                st.write("No active visitors on campus.")