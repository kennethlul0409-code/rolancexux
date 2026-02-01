import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 系統設定 (必須放在第一行)
# ==========================================
st.set_page_config(
    page_title="文心老師作文批閱",
    page_icon="🪶",
    layout="centered"
)

# ==========================================
# 2. API 與核心變數設定
# ==========================================

# ⚠️ 已填入您的 API KEY
API_KEY = "AIzaSyDULJDZicXPlA9g_5Hoj0oYv9XPhUuK3LA"

# 設定 API
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API Key 設定錯誤：{e}")

# 補充墨水的通關密碼
REFILL_PASSWORD = "anxux123"

# 初始化 Session State (記憶體)
if 'credits' not in st.session_state:
    st.session_state.credits = 10
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'grading_result' not in st.session_state:
    st.session_state.grading_result = None
if 'model_result' not in st.session_state:
    st.session_state.model_result = None

# ==========================================
# 3. 樣式設計 (還原木質風格)
# ==========================================
st.markdown("""
<style>
    /* 全站背景 */
    .stApp {
        background-color: #EFEBE9;
        background-image: radial-gradient(#D7CCC8 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* 文字顏色 - 深咖啡色 */
    h1, h2, h3, h4, p, div, span, label, li {
        color: #3E2723 !important;
        font-family: "Noto Serif TC", "Microsoft JhengHei", serif;
    }
    
    /* 按鈕樣式 (仿木紋) */
    div.stButton > button {
        background: linear-gradient(to bottom, #6D4C41, #4E342E);
        color: #FFECB3 !important;
        border: 2px solid #3E2723;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 0 #271c19;
        transition: all 0.2s;
        width: 100%;
        margin-top: 10px;
        padding: 10px 0;
    }
    div.stButton > button:hover {
        filter: brightness(1.1);
        transform: translateY(-2px);
    }
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: none;
    }
    
    /* 輸入框樣式 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FAF9F6;
        border: 2px solid #8D6E63;
        color: #3E2723;
    }
    
    /* 卡片區塊 */
    .wood-card {
        background-color: #FAF9F6;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #D7CCC8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* 墨水耗盡警告 */
    .no-ink {
        color: #D84315;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True    