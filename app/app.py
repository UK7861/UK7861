import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Friday Management Control Room", layout="wide", page_icon="🚀")

API_URL = "http://localhost:8000"

st.title("🚀 Friday — Management Control Room")
st.markdown("### Powered by JARVIS-Core v4.0 (Humanoid Intelligence)")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Global State")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Health", state["status"])
        m2.metric("Missions", state["mission_count"])
        m3.metric("Intel Level", state["intelligence_level"])
        m4.metric("Core", state["core_version"])
    except:
        st.error("Connection to Friday Core lost.")

    st.subheader("Command Interface")
    voice_input = st.text_input("Enter Command (English/Roman Urdu) 🎤")
    if st.button("Transmit Command"):
        if voice_input:
            st.success(f"Command '{voice_input}' transmitted to Friday CEO.")
            requests.post(f"{API_URL}/log", json={"message": f"CONTROL ROOM COMMAND: {voice_input}", "level": "INFO"})

    st.subheader("Agent Factory")
    if st.button("Synthesize New Agent"):
        st.info("Initiating workforce expansion sequence...")
        requests.post(f"{API_URL}/log", json={"message": "Manual Agent Synthesis Triggered.", "level": "WARNING"})

with col2:
    st.header("Dynamic Agent Intelligence")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()

        vitals = state.get("agent_vitals", {})
        if vitals:
            for agent, data in vitals.items():
                with st.expander(f"Agent: {agent} - {data['status']}"):
                    st.progress(data["progress"])
                    st.write(f"Vitals: {data['progress']}% | Integrity: 100%")
                    if agent == "QA Agent" and data.get("alerts", 0) > 0:
                        st.warning(f"Self-Healing active: {data['alerts']} alerts resolved.")
        else:
            st.info("All agents in Standby Mode.")

    except:
        st.error("Real-time telemetry unavailable.")

    st.header("Unified Mission Logs")
    try:
        response = requests.get(f"{API_URL}/state")
        state = response.json()
        logs = state.get("logs", [])
        if logs:
            log_df = pd.DataFrame(logs)
            st.dataframe(log_df.tail(20), use_container_width=True)
    except:
        st.write("Log buffer inaccessible.")

st.sidebar.image("https://img.icons8.com/nolan/256/iron-man.png", width=100)
st.sidebar.header("Operational Mode")
st.sidebar.toggle("Autonomous Expansion", value=True)
st.sidebar.toggle("Self-Healing Protocols", value=True)
st.sidebar.toggle("Scout Global Mode", value=True)

if st.sidebar.button("System Reboot"):
    st.warning("Rebooting Friday sub-systems...")
    requests.post(f"{API_URL}/log", json={"message": "System Reboot Initiated.", "level": "ERROR"})
