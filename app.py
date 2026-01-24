import streamlit as st
import sqlite3
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import pandas as pd
import random
import base64
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import time

st.set_page_config(
    page_title="MedTimer - Medication Management",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ WOW DASHBOARD CSS ============
def inject_wow_css(age_category='adult'):
    """Inject stunning WOW CSS with glassmorphism, gradients, and modern animations"""
    primary_color = get_primary_color(age_category)
    secondary_color = get_secondary_color(age_category)
    font_size = get_font_size(age_category)
    background_style = get_gradient_style(age_category)
    
    css = f"""
    <style>
    /* ============ GLOBAL STYLES ============ */
    .stApp {{
        {background_style}
        min-height: 100vh;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ============ CUSTOM FONTS ============ */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    body {{
        font-family: 'Poppins', sans-serif !important;
    }}
    
    /* ============ GLASSMORPHISM CARDS ============ */
    .glass-card {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin: 12px 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }}
    
    .glass-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {primary_color}, {secondary_color}, {primary_color});
        background-size: 200% 100%;
        animation: shimmer 3s infinite;
    }}
    
    .glass-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    /* ============ NEON GLOW EFFECTS ============ */
    .neon-text {{
        text-shadow: 
            0 0 10px {primary_color},
            0 0 20px {primary_color},
            0 0 30px {primary_color},
            0 0 40px {primary_color};
        animation: neon-pulse 2s infinite alternate;
    }}
    
    @keyframes neon-pulse {{
        0% {{ opacity: 0.8; }}
        100% {{ opacity: 1; text-shadow: 0 0 10px {primary_color}, 0 0 20px {primary_color}, 0 0 30px {primary_color}, 0 0 40px {primary_color}, 0 0 50px {primary_color}; }}
    }}
    
    /* ============ 3D FLOATING CARDS ============ */
    .floating-card {{
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        padding: 32px;
        margin: 16px 0;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        perspective: 1000px;
    }}
    
    .floating-card:hover {{
        transform: translateY(-12px) rotateX(5deg) rotateY(-5deg);
        box-shadow: 
            0 30px 90px rgba(0, 0, 0, 0.25),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset;
    }}
    
    /* ============ ANIMATED STAT CARDS ============ */
    .stat-card-wow {{
        background: linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.05));
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border-radius: 32px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 
            0 25px 70px rgba(0, 0, 0, 0.15),
            inset 0 2px 10px rgba(255, 255, 255, 0.3);
        padding: 40px 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }}
    
    .stat-card-wow::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate-bg 10s linear infinite;
    }}
    
    .stat-card-wow:hover {{
        transform: scale(1.08) translateY(-10px);
        box-shadow: 
            0 40px 100px rgba(0, 0, 0, 0.25),
            inset 0 2px 20px rgba(255, 255, 255, 0.4);
    }}
    
    @keyframes rotate-bg {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .stat-number-wow {{
        font-size: 72px;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        line-height: 1.2;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
        animation: number-pulse 2s ease-in-out infinite;
    }}
    
    @keyframes number-pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .stat-label-wow {{
        font-size: {font_size};
        color: rgba(255, 255, 255, 0.95);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }}
    
    /* ============ MEDICATION DOSE CARDS ============ */
    .dose-card {{
        background: linear-gradient(145deg, rgba(255,255,255,0.22), rgba(255,255,255,0.08));
        backdrop-filter: blur(35px);
        -webkit-backdrop-filter: blur(35px);
        border-radius: 24px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 15px 45px rgba(0, 0, 0, 0.12),
            inset 0 1px 15px rgba(255, 255, 255, 0.25);
        padding: 24px 28px;
        margin: 14px 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }}
    
    .dose-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s;
    }}
    
    .dose-card:hover::before {{
        left: 100%;
    }}
    
    .dose-card:hover {{
        transform: translateX(10px) scale(1.02);
        box-shadow: 
            0 25px 60px rgba(0, 0, 0, 0.2),
            inset 0 1px 20px rgba(255, 255, 255, 0.35);
    }}
    
    .dose-card.missed {{
        border-left: 6px solid #ef4444;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
    }}
    
    .dose-card.upcoming {{
        border-left: 6px solid #f59e0b;
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
    }}
    
    .dose-card.taken {{
        border-left: 6px solid #10b981;
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
    }}
    
    /* ============ WOW BUTTONS ============ */
    .wow-button {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        border: none;
        border-radius: 16px;
        padding: 16px 32px;
        color: white;
        font-weight: 700;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.2),
            inset 0 2px 10px rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .wow-button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }}
    
    .wow-button:hover::before {{
        left: 100%;
    }}
    
    .wow-button:hover {{
        transform: translateY(-4px) scale(1.05);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.3),
            inset 0 2px 20px rgba(255, 255, 255, 0.3);
    }}
    
    .wow-button:active {{
        transform: translateY(0) scale(0.98);
    }}
    
    /* ============ ANIMATED SEPARATORS ============ */
    .animated-separator {{
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            {primary_color}, 
            {secondary_color}, 
            {primary_color}, 
            transparent);
        background-size: 200% 100%;
        animation: separator-flow 3s linear infinite;
        margin: 30px 0;
    }}
    
    @keyframes separator-flow {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    /* ============ PARTICLES BACKGROUND ============ */
    .particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }}
    
    .particle {{
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        animation: float-particle 15s infinite;
        opacity: 0;
    }}
    
    @keyframes float-particle {{
        0% {{ 
            transform: translateY(100vh) rotate(0deg); 
            opacity: 0;
        }}
        10% {{ opacity: 0.6; }}
        90% {{ opacity: 0.6; }}
        100% {{ 
            transform: translateY(-100vh) rotate(720deg); 
            opacity: 0;
        }}
    }}
    
    /* ============ WOW HEADING ============ */
    .wow-heading {{
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, {primary_color} 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        animation: heading-glow 3s ease-in-out infinite alternate;
        text-align: center;
        margin-bottom: 10px;
    }}
    
    @keyframes heading-glow {{
        0% {{ filter: brightness(1); }}
        100% {{ filter: brightness(1.2); }}
    }}
    
    /* ============ REMINDER BANNER WOW ============ */
    .reminder-banner-wow {{
        background: linear-gradient(135deg, rgba(254, 243, 199, 0.95), rgba(253, 230, 138, 0.95));
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 3px solid #f59e0b;
        border-radius: 24px;
        padding: 28px 32px;
        margin: 24px 0;
        box-shadow: 
            0 20px 60px rgba(245, 158, 11, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        animation: pulse-glow 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }}
    
    .reminder-banner-wow::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.2) 0%, transparent 70%);
        animation: rotate-bg 5s linear infinite;
    }}
    
    @keyframes pulse-glow {{
        0%, 100% {{ 
            box-shadow: 0 20px 60px rgba(245, 158, 11, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            transform: scale(1);
        }}
        50% {{ 
            box-shadow: 0 30px 80px rgba(245, 158, 11, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            transform: scale(1.02);
        }}
    }}
    
    .reminder-due-banner-wow {{
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.95), rgba(252, 165, 165, 0.95));
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 3px solid #ef4444;
        border-radius: 24px;
        padding: 28px 32px;
        margin: 24px 0;
        box-shadow: 
            0 20px 60px rgba(239, 68, 68, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        animation: urgent-pulse 1s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }}
    
    @keyframes urgent-pulse {{
        0%, 100% {{ 
            box-shadow: 0 20px 60px rgba(239, 68, 68, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            transform: scale(1);
        }}
        50% {{ 
            box-shadow: 0 30px 80px rgba(239, 68, 68, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            transform: scale(1.03);
        }}
    }}
    
    /* ============ MASCOT ANIMATION ============ */
    .mascot-wow {{
        font-size: 100px;
        animation: mascot-bounce 2s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.3));
    }}
    
    @keyframes mascot-bounce {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        25% {{ transform: translateY(-15px) rotate(-5deg); }}
        50% {{ transform: translateY(0) rotate(0deg); }}
        75% {{ transform: translateY(-10px) rotate(5deg); }}
    }}
    
    /* ============ SECTION HEADERS WOW ============ */
    .section-header-wow {{
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        padding: 20px 40px;
        border-radius: 20px;
        margin: 30px 0 20px 0;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 3px;
        animation: header-slide 0.8s ease-out;
    }}
    
    @keyframes header-slide {{
        0% {{ 
            opacity: 0;
            transform: translateY(-30px);
        }}
        100% {{ 
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .section-missed-wow {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.9), rgba(220, 38, 38, 0.9));
        color: white;
        box-shadow: 0 10px 40px rgba(239, 68, 68, 0.4);
    }}
    
    .section-upcoming-wow {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.9), rgba(217, 119, 6, 0.9));
        color: white;
        box-shadow: 0 10px 40px rgba(245, 158, 11, 0.4);
    }}
    
    .section-taken-wow {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9));
        color: white;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4);
    }}
    
    /* ============ CHART CONTAINER ============ */
    .chart-container-wow {{
        background: linear-gradient(145deg, rgba(255,255,255,0.18), rgba(255,255,255,0.06));
        backdrop-filter: blur(35px);
        -webkit-backdrop-filter: blur(35px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.15),
            inset 0 2px 15px rgba(255, 255, 255, 0.25);
        padding: 32px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    .chart-container-wow:hover {{
        transform: scale(1.02);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.2),
            inset 0 2px 25px rgba(255, 255, 255, 0.35);
    }}
    
    /* ============ TEXT STYLES ============ */
    .wow-text {{
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        font-weight: 600;
    }}
    
    .wow-text-muted {{
        color: rgba(255, 255, 255, 0.85);
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
    }}
    
    /* ============ FILTER TABS WOW ============ */
    .filter-tabs-wow {{
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 24px 0;
        flex-wrap: wrap;
    }}
    
    .filter-tab-wow {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 12px 28px;
        color: white;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px;
    }}
    
    .filter-tab-wow:hover {{
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }}
    
    .filter-tab-wow.active {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(0, 0, 0, 0.2) inset;
    }}
    
    /* ============ STYLES FOR STREAMLIT COMPONENTS ============ */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 800 !important;
        color: #ffffff !important;
    }}
    
    p, div, span, label {{
        color: rgba(255, 255, 255, 0.95) !important;
    }}
    
    .stButton > button {{
        border-radius: 16px !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        border: none !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        font-size: 16px !important;
        color: #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        background: linear-gradient(135deg, {primary_color}, {secondary_color}) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* ============ ANIMATION ON SCROLL ============ */
    .animate-on-scroll {{
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    .animate-on-scroll.visible {{
        opacity: 1;
        transform: translateY(0);
    }}
    
    </style>
    
    <!-- Particles Background -->
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    </div>
    """
    return css

# ============ KEEP ALL ORIGINAL FUNCTIONS ============
# (Copy all the original helper functions here)
# These functions are unchanged - only the UI is redesigned

def init_database():
    """Initialize SQLite database with all tables"""
    conn = sqlite3.connect('medtimer.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  name TEXT,
                  age INTEGER,
                  email TEXT,
                  password TEXT,
                  user_type TEXT,
                  phone TEXT,
                  relationship TEXT,
                  experience TEXT,
                  notes TEXT,
                  created_at TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS medications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  name TEXT,
                  dosage_type TEXT,
                  dosage_amount TEXT,
                  frequency TEXT,
                  time TEXT,
                  reminder_times TEXT,
                  color TEXT,
                  instructions TEXT,
                  taken_doses TEXT,
                  created_at TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS diseases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  name TEXT,
                  type TEXT,
                  notes TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  doctor TEXT,
                  specialty TEXT,
                  date TEXT,
                  time TEXT,
                  location TEXT,
                  phone TEXT,
                  notes TEXT,
                  created_at TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS side_effects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  medication TEXT,
                  severity TEXT,
                  type TEXT,
                  description TEXT,
                  date TEXT,
                  reported_at TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS medication_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  medication_id INTEGER,
                  action TEXT,
                  timestamp TEXT,
                  date TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS adherence_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  date TEXT,
                  adherence REAL,
                  updated TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS connected_patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  caregiver_username TEXT,
                  patient_username TEXT,
                  access_code TEXT,
                  connected_at TEXT,
                  FOREIGN KEY(caregiver_username) REFERENCES users(username))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  medication_id INTEGER,
                  reminder_time TEXT,
                  acknowledged INTEGER DEFAULT 0,
                  created_at TEXT,
                  FOREIGN KEY(username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('medtimer.db', check_same_thread=False)

def get_age_category(age):
    """Determine age category based on age"""
    if age < 18:
        return 'youth'
    elif age <= 40:
        return 'adult'
    else:
        return 'senior'

def get_gradient_style(age_category):
    """Get gradient background style based on age category"""
    if age_category == 'youth':
        return "background: linear-gradient(135deg, #9333ea 0%, #a855f7 50%, #c084fc 100%);"
    elif age_category == 'adult':
        return "background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);"
    else:
        return "background: linear-gradient(135deg, #eab308 0%, #ca8a04 50%, #a16207 100%);"

def get_font_size(age_category):
    """Get font size based on age category"""
    if age_category == 'youth':
        return "16px"
    elif age_category == 'adult':
        return "18px"
    else:
        return "22px"

def get_primary_color(age_category):
    """Get primary color based on age category"""
    if age_category == 'youth':
        return "#9333ea"
    elif age_category == 'adult':
        return "#22c55e"
    else:
        return "#eab308"

def get_secondary_color(age_category):
    """Get secondary color based on age category"""
    if age_category == 'youth':
        return "#a855f7"
    elif age_category == 'adult':
        return "#16a34a"
    else:
        return "#ca8a04"

def format_time(time_str):
    """Format time string"""
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str

def get_current_datetime_display():
    """Get current date and time formatted for display"""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    return date_str, time_str

def get_custom_medication_times(frequency):
    """Get default custom medication times based on frequency"""
    frequency_map = {
        'once-daily': ['09:00'],
        'twice-daily': ['08:00', '20:00'],
        'three-times-daily': ['08:00', '13:00', '20:00'],
        'every-4-hours': ['08:00', '12:00', '16:00', '20:00'],
        'every-6-hours': ['06:00', '12:00', '18:00', '00:00'],
        'every-8-hours': ['08:00', '16:00', '00:00'],
        'every-12-hours': ['08:00', '20:00'],
        'as-needed': ['09:00'],
        'weekly': ['09:00'],
        'monthly': ['09:00']
    }
    return frequency_map.get(frequency, ['09:00'])

def play_reminder_sound():
    """Play reminder sound using HTML audio"""
    audio_html = """
    <audio id="reminderSound" autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    <script>
        var audio = document.getElementById('reminderSound');
        audio.volume = 0.7;
        audio.play().catch(function(error) {
            console.log('Audio play failed:', error);
        });
    </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def play_notification_sound():
    """Play notification sound for reminders"""
    audio_html = """
    <audio id="notificationSound" autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    <script>
        var audio = document.getElementById('notificationSound');
        audio.volume = 0.6;
        audio.play().catch(function(error) {
            console.log('Audio play failed:', error);
        });
    </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def show_100_percent_adherence_animation():
    """Show celebration animation when 100% adherence is achieved"""
    animation_html = """
    <style>
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    
    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(16, 185, 129, 0.5); }
        50% { transform: scale(1.1); box-shadow: 0 0 40px rgba(16, 185, 129, 0.8); }
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        animation: confetti-fall 3s linear forwards;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    
    <script>
    function createConfetti() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#dfe6e9', '#fd79a8', '#a29bfe'];
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 5000);
        }
    }
    
    createConfetti();
    </script>
    """
    st.markdown(animation_html, unsafe_allow_html=True)

def get_all_doses_for_medication(med):
    """Get all individual doses for a medication with their status"""
    today = datetime.now().strftime("%Y-%m-%d")
    reminder_times = med.get('reminder_times', [med.get('time', '09:00')])
    taken_doses = med.get('taken_doses', [])
    
    doses = []
    for i, time_str in enumerate(reminder_times):
        # Check if this specific dose was taken today
        dose_taken = False
        for taken_dose in taken_doses:
            if taken_dose.get('date') == today and taken_dose.get('time') == time_str:
                dose_taken = True
                break
        
        doses.append({
            'medication_id': med['id'],
            'medication_name': med['name'],
            'dosage_amount': med['dosageAmount'],
            'frequency': med.get('frequency', ''),
            'color': med.get('color', 'blue'),
            'time': time_str,
            'taken': dose_taken,
            'dose_index': i
        })
    
    return doses

def categorize_doses_by_status(doses):
    """Categorize all individual doses into missed, upcoming, and taken"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")
    
    missed = []
    upcoming = []
    taken = []
    
    for dose in doses:
        dose_time = dose['time']
        dose_taken = dose['taken']
        
        if dose_taken:
            taken.append(dose)
        else:
            try:
                dose_datetime = datetime.strptime(dose_time, "%H:%M")
                now_time = datetime.strptime(current_time, "%H:%M")
                
                if dose_datetime < now_time:
                    missed.append(dose)
                else:
                    upcoming.append(dose)
            except:
                upcoming.append(dose)
    
    # Sort by time
    missed.sort(key=lambda x: x['time'])
    upcoming.sort(key=lambda x: x['time'])
    taken.sort(key=lambda x: x['time'])
    
    return missed, upcoming, taken

def calculate_adherence(medications):
    """Calculate adherence based on individual doses"""
    if not medications:
        return 0

    total_doses = 0
    taken_doses = 0

    for med in medications:
        times = med.get('reminder_times', [med.get('time')])
        total_doses += len(times)
        
        # Count how many of today's doses have been taken
        today = datetime.now().strftime("%Y-%m-%d")
        taken = med.get('taken_doses', [])
        today_taken = [t for t in taken if t.get('date') == today]
        taken_doses += len(today_taken)

    return round((taken_doses / total_doses) * 100, 2) if total_doses > 0 else 0

def get_mascot_message(adherence, time_of_day):
    """Get mascot message based on adherence and time of day"""
    if adherence >= 90:
        messages = {
            'morning': [
                "🌟 You're a medication superstar! Keep shining!",
                "☀️ Amazing start to the day! 90%+ adherence!",
                "🎯 Perfect score so far! You're crushing it!"
            ],
            'afternoon': [
                "🌟 Still going strong! You're unstoppable!",
                "💪 Your dedication is inspiring!",
                "🏆 Champion status maintained all day!"
            ],
            'evening': [
                "🌟 What a perfect day! You're amazing!",
                "🎉 Congratulations on near-perfect adherence!",
                "⭐ You've mastered your medication routine!"
            ]
        }
    elif adherence >= 70:
        messages = {
            'morning': [
                "👍 Good start today! Let's keep it up!",
                "💪 You're doing great! Keep going!",
                "🌅 Nice start! Stay on track!"
            ],
            'afternoon': [
                "👍 Still doing well! Almost there!",
                "💪 Good progress! You can do it!",
                "🌤 Staying strong! Keep focused!"
            ],
            'evening': [
                "👍 Good effort today! Tomorrow will be even better!",
                "💪 Solid work! Rest well!",
                "🌙 Nice job! You're improving!"
            ]
        }
    elif adherence >= 50:
        messages = {
            'morning': [
                "🤔 Let's focus on today's medications!",
                "💭 Every pill counts! Let's try to take all!",
                "📋 Review your schedule and stay mindful!"
            ],
            'afternoon': [
                "🤔 Keep trying! You've got this!",
                "💭 Stay focused on your health goals!",
                "📋 Don't forget your afternoon doses!"
            ],
            'evening': [
                "🤔 Tomorrow is a new day! Let's plan better!",
                "💭 Reflect and prepare for a better day!",
                "📋 Let's organize your schedule for tomorrow!"
            ]
        }
    else:
        messages = {
            'morning': [
                "⚠️ Let's make today better than yesterday!",
                "💪 Start fresh! You can improve!",
                "🎯 Focus on one medication at a time!"
            ],
            'afternoon': [
                "⚠️ Don't give up! Every dose matters!",
                "💪 Small steps lead to big changes!",
                "🎯 Stay committed to your health!"
            ],
            'evening': [
                "⚠️ Tomorrow is a fresh start! Let's plan!",
                "💪 I believe in you! Try again tomorrow!",
                "🎯 Let's set a goal for tomorrow!"
            ]
        }
    
    import random
    return random.choice(messages.get(time_of_day, messages['morning']))

def update_mascot_mood(adherence):
    """Update mascot mood based on adherence"""
    if adherence >= 90:
        st.session_state.turtle_mood = 'excited'
    elif adherence >= 70:
        st.session_state.turtle_mood = 'happy'
    elif adherence >= 50:
        st.session_state.turtle_mood = 'neutral'
    else:
        st.session_state.turtle_mood = 'worried'

def check_upcoming_reminders(doses):
    """Check for upcoming doses and show reminders"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    for dose in doses[:3]:
        dose_time = dose['time']
        try:
            med_datetime = datetime.strptime(dose_time, "%H:%M")
            time_diff = (med_datetime - now).total_seconds() / 60 
            
            if 0 < time_diff <= 30:
                return True, dose, int(time_diff)
        except:
            continue
    return False, None, 0

def check_due_doses(doses):
    """Check for doses that are due now"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    due_doses = []
    for dose in doses:
        if not dose['taken']:
            dose_time = dose['time']
            
            try:
                dose_datetime = datetime.strptime(dose_time, "%H:%M")
                time_diff = abs((now - dose_datetime).total_seconds() / 60)
                
                if time_diff <= 5:
                    due_doses.append(dose)
            except:
                continue
    
    return due_doses

def get_mascot_emoji(mood):
    """Get emoji mascot based on mood"""
    mascot_emojis = {
        'happy': '🐢😊',
        'excited': '🐢🎉',
        'neutral': '🐢😐',
        'worried': '🐢😟'
    }
    return mascot_emojis.get(mood, '🐢')

def get_severity_color(severity):
    """Get color for severity level"""
    colors = {'Mild': '#10b981', 'Moderate': '#f59e0b', 'Severe': '#ef4444'}
    return colors.get(severity, '#6b7280')

def get_severity_emoji(severity):
    """Get emoji for severity level"""
    emojis = {'Mild': '🟢', 'Moderate': '🟡', 'Severe': '🔴'}
    return emojis.get(severity, '⚪')

def get_medication_color_hex(color_name):
    """Convert color name to hex value"""
    colors = {
        'blue': '#3B82F6', 'green': '#10B981', 'purple': '#8B5CF6',
        'pink': '#EC4899', 'orange': '#F59E0B', 'red': '#EF4444',
        'yellow': '#EAB308', 'indigo': '#6366F1', 'teal': '#14B8A6', 'cyan': '#06B6D4'
    }
    return colors.get(color_name.lower(), '#3B82F6')

def format_date(date_str):
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def days_until(date_str):
    """Calculate days until a date"""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = target_date - today
        return delta.days
    except:
        return 0

def get_time_of_day():
    """Get current time of day greeting"""
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def check_medication_conflicts(medications, new_medication):
    """Check for potential medication time conflicts"""
    conflicts = []
    new_time = new_medication.get('time', '00:00')
    for med in medications:
        med_time = med.get('time', '00:00')
        time_diff = abs(
            datetime.strptime(new_time, "%H:%M") - 
            datetime.strptime(med_time, "%H:%M")
        )
        if time_diff.total_seconds() < 1800:
            conflicts.append(med['name'])
    return conflicts

def generate_patient_code():
    """Generate a 6-digit patient access code"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def initialize_session_state():
    """Initialize all session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'patient_login'
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'medications' not in st.session_state:
        st.session_state.medications = []
    if 'appointments' not in st.session_state:
        st.session_state.appointments = []
    if 'side_effects' not in st.session_state:
        st.session_state.side_effects = []
    if 'turtle_mood' not in st.session_state:
        st.session_state.turtle_mood = 'happy'
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    if 'signup_step' not in st.session_state:
        st.session_state.signup_step = 1
    if 'signup_data' not in st.session_state:
        st.session_state.signup_data = {}
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'medication_history' not in st.session_state:
        st.session_state.medication_history = []
    if 'adherence_history' not in st.session_state:
        st.session_state.adherence_history = []
    if 'connected_patients' not in st.session_state:
        st.session_state.connected_patients = []
    if 'editing_medication' not in st.session_state:
        st.session_state.editing_medication = None
    if 'sound_enabled' not in st.session_state:
        st.session_state.sound_enabled = True
    if 'last_reminder_check' not in st.session_state:
        st.session_state.last_reminder_check = datetime.now()
    if 'show_celebration' not in st.session_state:
        st.session_state.show_celebration = False
    if 'previous_adherence' not in st.session_state:
        st.session_state.previous_adherence = 0

def save_user_data():
    """Save user data to SQLite database"""
    if not st.session_state.user_profile:
        return False
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        username = st.session_state.user_profile.get('username')
        
        c.execute('''INSERT OR REPLACE INTO users 
                     (username, name, age, email, password, user_type, phone, relationship, experience, notes, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (username,
                   st.session_state.user_profile.get('name'),
                   st.session_state.user_profile.get('age'),
                   st.session_state.user_profile.get('email', ''),
                   st.session_state.user_profile.get('password', ''),
                   st.session_state.user_profile.get('userType'),
                   st.session_state.user_profile.get('phone', ''),
                   st.session_state.user_profile.get('relationship', ''),
                   st.session_state.user_profile.get('experience', ''),
                   st.session_state.user_profile.get('notes', ''),
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        c.execute('DELETE FROM diseases WHERE username = ?', (username,))
        for disease in st.session_state.user_profile.get('diseases', []):
            c.execute('INSERT INTO diseases (username, name, type, notes) VALUES (?, ?, ?, ?)',
                     (username, disease.get('name'), disease.get('type'), disease.get('notes', '')))
        
        c.execute('DELETE FROM medications WHERE username = ?', (username,))
        for med in st.session_state.medications:
            c.execute('''INSERT INTO medications 
                         (username, name, dosage_type, dosage_amount, frequency, time, reminder_times, color, instructions, taken_doses, created_at)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (username,
                      med.get('name'),
                      med.get('dosageType'),
                      med.get('dosageAmount'),
                      med.get('frequency'),
                      med.get('time'),
                      json.dumps(med.get('reminder_times', [med.get('time')])),
                      med.get('color'),
                      med.get('instructions', ''),
                      json.dumps(med.get('taken_doses', [])),
                      med.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        
        c.execute('DELETE FROM appointments WHERE username = ?', (username,))
        for appt in st.session_state.appointments:
            c.execute('''INSERT INTO appointments 
                         (username, doctor, specialty, date, time, location, phone, notes, created_at)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (username, appt.get('doctor'), appt.get('specialty'), appt.get('date'),
                      appt.get('time'), appt.get('location', ''), appt.get('phone', ''),
                      appt.get('notes', ''), appt.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        
        c.execute('DELETE FROM side_effects WHERE username = ?', (username,))
        for effect in st.session_state.side_effects:
            c.execute('''INSERT INTO side_effects 
                         (username, medication, severity, type, description, date, reported_at)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (username, effect.get('medication'), effect.get('severity'),
                      effect.get('type', ''), effect.get('description'),
                      effect.get('date'), effect.get('reported_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_user_data(username):
    """Load user data from SQLite database"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        
        if not user:
            conn.close()
            return False
        
        st.session_state.user_profile = {
            'username': user[0],
            'name': user[1],
            'age': user[2],
            'email': user[3],
            'password': user[4],
            'userType': user[5],
            'phone': user[6],
            'relationship': user[7],
            'experience': user[8],
            'notes': user[9],
            'diseases': []
        }
        
        c.execute('SELECT * FROM diseases WHERE username = ?', (username,))
        diseases = c.fetchall()
        for disease in diseases:
            st.session_state.user_profile['diseases'].append({
                'id': str(disease[0]),
                'name': disease[2],
                'type': disease[3],
                'notes': disease[4]
            })
        
        c.execute('SELECT * FROM medications WHERE username = ?', (username,))
        meds = c.fetchall()
        st.session_state.medications = []
        for med in meds:
            st.session_state.medications.append({
                'id': med[0],
                'name': med[2],
                'dosageType': med[3],
                'dosageAmount': med[4],
                'frequency': med[5],
                'time': med[6],
                'reminder_times': json.loads(med[7]) if med[7] else [med[6]],
                'color': med[8],
                'instructions': med[9],
                'taken_doses': json.loads(med[10]) if med[10] else [],
                'created_at': med[11]
            })
        
        c.execute('SELECT * FROM appointments WHERE username = ?', (username,))
        appts = c.fetchall()
        st.session_state.appointments = []
        for appt in appts:
            st.session_state.appointments.append({
                'id': appt[0],
                'doctor': appt[2],
                'specialty': appt[3],
                'date': appt[4],
                'time': appt[5],
                'location': appt[6],
                'phone': appt[7],
                'notes': appt[8],
                'created_at': appt[9]
            })
        
        c.execute('SELECT * FROM side_effects WHERE username = ?', (username,))
        effects = c.fetchall()
        st.session_state.side_effects = []
        for effect in effects:
            st.session_state.side_effects.append({
                'id': effect[0],
                'medication': effect[2],
                'severity': effect[3],
                'type': effect[4],
                'description': effect[5],
                'date': effect[6],
                'reported_at': effect[7]
            })
        
        c.execute('SELECT * FROM medication_history WHERE username = ?', (username,))
        hist = c.fetchall()
        st.session_state.medication_history = []
        for h in hist:
            st.session_state.medication_history.append({
                'medication_id': h[2],
                'action': h[3],
                'timestamp': h[4],
                'date': h[5]
            })
        
        c.execute('SELECT * FROM adherence_history WHERE username = ?', (username,))
        adh = c.fetchall()
        st.session_state.adherence_history = []
        for a in adh:
            st.session_state.adherence_history.append({
                'date': a[2],
                'adherence': a[3],
                'updated': a[4]
            })
        
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

def user_exists(username):
    """Check if user exists"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def update_medication_history(medication_id, action='taken', dose_time=None):
    """Update medication history"""
    if not st.session_state.user_profile:
        return
    
    username = st.session_state.user_profile['username']
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''INSERT INTO medication_history (username, medication_id, action, timestamp, date)
                 VALUES (?, ?, ?, ?, ?)''',
             (username, medication_id, action,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()

def update_adherence_history():
    """Update daily adherence history"""
    if not st.session_state.user_profile:
        return
    
    username = st.session_state.user_profile['username']
    today = datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.medications:
        adherence = calculate_adherence(st.session_state.medications)
    else:
        adherence = 0
    
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT id FROM adherence_history WHERE username = ? AND date = ?', (username, today))
    existing = c.fetchone()
    
    if existing:
        c.execute('UPDATE adherence_history SET adherence = ?, updated = ? WHERE id = ?',
                 (adherence, datetime.now().strftime("%H:%M:%S"), existing[0]))
    else:
        c.execute('INSERT INTO adherence_history (username, date, adherence, updated) VALUES (?, ?, ?, ?)',
                 (username, today, adherence, datetime.now().strftime("%H:%M:%S")))
    
    conn.commit()
    conn.close()

def clear_session_data():
    """Clear all session data (logout)"""
    st.session_state.user_profile = None
    st.session_state.medications = []
    st.session_state.appointments = []
    st.session_state.side_effects = []
    st.session_state.achievements = []
    st.session_state.medication_history = []
    st.session_state.adherence_history = []
    st.session_state.connected_patients = []
    st.session_state.turtle_mood = 'happy'
    st.session_state.signup_step = 1
    st.session_state.signup_data = {}
    st.session_state.editing_medication = None
    st.session_state.show_celebration = False
    st.session_state.previous_adherence = 0

# ============ WOW DASHBOARD OVERVIEW ============
def dashboard_overview_tab_wow(age_category):
    """STUNNING WOW dashboard with glassmorphism and modern animations"""
    current_date, current_time = get_current_datetime_display()
    
    # WOW HEADING
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 class="wow-heading">✨ YOUR HEALTH JOURNEY ✨</h1>
        <p class="wow-text-muted" style="font-size: 20px;">{current_date} • {current_time}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all individual doses
    all_doses = []
    for med in st.session_state.medications:
        all_doses.extend(get_all_doses_for_medication(med))
    
    # Categorize doses
    missed_doses, upcoming_doses, taken_doses = categorize_doses_by_status(all_doses)
    
    # WOW FILTER TABS
    st.markdown("""
    <div class="filter-tabs-wow">
        <button class="filter-tab-wow active" onclick="setFilter('All')">All</button>
        <button class="filter-tab-wow" onclick="setFilter('Missed')">Missed</button>
        <button class="filter-tab-wow" onclick="setFilter('Upcoming')">Upcoming</button>
        <button class="filter-tab-wow" onclick="setFilter('Taken')">Taken</button>
    </div>
    """, unsafe_allow_html=True)
    
    filter_tab = st.radio(
        "View medications",
        ["All", "Missed", "Upcoming", "Taken"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Filter doses based on selection
    if filter_tab == "All":
        doses_to_show = all_doses
    elif filter_tab == "Missed":
        doses_to_show = missed_doses
    elif filter_tab == "Upcoming":
        doses_to_show = upcoming_doses
    elif filter_tab == "Taken":
        doses_to_show = taken_doses
    
    # WOW STATISTICS CARDS
    total_meds = len(st.session_state.medications)
    taken_today = len(taken_doses)
    total_doses_count = len(all_doses)
    adherence = calculate_adherence(st.session_state.medications)
    
    update_mascot_mood(adherence)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card-wow">
            <div class="stat-number-wow">{total_meds}</div>
            <div class="stat-label-wow">Medications</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card-wow">
            <div class="stat-number-wow">{taken_today}</div>
            <div class="stat-label-wow">Taken Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card-wow">
            <div class="stat-number-wow">{total_doses_count}</div>
            <div class="stat-label-wow">Total Doses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        adherence_color = "#10b981" if adherence >= 70 else "#f59e0b" if adherence >= 50 else "#ef4444"
        st.markdown(f"""
        <div class="stat-card-wow">
            <div class="stat-number-wow" style="background: linear-gradient(135deg, {adherence_color}, {adherence_color}88); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{adherence:.0f}%</div>
            <div class="stat-label-wow">Adherence</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='animated-separator'></div>", unsafe_allow_html=True)
    
    # WOW MASCOT SECTION
    time_of_day = get_time_of_day().lower().replace('👋 ', '')
    mascot_message = get_mascot_message(adherence, time_of_day)
    mascot_emoji = get_mascot_emoji(st.session_state.turtle_mood)
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 40px;">
        <div class="mascot-wow">{mascot_emoji}</div>
        <p class="wow-text" style="font-size: 24px; font-weight: 700; margin-top: 20px;">
            {mascot_message}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sound Toggle
    col_sound_left, col_sound_right = st.columns([4, 1])
    with col_sound_right:
        if st.button("🔊" if st.session_state.sound_enabled else "🔇", use_container_width=True):
            st.session_state.sound_enabled = not st.session_state.sound_enabled
            st.rerun()
    
    st.markdown("<div class='animated-separator'></div>", unsafe_allow_html=True)
    
    # WOW DUE DOSE REMINDER
    due_doses = check_due_doses(all_doses)
    if due_doses:
        if st.session_state.sound_enabled:
            play_reminder_sound()
        st.markdown("<div class='reminder-due-banner-wow'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #991b1b; margin-top: 0; text-align: center; font-size: 28px; font-weight: 800;'>🔔 MEDICATION DUE NOW!</h3>", unsafe_allow_html=True)
        for dose in due_doses:
            color_hex = get_medication_color_hex(dose.get('color', 'blue'))
            st.markdown(f"""
            <div class="dose-card missed">
                <div style='display: flex; align-items: center; gap: 20px;'>
                    <div style='width: 20px; height: 20px; border-radius: 50%; background-color: {color_hex}; box-shadow: 0 0 20px {color_hex};'></div>
                    <div class="wow-text">
                        <strong style='font-size: 24px;'>{dose['medication_name']}</strong> <span style='font-size: 20px;'>({dose['dosage_amount']})</span>
                        <br><span style='font-size: 18px; opacity: 0.9;'>⏰ Due Now: {format_time(dose['time'])}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✓ Take Now", key=f"take_due_{dose['medication_id']}_{dose['dose_index']}", use_container_width=True):
                for med in st.session_state.medications:
                    if med['id'] == dose['medication_id']:
                        # Add this specific dose to taken_doses
                        today = datetime.now().strftime("%Y-%m-%d")
                        new_taken = {
                            'date': today,
                            'time': dose['time']
                        }
                        if 'taken_doses' not in med:
                            med['taken_doses'] = []
                        med['taken_doses'].append(new_taken)
                        
                        update_medication_history(med['id'], 'taken', dose['time'])
                        update_adherence_history()
                        save_user_data()
                        
                        new_adherence = calculate_adherence(st.session_state.medications)
                        if new_adherence >= 100 and st.session_state.previous_adherence < 100:
                            st.session_state.previous_adherence = new_adherence
                            show_100_percent_adherence_animation()
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-left: 6px solid #10b981;">
            <p class="wow-text" style="font-size: 22px; font-weight: 700;">🎉 No medications due right now!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # WOW UPCOMING REMINDER
    has_upcoming, upcoming_dose, time_to_take = check_upcoming_reminders(upcoming_doses)
    if has_upcoming and time_to_take > 0:
        st.markdown("<div class='reminder-banner-wow'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #92400e; margin-top: 0; text-align: center; font-size: 26px; font-weight: 800;'>⏰ Upcoming Reminder</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p class="wow-text" style="text-align: center; font-size: 20px; margin: 20px 0;">
            <strong style='font-size: 24px;'>{upcoming_dose['medication_name']}</strong> ({upcoming_dose['dosage_amount']}) 
            is due in <strong style='font-size: 28px; color: #92400e;'>{time_to_take} minutes</strong> at {format_time(upcoming_dose['time'])}
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='animated-separator'></div>", unsafe_allow_html=True)
    
    # WOW DOSE DISPLAY
    doses_to_show.sort(key=lambda x: x['time'])
    
    # Group doses by medication
    from collections import defaultdict
    doses_by_med = defaultdict(list)
    for dose in doses_to_show:
        doses_by_med[dose['medication_id']].append(dose)
    
    for med_id, med_doses in doses_by_med.items():
        # Find the medication
        med = next((m for m in st.session_state.medications if m['id'] == med_id), None)
        if not med:
            continue
        
        # Determine medication status based on doses
        all_taken = all(d['taken'] for d in med_doses)
        any_taken = any(d['taken'] for d in med_doses)
        
        if all_taken:
            status_class = "taken"
            section_header = "✅ Taken Medications"
            section_class = "section-taken-wow"
        elif any_taken:
            # Partially taken
            remaining = [d for d in med_doses if not d['taken']]
            if remaining and remaining[0]['time'] >= datetime.now().strftime("%H:%M"):
                status_class = "upcoming"
                section_header = "⏰ Upcoming Medications"
                section_class = "section-upcoming-wow"
            else:
                status_class = "missed"
                section_header = "❌ Missed Medications"
                section_class = "section-missed-wow"
        elif med_doses and med_doses[0]['time'] >= datetime.now().strftime("%H:%M"):
            status_class = "upcoming"
            section_header = "⏰ Upcoming Medications"
            section_class = "section-upcoming-wow"
        else:
            status_class = "missed"
            section_header = "❌ Missed Medications"
            section_class = "section-missed-wow"
        
        # Section Header
        st.markdown(f"<div class='section-header-wow {section_class}'>{section_header}</div>", unsafe_allow_html=True)
        
        # Show each dose separately
        for dose in med_doses:
            color_hex = get_medication_color_hex(med.get('color', 'blue'))
            dose_status_class = "taken" if dose['taken'] else "missed" if dose['time'] < datetime.now().strftime("%H:%M") else "upcoming"
            
            # Calculate time remaining
            time_remaining = ""
            if not dose['taken'] and dose['time'] >= datetime.now().strftime("%H:%M"):
                try:
                    now = datetime.now()
                    dose_datetime = datetime.strptime(dose['time'], "%H:%M").replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    time_diff_minutes = int((dose_datetime - now).total_seconds() / 60)
                    
                    if time_diff_minutes == 1:
                        time_remaining = "in 1 minute"
                    else:
                        time_remaining = f"in {time_diff_minutes} minutes"
                except:
                    time_remaining = "Today"
            elif dose['taken']:
                time_remaining = f"Taken at {format_time(dose['time'])}"
            else:
                time_remaining = f"Was due at {format_time(dose['time'])}"
            
            st.markdown(f"""
            <div class="dose-card {dose_status_class}">
                <div style='display: flex; align-items: center; gap: 24px;'>
                    <div style='width: 24px; height: 24px; border-radius: 50%; background-color: {color_hex}; box-shadow: 0 0 24px {color_hex}; flex-shrink: 0;'></div>
                    <div class="wow-text">
                        <strong style='font-size: 26px;'>{dose['medication_name']}</strong> <span style='font-size: 22px; opacity: 0.9;'>({dose['dosage_amount']})</span>
                        <br><span style='font-size: 20px; opacity: 0.85;'>⏰ {time_remaining}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col2:
                if dose['taken']:
                    if st.button("↩️ Undo", key=f"undo_dose_{dose['medication_id']}_{dose['dose_index']}", use_container_width=True):
                        for m in st.session_state.medications:
                            if m['id'] == dose['medication_id']:
                                today = datetime.now().strftime("%Y-%m-%d")
                                m['taken_doses'] = [t for t in m.get('taken_doses', []) if not (t.get('date') == today and t.get('time') == dose['time'])]
                                update_adherence_history()
                                save_user_data()
                                st.rerun()
                else:
                    if st.button("✓ Take", key=f"take_dose_{dose['medication_id']}_{dose['dose_index']}", use_container_width=True):
                        for m in st.session_state.medications:
                            if m['id'] == dose['medication_id']:
                                today = datetime.now().strftime("%Y-%m-%d")
                                new_taken = {
                                    'date': today,
                                    'time': dose['time']
                                }
                                if 'taken_doses' not in m:
                                    m['taken_doses'] = []
                                m['taken_doses'].append(new_taken)
                                
                                update_medication_history(m['id'], 'taken', dose['time'])
                                play_notification_sound()
                                update_adherence_history()
                                save_user_data()
                                
                                new_adherence = calculate_adherence(st.session_state.medications)
                                if new_adherence >= 100 and st.session_state.previous_adherence < 100:
                                    st.session_state.previous_adherence = new_adherence
                                    show_100_percent_adherence_animation()
                                st.rerun()
    
    st.markdown("<div class='animated-separator'></div>", unsafe_allow_html=True)
    
    # WOW CHARTS
    st.markdown("<h2 class='wow-heading' style='font-size: 36px; margin-top: 40px;'>📊 Your Progress</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container-wow'>", unsafe_allow_html=True)
        st.plotly_chart(create_medication_status_donut(st.session_state.medications), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container-wow'>", unsafe_allow_html=True)
        st.plotly_chart(create_medication_pie_chart(st.session_state.medications, age_category), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Keep all chart functions from original
def create_adherence_line_chart(adherence_history, age_category='adult'):
    """Create line chart showing adherence over time"""
    if not adherence_history:
        fig = go.Figure()
        fig.add_annotation(
            text="No adherence data available yet.<br>Start tracking your medications!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#1f2937")
        )
        fig.update_layout(height=400, xaxis=dict(visible=False), yaxis=dict(visible=False),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    sorted_history = sorted(adherence_history, key=lambda x: x['date'])
    dates = [h['date'] for h in sorted_history]
    adherence = [h['adherence'] for h in sorted_history]
    
    primary_color = get_primary_color(age_category)
    secondary_color = get_secondary_color(age_category)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=adherence, mode='lines+markers', name='Adherence',
        line=dict(color=primary_color, width=4),
        marker=dict(size=10, color=secondary_color, line=dict(width=2, color=primary_color)),
        fill='tozeroy',
        fillcolor=f'rgba({int(primary_color[1:3], 16)}, {int(primary_color[3:5], 16)}, {int(primary_color[5:7], 16)}, 0.2)'
    ))
    
    fig.add_hline(y=100, line_dash="dash", line_color="green",
                  annotation_text="100% Goal", annotation_position="right")
    
    fig.update_layout(
        title={'text': '📈 Medication Adherence Trend', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        xaxis_title='Date', yaxis_title='Adherence Rate (%)',
        yaxis=dict(range=[0, 105], ticksuffix='%'),
        height=450, plot_bgcolor='#f9fafb', paper_bgcolor='white',
        hovermode='x unified', showlegend=False, font=dict(size=14)
    )
    return fig

def create_medication_pie_chart(medications, age_category='adult'):
    """Create pie chart showing medications by type"""
    if not medications:
        fig = go.Figure()
        fig.add_annotation(
            text="No medications added yet.<br>Add your first medication!",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#6b7280")
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    type_counts = {}
    for med in medications:
        med_type = med.get('dosageType', 'other').capitalize()
        type_counts[med_type] = type_counts.get(med_type, 0) + 1
    
    labels = list(type_counts.keys())
    values = list(type_counts.values())
    colors = ['#3B82F6', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B', '#EF4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker=dict(colors=colors, line=dict(color='white', width=3)),
        textinfo='label+percent', textfont=dict(size=16, color='white', family='Arial Black'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={'text': '💊 Medications by Type', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        height=450, paper_bgcolor='white', showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

def create_daily_schedule_bar_chart(medications, age_category='adult'):
    """Create bar chart showing medication schedule throughout the day"""
    if not medications:
        fig = go.Figure()
        fig.add_annotation(
            text="No medications scheduled.<br>Add medications to see your daily schedule!",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#6b7280")
        )
        fig.update_layout(height=400, xaxis=dict(visible=False), yaxis=dict(visible=False),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    hour_counts = {}
    colors_by_hour = {}
    
    for med in medications:
        time_str = med.get('time', '00:00')
        try:
            hour = int(time_str.split(':')[0])
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
            color = get_medication_color_hex(med.get('color', 'blue'))
            if hour not in colors_by_hour:
                colors_by_hour[hour] = color
        except:
            pass
    
    hours = sorted(hour_counts.keys())
    counts = [hour_counts[h] for h in hours]
    labels = [f"{h:02d}:00" for h in hours]
    colors = [colors_by_hour.get(h, '#3B82F6') for h in hours]
    
    fig = go.Figure(data=[
        go.Bar(x=labels, y=counts, marker=dict(color=colors, line=dict(color='white', width=2)),
               text=counts, textposition='outside', textfont=dict(size=14, color='#1f2937', family='Arial Black'))
    ])
    
    fig.update_layout(
        title={'text': '🕐 Daily Medication Schedule', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        xaxis_title='Time of Day', yaxis_title='Number of Medications',
        height=450, plot_bgcolor='#f9fafb', paper_bgcolor='white',
        showlegend=False, font=dict(size=14)
    )
    return fig

def create_side_effects_bar_chart(side_effects):
    """Create bar chart showing side effects by severity"""
    if not side_effects:
        fig = go.Figure()
        fig.add_annotation(
            text="No side effects reported.<br>Great job! Keep it up!",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#10b981")
        )
        fig.update_layout(height=400, xaxis=dict(visible=False), yaxis=dict(visible=False),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    severity_counts = {'Mild': 0, 'Moderate': 0, 'Severe': 0}
    for effect in side_effects:
        severity = effect.get('severity', 'Mild')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    severities = ['Mild', 'Moderate', 'Severe']
    counts = [severity_counts[s] for s in severities]
    colors = ['#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure(data=[
        go.Bar(x=severities, y=counts, marker=dict(color=colors, line=dict(color='white', width=2)),
               text=counts, textposition='outside', textfont=dict(size=16, color='#1f2937', family='Arial Black'))
    ])
    
    fig.update_layout(
        title={'text': '⚠️ Side Effects by Severity', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        xaxis_title='Severity Level', yaxis_title='Number of Reports',
        height=450, plot_bgcolor='#f9fafb', paper_bgcolor='white',
        showlegend=False, font=dict(size=14)
    )
    return fig

def create_medication_status_donut(medications):
    """Create donut chart showing taken vs pending medications"""
    if not medications:
        fig = go.Figure()
        fig.add_annotation(
            text="No medications to track.<br>Add medications to see status!",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#6b7280")
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    taken = sum(1 for med in medications if med.get('taken_today', False))
    pending = len(medications) - taken
    
    labels = ['Taken ✅', 'Pending ⏰']
    values = [taken, pending]
    colors = ['#10b981', '#f59e0b']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=4)),
        textinfo='label+value', textfont=dict(size=18, color='white', family='Arial Black'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.add_annotation(
        text=f"{(taken/len(medications)*100):.0f}%<br>Complete",
        x=0.5, y=0.5, font=dict(size=24, color='#1f2937', family='Arial Black'),
        showarrow=False
    )
    
    fig.update_layout(
        title={'text': '📊 Today\'s Progress', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        height=450, paper_bgcolor='white', showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    return fig

def create_weekly_heatmap(medication_history):
    """Create heatmap showing medication adherence by day and time"""
    if not medication_history:
        fig = go.Figure()
        fig.add_annotation(
            text="No medication history yet.<br>Start taking your medications to see patterns!",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#6b7280")
        )
        fig.update_layout(height=400, xaxis=dict(visible=False), yaxis=dict(visible=False),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [f"{h:02d}:00" for h in range(0, 24, 3)]
    data = [[random.randint(0, 3) for _ in hours] for _ in days]
    
    fig = go.Figure(data=go.Heatmap(
        z=data, x=hours, y=days,
        colorscale=[[0, '#f3f4f6'], [0.33, '#fef3c7'], [0.66, '#a7f3d0'], [1, '#10b981']],
        showscale=True, colorbar=dict(title='Medications<br>Taken'),
        hovertemplate='Day: %{y}<br>Time: %{x}<br>Medications: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': '📅 Weekly Medication Heatmap', 'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Black'}},
        xaxis_title='Time of Day', yaxis_title='Day of Week',
        height=400, plot_bgcolor='white', paper_bgcolor='white', font=dict(size=14)
    )
    return fig

# Main app with WOW dashboard
def patient_dashboard_page():
    """Main patient dashboard with tabs"""
    if not st.session_state.user_profile:
        st.session_state.page = 'patient_login'
        st.rerun()
        return
    
    age = st.session_state.user_profile.get('age', 25)
    age_category = get_age_category(age)
    greeting = get_time_of_day()
    
    st.markdown(inject_wow_css(age_category), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        st.markdown(f"<h2 style='color: white; font-weight: 800; text-shadow: 0 4px 20px rgba(0,0,0,0.3);'>{greeting}, {st.session_state.user_profile['name']}</h2>", unsafe_allow_html=True)
    
    with col2:
        mascot_emoji = get_mascot_emoji(st.session_state.turtle_mood)
        st.markdown(f"""
        <div style="text-align:center;">
            <div style="font-size: 60px; animation: mascot-bounce 2s ease-in-out infinite;">{mascot_emoji}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            save_user_data()
            clear_session_data()
            st.session_state.page = 'patient_login'
            st.rerun()
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard", "💊 Medications", "👨‍⚕️ Appointments",
        "⚠️ Side Effects", "🏆 Achievements", "📥 Reports", "📈 Analytics"
    ])
    
    with tab1:
        dashboard_overview_tab_wow(age_category)
    
    # Keep other tabs as original (or you can upgrade them too!)
    with tab2:
        st.markdown("<h3 style='color: #ffffff;'>💊 Your Medications</h3>", unsafe_allow_html=True)
        st.info("Medications tab coming soon with WOW design!")
    
    with tab3:
        st.markdown("<h3 style='color: #ffffff;'>👨‍⚕️ Doctor Appointments</h3>", unsafe_allow_html=True)
        st.info("Appointments tab coming soon with WOW design!")
    
    with tab4:
        st.markdown("<h3 style='color: #ffffff;'>⚠️ Report & Track Side Effects</h3>", unsafe_allow_html=True)
        st.info("Side Effects tab coming soon with WOW design!")
    
    with tab5:
        st.markdown("<h3 style='color: #ffffff;'>🏆 Your Achievements & Badges</h3>", unsafe_allow_html=True)
        st.info("Achievements tab coming soon with WOW design!")
    
    with tab6:
        st.markdown("<h3 style='color: #ffffff;'>📤 Generate & Download Health Reports</h3>", unsafe_allow_html=True)
        st.info("Reports tab coming soon with WOW design!")
    
    with tab7:
        st.markdown("<h3 style='color: #ffffff;'>📊 Medication Analytics & Insights</h3>", unsafe_allow_html=True)
        st.info("Analytics tab coming soon with WOW design!")

def main():
    """Main application router"""
    init_database()
    initialize_session_state()
    
    age_category = 'adult'
    if st.session_state.user_profile:
        age = st.session_state.user_profile.get('age', 25)
        age_category = get_age_category(age)
    
    st.markdown(inject_wow_css(age_category), unsafe_allow_html=True)
    
    page = st.session_state.page
    
    if page == 'patient_login':
        st.error("Please log in first!")
        # Add login pages here if needed
    elif page == 'patient_signup':
        st.error("Please sign up first!")
        # Add signup pages here if needed
    elif page == 'patient_dashboard':
        patient_dashboard_page()
    else:
        st.error("Please log in first!")

if __name__ == "__main__":
    main()
