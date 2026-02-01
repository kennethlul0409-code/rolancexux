import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ==========================================
# 1. 設定與樣式 (仿造原本的木質與紙張風格)
# ==========================================
st.set_page_config(
    page_title="文心老師作文批閱",
    page_icon="🪶",
    layout="centered"
)

# 自訂 CSS 樣式 (移植原本的 Tailwind 色調)
st.markdown("""
<style>
    /* 背景色 */
    .stApp {
        background-color: #EFEBE9;
        background-image: radial-gradient(#D7CCC8 1px, transparent 1px);
        background-size: 20px 20px;
    }
    /* 標題字體 */
    h1, h2, h3 {
        color: #5D4037 !important;
        font-family: "Noto Serif TC", serif;
    }
    /* 按鈕樣式 (木紋風格) */
    .stButton>button {
        background: linear-gradient(to bottom, #6D4C41, #4E342E);
        color: #FFECB3 !important;
        border: 2px solid #3E2723;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
    }
    /* 區塊樣式 */
    .paper-card {
        background-color: #FAF9F6;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #D7CCC8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .feedback-box {
        background-color: #FAF9F6;
        padding: 25px;
        border-radius: 8px;
        border-left: 5px solid #8D6E63;
        font-family: "Noto Serif TC", serif;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 系統邏輯與 API 設定
# ==========================================

# ⚠️ 請在此填入你的 Gemini API Key，或是從 Streamlit Secrets 讀取
# 建議之後設定在 Streamlit Cloud 的 Secrets 裡，這裡先用變數示範
# 如果你有設定 secrets，請改用 st.secrets["GEMINI_API_KEY"]
API_KEY = "AIzaSyDULJDZicXPlA9g_5Hoj0oYv9XPhUuK3LA" 

try:
    genai.configure(api_key=API_KEY)
except:
    st.error("請確認 API Key 是否正確設定。")

# 積分系統設定
MAX_CREDITS = 10
REFILL_PASSWORD = "anxux123"

# 初始化 Session State (記憶體)
if 'credits' not in st.session_state:
    st.session_state.credits = MAX_CREDITS
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'result' not in st.session_state:
    st.session_state.result = None

# ==========================================
# 3. Prompt (提示詞) 設定 - 核心靈魂
# ==========================================

BODHISATTVA_PROMPT = """
你是一位慈悲為懷、溫柔敦厚的資深國文老師「文心菩薩」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇學生的作文？
2. 如果內容無效（如亂碼、網址、無意義文字），請回傳 `[REJECT]` 開頭的訊息。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出使用 Markdown 格式，包含：
### 🌸 總體評分
### ✨ 亮點讚賞
### 💡 名師建議 (不少於100字，語氣溫柔婉轉)
### 📖 推薦詞句

風格：如春風般溫柔，多給予鼓勵。使用繁體中文。
"""

VAJRA_PROMPT = """
你是一位嚴格苛刻、目光如炬的資深國文總編輯「怒目金剛」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇值得批閱的作文？
2. 如果內容無效，請回傳 `[REJECT]` 開頭的訊息並嚴厲斥責。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出使用 Markdown 格式，包含：
### 🔥 總體評分
### ⚡ 毒舌點評 (直指核心問題)
### 🔨 嚴格建議 (不少於100字，不留情面)
### 🚀 改進方向

風格：嚴厲、直接、高標準，雞蛋裡挑骨頭。使用繁體中文。
"""

MODEL_ESSAY_PROMPT = """
你是一位榮獲文學獎的資深作家。請根據題目、文體與等級撰寫範文。
【格式要求】：每個段落開頭必須包含兩個全形空格（　　）。
請直接輸出範文內容。
"""

# ==========================================
# 4. 功能函數
# ==========================================

def deduct_credit():
    if st.session_state.credits > 0:
        st.session_state.credits -= 1
        return True
    return False

def refill_credits(password):
    if password == REFILL_PASSWORD:
        st.session_state.credits = MAX_CREDITS
        return True
    return False

def get_gemini_response(prompt, content, is_image=False):
    model = genai.GenerativeModel('gemini-1.5-flash') # 使用最新的 flash 模型
    
    try:
        if is_image:
            response = model.generate_content([prompt, content])
        else:
            response = model.generate_content(prompt + "\n\n學生作文：\n" + content)
        return response.text
    except Exception as e:
        return f"發生錯誤：{str(e)}"

# ==========================================
# 5. 介面呈現 (UI)
# ==========================================

# 頂部導覽列
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🪶 文心老師")
    st.caption("智慧作文批閱系統")
with col2:
    st.metric("剩餘墨水", f"{st.session_state.credits} / {MAX_CREDITS}")

# --- 頁面路由 ---

# 1. 首頁 (Home)
if st.session_state.page == 'home':
    st.markdown("### 請選擇您的學習模式")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("🖊️ **作文批閱**\n\n上傳作文，獲得專業評語。")
        if st.button("進入批閱模式"):
            st.session_state.page = 'grading_setup'
            st.rerun()
            
    with c2:
        st.success("📖 **範文參考**\n\n輸入題目，生成名師範文。")
        if st.button("進入範文模式"):
            st.session_state.page = 'model_essay'
            st.rerun()

    # 補充墨水區
    if st.session_state.credits == 0:
        st.warning("⚠️ 墨水已耗盡")
        