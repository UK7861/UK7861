import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Friday Management Control Room", layout="wide")

API_URL = "http://localhost:8000"

st.title("🚀 Friday — Management Control Room")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("System Status")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()
        st.metric("System Health", state["status"])
        st.metric("Missions Completed", state["mission_count"])
        st.metric("Agents Online", state["agents_online"])
    except:
        st.error("Could not connect to API Server")

    st.subheader("Mission Control")
    client_req = st.text_area("Enter Client Requirements")
    if st.button("Launch Mission"):
        st.info("Mission sequence initiated via Main Agent...")
        # In a real app, this would call main.py's run_agency_mission

with col2:
    st.header("Real-time Agent Activities")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()

        # Display agent vitals
        vitals = state.get("agent_vitals", {})
        if vitals:
            for agent, data in vitals.items():
                st.write(f"**{agent}**")
                st.progress(data["progress"])
                st.caption(f"Status: {data['status']}")
        else:
            st.info("No active agent tasks.")

    except:
        st.error("Data unavailable")

    st.header("Recent Mission Logs")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()
        logs = state.get("logs", [])
        if logs:
            log_df = pd.DataFrame(logs)
            st.table(log_df.tail(10))
    except:
        st.write("Logs unavailable")

st.sidebar.header("Friday Settings")
st.sidebar.checkbox("Auto-Scout Mode", value=True)
st.sidebar.checkbox("Autonomous Cycle", value=False)
if st.sidebar.button("Refresh Data"):
    st.rerun()
