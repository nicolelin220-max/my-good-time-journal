import streamlit as st
import pandas as pd
from datetime import datetime

# --- SETTINGS & STYLE ---
st.set_page_config(page_title="Good Time Journal", page_icon="🌿")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }
    .main { background-color: #FAF9F6; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
st.title("🌿 My Good Time Journal")
st.write("A space to reflect on what gives you energy and flow.")

# Simple Session State to store data in this demo 
# (In a real deployment, we'd link this to Google Sheets)
if 'journal_data' not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=["Date", "Activity", "Flow", "Energy", "Insights"])

# --- INPUT SECTION ---
with st.expander("✨ Log a New Moment", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now())
        activity = st.text_input("Activity Name", placeholder="e.g., Writing poetry")
    with col2:
        flow = st.select_slider("Engagement (Flow)", options=list(range(11)), value=5)
        energy = st.select_slider("Energy Level", options=list(range(-5, 6)), value=0)
    
    insight = st.text_area("What did you notice? (AEIOU Reflection)", placeholder="Who were you with? How was the environment?")
    
    if st.button("Add to Journal"):
        if activity:
            new_entry = pd.DataFrame([[date, activity, flow, energy, insight]], 
                                     columns=["Date", "Activity", "Flow", "Energy", "Insights"])
            st.session_state.journal_data = pd.concat([st.session_state.journal_data, new_entry], ignore_index=True)
            st.success("Entry saved successfully!")
        else:
            st.error("Please provide an activity name.")

# --- DASHBOARD SECTION ---
if not st.session_state.journal_data.empty:
    df = st.session_state.journal_data
    
    st.divider()
    st.subheader("📊 Your Weekly Pulse")
    
    m1, m2 = st.columns(2)
    m1.metric("Avg Engagement", f"{round(df['Flow'].mean(), 1)} / 10")
    m2.metric("Avg Energy", f"{round(df['Energy'].mean(), 1)} ⚡")

    # Flow vs Energy Chart
    st.line_chart(df.set_index("Date")[["Flow", "Energy"]])

    # History
    st.subheader("📜 Reflection History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No entries yet. Take a moment to record your first 'Good Time'.")