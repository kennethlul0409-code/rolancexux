import os

def create_project():
    # 定義所有檔案路徑與內容
    files = {
        "index.tsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""",

        "metadata.json": """{
  "name": "文心老師作文批閱系統(確認版)",
  "description": "AI 驅動的作文自動批閱系統，提供專業、溫柔的寫作建議與評分。",
  "requestFramePermissions": []
}""",

        "index.html": """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>文心老師作文批閱</title>
  
  <!-- PWA Settings -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="theme-color" content="#5D4037">
  
  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@400;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            paper: '#FAF9F6',
            'paper-dark': '#F5F5F0',
            wood: {
              50: '#EFEBE9',
              100: '#D7CCC8',
              200: '#BCAAA4',
              300: '#A1887F',
              400: '#8D6E63',
              500: '#795548',
              600: '#6D4C41',
              700: '#5D4037',
              800: '#4E342E',
              900: '#3E2723',
            },
            gold: '#FFECB3',
          },
          fontFamily: {
            serif: ['"Noto Serif TC"', 'serif'],
            sans: ['"Noto Sans TC"', 'sans-serif'],
          },
          boxShadow: {
            'wood-btn': '0 4px 0 #3E2723, 0 5px 10px rgba(0,0,0,0.2)',
            'wood-btn-active': '0 0 0 #3E2723, inset 0 2px 5px rgba(0,0,0,0.2)',
            'figurine': '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
          },
          animation: {
            'float': 'float 3s ease-in-out infinite',
          },
          keyframes: {
            float: {
              '0%, 100%': { transform: 'translateY(0)' },
              '50%': { transform: 'translateY(-10px)' },
            }
          }
        }
      }
    }
  </script>

  <!-- Markdown Parser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <!-- Import Map for Google GenAI -->
  <script type="importmap">
{
  "imports": {
    "@google/genai": "https://esm.sh/@google/genai@^1.39.0",
    "react": "https://esm.sh/react@^19.2.4",
    "react-dom/": "https://esm.sh/react-dom@^19.2.4/",
    "react/": "https://esm.sh/react@^19.2.4/",
    "react-markdown": "https://esm.sh/react-markdown@^10.1.0",
    "lucide-react": "https://esm.sh/lucide-react@^0.563.0"
  }
}
</script>

  <style>
    body {
      background-color: #EFEBE9; 
      background-image: radial-gradient(#D7CCC8 1px, transparent 1px);
      background-size: 20px 20px;
      font-family: 'Noto Sans TC', sans-serif;
      color: #3E2723;
      overscroll-behavior-y: none;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #EFEBE9; }
    ::-webkit-scrollbar-thumb { background: #8D6E63; border-radius: 4px; }

    /* Markdown Styles */
    .markdown-body h1, .markdown-body h2 {
      font-family: 'Noto Serif TC', serif;
      color: #3E2723;
      margin-top: 1.5em;
      margin-bottom: 0.5em;
      font-weight: 700;
      border-bottom: 2px solid #D7CCC8;
      padding-bottom: 0.3em;
    }
    .markdown-body p { margin-bottom: 1em; line-height: 1.8; }
    .markdown-body strong { color: #8D6E63; font-weight: 700; }
    .markdown-body blockquote { 
      border-left: 4px solid #8D6E63; 
      padding: 1rem; 
      background: #FAF9F6; 
      color: #5D4037;
      font-style: italic;
      margin: 1em 0;
      border-radius: 0 8px 8px 0;
    }
    
    /* Animations */
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .animate-fade-in-up { animation: fadeInUp 0.5s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
    
    /* Loader */
    .spinner {
      border: 3px solid rgba(255, 236, 179, 0.3);
      border-radius: 50%;
      border-top: 3px solid #FFECB3;
      width: 20px;
      height: 20px;
      animation: spin 1s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./index.tsx"></script>
</body>
</html>""",

        "types.ts": """export enum InputMode {
  UNSELECTED = 'UNSELECTED',
  TEXT = 'TEXT',
  IMAGE = 'IMAGE'
}

export enum AppMode {
  HOME = 'HOME',
  GRADING = 'GRADING',
  MODEL_ESSAY = 'MODEL_ESSAY'
}

export enum EssayLevel {
  ELEMENTARY = '國小',
  JUNIOR = '國中',
  SENIOR = '高中',
  ADULT = '成人'
}

export enum EssayGenre {
  NARRATIVE = '記敘文',
  LYRIC = '抒情文',
  ARGUMENTATIVE = '議論文'
}

export enum GradingPersona {
  UNSELECTED = 'UNSELECTED',
  BODHISATTVA = '低眉菩薩',
  VAJRA = '怒目金剛'
}

export interface AnalysisState {
  isLoading: boolean;
  result: string | null;
  error: string | null;
}

export interface GeminiConfig {
  systemInstruction: string;
}

export interface User {
  username: string;
  password?: string;
  credits: number;
}""",

        "services/geminiService.ts": """import { GoogleGenAI } from "@google/genai";
import { GradingPersona } from "../types";

// 溫柔風格
const BODHISATTVA_INSTRUCTION = `
你是一位慈悲為懷、溫柔敦厚的資深國文老師「文心菩薩」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇學生的作文？
2. 如果內容僅是「網址連結」、「一句話的題目」、「亂碼」、「非作文的說明文字」或「極短的無意義語句」，請直接退件。

【退件處理】：
若判定無效，請回傳以 \`[REJECT]\` 開頭的訊息。
語氣要求：溫柔婉轉，說明這看起來不像作文（例如：「這似乎只是一個網址呢...」），請孩子重新上傳正確的內容。並告知這次不扣墨水。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出必須包含：【總體評分】、【亮點讚賞】、【名師建議】(不少於100字)、【推薦詞句】。

風格與規範：
1. **嚴禁無中生有**：絕對不能評論文章中「不存在」的情節或優點。只針對看得到的文字或圖片內容進行講評。
2. 語氣要如同春風般溫柔，多給予鼓勵與肯定。
3. 即使有缺點，也要用委婉的方式提出建議（例如：「如果...會更好」）。
4. 使用繁體中文。
`;

// 嚴厲風格
const VAJRA_INSTRUCTION = `
你是一位嚴格苛刻、目光如炬的資深國文總編輯「怒目金剛」。
收到內容後，請先執行【有效性檢查】：
1. 這是否是一篇值得批閱的作文？
2. 如果內容僅是「網址連結」、「一句話的題目」、「亂碼」、「非作文的說明文字」或「極短的無意義語句」，請直接退件。

【退件處理】：
若判定無效，請回傳以 \`[REJECT]\` 開頭的訊息。
語氣要求：嚴厲斥責，大罵這是敷衍了事、粗心大意（例如：「拿個網址就想來騙分數？」），要求重寫。並告知這次「暫且」不扣墨水。

【正常批閱】：
若內容有效，請從內容、結構、修辭三個維度分析。
輸出必須包含：【總體評分】、【毒舌點評】、【嚴格建議】(不少於100字)、【改進方向】。

風格與規範：
1. **嚴禁無中生有**：若文章內容空洞，就直接罵它空洞，絕對不要自己腦補不存在的情節來湊字數。
2. 語氣要嚴厲、直接，不留情面，極盡刁難。
3. 專注於找出邏輯漏洞、用詞不當、結構鬆散之處，雞蛋裡挑骨頭。
4. 直指核心問題，要求高標準的文學表現。
5. 使用繁體中文。
`;

const MODEL_ESSAY_SYSTEM_INSTRUCTION = `
你是一位榮獲多項文學獎的資深作家與國文名師。
請根據使用者提供的「題目」、「文體」與「等級」，撰寫一篇高品質的範文。

【嚴格文體規範】(必須遵守，不可混淆)：
1. 記敘文 (Narrative)：
   - 核心：寫人、記事。
   - 結構：必須具備完整的故事軸線（起因、經過、結果）。
   - 重點：透過具體的事件細節來呈現主題，避免過多空泛的議論。
   
2. 抒情文 (Lyric)：
   - 核心：抒發情感、感悟。
   - 結構：可以是觸景生情、或藉物詠志。
   - 重點：必須運用感官描寫（視、聽、嗅、味、觸）來堆疊氛圍，文字需優美感性，著重內心活動的刻畫。

3. 議論文 (Argumentative)：
   - 核心：說理、論證。
   - 結構：必須包含「論點」(主張)、「論據」(例子或數據)、「論證」(邏輯推演)。
   - 架構：採「引論(提出問題) -> 本論(分析問題) -> 結論(解決問題)」的三段式或四段式結構。
   - 重點：邏輯清晰，語氣堅定客觀，避免過多無關的感性描述。

【等級字數規範】：
1. 國小：約 400 字。用詞簡單，結構單純。
2. 國中：約 600 字。修辭豐富，嘗試夾敘夾議。
3. 高中：約 800 字。結構嚴謹，引用經典。
4. 成人：約 1200 字。見解獨到，文風洗鍊。

【格式規範】：
**重要：** 每個段落的開頭必須「強制」包含兩個全形空格（　　）作為縮排。這是中文正式作文的標準格式，請務必嚴格遵守，確保文章視覺上的整齊與規範。

輸出格式：
請直接輸出範文內容，不需要額外的寒暄。
若題目為空，請自行根據「文體」與「等級」擬定一個適合的經典題目。
`;

const getApiKey = () => {
  if (!process.env.API_KEY) {
    throw new Error("API Key is missing. Please set process.env.API_KEY.");
  }
  return process.env.API_KEY;
};

// Common model ID
const MODEL_ID = "gemini-3-flash-preview";

export const analyzeEssay = async (
  content: string, 
  isImage: boolean,
  persona: GradingPersona
): Promise<string> => {
  const apiKey = getApiKey();
  const ai = new GoogleGenAI({ apiKey });
  
  try {
    let contentsPayload;

    if (isImage) {
      // Content is a base64 string
      const base64Data = content.split(',')[1]; // Remove data URL prefix
      const mimeType = content.split(';')[0].split(':')[1];

      contentsPayload = {
        parts: [
          {
            inlineData: {
              mimeType: mimeType,
              data: base64Data
            }
          },
          {
            text: "請批閱這篇作文圖片。請先判斷這是否為有效的作文內容。"
          }
        ]
      };
    } else {
      // Content is plain text
      contentsPayload = {
        parts: [{ text: content }]
      };
    }

    // Select instruction based on persona
    const instruction = persona === GradingPersona.VAJRA 
      ? VAJRA_INSTRUCTION 
      : BODHISATTVA_INSTRUCTION;

    const response = await ai.models.generateContent({
      model: MODEL_ID,
      contents: contentsPayload,
      config: {
        systemInstruction: instruction,
        temperature: 0.7,
      }
    });

    if (response.text) {
      return response.text;
    } else {
      throw new Error("No response text generated.");
    }

  } catch (error) {
    console.error("Gemini API Error:", error);
    throw new Error(error instanceof Error ? error.message : "Unknown error occurred while contacting Gemini.");
  }
};

export const generateModelEssay = async (
  topic: string,
  level: string,
  genre: string
): Promise<string> => {
  const apiKey = getApiKey();
  const ai = new GoogleGenAI({ apiKey });

  try {
    const prompt = `題目：${topic || '（請自訂適合題目）'}\n文體：${genre}\n等級：${level}`;

    const response = await ai.models.generateContent({
      model: MODEL_ID,
      contents: { parts: [{ text: prompt }] },
      config: {
        systemInstruction: MODEL_ESSAY_SYSTEM_INSTRUCTION,
        temperature: 0.8, 
      }
    });

    if (response.text) {
      return response.text;
    } else {
      throw new Error("No model essay generated.");
    }
  } catch (error) {
    console.error("Gemini API Error:", error);
    throw new Error(error instanceof Error ? error.message : "Unknown error occurred while generating model essay.");
  }
};""",

        "components/Button.tsx": """import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  isLoading?: boolean;
  loadingText?: string;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  isLoading = false, 
  loadingText = '處理中...',
  className = '',
  disabled,
  ...props 
}) => {
  // Common styles
  const baseStyles = "relative font-serif font-bold tracking-wide rounded-lg transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed transform active:translate-y-[4px]";
  
  // Specific variants
  const variants = {
    // Rich Dark Wood with Gold text and 3D effect
    primary: `
      bg-gradient-to-b from-wood-600 to-wood-800 
      text-gold 
      border-2 border-wood-900 
      shadow-wood-btn 
      active:shadow-wood-btn-active 
      hover:brightness-110
      px-8 py-3 text-lg
    `,
    // Light Wood / Parchment style
    secondary: `
      bg-paper 
      text-wood-800 
      border-2 border-wood-400 
      shadow-[0_4px_0_#A1887F] 
      active:shadow-none 
      hover:bg-wood-50
      px-6 py-2
    `,
    // Subtle link style but with wood colors
    ghost: `
      bg-transparent 
      text-wood-600 
      hover:text-wood-800 
      hover:bg-wood-200/20
      px-4 py-2 
      !shadow-none !translate-y-0
    `
  };

  return (
    <button 
      className={`${baseStyles} ${variants[variant]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {/* Texture overlay for primary button */}
      {variant === 'primary' && (
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/wood-pattern.png')] opacity-20 rounded-lg pointer-events-none"></div>
      )}

      {isLoading ? (
        <>
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="relative z-10">{loadingText}</span>
        </>
      ) : (
        <span className="relative z-10 flex items-center gap-2">{children}</span>
      )}
    </button>
  );
};""",

        "components/ResultDisplay.tsx": """import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Save, ArrowLeft, Feather } from 'lucide-react';
import { Button } from './Button';
import { InputMode } from '../types';

interface ResultDisplayProps {
  content: string;
  originalContent: string;
  inputMode: InputMode;
  onBack: () => void;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ 
  content, 
  originalContent, 
  inputMode,
  onBack 
}) => {
  const handleSave = () => {
    // Generate an HTML file that includes both the original essay and the feedback
    const date = new Date().toLocaleDateString('zh-TW');
    const htmlContent = `
      <!DOCTYPE html>
      <html lang="zh-TW">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>文心老師作文批閱存檔 - ${date}</title>
        <style>
          body { font-family: "Noto Serif TC", serif; line-height: 1.8; color: #3E2723; max-width: 900px; margin: 0 auto; padding: 40px; background-color: #FAF9F6; }
          .container { border: 1px solid #D7CCC8; padding: 40px; }
          h1 { color: #5D4037; border-bottom: 2px solid #8D6E63; padding-bottom: 20px; text-align: center; }
          h2 { color: #8D6E63; margin-top: 40px; }
          .box { background: #EFEBE9; padding: 20px; border-radius: 8px; }
          .feedback { white-space: pre-wrap; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>文心老師批閱存檔 - ${date}</h1>
          <h2>您的作文</h2>
          <div class="box">
             ${inputMode === InputMode.IMAGE 
                ? `<img src="${originalContent}" style="max-width:100%" />` 
                : originalContent.replace(/\n/g, '<br/>')}
          </div>
          <h2>名師評語</h2>
          <div class="feedback">${content.replace(/\n/g, '<br/>')}</div>
        </div>
      </body>
      </html>
    `;

    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `文心老師批閱存檔_${new Date().toISOString().slice(0,10)}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="animate-fade-in-up flex flex-col gap-6">
      {/* Main Result Card */}
      <div className="bg-paper border-2 border-wood-200 rounded-xl shadow-card overflow-hidden relative">
        
        {/* Decorative Top Border */}
        <div className="h-2 bg-gradient-to-r from-wood-400 via-wood-600 to-wood-400"></div>

        {/* Header */}
        <div className="bg-wood-50 px-8 py-5 border-b border-wood-200 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-wood-700 text-gold rounded-full flex items-center justify-center shadow-inner">
              <Feather size={20} />
            </div>
            <div>
              <h2 className="text-2xl font-serif font-bold text-wood-900">批閱結果</h2>
              <p className="text-xs text-wood-500 font-sans">由文心老師親自點評</p>
            </div>
          </div>
        </div>
        
        {/* Content Area */}
        <div className="p-8 md:p-12 markdown-body bg-paper min-h-[400px]">
          {/* Watermark */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-5 pointer-events-none">
            <Feather size={300} strokeWidth={0.5} />
          </div>
          
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>

        {/* Footer Actions */}
        <div className="bg-wood-100/50 px-8 py-6 border-t border-wood-200 flex flex-col-reverse sm:flex-row gap-4 justify-between items-center">
          <Button variant="secondary" onClick={onBack} className="w-full sm:w-auto">
            <ArrowLeft size={18} />
            返回首頁
          </Button>
          <Button variant="primary" onClick={handleSave} className="w-full sm:w-auto">
            <Save size={18} />
            收藏這份評語
          </Button>
        </div>
      </div>
    </div>
  );
};""",

        "App.tsx": """import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Upload, FileText, Image as ImageIcon, Sparkles, AlertCircle, ArrowLeft, BookOpen, PenTool, Save, Feather, Ticket, Lock, KeyRound, Cat, Smile, Flame } from 'lucide-react';
import { InputMode, AnalysisState, AppMode, EssayLevel, EssayGenre, GradingPersona } from './types';
import { analyzeEssay, generateModelEssay } from './services/geminiService';
import { Button } from './components/Button';
import { ResultDisplay } from './components/ResultDisplay';
import ReactMarkdown from 'react-markdown';

const MAX_CREDITS = 10;
const STORAGE_KEY = 'wenxin_credits';
const REFILL_PASSWORD = 'anxux123'; // 設定固定通關密碼

const App: React.FC = () => {
  // Top level navigation state
  const [appMode, setAppMode] = useState<AppMode>(AppMode.HOME);
  
  // Credit System State
  const [credits, setCredits] = useState<number>(0);
  const [showCreditModal, setShowCreditModal] = useState(false);

  // Grading Mode State
  const [gradingPersona, setGradingPersona] = useState<GradingPersona>(GradingPersona.UNSELECTED);
  const [gradingInputMode, setGradingInputMode] = useState<InputMode>(InputMode.UNSELECTED);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [gradingState, setGradingState] = useState<AnalysisState>({
    isLoading: false,
    result: null,
    error: null,
  });

  // Model Essay Mode State
  const [modelTopic, setModelTopic] = useState('');
  const [modelLevel, setModelLevel] = useState<EssayLevel>(EssayLevel.JUNIOR);
  const [modelGenre, setModelGenre] = useState<EssayGenre>(EssayGenre.NARRATIVE);
  const [modelState, setModelState] = useState<AnalysisState>({
    isLoading: false,
    result: null,
    error: null,
  });

  const fileInputRef = useRef<HTMLInputElement>(null);

  // --- Credit Logic ---
  useEffect(() => {
    // Load from storage
    const storedCredits = localStorage.getItem(STORAGE_KEY);
    // Initialize credits: if storage exists use it, otherwise max
    let currentCredits = storedCredits ? parseInt(storedCredits) : MAX_CREDITS;
    
    setCredits(currentCredits);
    localStorage.setItem(STORAGE_KEY, currentCredits.toString());
  }, []);

  const deductCredit = (): boolean => {
    if (credits > 0) {
      const newCredits = credits - 1;
      setCredits(newCredits);
      localStorage.setItem(STORAGE_KEY, newCredits.toString());
      return true;
    } else {
      setShowCreditModal(true);
      return false;
    }
  };

  const refillCredits = () => {
    setCredits(MAX_CREDITS);
    localStorage.setItem(STORAGE_KEY, MAX_CREDITS.toString());
    setShowCreditModal(false);
  };

  // --- Reset Handlers ---
  const resetToHome = () => {
    setAppMode(AppMode.HOME);
    setGradingPersona(GradingPersona.UNSELECTED);
    setGradingInputMode(InputMode.UNSELECTED);
    setGradingState({ isLoading: false, result: null, error: null });
    setModelState({ isLoading: false, result: null, error: null });
  };

  const resetGradingInput = () => {
    setGradingInputMode(InputMode.UNSELECTED);
    setGradingState({ isLoading: false, result: null, error: null });
    setInputText('');
    setSelectedImage(null);
  };

  const resetGradingPersona = () => {
     setGradingPersona(GradingPersona.UNSELECTED);
     resetGradingInput();
  };

  // --- Logic for Grading ---
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setGradingState(prev => ({ ...prev, error: '請上傳圖片格式檔案 (JPG, PNG等)。' }));
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
        setGradingState(prev => ({ ...prev, error: null }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGradingSubmit = useCallback(async () => {
    // 1. Check if user has credits (but don't deduct yet)
    if (credits <= 0) {
      setShowCreditModal(true);
      return;
    }

    setGradingState({ isLoading: true, result: null, error: null });

    try {
      let content = '';
      let isImage = false;

      if (gradingInputMode === InputMode.TEXT) {
        if (!inputText.trim()) {
          throw new Error("請輸入作文內容。");
        }
        content = inputText;
      } else if (gradingInputMode === InputMode.IMAGE) {
        if (!selectedImage) {
          throw new Error("請上傳作文圖片。");
        }
        content = selectedImage;
        isImage = true;
      } else {
        throw new Error("請先選擇輸入模式");
      }

      // Pass the persona to the service
      const rawResult = await analyzeEssay(content, isImage, gradingPersona);
      
      // 2. Check for [REJECT] tag
      if (rawResult.trim().startsWith('[REJECT]')) {
        // Remove the tag and show the rejection message
        const cleanMessage = rawResult.replace('[REJECT]', '').trim();
        setGradingState({ isLoading: false, result: cleanMessage, error: null });
        // NOTE: We do NOT deduct credits here
      } else {
        // Valid essay -> Deduct credit and show result
        deductCredit();
        setGradingState({ isLoading: false, result: rawResult, error: null });
      }

    } catch (err) {
      setGradingState({ 
        isLoading: false, 
        result: null, 
        error: err instanceof Error ? err.message : '發生未知錯誤' 
      });
    }
  }, [gradingInputMode, inputText, selectedImage, gradingPersona, credits]);

  // --- Logic for Model Essay ---
  const handleModelSubmit = useCallback(async () => {
    // For generating model essay, we deduct immediately as it always generates something valid
    if (!deductCredit()) return;

    setModelState({ isLoading: true, result: null, error: null });
    try {
      if (!modelTopic.trim()) {
         // Allow empty topic
      }
      const result = await generateModelEssay(modelTopic, modelLevel, modelGenre);
      setModelState({ isLoading: false, result, error: null });
    } catch (err) {
      setModelState({
        isLoading: false,
        result: null,
        error: err instanceof Error ? err.message : '發生未知錯誤'
      });
    }
  }, [modelTopic, modelLevel, modelGenre, credits]);

  const handleSaveModelEssay = () => {
    if (!modelState.result) return;
    const date = new Date().toLocaleDateString('zh-TW');
    const htmlContent = `
      <!DOCTYPE html>
      <html lang="zh-TW">
      <head>
        <meta charset="UTF-8">
        <title>文心老師範文存檔 - ${modelTopic}</title>
        <style>
          body { font-family: "Noto Serif TC", serif; line-height: 1.8; color: #3E2723; max-width: 900px; margin: 0 auto; padding: 40px; background-color: #FAF9F6; }
          .container { border: 1px solid #D7CCC8; padding: 40px; }
          h1 { color: #5D4037; border-bottom: 2px solid #8D6E63; padding-bottom: 20px; text-align: center; }
          .meta { color: #8D6E63; text-align: center; margin-bottom: 30px; font-size: 0.9em; }
          .content { white-space: pre-wrap; font-size: 1.1em; }
          .footer { margin-top: 50px; text-align: center; color: #BCAAA4; font-size: 0.8em; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>${modelTopic || '無題'}</h1>
          <div class="meta">
             文體：${modelGenre} | 程度：${modelLevel} | 日期：${date}
          </div>
          <div class="content">${modelState.result.replace(/\n/g, '<br/>')}</div>
          <div class="footer">本範文由文心老師 AI 系統生成</div>
        </div>
      </body>
      </html>
    `;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `範文_${modelTopic || '未命名'}_${date}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // --- Components ---

  const WoodenMenuButton = ({ onClick, icon: Icon, title, desc }: { onClick: () => void, icon: any, title: string, desc: string }) => (
    <button
      onClick={onClick}
      className="group relative w-full overflow-hidden rounded-2xl border-[3px] border-[#3E2723] bg-gradient-to-b from-[#8D6E63] to-[#5D4037] shadow-[0_6px_0_#271c19,0_15px_20px_rgba(0,0,0,0.3)] transition-all active:translate-y-[4px] active:shadow-none hover:brightness-110"
    >
      <div className="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/wood-pattern.png')]"></div>
      
      <div className="relative p-8 flex flex-col items-center text-center">
        <div className="mb-4 text-[#FFECB3] drop-shadow-md transform group-hover:scale-110 transition-transform duration-300">
          <Icon size={56} strokeWidth={1.5} />
        </div>
        <h3 className="text-3xl font-serif font-bold text-[#FFECB3] mb-2 tracking-widest drop-shadow-md">
          {title}
        </h3>
        <div className="h-[1px] w-16 bg-[#FFECB3]/40 my-3"></div>
        <p className="text-[#D7CCC8] font-medium text-sm">
          {desc}
        </p>
      </div>
      <div className="absolute top-0 left-0 right-0 h-1 bg-white/20"></div>
    </button>
  );

  const OutOfCreditsModal = () => {
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);

    const handleSubmit = () => {
      if (password === REFILL_PASSWORD) {
        refillCredits();
      } else {
        setError(true);
        setTimeout(() => setError(false), 500); // Reset error state for animation
      }
    };

    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
        <div className="bg-paper border-4 border-wood-700 rounded-xl max-w-sm w-full shadow-2xl relative overflow-hidden flex flex-col">
          {/* Wood texture top */}
          <div className="h-4 bg-wood-700 w-full absolute top-0"></div>
          
          <div className="p-8 text-center flex-1 flex flex-col items-center">
            <div className="w-16 h-16 bg-wood-100 rounded-full flex items-center justify-center mb-4 shadow-inner">
              <Lock size={32} className="text-wood-600" />
            </div>
            
            <h3 className="text-xl font-serif font-bold text-wood-900 mb-2">墨水已耗盡</h3>
            
            <p className="text-wood-600 mb-6 text-sm leading-relaxed">
              今日的免費額度已達上限。<br/>
              請輸入通關密碼補充墨水。
            </p>

            <div className="w-full space-y-3">
              <div className="relative">
                <input 
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="輸入通關密碼..."
                  className={`w-full px-4 py-2 pl-10 rounded-lg border-2 bg-paper-dark outline-none font-mono text-wood-900 placeholder:text-wood-300 transition-all ${error ? 'border-red-400 ring-2 ring-red-200 animate-pulse' : 'border-wood-200 focus:border-wood-500'}`}
                />
                <KeyRound size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-wood-400" />
              </div>
              
              <div className="flex gap-2">
                 <Button 
                  onClick={() => setShowCreditModal(false)}
                  variant="ghost"
                  className="flex-1 !text-sm"
                >
                  關閉
                </Button>
                <Button 
                  onClick={handleSubmit}
                  className="flex-1 !py-2 !text-sm"
                >
                  補充墨水
                </Button>
              </div>
            </div>
          </div>
          
          {/* Wood texture bottom */}
          <div className="h-4 bg-wood-700 w-full mt-auto"></div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen pb-20 font-sans text-wood-900">
      {/* Header */}
      <header className="bg-wood-800 text-wood-50 shadow-md sticky top-0 z-20 border-b-4 border-wood-900">
        <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/wood-pattern.png')] pointer-events-none"></div>
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between relative z-10">
          <div 
            className="flex items-center gap-3 cursor-pointer hover:opacity-90 transition-opacity"
            onClick={resetToHome}
          >
            <div className="w-10 h-10 bg-wood-100 text-wood-800 rounded-lg flex items-center justify-center shadow-lg border-2 border-wood-300">
              <Sparkles size={22} fill="currentColor" className="text-wood-600" />
            </div>
            <div>
              <h1 className="text-2xl font-serif font-bold tracking-wide text-[#FFECB3] drop-shadow-sm">文心老師</h1>
              <p className="text-xs text-wood-200 font-serif tracking-wider">智慧作文批閱系統</p>
            </div>
          </div>
          
          {/* Credit Counter */}
          <div className="flex items-center gap-2 bg-wood-900/60 px-3 py-1.5 rounded-lg border border-wood-600 shadow-inner">
             <Ticket size={16} className={credits === 0 ? "text-red-400" : "text-gold"} />
             <span className={`text-sm font-bold font-mono ${credits === 0 ? "text-red-400" : "text-[#FFECB3]"}`}>
               {credits} / {MAX_CREDITS}
             </span>
          </div>
        </div>
      </header>

      {showCreditModal && <OutOfCreditsModal />}

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-8 relative">

        {/* --- VIEW: HOME MENU --- */}
        {appMode === AppMode.HOME && (
          <div className="animate-fade-in-up flex flex-col items-center justify-center min-h-[60vh]">
            <section className="text-center space-y-4 mb-12">
              <h2 className="text-3xl md:text-4xl font-serif font-bold text-wood-900 leading-tight">
                請選擇您的<span className="text-wood-600 decoration-wood-300 underline underline-offset-4">學習模式</span>
              </h2>
              <div className="flex flex-col items-center gap-2">
                <p className="text-lg text-wood-600 max-w-2xl mx-auto font-serif">
                  展卷批閱，或觀摩名家手筆。<br className="hidden sm:block"/>
                  在文字的森林中，遇見更好的自己。
                </p>
                <div className="mt-2 inline-flex items-center gap-2 px-4 py-1 bg-wood-100 text-wood-700 rounded-full text-sm font-bold border border-wood-300">
                  <Feather size={14} /> 剩餘可用墨水：{credits} 次
                </div>
              </div>
            </section>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-3xl px-4">
              <WoodenMenuButton 
                onClick={() => setAppMode(AppMode.GRADING)}
                icon={PenTool}
                title="作文批閱"
                desc="上傳您的作文，獲得專業評語與建議"
              />
              <WoodenMenuButton 
                onClick={() => setAppMode(AppMode.MODEL_ESSAY)}
                icon={BookOpen}
                title="範文參考"
                desc="輸入題目與等級，生成高品質名師範文"
              />
            </div>
          </div>
        )}

        {/* --- VIEW: GRADING MODE --- */}
        {appMode === AppMode.GRADING && (
          <>
            {/* Step 1: Persona Selection */}
            {gradingPersona === GradingPersona.UNSELECTED && (
              <div className="animate-fade-in-up flex flex-col items-center justify-center min-h-[50vh]">
                 <Button 
                  variant="ghost"
                  onClick={resetToHome}
                  className="self-start mb-6 !pl-0"
                >
                   <ArrowLeft size={18} />
                   返回主選單
                </Button>

                <h2 className="text-2xl font-serif font-bold text-wood-800 mb-8 border-b-2 border-wood-200 pb-2">請選擇批閱老師</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full max-w-3xl items-stretch">
                   {/* Bodhisattva - Gentle Smile Icon */}
                   <button
                    onClick={() => setGradingPersona(GradingPersona.BODHISATTVA)}
                    className="group relative bg-paper p-6 rounded-2xl shadow-card hover:shadow-xl border-2 border-transparent hover:border-yellow-400 transition-all duration-300 flex flex-col items-center text-center overflow-visible mt-6 h-full"
                  >
                    {/* Icon Container */}
                    <div className="w-32 h-32 bg-amber-100 rounded-full flex items-center justify-center mb-6 shadow-inner transform transition-transform duration-300 group-hover:scale-110">
                       <Smile size={64} className="text-amber-600" />
                    </div>

                    <h3 className="text-2xl font-serif font-bold text-wood-800 mb-2">低眉菩薩</h3>
                    <div className="px-3 py-1 bg-amber-100 text-amber-800 text-xs rounded-full mb-4 font-bold">溫柔・鼓勵</div>
                    <p className="text-wood-600 text-sm leading-relaxed">
                      「孩子，你已經很棒了。」<br/>
                      用溫暖的眼光發掘你的亮點，<br/>給予如春風般的建議。
                    </p>
                  </button>

                   {/* Vajra - Angry Flame Icon */}
                   <button
                    onClick={() => setGradingPersona(GradingPersona.VAJRA)}
                    className="group relative bg-paper p-6 rounded-2xl shadow-card hover:shadow-xl border-2 border-transparent hover:border-red-500 transition-all duration-300 flex flex-col items-center text-center overflow-visible mt-6 h-full"
                  >
                    {/* Icon Container */}
                    <div className="w-32 h-32 bg-red-100 rounded-full flex items-center justify-center mb-6 shadow-inner transform transition-transform duration-300 group-hover:scale-110">
                       <Flame size={64} className="text-red-600" />
                    </div>

                    <h3 className="text-2xl font-serif font-bold text-red-900 mb-2">怒目金剛</h3>
                    <div className="px-3 py-1 bg-red-100 text-red-900 text-xs rounded-full mb-4 font-bold">嚴厲・毒舌</div>
                    <p className="text-wood-600 text-sm leading-relaxed">
                      「這裡邏輯不通，重寫！」<br/>
                      極盡刁難，不留情面，<br/>雞蛋裡挑骨頭的魔鬼訓練。
                    </p>
                  </button>
                </div>
              </div>
            )}

            {/* Step 2: Input Method Selection */}
            {gradingPersona !== GradingPersona.UNSELECTED && gradingInputMode === InputMode.UNSELECTED && (
              <div className="animate-fade-in-up flex flex-col items-center justify-center min-h-[50vh]">
                 <Button 
                  variant="ghost"
                  onClick={resetGradingPersona}
                  className="self-start mb-6 !pl-0"
                >
                   <ArrowLeft size={18} />
                   重新選擇老師
                </Button>

                <h2 className="text-2xl font-serif font-bold text-wood-800 mb-8 border-b-2 border-wood-200 pb-2">請選擇輸入方式</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-2xl">
                  {/* Selection Card: Text */}
                  <button
                    onClick={() => setGradingInputMode(InputMode.TEXT)}
                    className="group bg-paper p-8 rounded-2xl shadow-card hover:shadow-xl border-2 border-wood-100 hover:border-wood-400 transition-all duration-300 flex flex-col items-center text-center transform hover:-translate-y-1 relative overflow-hidden"
                  >
                    <div className="w-20 h-20 bg-wood-50 rounded-full flex items-center justify-center mb-5 group-hover:bg-wood-600 group-hover:text-white transition-colors duration-300 text-wood-500 shadow-inner">
                      <FileText size={36} />
                    </div>
                    <h3 className="text-xl font-bold text-wood-800 mb-2 font-serif">文字輸入</h3>
                    <p className="text-wood-500 text-sm">直接在數位稿紙上撰寫</p>
                  </button>

                   {/* Selection Card: Image */}
                  <button
                    onClick={() => setGradingInputMode(InputMode.IMAGE)}
                    className="group bg-paper p-8 rounded-2xl shadow-card hover:shadow-xl border-2 border-wood-100 hover:border-wood-400 transition-all duration-300 flex flex-col items-center text-center transform hover:-translate-y-1 relative overflow-hidden"
                  >
                    <div className="w-20 h-20 bg-wood-50 rounded-full flex items-center justify-center mb-5 group-hover:bg-wood-600 group-hover:text-white transition-colors duration-300 text-wood-500 shadow-inner">
                      <ImageIcon size={36} />
                    </div>
                    <h3 className="text-xl font-bold text-wood-800 mb-2 font-serif">圖片上傳</h3>
                    <p className="text-wood-500 text-sm">拍攝手寫稿件進行辨識</p>
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Editor View */}
            {gradingPersona !== GradingPersona.UNSELECTED && gradingInputMode !== InputMode.UNSELECTED && (
              <div className="animate-fade-in">
                <div className="flex justify-between items-center mb-4">
                  <Button 
                    variant="ghost"
                    onClick={resetGradingInput} 
                    className="!pl-0"
                  >
                     <ArrowLeft size={18} />
                     重新選擇輸入
                  </Button>
                  <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${gradingPersona === GradingPersona.BODHISATTVA ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-900'}`}>
                    {/* Replaced Icon with Cat */}
                    <Cat size={16} className={gradingPersona === GradingPersona.BODHISATTVA ? 'text-amber-600' : 'text-red-600'} />
                    {gradingPersona}
                  </div>
                </div>

                {/* Input Card Container */}
                <section className={`bg-paper rounded-xl shadow-card border-2 border-wood-200 overflow-hidden relative ${gradingState.result ? 'opacity-50 pointer-events-none grayscale' : ''}`}>
                  {/* Card Header */}
                  <div className="bg-wood-100/30 px-6 py-4 border-b border-wood-200 flex items-center gap-2 text-wood-700 font-medium font-serif">
                    {gradingInputMode === InputMode.TEXT ? <FileText size={20}/> : <ImageIcon size={20}/>}
                    {gradingInputMode === InputMode.TEXT ? '文字編輯模式' : '圖片辨識模式'}
                  </div>

                  <div className="p-6 md:p-8">
                    {gradingInputMode === InputMode.TEXT ? (
                      <div className="space-y-4">
                        <div className="relative">
                          <textarea
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder="請在此輸入您的作文內容..."
                            className="w-full h-80 p-6 rounded-lg border-2 border-wood-200 focus:border-wood-500 focus:ring-0 resize-none bg-paper-dark font-serif text-lg leading-loose placeholder:text-wood-300 outline-none transition-colors text-wood-900 shadow-inner"
                            style={{ backgroundImage: 'linear-gradient(transparent 1.9em, #E0E0E0 2em)', backgroundSize: '100% 2em', lineHeight: '2em' }}
                          />
                        </div>
                        <div className="text-right text-sm text-wood-500 font-mono">目前字數: {inputText.length}</div>
                      </div>
                    ) : (
                      <div className="space-y-6">
                        <div 
                          onClick={() => fileInputRef.current?.click()}
                          className={`border-4 border-dashed rounded-xl h-80 flex flex-col items-center justify-center cursor-pointer transition-all bg-wood-50 hover:bg-wood-100/50 ${selectedImage ? 'border-wood-500' : 'border-wood-200 hover:border-wood-400'}`}
                        >
                          {selectedImage ? (
                            <img src={selectedImage} alt="Uploaded" className="h-full w-full object-contain p-2 rounded-lg" />
                          ) : (
                            <div className="text-center space-y-3 p-4">
                              <div className="w-16 h-16 bg-wood-200 rounded-full flex items-center justify-center mx-auto text-wood-600"><Upload size={32} /></div>
                              <div className="text-wood-700 font-bold text-lg font-serif">點擊上傳作文照片</div>
                              <p className="text-wood-400 text-sm">支援 JPG, PNG 格式</p>
                            </div>
                          )}
                          <input type="file" ref={fileInputRef} onChange={handleFileChange} accept="image/*" className="hidden" />
                        </div>
                        {selectedImage && (
                          <div className="flex justify-center">
                            <Button variant="secondary" onClick={(e) => { e.stopPropagation(); setSelectedImage(null); }}>
                               重新上傳
                            </Button>
                          </div>
                        )}
                      </div>
                    )}

                    {gradingState.error && (
                      <div className="mt-6 p-4 bg-red-50 text-red-800 border border-red-200 rounded-lg flex items-center gap-3 text-sm animate-pulse">
                        <AlertCircle size={18} />
                        {gradingState.error}
                      </div>
                    )}

                    {!gradingState.result && (
                      <div className="mt-8 flex justify-center">
                        <Button onClick={handleGradingSubmit} isLoading={gradingState.isLoading} className="w-full sm:w-auto min-w-[200px]">
                          {credits > 0 ? `開始批閱 (消耗1墨水)` : `墨水不足`}
                        </Button>
                      </div>
                    )}
                  </div>
                </section>

                {/* Result */}
                {gradingState.result && (
                  <div className="mt-8 pb-12">
                    <ResultDisplay 
                      content={gradingState.result} 
                      originalContent={gradingInputMode === InputMode.TEXT ? inputText : (selectedImage || '')}
                      inputMode={gradingInputMode}
                      onBack={resetGradingInput}
                    />
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {/* --- VIEW: MODEL ESSAY MODE --- */}
        {appMode === AppMode.MODEL_ESSAY && (
          <div className="animate-fade-in">
            <Button 
              variant="ghost"
              onClick={resetToHome}
              className="mb-4 !pl-0"
            >
               <ArrowLeft size={18} />
               返回主選單
            </Button>

            <div className="flex flex-col md:flex-row gap-8">
              {/* Left: Input Form */}
              <div className="w-full md:w-1/3 space-y-6">
                <section className="bg-paper rounded-xl shadow-card border border-wood-200 overflow-hidden p-6 sticky top-24">
                  <h2 className="text-xl font-serif font-bold text-wood-800 mb-6 flex items-center gap-2 border-b border-wood-100 pb-3">
                    <BookOpen size={24} className="text-wood-600"/>
                    範文設定
                  </h2>
                  
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-bold text-wood-600 mb-2 font-serif">範文題目</label>
                      <input 
                        type="text" 
                        value={modelTopic}
                        onChange={(e) => setModelTopic(e.target.value)}
                        placeholder="例如：我的夢想..."
                        className="w-full px-4 py-3 rounded-lg border-2 border-wood-200 focus:border-wood-500 focus:ring-0 outline-none bg-paper-dark text-wood-900 placeholder:text-wood-300"
                      />
                    </div>

                     <div>
                      <label className="block text-sm font-bold text-wood-600 mb-2 font-serif">文體類型</label>
                      <div className="relative">
                        <select 
                          value={modelGenre}
                          onChange={(e) => setModelGenre(e.target.value as EssayGenre)}
                          className="w-full px-4 py-3 rounded-lg border-2 border-wood-200 focus:border-wood-500 focus:ring-0 outline-none bg-paper-dark text-wood-900 appearance-none cursor-pointer"
                        >
                          <option value={EssayGenre.NARRATIVE}>記敘文 (寫人記事)</option>
                          <option value={EssayGenre.LYRIC}>抒情文 (情感抒發)</option>
                          <option value={EssayGenre.ARGUMENTATIVE}>議論文 (說理分析)</option>
                        </select>
                        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-wood-500">
                          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-bold text-wood-600 mb-2 font-serif">適用等級</label>
                      <div className="relative">
                        <select 
                          value={modelLevel}
                          onChange={(e) => setModelLevel(e.target.value as EssayLevel)}
                          className="w-full px-4 py-3 rounded-lg border-2 border-wood-200 focus:border-wood-500 focus:ring-0 outline-none bg-paper-dark text-wood-900 appearance-none cursor-pointer"
                        >
                          <option value={EssayLevel.ELEMENTARY}>國小 (約 400 字)</option>
                          <option value={EssayLevel.JUNIOR}>國中 (約 600 字)</option>
                          <option value={EssayLevel.SENIOR}>高中 (約 800 字)</option>
                          <option value={EssayLevel.ADULT}>成人 (約 1200 字)</option>
                        </select>
                        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-wood-500">
                          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                        </div>
                      </div>
                    </div>

                    <Button 
                      onClick={handleModelSubmit}
                      isLoading={modelState.isLoading}
                      loadingText="生成中..."
                      className="w-full mt-4"
                    >
                      {credits > 0 ? `生成範文 (消耗1墨水)` : `墨水不足`}
                    </Button>
                    
                    {modelState.error && (
                      <p className="text-red-500 text-sm mt-2">{modelState.error}</p>
                    )}
                  </div>
                </section>
              </div>

              {/* Right: Display */}
              <div className="w-full md:w-2/3">
                 {modelState.result ? (
                   <div className="bg-paper border-2 border-wood-200 rounded-xl shadow-card overflow-hidden animate-fade-in-up relative flex flex-col">
                      <div className="bg-wood-50 px-6 py-4 border-b border-wood-200 flex justify-between items-center flex-wrap gap-2">
                        <div className="flex items-center gap-2">
                          <div className="w-1.5 h-6 bg-wood-600 rounded-full"></div>
                          <h2 className="text-xl font-serif font-bold text-wood-800">名師範文：{modelTopic || '無題'}</h2>
                        </div>
                        <div className="flex gap-2">
                          <span className="text-xs px-3 py-1 bg-wood-200 text-wood-800 rounded-full font-serif font-bold">
                            {modelGenre}
                          </span>
                          <span className="text-xs px-3 py-1 bg-wood-200 text-wood-800 rounded-full font-serif font-bold">
                            {modelLevel}
                          </span>
                        </div>
                      </div>
                      <div className="p-8 markdown-body bg-paper min-h-[500px]">
                         <ReactMarkdown>{modelState.result}</ReactMarkdown>
                      </div>
                      
                      {/* Footer Bar with Save Button */}
                      <div className="bg-wood-100/30 px-6 py-4 border-t border-wood-200 flex justify-between items-center mt-auto">
                        <span className="text-sm text-wood-500 font-serif">— 文心老師 AI 寫作教室 —</span>
                        <Button 
                          variant="secondary" 
                          onClick={handleSaveModelEssay}
                          className="!px-4 !py-2 !text-sm"
                          title="下載範文"
                        >
                          <Save size={16} />
                          存檔
                        </Button>
                      </div>
                   </div>
                 ) : (
                   <div className="h-full min-h-[400px] border-4 border-dashed border-wood-200 rounded-xl flex flex-col items-center justify-center text-wood-400 bg-wood-50/50">
                     <BookOpen size={48} className="mb-4 opacity-50"/>
                     <p className="font-serif">設定題目、文體與等級後，範文將顯示於此</p>
                   </div>
                 )}
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
};

export default App;""",

        "services/userService.ts": """import { User } from '../types';

const DB_KEY = 'wenxin_users_db';
const SESSION_KEY = 'wenxin_current_session';
const DEFAULT_CREDITS = 10;

// 模擬資料庫操作
const getDb = (): User[] => {
  const data = localStorage.getItem(DB_KEY);
  return data ? JSON.parse(data) : [];
};

const saveDb = (users: User[]) => {
  localStorage.setItem(DB_KEY, JSON.stringify(users));
};

export const userService = {
  // 註冊
  register: (username: string, password: string): { success: boolean; message?: string; user?: User } => {
    const users = getDb();
    if (users.find(u => u.username === username)) {
      return { success: false, message: '此帳號已被註冊' };
    }

    const newUser: User = {
      username,
      password,
      credits: DEFAULT_CREDITS
    };

    users.push(newUser);
    saveDb(users);
    return { success: true, user: newUser };
  },

  // 登入
  login: (username: string, password: string): { success: boolean; message?: string; user?: User } => {
    const users = getDb();
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
      // 儲存 session
      localStorage.setItem(SESSION_KEY, JSON.stringify(user));
      return { success: true, user };
    }
    
    return { success: false, message: '帳號或密碼錯誤' };
  },

  // 登出
  logout: () => {
    localStorage.removeItem(SESSION_KEY);
  },

  // 獲取當前登入者
  getCurrentUser: (): User | null => {
    const session = localStorage.getItem(SESSION_KEY);
    if (!session) return null;
    
    // 確保拿到最新的額度資料 (因為 session 可能是舊的)
    const sessionUser = JSON.parse(session);
    const users = getDb();
    const freshUser = users.find(u => u.username === sessionUser.username);
    return freshUser || null;
  },

  // 更新額度 (扣款或儲值)
  updateCredits: (username: string, newCredits: number): User | null => {
    const users = getDb();
    const userIndex = users.findIndex(u => u.username === username);
    
    if (userIndex === -1) return null;
    
    users[userIndex].credits = newCredits;
    saveDb(users);
    
    // 更新 session
    localStorage.setItem(SESSION_KEY, JSON.stringify(users[userIndex]));
    
    return users[userIndex];
  }
};"""
    }

    for path, content in files.items():
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {path}")

if __name__ == "__main__":
    create_project()