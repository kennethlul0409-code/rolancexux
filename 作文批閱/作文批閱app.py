import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 系統設定與樣式 (還原木質風格)
# ==========================================
st.set_page_config(page_title="文心老師作文批閱", page_icon="🪶", layout="centered")

# ⚠️⚠️⚠️ 請在此填入你的 API KEY ⚠️⚠️⚠️
API_KEY = "這裡貼上你的_API_KEY" 

# 設定 API
try:
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key 設定有誤，請檢查程式碼第 11 行。")

# 注入 CSS 樣式 (仿造你的 React Tailwind 風格)
st.markdown("""
<style>
    /* 全站背景 */
    .stApp {
        background-color: #EFEBE9;
        background-image: radial-gradient(#D7CCC8 1px, transparent 1px);
        background-size: 20px 20px;
    }
    /* 字體顏色 */
    h1, h2, h3, p, div, span, label {
        color: #3E2723 !important;
        font-family: "Noto Serif TC", serif;
    }
    /* 按鈕樣式 (仿木紋) */
    div.stButton > button {
        background: linear-gradient(to bottom, #6D4C41, #4E342E);
        color: #FFECB3 !important;
        border: 2px solid #3E2723;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 0 #271c19;
        transition: all 0.2s;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: none;
    }
    /* 次要按鈕 (返回鍵) */
    .secondary-btn > button {
        background: #FAF9F6;
        color: #5D4037 !important;
        border: 2px solid #A1887F;
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
    /* 墨水顯示 */
    [data-testid="stMetricValue"] {
        color: #D84315 !important;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心 Prompt (從你的 React 程式碼原樣搬運)
# ==========================================

BODHISATTVA_INSTRUCTION = """
你是一位慈悲為懷、溫柔敦厚的資深國文老師「文心菩薩」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇學生的作文？
2. 如果內容僅是「網址連結」、「一句話的題目」、「亂碼」、「非作文的說明文字」或「極短的無意義語句」，請直接退件。

【退件處理】：
若判定無效，請回傳以 `[REJECT]` 開頭的訊息。
語氣要求：溫柔婉轉，說明這看起來不像作文，請孩子重新上傳。並告知這次不扣墨水。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出必須包含：【總體評分】、【亮點讚賞】、【名師建議】(不少於100字)、【推薦詞句】。

風格與規範：
1. **嚴禁無中生有**：絕對不能評論文章中「不存在」的情節或優點。
2. 語氣要如同春風般溫柔，多給予鼓勵與肯定。
3. 即使有缺點，也要用委婉的方式提出建議。
4. 使用繁體中文。
"""

VAJRA_INSTRUCTION = """
你是一位嚴格苛刻、目光如炬的資深國文總編輯「怒目金剛」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇值得批閱的作文？
2. 如果內容僅是「網址連結」、「一句話的題目」、「亂碼」、「非作文的說明文字」或「極短的無意義語句」，請直接退件。

【退件處理】：
若判定無效，請回傳以 `[REJECT]` 開頭的訊息。
語氣要求：嚴厲斥責，大罵這是敷衍了事，要求重寫。並告知這次「暫且」不扣墨水。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出必須包含：【總體評分】、【毒舌點評】、【嚴格建議】(不少於100字)、【改進方向】。

風格與規範：
1. **嚴禁無中生有**：若文章內容空洞，就直接罵它空洞。
2. 語氣要嚴厲、直接，不留情面，極盡刁難。
3. 專注於找出邏輯漏洞、用詞不當、結構鬆散之處。
4. 使用繁體中文。
"""

MODEL_ESSAY_INSTRUCTION = """
你是一位榮獲多項文學獎的資深作家與國文名師。
請根據使用者提供的「題目」、「文體」與「等級」，撰寫一篇高品質的範文。

【嚴格文體規範】：
1. 記敘文：核心寫人記事，結構要有起因經過結果。
2. 抒情文：運用感官描寫，文字優美感性。
3. 議論文：必須包含論點、論據、論證，採三段式或四段式結構。

【格式規範】：
**重要：** 每個段落的開頭必須「強制」包含兩個全形空格（　　）作為縮排。

輸出格式：
請直接輸出範文內容，不需要額外的寒暄。
若題目為空，請自行根據「文體」與「等級」擬定一個適合的經典題目。
"""

# ==========================================
# 3. 狀態管理 (Session State)
# ==========================================
# 初始化變數
if 'credits' not in st.session_state:
    st.session_state.credits = 10
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'grading_result' not in st.session_state:
    st.session_state.grading_result = None
if 'model_result' not in st.session_state:
    st.session_state.model_result = None

REFILL_PASSWORD = "anxux123"

# ==========================================
# 4. 邏輯函數
# ==========================================

def call_gemini(prompt, content, is_image=False, system_prompt=""):
    """呼叫 Gemini API"""
    try        