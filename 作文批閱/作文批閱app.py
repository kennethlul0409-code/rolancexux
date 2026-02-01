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
# 2. API 與變數設定
# ==========================================

# ⚠️ 你的 API Key
API_KEY = "AIzaSyDULJDZicXPlA9g_5Hoj0oYv9XPhUuK3LA"

# 設定 API
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API Key 設定錯誤：{e}")

REFILL_PASSWORD = "anxux123"

# 初始化變數
if 'credits' not in st.session_state:
    st.session_state.credits = 10
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'grading_result' not in st.session_state:
    st.session_state.grading_result = None
if 'model_result' not in st.session_state:
    st.session_state.model_result = None

# ==========================================
# 3. 樣式設計 (將 CSS 獨立出來，避免語法錯誤)
# ==========================================
custom_css = """
<style>
    .stApp {
        background-color: #EFEBE9;
        background-image: radial-gradient(#D7CCC8 1px, transparent 1px);
        background-size: 20px 20px;
    }
    h1, h2, h3, h4, p, div, span, label, li {
        color: #3E2723 !important;
        font-family: "Noto Serif TC", serif;
    }
    div.stButton > button {
        background: linear-gradient(to bottom, #6D4C41, #4E342E);
        color: #FFECB3 !important;
        border: 2px solid #3E2723;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        margin-top: 10px;
        padding: 10px 0;
    }
    .wood-card {
        background-color: #FAF9F6;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #D7CCC8;
        margin-bottom: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 4. 核心 Prompt
# ==========================================

BODHISATTVA_INSTRUCTION = """
你是一位慈悲為懷、溫柔敦厚的資深國文老師「文心菩薩」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇學生的作文？
2. 如果內容無效，請回傳 `[REJECT]` 開頭的訊息。

【退件處理】：
若判定無效，請回傳 `[REJECT]` 開頭訊息，語氣溫柔。

【正常批閱】：
若內容有效，請從內容、結構、修辭分析。
輸出包含：【總體評分】、【亮點讚賞】、【名師建議】(不少於100字)、【推薦詞句】。
語氣如春風般溫柔，多給予鼓勵。
"""

VAJRA_INSTRUCTION = """
你是一位嚴格苛刻的資深國文總編輯「怒目金剛」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇值得批閱的作文？
2. 如果內容無效，請回傳 `[REJECT]` 開頭的訊息並嚴厲斥責。

【正常批閱】：
輸出包含：【總體評分】、【毒舌點評】、【嚴格建議】(不少於100字)、【改進方向】。
語氣嚴厲、直接，不留情面。
"""

MODEL_ESSAY_INSTRUCTION = """
你是一位榮獲文學獎的資深作家。請根據「題目」、「文體」與「等級」撰寫範文。
每個段落開頭必須「強制」包含兩個全形空格（　　）。
"""

# ==========================================
# 5. 功能函數
# ==========================================

def call_gemini(prompt, content, is_image=False, system_prompt=""):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
        if is_image:
            response = model.generate_content([content, prompt])
        else:
            response = model.generate_content(f"{prompt}\n\n內容：\n{content}")
        return response.text
    except Exception as e:
        return f"錯誤：{str(e)}"

def go_home():
    st.session_state.page = 'home'
    st.session_state.grading_result = None
    st.session_state.model_result = None

# ==========================================
# 6. 頁面邏輯
# ==========================================

# 頂部
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🪶 文心老師")
with col2:
    st.markdown(f"### 墨水：{st.session_state.credits}")

# 墨水耗盡
if st.session_state.credits <= 0:
    st.warning("⚠️ 墨水耗盡")
    pwd = st.text_input("輸入通關密碼", type="password")
    if st.button("補充"):
        if pwd == REFILL_PASSWORD:
            st.session_state.credits = 10
            st.success("已補滿！")
            st.rerun()
        else:
            st.error("密碼錯誤")
    st.stop()

# --- 首頁 ---
if st.session_state.page == 'home':
    st.info("請選擇學習模式")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="wood-card">', unsafe_allow_html=True)
        st.subheader("🖊️ 作文批閱")
        if st.button("進入批閱"):
            st.session_state.page = 'grading_setup'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="wood-card">', unsafe_allow_html=True)
        st.subheader("📖 範文參考")
        if st.button("進入範文"):
            st.session_state.page = 'model_setup'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 批閱設定 ---
elif st.session_state.page == 'grading_setup':
    if st.button("⬅️ 返回"): go_home(); st.rerun()
    st.markdown("### 作文批閱")
    
    persona = st.radio("風格", ["😊 低眉菩薩", "🔥 怒目金剛"], horizontal=True)
    input_type = st.radio("方式", ["📝 文字", "📷 圖片"], horizontal=True)
    
    user_content = None
    is_image = False
    
    if "文字" in input_type:
        user_content = st.text_area("貼上作文", height=200)
    else:
        up_file = st.file_uploader("上傳圖片", type=['png', 'jpg'])
        if up_file:
            user_content = Image.open(up_file)
            st.image(user_content, use_column_width=True)
            is_image = True

    if st.button("✨ 開始批閱 (消耗1墨水)"):
        if user_content:
            with st.spinner("分析中..."):
                sys = BODHISATTVA_INSTRUCTION if "菩薩" in persona else VAJRA_INSTRUCTION
                res = call_gemini("請批閱", user_content, is_image, sys)
                
                if "[REJECT]" in res:
                    st.error(res.replace("[REJECT]", ""))
                else:
                    st.session_state.credits -= 1
                    st.session_state.grading_result = res
                    st.session_state.page = 'grading_result'
                    st.rerun()
        else:
            st.error("請輸入內容")

# --- 批閱結果 ---
elif st.session_state.page == 'grading_result':
    if st.button("⬅️ 返回"): go_home(); st.rerun()
    st.markdown('<div class="wood-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.grading_result)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 範文設定 ---
elif st.session_state.page == 'model_setup':
    if st.button("⬅️ 返回"): go_home(); st.rerun()
    st.markdown("### 範文生成")
    
    topic = st.text_input("題目")
    genre = st.selectbox("文體", ["記敘文", "抒情文", "議論文"])
    level = st.selectbox("等級", ["國小", "國中", "高中", "成人"])
    
    if st.button("🖋️ 生成 (消耗1墨水)"):
        with st.spinner("撰寫中..."):
            p_text = f"題目：{topic}\n文體：{genre}\n等級：{level}"
            res = call_gemini(p_text, "", False, MODEL_ESSAY_INSTRUCTION)
            st.session_state.credits -= 1
            st.session_state.model_result = res
            st.session_state.page = 'model_result'
            st.rerun()

# --- 範文結果 ---
elif st.session_state.page == 'model_result':
    if st.button("⬅️ 返回"): go_home(); st.rerun()
    st.markdown('<div class="wood-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.model_result)
    st.markdown('</div>', unsafe_allow_html=True)