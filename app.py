import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Campus Gatekeeper AI", page_icon="🛡️", layout="centered")
st.title("🛡️ Smart Gatekeeper System")

tab1, tab2 = st.tabs(["Log New Entry (AI)", "Active Campus Dashboard"])

with tab1:
    st.subheader("Fast Entry Logging")
    st.info("Guards: Just type what the visitor says. The AI will sort it out.")
    
    # Wrap in a form so users can hit Enter to submit
    with st.form("entry_form"):
        raw_input = st.text_input("Raw Entry Details", placeholder="e.g. parents of students , no2")
        submitted = st.form_submit_button("Log Entry")
        
        if submitted:
            if not raw_input:
                st.warning("Please enter some text.")
            else:
                with st.spinner("AI is processing and saving to database..."):
                    try:
                        res = requests.post(f"{API_URL}/log-entry", json={"raw_text": raw_input})
                        if res.status_code == 200:
                            data = res.json()["data"]
                            st.success(f"✅ Logged! **Name:** {data['visitor_name']} | **Visiting:** {data['visiting_student']} | **Vehicle:** {data['vehicle_number']}")
                        else:
                            # Show the exact error from the backend
                            st.error(f"Backend Error: {res.json().get('detail', res.text)}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend. Is `uvicorn main:app --reload` running in your other terminal?")

with tab2:
    st.subheader("Currently on Campus")
    
    try:
        # 1. Fetch and show Active Visitors
        res = requests.get(f"{API_URL}/active-visitors")
        if res.status_code == 200:
            visitors = res.json()
            if visitors:
                df = pd.DataFrame(visitors)
                df = df[["id", "visitor_name", "visiting_student", "vehicle_number", "entry_time"]]
                st.dataframe(df, use_container_width=True)
                
                st.markdown("### Log Exit")
                col1, col2 = st.columns([2, 2])
                with col1:
                    # Use a Dropdown menu instead of manual number typing!
                    options = {v["id"]: f"ID {v['id']} - {v['visitor_name']} ({v['vehicle_number']})" for v in visitors}
                    exit_id = st.selectbox("Select Visitor to Exit", options=list(options.keys()), format_func=lambda x: options[x])
                
                with col2:
                    st.write("") # spacing
                    st.write("")
                    if st.button("Confirm Exit"):
                        exit_res = requests.post(f"{API_URL}/log-exit/{exit_id}")
                        if exit_res.status_code == 200:
                            st.success("Exit logged successfully!")
                            st.rerun() # Instantly refresh the page to update the tables
                        else:
                            st.error("Could not log exit.")
            else:
                st.info("No active visitors currently on campus.")

        # 2. Fetch and show Exit History (Previous Records)
        st.markdown("---")
        st.subheader("Exit History (Previous Records)")
        hist_res = requests.get(f"{API_URL}/visitor-history")
        if hist_res.status_code == 200:
            history = hist_res.json()
            if history:
                hist_df = pd.DataFrame(history)
                hist_df = hist_df[["id", "visitor_name", "visiting_student", "vehicle_number", "entry_time", "exit_time"]]
                st.dataframe(hist_df, use_container_width=True)
            else:
                st.write("No previous records yet.")

    except Exception as e:
        st.error(f"Could not load dashboard. Make sure the FastAPI backend is running. Error: {e}")