import streamlit as st
import streamlit.components.v1 as components
import json
import os
import sqlite3
import hashlib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date, time
import time as time_module
import random
import base64
from io import BytesIO
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="MedTimer - Smart Medication Management",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .medication-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .medication-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .medication-card.taken {
        border-left-color: #10b981;
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .medication-card.missed {
        border-left-color: #ef4444;
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
    }
    
    .medication-card.upcoming {
        border-left-color: #f59e0b;
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-badge.taken {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .status-badge.missed {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .status-badge.upcoming {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Tab styling */
    .tab-button {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        color: #4338ca;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0.25rem;
    }
    
    .tab-button:hover {
        background: linear-gradient(135deg, #c7d2fe 0%, #a5b4fc 100%);
        transform: translateY(-2px);
    }
    
    .tab-button.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Stat card */
    .stat-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Floating animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Celebration overlay */
    .celebration-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(102, 126, 234, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .celebration-content {
        text-align: center;
        color: white;
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .celebration-trophy {
        font-size: 8rem;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-30px); }
        60% { transform: translateY(-15px); }
    }
    
    .celebration-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
        background: linear-gradient(90deg, #fbbf24, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Confetti */
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: confetti-fall 3s ease-out forwards;
    }
    
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Enhanced input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .info-box.warning {
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
        border-left-color: #f59e0b;
    }
    
    .info-box.error {
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
        border-left-color: #ef4444;
    }
    
    .info-box.info {
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%);
        border-left-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE SETUP
# ============================================================================

DB_FILE = "medtimer.db"

def init_db():
    """Initialize the database with all required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            time TEXT NOT NULL,
            reminder_times TEXT,
            taken_doses TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            specialty TEXT,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            location TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Side effects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS side_effects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medication_name TEXT NOT NULL,
            symptom TEXT NOT NULL,
            severity TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Medication history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medication_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medication_id INTEGER NOT NULL,
            taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scheduled_time TEXT NOT NULL,
            dose_index INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (medication_id) REFERENCES medications(id) ON DELETE CASCADE
        )
    ''')
    
    # User settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            reminder_enabled BOOLEAN DEFAULT 1,
            reminder_advance_time INTEGER DEFAULT 30,
            theme TEXT DEFAULT 'light',
            timezone TEXT DEFAULT 'UTC',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash."""
    return hash_password(password) == hashed

def format_time(time_str):
    """Format time to 12-hour format."""
    try:
        if time_str:
            dt = datetime.strptime(time_str, "%H:%M")
            return dt.strftime("%I:%M %p")
        return time_str
    except:
        return time_str

def parse_time(time_str):
    """Parse time string to datetime object."""
    try:
        if ':' in time_str:
            return datetime.strptime(time_str, "%H:%M").time()
        return datetime.strptime(time_str, "%I:%M %p").time()
    except:
        return None

def get_time_until(time_str):
    """Get time until a specific time today."""
    try:
        now = datetime.now()
        target_time = parse_time(time_str)
        target = datetime.combine(now.date(), target_time)
        
        if target < now:
            target += timedelta(days=1)
        
        delta = target - now
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60
        
        if delta.days > 0:
            return f"{delta.days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except:
        return "Unknown"

def get_medication_status(medication, current_time=None):
    """
    Determine medication status: taken, missed, or upcoming.
    medication: dict with keys including 'time', 'reminder_times', 'taken_doses'
    """
    if current_time is None:
        current_time = datetime.now()
    
    # Handle medications with multiple doses
    reminder_times = medication.get('reminder_times', [])
    taken_doses = medication.get('taken_doses', [])
    
    if reminder_times:
        # Multi-dose medication
        doses = []
        for i, dose_time in enumerate(reminder_times):
            dose_status = {
                'time': dose_time,
                'dose_index': i,
                'taken': dose_time in taken_doses
            }
            
            # Determine if missed
            try:
                dose_dt = datetime.strptime(dose_time, "%H:%M")
                dose_datetime = datetime.combine(current_time.date(), dose_dt.time())
                
                if dose_datetime < current_time and not dose_status['taken']:
                    dose_status['status'] = 'missed'
                elif dose_status['taken']:
                    dose_status['status'] = 'taken'
                else:
                    dose_status['status'] = 'upcoming'
            except:
                dose_status['status'] = 'upcoming'
            
            doses.append(dose_status)
        
        return doses
    else:
        # Single-dose medication
        try:
            med_time = parse_time(medication['time'])
            med_datetime = datetime.combine(current_time.date(), med_time)
            
            if med_datetime < current_time:
                return [{'time': medication['time'], 'dose_index': 0, 'taken': False, 'status': 'missed'}]
            else:
                return [{'time': medication['time'], 'dose_index': 0, 'taken': False, 'status': 'upcoming'}]
        except:
            return [{'time': medication['time'], 'dose_index': 0, 'taken': False, 'status': 'upcoming'}]

def expand_medication_doses(medications):
    """
    Expand medications with multiple doses into individual dose entries.
    Returns a list where each dose is a separate entry.
    """
    expanded = []
    current_time = datetime.now()
    
    for med in medications:
        reminder_times = med.get('reminder_times', [])
        taken_doses = med.get('taken_doses', [])
        
        if reminder_times:
            # Multi-dose medication - expand into individual doses
            for i, dose_time in enumerate(reminder_times):
                dose_entry = {
                    'id': f"{med['id']}_dose_{i}",
                    'original_id': med['id'],
                    'name': med['name'],
                    'dosage': med['dosage'],
                    'frequency': med['frequency'],
                    'time': dose_time,
                    'dose_index': i,
                    'dose_label': get_dose_label(i, len(reminder_times)),
                    'taken': dose_time in taken_doses,
                    'taken_doses': taken_doses,
                    'notes': med.get('notes', ''),
                    'created_at': med.get('created_at', '')
                }
                
                # Determine status
                status_info = get_medication_status(dose_entry, current_time)
                if status_info:
                    dose_entry['status'] = status_info[0]['status']
                else:
                    dose_entry['status'] = 'upcoming'
                
                expanded.append(dose_entry)
        else:
            # Single-dose medication
            dose_entry = {
                'id': med['id'],
                'original_id': med['id'],
                'name': med['name'],
                'dosage': med['dosage'],
                'frequency': med['frequency'],
                'time': med['time'],
                'dose_index': 0,
                'dose_label': '',
                'taken': False,
                'taken_doses': [],
                'notes': med.get('notes', ''),
                'created_at': med.get('created_at', '')
            }
            
            # Determine status
            status_info = get_medication_status(dose_entry, current_time)
            if status_info:
                dose_entry['status'] = status_info[0]['status']
            else:
                dose_entry['status'] = 'upcoming'
            
            expanded.append(dose_entry)
    
    return expanded

def get_dose_label(index, total):
    """Get label for dose based on index and total."""
    labels = {
        1: [''],
        2: ['Morning', 'Evening'],
        3: ['Morning', 'Afternoon', 'Evening'],
        4: ['Morning', 'Afternoon', 'Evening', 'Night']
    }
    
    if total in labels:
        return labels[total][index]
    else:
        return f'Dose {index + 1}'

def calculate_adherence_expanded(medications):
    """
    Calculate adherence percentage based on expanded doses.
    This correctly handles medications with multiple doses per day.
    """
    if not medications:
        return 0.0
    
    expanded = expand_medication_doses(medications)
    
    if not expanded:
        return 0.0
    
    # Count total doses and taken doses
    total_doses = len(expanded)
    taken_doses = sum(1 for dose in expanded if dose['taken'])
    
    if total_doses == 0:
        return 0.0
    
    return (taken_doses / total_doses) * 100

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def register_user(username, email, password):
    """Register a new user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        
        if user and verify_password(password, user[2]):
            return {'id': user[0], 'username': user[1]}
        return None
    finally:
        conn.close()

def get_user_medications(user_id):
    """Get all medications for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, name, dosage, frequency, time, reminder_times, taken_doses, notes, created_at FROM medications WHERE user_id = ?",
            (user_id,)
        )
        medications = []
        for row in cursor.fetchall():
            medications.append({
                'id': row[0],
                'name': row[1],
                'dosage': row[2],
                'frequency': row[3],
                'time': row[4],
                'reminder_times': json.loads(row[5]) if row[5] else [],
                'taken_doses': json.loads(row[6]) if row[6] else [],
                'notes': row[7],
                'created_at': row[8]
            })
        return medications
    finally:
        conn.close()

def add_medication(user_id, name, dosage, frequency, time, reminder_times=None, notes=None):
    """Add a new medication for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        reminder_times_json = json.dumps(reminder_times) if reminder_times else None
        cursor.execute(
            """INSERT INTO medications (user_id, name, dosage, frequency, time, reminder_times, taken_doses, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, name, dosage, frequency, time, reminder_times_json, json.dumps([]), notes)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def update_medication(med_id, name, dosage, frequency, time, reminder_times=None, notes=None):
    """Update an existing medication."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        reminder_times_json = json.dumps(reminder_times) if reminder_times else None
        cursor.execute(
            """UPDATE medications SET name=?, dosage=?, frequency=?, time=?, reminder_times=?, notes=?
               WHERE id=?""",
            (name, dosage, frequency, time, reminder_times_json, notes, med_id)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def delete_medication(med_id):
    """Delete a medication."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM medications WHERE id=?", (med_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def mark_dose_taken(med_id, dose_index=0):
    """Mark a specific dose as taken."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Get current medication data
        cursor.execute(
            "SELECT reminder_times, taken_doses FROM medications WHERE id=?",
            (med_id,)
        )
        row = cursor.fetchone()
        
        if row:
            reminder_times = json.loads(row[0]) if row[0] else []
            taken_doses = json.loads(row[1]) if row[1] else []
            
            # Determine which time to mark as taken
            if reminder_times and dose_index < len(reminder_times):
                time_to_mark = reminder_times[dose_index]
            else:
                # Use the main time
                cursor.execute("SELECT time FROM medications WHERE id=?", (med_id,))
                time_row = cursor.fetchone()
                time_to_mark = time_row[0] if time_row else None
            
            if time_to_mark and time_to_mark not in taken_doses:
                taken_doses.append(time_to_mark)
                cursor.execute(
                    "UPDATE medications SET taken_doses=? WHERE id=?",
                    (json.dumps(taken_doses), med_id)
                )
                
                # Add to history
                cursor.execute(
                    """INSERT INTO medication_history (user_id, medication_id, scheduled_time, dose_index)
                       SELECT user_id, id, ?, ? FROM medications WHERE id=?""",
                    (time_to_mark, dose_index, med_id)
                )
                
                conn.commit()
                return True
        return False
    except Exception as e:
        print(f"Error marking dose taken: {e}")
        return False
    finally:
        conn.close()

def unmark_dose_taken(med_id, dose_index=0):
    """Unmark a specific dose as taken."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Get current medication data
        cursor.execute(
            "SELECT reminder_times, taken_doses FROM medications WHERE id=?",
            (med_id,)
        )
        row = cursor.fetchone()
        
        if row:
            reminder_times = json.loads(row[0]) if row[0] else []
            taken_doses = json.loads(row[1]) if row[1] else []
            
            # Determine which time to unmark
            if reminder_times and dose_index < len(reminder_times):
                time_to_unmark = reminder_times[dose_index]
            else:
                cursor.execute("SELECT time FROM medications WHERE id=?", (med_id,))
                time_row = cursor.fetchone()
                time_to_unmark = time_row[0] if time_row else None
            
            if time_to_unmark and time_to_unmark in taken_doses:
                taken_doses.remove(time_to_unmark)
                cursor.execute(
                    "UPDATE medications SET taken_doses=? WHERE id=?",
                    (json.dumps(taken_doses), med_id)
                )
                conn.commit()
                return True
        return False
    except Exception as e:
        print(f"Error unmarking dose taken: {e}")
        return False
    finally:
        conn.close()

def get_user_appointments(user_id):
    """Get all appointments for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, doctor_name, specialty, appointment_date, appointment_time, location, notes, created_at FROM appointments WHERE user_id = ? ORDER BY appointment_date, appointment_time",
            (user_id,)
        )
        appointments = []
        for row in cursor.fetchall():
            appointments.append({
                'id': row[0],
                'doctor_name': row[1],
                'specialty': row[2],
                'appointment_date': row[3],
                'appointment_time': row[4],
                'location': row[5],
                'notes': row[6],
                'created_at': row[7]
            })
        return appointments
    finally:
        conn.close()

def add_appointment(user_id, doctor_name, specialty, appointment_date, appointment_time, location=None, notes=None):
    """Add a new appointment."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO appointments (user_id, doctor_name, specialty, appointment_date, appointment_time, location, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, doctor_name, specialty, appointment_date, appointment_time, location, notes)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def update_appointment(app_id, doctor_name, specialty, appointment_date, appointment_time, location=None, notes=None):
    """Update an appointment."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """UPDATE appointments SET doctor_name=?, specialty=?, appointment_date=?, appointment_time=?, location=?, notes=?
               WHERE id=?""",
            (doctor_name, specialty, appointment_date, appointment_time, location, notes, app_id)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def delete_appointment(app_id):
    """Delete an appointment."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM appointments WHERE id=?", (app_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user_side_effects(user_id):
    """Get all side effects for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, medication_name, symptom, severity, date, time, notes, created_at FROM side_effects WHERE user_id = ? ORDER BY date DESC, time DESC",
            (user_id,)
        )
        side_effects = []
        for row in cursor.fetchall():
            side_effects.append({
                'id': row[0],
                'medication_name': row[1],
                'symptom': row[2],
                'severity': row[3],
                'date': row[4],
                'time': row[5],
                'notes': row[6],
                'created_at': row[7]
            })
        return side_effects
    finally:
        conn.close()

def add_side_effect(user_id, medication_name, symptom, severity, date, time, notes=None):
    """Add a new side effect."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO side_effects (user_id, medication_name, symptom, severity, date, time, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, medication_name, symptom, severity, date, time, notes)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def delete_side_effect(se_id):
    """Delete a side effect."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM side_effects WHERE id=?", (se_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_medication_history(user_id, days=30):
    """Get medication history for the specified number of days."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """SELECT mh.id, m.name, m.dosage, mh.taken_at, mh.scheduled_time, mh.dose_index
               FROM medication_history mh
               JOIN medications m ON mh.medication_id = m.id
               WHERE mh.user_id = ? AND mh.taken_at >= datetime('now', ?)
               ORDER BY mh.taken_at DESC""",
            (user_id, f'-{days} days')
        )
        history = []
        for row in cursor.fetchall():
            history.append({
                'id': row[0],
                'name': row[1],
                'dosage': row[2],
                'taken_at': row[3],
                'scheduled_time': row[4],
                'dose_index': row[5]
            })
        return history
    finally:
        conn.close()

# ============================================================================
# CELEBRATION FUNCTIONS
# ============================================================================

def display_celebration():
    """Display a spectacular celebration animation."""
    st.markdown("""
    <div class="celebration-overlay">
        <div class="celebration-content">
            <div class="celebration-trophy">🏆</div>
            <div class="celebration-title">Congratulations!</div>
            <p style="font-size: 1.5rem; margin: 1rem 0;">You've completed all your medications for today!</p>
            <p style="font-size: 1.2rem; opacity: 0.9;">Keep up the excellent work! 💪</p>
        </div>
    </div>
    <script>
        // Create confetti
        function createConfetti() {
            const colors = ['#fbbf24', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#8b5cf6'];
            for (let i = 0; i < 50; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
                document.querySelector('.celebration-overlay').appendChild(confetti);
            }
        }
        
        createConfetti();
        
        // Auto dismiss after 5 seconds
        setTimeout(function() {
            document.querySelector('.celebration-overlay').style.display = 'none';
        }, 5000);
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# REMINDER FUNCTIONS
# ============================================================================

def check_reminders(medications):
    """
    Check for medication reminders.
    Returns list of medications that need reminders.
    """
    reminders = []
    current_time = datetime.now()
    
    for med in medications:
        reminder_times = med.get('reminder_times', [])
        taken_doses = med.get('taken_doses', [])
        
        # Check each dose time
        times_to_check = reminder_times if reminder_times else [med['time']]
        
        for dose_time in times_to_check:
            if dose_time in taken_doses:
                continue
            
            try:
                reminder_dt = datetime.strptime(dose_time, "%H:%M")
                reminder_datetime = datetime.combine(current_time.date(), reminder_dt.time())
                
                # Calculate time until dose
                time_until = (reminder_datetime - current_time).total_seconds() / 60  # in minutes
                
                # 30-minute advance warning
                if 28 <= time_until <= 32:
                    reminders.append({
                        'medication': med,
                        'time': dose_time,
                        'type': 'advance',
                        'message': f"Time to take {med['name']} in 30 minutes!"
                    })
                # 5-minute due alert
                elif -5 <= time_until <= 5:
                    reminders.append({
                        'medication': med,
                        'time': dose_time,
                        'type': 'due',
                        'message': f"It's time to take {med['name']} now!"
                    })
            except:
                continue
    
    return reminders

def display_reminders(reminders):
    """Display medication reminders."""
    if not reminders:
        return
    
    st.markdown("### 🔔 Reminders")
    
    for reminder in reminders:
        if reminder['type'] == 'advance':
            st.markdown(f"""
            <div class="info-box warning">
                <strong>⏰ Upcoming Reminder</strong><br>
                {reminder['message']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-box error">
                <strong>🚨 Due Now!</strong><br>
                {reminder['message']}
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# UI COMPONENTS
# ============================================================================

def create_unique_tab_buttons(location_prefix, active_tab):
    """
    Create unique tab buttons with location prefix to avoid duplicate key errors.
    location_prefix: 'dashboard' or 'medications'
    """
    tabs = ['All', 'Missed', 'Upcoming', 'Taken']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(tabs[0], key=f"{location_prefix}_tab_all", 
                    disabled=active_tab == tabs[0]):
            return tabs[0]
    
    with col2:
        if st.button(tabs[1], key=f"{location_prefix}_tab_missed", 
                    disabled=active_tab == tabs[1]):
            return tabs[1]
    
    with col3:
        if st.button(tabs[2], key=f"{location_prefix}_tab_upcoming", 
                    disabled=active_tab == tabs[2]):
            return tabs[2]
    
    with col4:
        if st.button(tabs[3], key=f"{location_prefix}_tab_taken", 
                    disabled=active_tab == tabs[3]):
            return tabs[3]
    
    return active_tab

def display_medication_card(medication, show_actions=True):
    """Display a single medication card with status."""
    status = medication.get('status', 'upcoming')
    dose_label = medication.get('dose_label', '')
    
    status_emoji = {
        'taken': '✅',
        'missed': '❌',
        'upcoming': '⏰'
    }
    
    st.markdown(f"""
    <div class="medication-card {status}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700;">
                    {status_emoji.get(status, '💊')} {medication['name']}
                    {f" - {dose_label}" if dose_label else ""}
                </h3>
                <p style="margin: 0.5rem 0; color: #6b7280;">
                    <strong>Dosage:</strong> {medication['dosage']}<br>
                    <strong>Time:</strong> {format_time(medication['time'])}<br>
                    {f"<strong>Frequency:</strong> {medication['frequency']}<br>" if medication.get('frequency') else ""}
                    {f"<strong>Notes:</strong> {medication['notes']}" if medication.get('notes') else ""}
                </p>
            </div>
            <div style="text-align: right;">
                <span class="status-badge {status}">{status.upper()}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if show_actions:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Take", key=f"take_{medication['id']}", use_container_width=True):
                original_id = medication.get('original_id', medication['id'])
                dose_index = medication.get('dose_index', 0)
                if mark_dose_taken(original_id, dose_index):
                    st.success("Medication marked as taken!")
                    st.rerun()
        
        with col2:
            if status == 'taken' and st.button("↩ Undo", key=f"undo_{medication['id']}", use_container_width=True):
                original_id = medication.get('original_id', medication['id'])
                dose_index = medication.get('dose_index', 0)
                if unmark_dose_taken(original_id, dose_index):
                    st.success("Medication unmarked!")
                    st.rerun()

def display_medication_checklist_with_tabs(location_prefix, medications, show_celebration=False):
    """
    Display medication checklist with tabs (All, Missed, Upcoming, Taken).
    location_prefix: 'dashboard' or 'medications' to create unique button keys
    """
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'All'
    
    # Create unique tab buttons
    active_tab = create_unique_tab_buttons(location_prefix, st.session_state.active_tab)
    st.session_state.active_tab = active_tab
    
    # Expand medications to handle multi-dose
    expanded_medications = expand_medication_doses(medications)
    
    # Filter medications based on active tab
    if active_tab == 'All':
        filtered_meds = expanded_medications
    elif active_tab == 'Missed':
        filtered_meds = [med for med in expanded_medications if med.get('status') == 'missed']
    elif active_tab == 'Upcoming':
        filtered_meds = [med for med in expanded_medications if med.get('status') == 'upcoming']
    elif active_tab == 'Taken':
        filtered_meds = [med for med in expanded_medications if med.get('status') == 'taken']
    else:
        filtered_meds = expanded_medications
    
    # Display medications
    if filtered_meds:
        # Sort by time
        filtered_meds.sort(key=lambda x: x['time'])
        
        for med in filtered_meds:
            display_medication_card(med, show_actions=True)
    else:
        st.info(f"No medications in the '{active_tab}' category.")
    
    # Check if all medications for today are taken
    if show_celebration and location_prefix == 'dashboard':
        upcoming_and_missed = [med for med in expanded_medications 
                              if med.get('status') in ['upcoming', 'missed']]
        
        if not upcoming_and_missed and expanded_medications:
            display_celebration()

def display_dashboard(user_id):
    """Display the main dashboard."""
    st.markdown("""
    <div class="main-header">
        <h1>💊 Welcome to MedTimer</h1>
        <p>Your smart medication management companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    medications = get_user_medications(user_id)
    appointments = get_user_appointments(user_id)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        adherence = calculate_adherence_expanded(medications)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{adherence:.1f}%</div>
            <div class="stat-label">Adherence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        expanded = expand_medication_doses(medications)
        taken_count = sum(1 for med in expanded if med.get('taken'))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{taken_count}/{len(expanded)}</div>
            <div class="stat-label">Taken Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        upcoming_count = len([app for app in appointments 
                            if datetime.strptime(app['appointment_date'], "%Y-%m-%d") >= datetime.now().date()])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{upcoming_count}</div>
            <div class="stat-label">Upcoming Appointments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        side_effects = get_user_side_effects(user_id)
        recent_se = len([se for se in side_effects if se['date'] == str(date.today())])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{recent_se}</div>
            <div class="stat-label">Side Effects Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reminders
    reminders = check_reminders(medications)
    display_reminders(reminders)
    
    st.markdown("---")
    
    # Medication Checklist
    st.markdown("### 💊 Today's Medications")
    display_medication_checklist_with_tabs('dashboard', medications, show_celebration=True)
    
    st.markdown("---")
    
    # Upcoming Appointments
    st.markdown("### 📅 Upcoming Appointments")
    upcoming_apps = [app for app in appointments 
                    if datetime.strptime(app['appointment_date'], "%Y-%m-%d") >= datetime.now().date()]
    upcoming_apps.sort(key=lambda x: (x['appointment_date'], x['appointment_time']))
    
    if upcoming_apps:
        for app in upcoming_apps[:5]:
            st.markdown(f"""
            <div class="medication-card">
                <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700;">
                    👨‍⚕️ {app['doctor_name']} - {app.get('specialty', '')}
                </h3>
                <p style="margin: 0.5rem 0; color: #6b7280;">
                    <strong>Date:</strong> {app['appointment_date']}<br>
                    <strong>Time:</strong> {format_time(app['appointment_time'])}<br>
                    {f"<strong>Location:</strong> {app['location']}" if app.get('location') else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No upcoming appointments.")

def display_medications_page(user_id):
    """Display the medications management page."""
    st.markdown("### 💊 Medication Management")
    
    medications = get_user_medications(user_id)
    
    # Add new medication
    with st.expander("➕ Add New Medication", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Medication Name", key="new_med_name")
            dosage = st.text_input("Dosage (e.g., 500mg)", key="new_med_dosage")
        
        with col2:
            frequency = st.selectbox(
                "Frequency",
                ["Once Daily", "Twice Daily", "Thrice Daily", "Four Times Daily", "As Needed"],
                key="new_med_frequency"
            )
            time_input = st.time_input("Primary Time", key="new_med_time")
        
        # Generate reminder times based on frequency
        if frequency == "Once Daily":
            reminder_times = [time_input.strftime("%H:%M")]
        elif frequency == "Twice Daily":
            reminder_times = [
                time_input.strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=12)).strftime("%H:%M")
            ]
        elif frequency == "Thrice Daily":
            reminder_times = [
                time_input.strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=6)).strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=12)).strftime("%H:%M")
            ]
        elif frequency == "Four Times Daily":
            reminder_times = [
                time_input.strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=4)).strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=8)).strftime("%H:%M"),
                (datetime.combine(date.today(), time_input) + timedelta(hours=12)).strftime("%H:%M")
            ]
        else:
            reminder_times = None
        
        notes = st.text_area("Notes (optional)", key="new_med_notes")
        
        if st.button("Add Medication", key="add_med_btn"):
            if name and dosage:
                add_medication(
                    user_id, name, dosage, frequency,
                    time_input.strftime("%H:%M"), reminder_times, notes
                )
                st.success("Medication added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("---")
    
    # Display medications with tabs
    display_medication_checklist_with_tabs('medications', medications, show_celebration=False)

def display_appointments_page(user_id):
    """Display the appointments management page."""
    st.markdown("### 📅 Appointment Management")
    
    appointments = get_user_appointments(user_id)
    
    # Add new appointment
    with st.expander("➕ Add New Appointment", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            doctor_name = st.text_input("Doctor Name", key="new_app_doctor")
            specialty = st.text_input("Specialty (optional)", key="new_app_specialty")
        
        with col2:
            appointment_date = st.date_input("Date", key="new_app_date")
            appointment_time = st.time_input("Time", key="new_app_time")
        
        location = st.text_input("Location (optional)", key="new_app_location")
        notes = st.text_area("Notes (optional)", key="new_app_notes")
        
        if st.button("Add Appointment", key="add_app_btn"):
            if doctor_name and appointment_date and appointment_time:
                add_appointment(
                    user_id, doctor_name, specialty,
                    str(appointment_date), appointment_time.strftime("%H:%M"),
                    location, notes
                )
                st.success("Appointment added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("---")
    
    # Display appointments
    if appointments:
        for app in appointments:
            with st.expander(f"👨‍⚕️ {app['doctor_name']} - {app['appointment_date']} at {format_time(app['appointment_time'])}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f9fafb; border-radius: 10px;">
                        <p style="margin: 0.5rem 0;"><strong>Doctor:</strong> {app['doctor_name']}</p>
                        <p style="margin: 0.5rem 0;"><strong>Specialty:</strong> {app.get('specialty', 'N/A')}</p>
                        <p style="margin: 0.5rem 0;"><strong>Date:</strong> {app['appointment_date']}</p>
                        <p style="margin: 0.5rem 0;"><strong>Time:</strong> {format_time(app['appointment_time'])}</p>
                        {f"<p style='margin: 0.5rem 0;'><strong>Location:</strong> {app['location']}</p>" if app.get('location') else ""}
                        {f"<p style='margin: 0.5rem 0;'><strong>Notes:</strong> {app['notes']}</p>" if app.get('notes') else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑 Delete", key=f"delete_app_{app['id']}"):
                        delete_appointment(app['id'])
                        st.success("Appointment deleted!")
                        st.rerun()
    else:
        st.info("No appointments scheduled.")

def display_side_effects_page(user_id):
    """Display the side effects tracking page."""
    st.markdown("### ⚠️ Side Effects Tracker")
    
    side_effects = get_user_side_effects(user_id)
    medications = get_user_medications(user_id)
    medication_names = [med['name'] for med in medications]
    
    # Add new side effect
    with st.expander("➕ Report Side Effect", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            medication_name = st.selectbox("Medication", medication_names, key="new_se_med")
            symptom = st.text_input("Symptom", key="new_se_symptom")
        
        with col2:
            severity = st.selectbox(
                "Severity",
                ["Mild", "Moderate", "Severe"],
                key="new_se_severity"
            )
            se_date = st.date_input("Date", key="new_se_date")
            se_time = st.time_input("Time", key="new_se_time")
        
        notes = st.text_area("Notes (optional)", key="new_se_notes")
        
        if st.button("Report Side Effect", key="add_se_btn"):
            if medication_name and symptom and severity:
                add_side_effect(
                    user_id, medication_name, symptom, severity,
                    str(se_date), se_time.strftime("%H:%M"), notes
                )
                st.success("Side effect reported!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("---")
    
    # Display side effects
    if side_effects:
        for se in side_effects:
            with st.expander(f"⚠️ {se['symptom']} - {se['date']} at {format_time(se['time'])}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    severity_colors = {
                        'Mild': '#10b981',
                        'Moderate': '#f59e0b',
                        'Severe': '#ef4444'
                    }
                    severity_color = severity_colors.get(se['severity'], '#6b7280')
                    
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f9fafb; border-radius: 10px;">
                        <p style="margin: 0.5rem 0;"><strong>Medication:</strong> {se['medication_name']}</p>
                        <p style="margin: 0.5rem 0;"><strong>Symptom:</strong> {se['symptom']}</p>
                        <p style="margin: 0.5rem 0;">
                            <strong>Severity:</strong> 
                            <span style="background: {severity_color}; color: white; padding: 0.2rem 0.8rem; border-radius: 10px; font-weight: 600;">
                                {se['severity']}
                            </span>
                        </p>
                        <p style="margin: 0.5rem 0;"><strong>Date:</strong> {se['date']}</p>
                        <p style="margin: 0.5rem 0;"><strong>Time:</strong> {format_time(se['time'])}</p>
                        {f"<p style='margin: 0.5rem 0;'><strong>Notes:</strong> {se['notes']}</p>" if se.get('notes') else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑 Delete", key=f"delete_se_{se['id']}"):
                        delete_side_effect(se['id'])
                        st.success("Side effect deleted!")
                        st.rerun()
    else:
        st.info("No side effects reported.")

def display_reports_page(user_id):
    """Display the reports and analytics page."""
    st.markdown("### 📊 Reports & Analytics")
    
    medications = get_user_medications(user_id)
    history = get_medication_history(user_id, days=30)
    
    # Adherence Chart
    st.markdown("#### 📈 Adherence Over Time")
    
    if history:
        # Create daily adherence data
        daily_data = {}
        for entry in history:
            date_str = datetime.strptime(entry['taken_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            if date_str not in daily_data:
                daily_data[date_str] = {'taken': 0, 'total': 0}
            daily_data[date_str]['taken'] += 1
        
        # Calculate total doses per day
        for med in medications:
            reminder_times = med.get('reminder_times', [])
            total_doses = len(reminder_times) if reminder_times else 1
            for date_str in daily_data:
                daily_data[date_str]['total'] += total_doses
        
        # Prepare data for chart
        dates = sorted(daily_data.keys())
        adherence_rates = [
            (daily_data[date]['taken'] / daily_data[date]['total'] * 100) if daily_data[date]['total'] > 0 else 0
            for date in dates
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=adherence_rates,
            mode='lines+markers',
            name='Adherence %',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Medication Adherence Over Last 30 Days",
            xaxis_title="Date",
            yaxis_title="Adherence (%)",
            yaxis=dict(range=[0, 100]),
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for adherence chart.")
    
    # Side Effects Summary
    st.markdown("#### ⚠️ Side Effects Summary")
    
    side_effects = get_user_side_effects(user_id)
    
    if side_effects:
        # Count by severity
        severity_counts = {'Mild': 0, 'Moderate': 0, 'Severe': 0}
        for se in side_effects:
            severity_counts[se['severity']] += 1
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(severity_counts.keys()),
                y=list(severity_counts.values()),
                marker_color=['#10b981', '#f59e0b', '#ef4444']
            )
        ])
        
        fig.update_layout(
            title="Side Effects by Severity",
            xaxis_title="Severity",
            yaxis_title="Count",
            height=300,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Side effects by medication
        st.markdown("##### Side Effects by Medication")
        
        med_counts = {}
        for se in side_effects:
            if se['medication_name'] not in med_counts:
                med_counts[se['medication_name']] = 0
            med_counts[se['medication_name']] += 1
        
        fig = px.pie(
            values=list(med_counts.values()),
            names=list(med_counts.keys()),
            title="Side Effects Distribution by Medication"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No side effects data available.")
    
    # Medication History Table
    st.markdown("#### 📋 Recent Medication History")
    
    if history:
        df = pd.DataFrame(history)
        df['taken_at'] = pd.to_datetime(df['taken_at']).dt.strftime("%Y-%m-%d %I:%M %p")
        df['scheduled_time'] = df['scheduled_time'].apply(format_time)
        
        st.dataframe(
            df[['name', 'dosage', 'scheduled_time', 'taken_at']].head(20),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No medication history available.")

def display_settings_page(user_id):
    """Display the settings page."""
    st.markdown("### ⚙️ Settings")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get current settings
    cursor.execute("SELECT reminder_enabled, reminder_advance_time, theme, timezone FROM user_settings WHERE user_id=?", (user_id,))
    settings = cursor.fetchone()
    
    if not settings:
        cursor.execute(
            "INSERT INTO user_settings (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()
        settings = (1, 30, 'light', 'UTC')
    
    conn.close()
    
    reminder_enabled, reminder_advance_time, theme, timezone = settings
    
    # Reminder settings
    st.markdown("#### 🔔 Reminder Settings")
    
    new_reminder_enabled = st.checkbox(
        "Enable Medication Reminders",
        value=bool(reminder_enabled),
        key="reminder_enabled"
    )
    
    new_advance_time = st.slider(
        "Advance Warning Time (minutes)",
        min_value=5,
        max_value=60,
        value=reminder_advance_time,
        key="advance_time"
    )
    
    if st.button("Save Reminder Settings", key="save_reminder_settings"):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_settings SET reminder_enabled=?, reminder_advance_time=? WHERE user_id=?",
            (int(new_reminder_enabled), new_advance_time, user_id)
        )
        conn.commit()
        conn.close()
        st.success("Reminder settings saved!")
    
    st.markdown("---")
    
    # Theme settings
    st.markdown("#### 🎨 Theme Settings")
    
    new_theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if theme == 'light' else 1,
        key="theme_select"
    )
    
    if st.button("Save Theme Settings", key="save_theme_settings"):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_settings SET theme=? WHERE user_id=?",
            (new_theme.lower(), user_id)
        )
        conn.commit()
        conn.close()
        st.success("Theme settings saved!")

# ============================================================================
# AUTHENTICATION
# ============================================================================

def display_login_page():
    """Display the login page."""
    st.markdown("""
    <div class="main-header">
        <h1>💊 MedTimer</h1>
        <p>Smart Medication Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            user = authenticate_user(username, password)
            if user:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.success(f"Welcome back, {user['username']}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    
    with tab2:
        st.markdown("### Register")
        
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        
        if st.button("Register", key="reg_btn", use_container_width=True):
            if not all([new_username, new_email, new_password]):
                st.error("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                user_id = register_user(new_username, new_email, new_password)
                if user_id:
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username or email already exists.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function."""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Display login page if not logged in
    if not st.session_state.logged_in:
        display_login_page()
        return
    
    # Main navigation
    user_id = st.session_state.user['id']
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="margin: 0;">👤 {st.session_state.user['username']}</h2>
            <p style="margin: 0.5rem 0; color: #6b7280;">MedTimer User</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "💊 Medications", "📅 Appointments", "⚠️ Side Effects", "📊 Reports", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Display selected page
    if page == "🏠 Dashboard":
        display_dashboard(user_id)
    elif page == "💊 Medications":
        display_medications_page(user_id)
    elif page == "📅 Appointments":
        display_appointments_page(user_id)
    elif page == "⚠️ Side Effects":
        display_side_effects_page(user_id)
    elif page == "📊 Reports":
        display_reports_page(user_id)
    elif page == "⚙️ Settings":
        display_settings_page(user_id)

# Run the application
if __name__ == "__main__":
    main()
