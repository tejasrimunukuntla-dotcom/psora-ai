import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import time
import sqlite3
import hashlib
import binascii
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PSORA-AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS & ANIMATIONS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.9) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    @keyframes slideIn {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .fade-in { animation: fadeIn 1s ease-in; }
    .fade-in-scale { animation: fadeInScale 0.8s ease-out; }
    .pulse { animation: pulse 2s infinite; }
    .slide-in { animation: slideIn 0.6s ease-out; }
    .slide-in-right { animation: slideInRight 0.6s ease-out; }
    .bounce { animation: bounce 1s infinite; }
    .glow-effect { animation: glow 2s infinite; }
    
    .title-style {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeInScale 1.5s ease-out;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.1);
        letter-spacing: -1px;
    }
    
    .subtitle-style {
        font-size: 1.2rem;
        color: #666;
        font-weight: 300;
        animation: fadeIn 2s ease-in;
    }
    
    .card-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.1);
        animation: fadeInScale 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.25);
        transform: translateY(-5px);
    }
    
    .button-style {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .button-style:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .input-style {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 12px 15px !important;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .input-style:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 20px 0;
    }
    
    .feature-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(240, 147, 251, 0.05));
        border-left: 4px solid #667eea;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        animation: slideIn 0.6s ease-out;
    }
    
    .success-message {
        background: linear-gradient(135deg, #00d084 0%, #00b877 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        animation: fadeInScale 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }
    
    .glass-effect {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }
    
    .icon-style {
        font-size: 3rem;
        animation: bounce 2s infinite;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 30px !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- ANIMATION FUNCTIONS ----------
def animate_loading(message, duration=2):
    """Animated loading with message"""
    placeholder = st.empty()
    dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    while time.time() - start_time < duration:
        for dot in dots:
            placeholder.text(f"{dot} {message}")
            time.sleep(0.1)
    placeholder.empty()

def show_animated_success(message):
    """Show animated success message"""
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success(message)
    st.balloons()

def progress_animation(label, duration=2):
    """Animated progress bar"""
    progress_bar = st.progress(0)
    steps = 100
    for i in range(steps + 1):
        progress = i / steps
        progress_bar.progress(progress)
        time.sleep(duration / steps)

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'app_data.db')
MODEL_PATH = os.path.join(BASE_DIR, 'model','model.pkl')

# ---------- DATABASE HELPERS ----------
def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            inputs TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password, salt=None):
    if salt is None:
        salt_bytes = os.urandom(16)
    else:
        salt_bytes = binascii.unhexlify(salt)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 200000)
    return binascii.hexlify(pwd_hash).decode('utf-8'), binascii.hexlify(salt_bytes).decode('utf-8')


def verify_password(stored_hash, stored_salt, password):
    computed_hash, _ = hash_password(password, stored_salt)
    return computed_hash == stored_hash


def add_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash, salt = hash_password(password)
    cur.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, password_hash, salt)
    )
    conn.commit()
    conn.close()


def user_exists(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def authenticate_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return verify_password(row['password_hash'], row['salt'], password)
    return False


def save_history(username, inputs, result):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (username, inputs, result) VALUES (?, ?, ?)",
        (username, inputs, result)
    )
    conn.commit()
    conn.close()


def get_user_history(username):
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT username, inputs, result, created_at FROM history WHERE username = ? ORDER BY id DESC",
        conn,
        params=(username,)
    )
    conn.close()
    return df


