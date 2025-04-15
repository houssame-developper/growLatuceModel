import os
from pyexpat import model
import streamlit as st
import joblib
import requests

@st.cache_resource
def load_model():
    model_path = "model.joblib"  # تأكد من أن هذا هو مسار الموديل الخاص بك
    if not os.path.exists(model_path):
        url = "https://www.mediafire.com/file/kxu5c7iijyr7eg8/model.joblib"
        response = requests.get(url)
        with open(model_path, 'wb') as file:
            file.write(response.content)
    # حتى لا يعيد التحميل كل مرة
    model = joblib.load(model_path)  # غيّر الاسم حسب اسم الملف
    return model


# اللغات
languages = {
    "🇲🇦 العربية": {"title": "📊 توقع حالة النبات", "predict": "🔍 تنبؤ", "result": "🔍 النتيجة",
                    "temp": "درجة الحرارة (°C)", "hum": "الرطوبة (%)", "tds": "قيمة TDS (ppm)",
                    "ph": "مستوى pH", "days": "أيام النمو"},
    "🇺🇸 English": {"title": "📊 Plant Status Prediction", "predict": "🔍 Predict", "result": "🔍 Result",
                    "temp": "Temperature (°C)", "hum": "Humidity (%)", "tds": "TDS Value (ppm)",
                    "ph": "pH Level", "days": "Growth Days"},
    "🇫🇷 Français": {"title": "📊 Prédiction de l'État de la Plante", "predict": "🔍 Prédire", "result": "🔍 Résultat",
                    "temp": "Température (°C)", "hum": "Humidité (%)", "tds": "Valeur TDS (ppm)",
                    "ph": "Niveau pH", "days": "Jours de croissance"}
}

# اختيار اللغة
language = st.sidebar.selectbox(
    "🌍 اختر اللغة / Choose Language / Choisissez la langue", 
    list(languages.keys()),
    key="language_selectbox"  # إضافة مفتاح فريد
)

texts = languages[language]

# اختيار الوضع (Light or Dark Mode)
theme = st.sidebar.radio(
    "🌙/🌞 اختر الوضع", 
    ("Light Mode", "Dark Mode"),
    key="theme_radio"  # مفتاح فريد للوضع
)

