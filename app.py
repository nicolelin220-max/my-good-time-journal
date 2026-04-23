import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. 頁面配置與溫馨樣式設定 ---
st.set_page_config(page_title="Good Time Journal", page_icon="🌿", layout="centered")

# 這裡整合了字體、暖色調背景以及針對深色模式的 Metric 顯示修正
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Quicksand', sans-serif; 
    }

    .main { background-color: #FAF9F6; }

    /* 針對 Metric 記憶卡片的深色模式修正：確保白底黑字 */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #F0EAD6;
    }

    /* 強制 Label (標題，如 Avg Engagement) 顏色 */
    [data-testid="stMetricLabel"] > div {
        color: #555e6d !important;
    }

    /* 強制 Value (數值，如 5.0/10) 顏色 */
    [data-testid="stMetricValue"] > div {
        color: #1a1c1f !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 建立 Google Sheets 雲端連線 ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 讀取現有資料 (ttl=0 確保每次都抓取最新狀態)
try:
    existing_data = conn.read(ttl=0)
except Exception:
    # 若讀取失敗（例如第一次執行），建立空表格
    existing_data = pd.DataFrame(columns=["Date", "Activity", "Flow", "Energy", "Insights"])

# --- 3. 標題區塊 ---
st.title("🌿 My Good Time Journal")
st.write("Welcome back. Let's record the energy of your day.")

# --- 4. 輸入紀錄區塊 (使用 Form 確保提交穩定) ---
with st.expander("✨ Log a New Moment", expanded=True):
    with st.form("journal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date_val = st.date_input("Date", datetime.now())
            activity_val = st.text_input("Activity Name", placeholder="e.g., Drafting the workflow")
        with col2:
            flow_val = st.select_slider("Engagement (Flow)", options=list(range(11)), value=5)
            energy_val = st.select_slider("Energy Level", options=list(range(-5, 6)), value=0)
        
        insight_val = st.text_area("What did you notice? (AEIOU Reflection)", placeholder="Environment, Interaction, etc.")
        
        submitted = st.form_submit_button("Save to Cloud")
        
        if submitted:
            if activity_val:
                # 建立新資料列 (日期轉為字串方便儲存)
                new_entry = pd.DataFrame([[str(date_val), activity_val, flow_val, energy_val, insight_val]], 
                                         columns=["Date", "Activity", "Flow", "Energy", "Insights"])
                
                # 合併舊資料與新資料，並更新回 Google Sheets
                updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                conn.update(data=updated_df)
                
                st.success("Entry saved to Google Sheets!")
                st.rerun() # 自動重新整理，更新下方圖表
            else:
                st.error("Please enter an activity name to save.")

# --- 5. 數據呈現與歷史紀錄 ---
if not existing_data.empty:
    st.divider()
    st.subheader("📊 Your Weekly Pulse")
    
    # 指標顯示 (已透過 CSS 修正深色模式問題)
    m1, m2 = st.columns(2)
    m1.metric("Avg Engagement", f"{round(pd.to_numeric(existing_data['Flow']).mean(), 1)} / 10")
    m2.metric("Avg Energy", f"{round(pd.to_numeric(existing_data['Energy']).mean(), 1)} ⚡")

    # 趨勢圖表
    st.line_chart(existing_data.set_index("Date")[["Flow", "Energy"]])

    # 歷史資料表格
    st.subheader("📜 Reflection History")
    st.dataframe(existing_data.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("Your journal is empty. Take a moment to record your first 'Good Time'! 🌸")

st.markdown("---")
st.caption("Capture patterns, design your life.")