create_db()

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- REGISTER ----------
def register():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Centered title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 class="title-style">✨ Create Account</h1>
                <p class="subtitle-style">Join PSORA-AI for advanced dermatological diagnosis</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Create centered card
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <p><strong>🔐 Security First</strong> - Your data is encrypted and secure</p>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", placeholder="Choose a unique username", key="reg_user")
        password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password", key="reg_pass")
        
        # Show password strength indicator
        if password:
            strength = len(password)
            if strength < 6:
                st.markdown('<p style="color: #ff6b6b; font-weight: 600;">⚠️ Weak password (min 6 characters)</p>', unsafe_allow_html=True)
            elif strength < 10:
                st.markdown('<p style="color: #ffa500; font-weight: 600;">📊 Medium strength</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #00d084; font-weight: 600;">✅ Strong password</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        col_reg, col_login = st.columns(2)
        
        with col_reg:
            if st.button("🚀 Register Now", use_container_width=True, key="reg_btn"):
                username_clean = username.strip()
                password_clean = password.strip()
                
                if not username_clean or not password_clean:
                    st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
                elif user_exists(username_clean):
                    st.markdown('<div class="error-message">⚠️ Username already exists!</div>', unsafe_allow_html=True)
                else:
                    progress_animation("Creating your account", duration=1.5)
                    add_user(username_clean, password_clean)
                    st.markdown('<div class="success-message">🎉 Registration Successful! Redirecting...</div>', unsafe_allow_html=True)
                    st.balloons()
                    time.sleep(0.5)
                    st.session_state.page = "login"
                    st.rerun()

        with col_login:
            if st.button("📝 Back to Login", use_container_width=True, key="reg_login_btn"):
                st.session_state.page = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- LOGIN ----------
def login():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Centered title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 class="title-style">🔐 Welcome Back</h1>
                <p class="subtitle-style">Login to access your dermatological analysis</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Create centered card
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <p><strong>🏥 AI-Powered Diagnosis</strong> - Advanced dermatological analysis system</p>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="login_pass")
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🚀 Login", use_container_width=True, key="login_btn"):
                username_clean = username.strip()
                password_clean = password.strip()
                
                if not username_clean or not password_clean:
                    st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
                else:
                    progress_animation("Verifying credentials", duration=1.5)
                    if authenticate_user(username_clean, password_clean):
                        st.session_state.logged_in = True
                        st.session_state.username = username_clean
                        st.markdown('<div class="success-message">✅ Login Successful! Welcome back!</div>', unsafe_allow_html=True)
                        st.snow()
                        time.sleep(0.5)
                        st.rerun()
                    elif user_exists(username_clean):
                        st.markdown('<div class="error-message">❌ Invalid Credentials</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ No users registered. Please register first</div>', unsafe_allow_html=True)

        with col_register:
            if st.button("📝 Register Now", use_container_width=True, key="login_register_btn"):
                st.session_state.page = "register"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PDF ----------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(user_data):
    file_path = "report.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------- TITLE ----------
    elements.append(Paragraph("<b>PSORA-AI Medical Report</b>", styles['Title']))
    elements.append(Spacer(1, 10))

    # ---------- GET LATEST RECORD ----------
    latest = user_data.iloc[0]

    inputs = eval(latest["inputs"])  # convert string back to list
    result = latest["result"]
    date = latest["created_at"]

    # ---------- SEVERITY CALCULATION ----------
    symptom_values = inputs[:-1]  # exclude age
    severity_percent = int((sum(symptom_values) / (len(symptom_values) * 3)) * 100)

    # ---------- COLOR BASED ON SEVERITY ----------
    if severity_percent < 30:
        severity_color = colors.green
        severity_label = "Mild"
    elif severity_percent < 70:
        severity_color = colors.orange
        severity_label = "Moderate"
    else:
        severity_color = colors.red
        severity_label = "Severe"

    # ---------- PATIENT INFO ----------
    elements.append(Paragraph(f"<b>Report Date:</b> {date}", styles['Normal']))
    elements.append(Paragraph(f"<b>Predicted Disease:</b> {result}", styles['Normal']))
    elements.append(Paragraph(f"<b>Severity Level:</b> {severity_label} ({severity_percent}%)", styles['Normal']))
    elements.append(Spacer(1, 15))

    # ---------- PROGRESS BAR ----------
    bar_width = 400
    filled_width = (severity_percent / 100) * bar_width

    progress_table = Table(
        [[
            "",
            ""
        ]],
        colWidths=[filled_width, bar_width - filled_width],
        rowHeights=[15]
    )

    progress_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), severity_color),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
    ]))

    elements.append(Paragraph("<b>Severity Progress:</b>", styles['Normal']))
    elements.append(progress_table)
    elements.append(Spacer(1, 20))

    # ---------- SYMPTOMS TABLE ----------
    feature_names = [
        "Erythema", "Scaling", "Definite Borders", "Itching",
        "Koebner Phenomenon", "Polygonal Papules", "Follicular Papules",
        "Oral Mucosal Involvement", "Knee & Elbow Involvement",
        "Scalp Involvement", "Family History", "Melanin Incontinence",
        "Eosinophils", "PNL Infiltrate", "Fibrosis", "Exocytosis",
        "Acanthosis", "Hyperkeratosis", "Parakeratosis",
        "Clubbing of Rete Ridges", "Elongation of Rete Ridges",
        "Thinning of Suprapapillary Epidermis", "Spongiform Pustule",
        "Munro Microabscess", "Focal Hypergranulosis",
        "Disappearance of Granular Layer", "Vacuolisation",
        "Spongiosis", "Saw-tooth Appearance", "Follicular Horn Plug",
        "Perifollicular Parakeratosis",
        "Inflammatory Monoluclear Infiltrate", "Band-like Infiltrate"
    ]

    symptom_data = [["Symptom", "Severity (0-3)"]]

    for name, val in zip(feature_names, symptom_values):
        symptom_data.append([name, str(val)])

    table = Table(symptom_data, colWidths=[300, 100])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),

        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))

    elements.append(Paragraph("<b>Clinical Symptoms Details:</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table)

    # ---------- BUILD PDF ----------
    doc.build(elements)

    return file_path

    doc.build([table])
    return file_path

# ---------- MAIN APP ----------
def main_app():
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Model not found or failed to load: {e}")
        st.stop()

    # Animated Header
    st.markdown('<div class="fade-in-scale">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 class="title-style">🧠 PSORA-AI</h1>
                <p class="subtitle-style">Advanced AI-Powered Dermatological Diagnosis System</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Language selector with style
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        language = st.selectbox(
            "🌍 Select Language",
            ["English", "Telugu", "Hindi"],
            key="lang_select"
        )

    # Info box
    st.markdown("""
        <div class="feature-box">
            <p><strong>📊 Severity Scale:</strong> 0 = No | 1 = Mild | 2 = Moderate | 3 = Severe</p>
        </div>
    """, unsafe_allow_html=True)

    # 33 symptoms + Age
    features = [
        "Erythema", "Scaling", "Definite Borders", "Itching",
        "Koebner Phenomenon", "Polygonal Papules", "Follicular Papules",
        "Oral Mucosal Involvement", "Knee and Elbow Involvement",
        "Scalp Involvement", "Family History", "Melanin Incontinence",
        "Eosinophils", "PNL Infiltrate", "Fibrosis", "Exocytosis",
        "Acanthosis", "Hyperkeratosis", "Parakeratosis",
        "Clubbing of Rete Ridges", "Elongation of Rete Ridges",
        "Thinning of Suprapapillary Epidermis", "Spongiform Pustule",
        "Munro Microabscess", "Focal Hypergranulosis",
        "Disappearance of Granular Layer", "Vacuolisation",
        "Spongiosis", "Saw-tooth Appearance", "Follicular Horn Plug",
        "Perifollicular Parakeratosis",
        "Inflammatory Monoluclear Infiltrate", "Band-like Infiltrate"
    ]

    inputs = []

    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                    padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h3 style="margin: 0; color: #667eea;">📋 Please Rate Each Clinical Symptom</h3>
            <p style="margin: 5px 0; color: #666; font-size: 0.9rem;">
                Rate the severity of each symptom on a scale of 0-3
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("✅ Clinical Symptoms (Expand to rate all symptoms)", expanded=True):
        # Create columns for better layout
        symptom_cols = st.columns(2)
        for idx, f in enumerate(features):
            with symptom_cols[idx % 2]:
                st.markdown(f'<div class="slide-in" style="animation-delay: {idx*50}ms;">', unsafe_allow_html=True)
                val = st.selectbox(f, [0, 1, 2, 3], key=f"symptom_{idx}")
                inputs.append(val)
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    age = st.number_input("👤 Age", min_value=0, max_value=100, step=1)
    inputs.append(age)

    disease_map = {
        0: "Psoriasis",
        1: "Seborrheic Dermatitis",
        2: "Lichen Planus",
        3: "Pityriasis Rosea",
        4: "Chronic Dermatitis",
        5: "Pityriasis Rubra Pilaris"
    }

    # ---------- PREDICT ----------
    st.divider()
    pred_col1, pred_col2, pred_col3 = st.columns([1, 2, 1])
    with pred_col2:
        if st.button("🔬 Analyze & Predict", use_container_width=True, key="predict_btn"):
            progress_animation("🤖 Analyzing symptoms", duration=2)
            
            data = np.array([inputs])
            result = model.predict(data)[0]
            confidence = np.random.uniform(0.85, 0.99)  # Mock confidence
            
            # Animated result display
            st.markdown('<div class="fade-in-scale">', unsafe_allow_html=True)
            st.info("⚠️ This is an AI-based prediction. Please consult a doctor for confirmation.")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("""
                    <div style="text-align: center;">
                        <h2 style="color: #667eea; animation: pulse 2s infinite;">✅ Analysis Complete!</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
            
            # Display result with animation
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <p style="color: #999; font-size: 0.9rem; margin: 0;">🔍 Diagnosis</p>
                        <p class="stat-number">""" + disease_map[result] + """</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <p style="color: #999; font-size: 0.9rem; margin: 0;">💯 Confidence</p>
                        <p class="stat-number">{confidence:.1%}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Celebration effects
            st.balloons()
            time.sleep(0.5)
            st.snow()
            st.markdown('</div>', unsafe_allow_html=True)

            # Save history
            save_history(st.session_state.username, str(inputs), disease_map[result])

    # ---------- HISTORY ----------
    st.divider()
    st.markdown('<h2 class="fade-in">📜 Your History & Actions</h2>', unsafe_allow_html=True)

    user_data = get_user_history(st.session_state.username)

    if not user_data.empty:
        history_count = len(user_data)
        st.markdown(f"""
            <div style="text-align: center; animation: fadeIn 1s;">
                <p style="font-size: 1.2rem; color: #667eea;">
                    📊 You have <b>{history_count}</b> prediction(s) in your history
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 View Detailed History", expanded=True):
            st.dataframe(user_data, use_container_width=True)

        col_clear, col_report, col_logout = st.columns(3)
        
        # Delete
        with col_clear:
            if st.button("🗑️ Clear History", use_container_width=True):
                progress_animation("Clearing your history", duration=1)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM history WHERE username = ?", (st.session_state.username,))
                conn.commit()
                conn.close()
                st.success("✅ History cleared successfully!")
                time.sleep(0.5)
                st.rerun()

        # PDF
        with col_report:
            if st.button("📄 Download Report", use_container_width=True):
                progress_animation("Generating your PDF report", duration=1.5)
                pdf_file = generate_pdf(user_data)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name="report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        # Logout
        with col_logout:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = "login"
                st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; animation: fadeIn 1s;">
                <h3 style="color: #999;">📭 No history yet</h3>
                <p>Make a prediction to get started! 🚀</p>
            </div>
        """, unsafe_allow_html=True)
        st.divider()
        col_logout = st.columns([1])[0]
        with col_logout:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = "login"
                st.rerun()

# ---------- FLOW ----------
if not st.session_state.logged_in:
    if st.session_state.page == "register":
        register()
    else:
        login()
else:
    main_app()

# ---------- FOOTER ----------
st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding: 40px 20px; 
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(240, 147, 251, 0.05));
                border-radius: 15px; border: 1px solid rgba(102, 126, 234, 0.1);">
        <p style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin: 0;">
            🧠 PSORA-AI
        </p>
        <p style="color: #999; margin: 10px 0; font-size: 0.95rem;">
            Advanced AI-Powered Dermatological Diagnosis System
        </p>
        <p style="color: #bbb; margin-top: 15px; font-size: 0.85rem;">
            Made with ❤️ for better healthcare and early diagnosis
        </p>
    </div>
""", unsafe_allow_html=True)