# تخصيص الألوان في الوضع الفاتح
if theme == "Light Mode":
    st.markdown(
        """
        <style>
        :root {
            --primary: #1e88e5;
            --primary-hover: #1565c0;
            --background: #f8f9fa;
            --secondary-background: #ffffff;
            --text: #212121;
            --secondary-text: #616161;
            --border: #e0e0e0;
            --hover: #f5f5f5;
            --shadow: rgba(0,0,0,0.1);
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .stApp {
            background-color: var(--background);
        }
        
        .sidebar .sidebar-content {
            background-color: var(--secondary-background);
            border-right: 1px solid var(--border);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--primary);
            font-weight: 600;
        }
        
        /* Center the main title */
        h1 {
            margin-bottom: 1.5rem;
            font-size: 2.2rem;
            text-align: center !important;
        }
        
        /* Add this for the title container */
        [data-testid="stHeader"] {
            text-align: center !important;
            display: block;
            width: 100%;
        }
        
        /* This ensures title text is centered */
        .main .block-container [data-testid="stMarkdownContainer"] h1 {
            text-align: center !important;
            width: 100%;
            display: block;
        }
        
        /* Form elements */
        .stTextInput, .stNumberInput, .stSelectbox {
            background-color: var(--secondary-background);
            border-radius: 8px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 4px var(--shadow);
            margin-bottom: 1rem;
            padding: 0.5rem;
        }
        
        .stTextInput > div, .stNumberInput > div {
            background-color: var(--secondary-background) !important;
        }
        
        .stTextInput input, .stNumberInput input {
            color: var(--text) !important;
            background-color: var(--secondary-background) !important;
            border-radius: 4px;
            padding: 0.75rem !important;
            text-align: center;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary);
            color: white !important;
            border: none;
            padding: 12px 28px;
            border-radius: 6px;
            font-weight: 500;
            font-size: 1rem;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 5px var(--shadow);
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px var(--shadow);
        }
        
        /* Container styling */
        .main .block-container {
            padding: 2rem;
            max-width: 1200px;
            background-color: var(--secondary-background);
            border-radius: 12px;
            box-shadow: 0 4px 12px var(--shadow);
            margin-top: 1rem;
        }
        
        /* Labels */
        label, .stRadio label {
            color: var(--text) !important;
            font-weight: 500;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        /* Result container */
        .element-container {
            background-color: var(--secondary-background);
            border-radius: 8px;
            border-left: 5px solid var(--primary);
        }
        
        /* Sidebar styling */
        .css-1aumxhk, [data-testid="stSidebar"] {
            background-color: var(--secondary-background);
            border-right: 1px solid var(--border);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            padding: 0.5rem 0;
        }
        
        /* Select box */
        .stSelectbox div[data-baseweb="select"] {
            background-color: var(--secondary-background);
            border-color: var(--border);
        }
        
        /* Radio buttons - FIX HERE */
        [role="radiogroup"] {
            background-color: var(--secondary-background) !important;
            padding: 0.5rem !important;
            border-radius: 8px !important;
            border: 1px solid var(--border) !important;
        }
        
        [data-baseweb="radio"] {
            background-color: var(--secondary-background) !important;
            margin: 0.25rem 0 !important;
        }
        
        [data-baseweb="radio"] input {
            background-color: var(--secondary-background) !important;
        }
        
        [data-baseweb="radio"] div {
            background-color: var(--secondary-background) !important;
        }
        
        /* The actual radio circle */
        [data-baseweb="radio"] div:first-of-type {
            border-color: var(--primary) !important;
        }
        
        /* The inner dot when selected */
        [data-baseweb="radio"] div:first-of-type div {
            background-color: var(--primary) !important;
        }
        
        /* The text label for the radio */
        [data-baseweb="radio"] div:last-child {
            color: var(--text) !important;
        }
        
        /* Column layout improvement */
        .row-widget.stHorizontal {
            gap: 1.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

else:
    st.markdown(
        """
        <style>
        :root {
            --primary: #4a8fe7;
            --background: #2a2a2a;
            --secondary-background: #444444;
            --text: #ffffff;
            --border: #555555;
            --hover: #3a3a3a;
            --shadow: rgba(0,0,0,0.3);
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
        }
        
        .sidebar .sidebar-content {
            background-color: var(--secondary-background);
        }
        
        .stTextInput, .stNumberInput, .stButton, .stTextArea {
            background-color: var(--secondary-background);
            color: var(--text);
            border: 1px solid var(--border);
        }
        
        /* Center the main title in dark mode too */
        h1 {
            text-align: center !important;
            width: 100%;
        }
        
        .main .block-container [data-testid="stMarkdownContainer"] h1 {
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)

# العنوان
st.markdown(f"<h1>{texts['title']}</h1>", unsafe_allow_html=True)

# إدخال البيانات من المستخدم
col1, col2 = st.columns(2)
with col1:
    temp = st.number_input(texts["temp"], value=30.0, key="temp_input")
    humidity = st.number_input(texts["hum"], value=50.0, key="humidity_input")
with col2:
    tds = st.number_input(texts["tds"], value=500.0, key="tds_input")
    ph = st.number_input(texts["ph"], value=6.0, key="ph_input")
    

# زر التنبؤ
if st.button(texts["predict"], key="predict_button"):
    # تجهيز البيانات بصيغة مناسبة للموديل
    features = [[temp, humidity, tds, ph,]]
    model= load_model()  # تحميل الموديل
    # توقع النتيجة باستخدام الموديل
    prediction = model.predict(features)

    # عرض النتيجة في صندوق نص
    with st.container():
        st.subheader(texts["result"])
        st.markdown(
            f"""
            <div style="
                background-color: var(--secondary-background);
                color: var(--text);
                border-radius: 8px;
                padding: 20px;
                border-left: 5px solid var(--primary);
                margin: 16px 0;
                box-shadow: 0 3px 8px var(--shadow);
                text-align: center;
            ">
                <h3 style="color: var(--primary); margin: 0; font-size: 1.4rem;">{prediction[0]}</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
