import streamlit as st
import pandas as pd
import json
import os
import sqlite3
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Homeopathy Clinical Intake & Consultation System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        color: #1B4D3E;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #4A7C59;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #1B4D3E;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
    }
    .remedy-card {
        background-color: #F4F9F5;
        border-left: 5px solid #2E7D32;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Data Persistence Setup
DATA_DIR = os.path.join(os.path.dirname(__file__), "consultations")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(os.path.dirname(__file__), "homeopathy.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS consultations (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    patient_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    phone TEXT,
                    chief_complaint TEXT,
                    thermal TEXT,
                    thirst TEXT,
                    mindset TEXT,
                    modalities TEXT,
                    full_json TEXT,
                    prescription TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# App Header
st.markdown('<div class="main-title">🌿 Homeopathy Clinical Intake & Consultation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Comprehensive Classical Homeopathic Case Taking, Symptom Synthesis & Remedy Intelligence</div>', unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📋 Patient Intake Questionnaire", "🩺 Doctor Review & Prescriber", "📊 Records Directory & Analytics"])

# ==================== TAB 1: PATIENT INTAKE FORM ====================
with tab1:
    st.info("💡 Patients or Clinical Assistants: Complete all sections below. This detailed constitutional history enables exact homeopathic remedy selection.")
    
    with st.form("patient_intake_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_name = st.text_input("Full Name *", placeholder="e.g. John Doe")
            age = st.number_input("Age *", min_value=1, max_value=120, value=30)
        with col2:
            gender = st.selectbox("Gender *", ["Select", "Male", "Female", "Other"])
            phone = st.text_input("Contact Phone / Email", placeholder="+1 555-0199 / email@domain.com")
        with col3:
            occupation = st.text_input("Occupation", placeholder="e.g. Software Engineer, Executive")
            visit_date = st.date_input("Consultation Date", datetime.now())

        st.subheader("1. Chief Complaints & Symptom Characteristics")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            chief_complaint = st.text_area("Chief Complaint (Primary Problem & Duration) *", placeholder="Describe primary symptoms, location, and how long you have had them...")
            sensation_type = st.multiselect("Sensation / Pain Type", ["Throbbing", "Burning", "Stitching / Sharp", "Dull / Aching", "Cramping", "Numbness", "Itching", "Heaviness"])
        with col_c2:
            onset_trigger = st.text_input("Onset Trigger / Cause", placeholder="e.g. After grief, cold exposure, overwork, wet weather")
            affected_side = st.selectbox("Affected Body Side", ["Not Specific", "Right Side", "Left Side", "Alternating Sides", "Diagonal"])

        st.subheader("2. Physical Generals & Thermal Constitution")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            thermal = st.selectbox("Thermal Preference *", ["Select", "Chilly (Sensitive to cold / Craves warmth)", "Hot-blooded (Sensitive to heat / Craves cool air)", "Ambi-thermal (Neutral)"])
            sweat_pattern = st.multiselect("Sweat Characteristics", ["Profuse", "Scanty", "Offensive odor", "Staining", "Head / Neck only", "Palms / Soles"])
        with col_g2:
            thirst = st.selectbox("Thirst Pattern *", ["Large quantities at long intervals", "Small sips frequently", "Thirstless", "Craves ice-cold water", "Craves warm drinks"])
            appetite_cravings = st.multiselect("Food Cravings", ["Salty", "Sweet", "Sour / Acidic", "Spicy / Highly Seasoned", "Fatty / Rich foods", "Warm food", "Cold food / Ice cream"])
        with col_g3:
            food_aversions = st.multiselect("Food Aversions / Aggravations", ["Milk / Dairy", "Fatty foods", "Meat", "Sweets", "Bread", "Eggs", "Coffee"])
            sleep_posture = st.selectbox("Sleep Position Preference", ["On Back", "On Stomach", "On Right Side", "On Left Side", "Position Changes Constantly"])

        st.subheader("3. Mind & Emotional Temperament")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            temperament = st.multiselect("Emotional & Mental Traits", [
                "Anxious / Restless", "Irritable / Quick-tempered", "Mild / Gentle / Weepy",
                "Fastidious / Perfectionist", "Reserved / Consolation aggravates", "Fear of illness / Death",
                "Depressed / Sad", "Hurried / Impatient", "Sensitive to noise / light"
            ])
        with col_m2:
            mind_notes = st.text_area("Detailed Emotional Description", placeholder="Describe how stress, anger, grief, or fear affects your daily well-being...")

        st.subheader("4. Modalities (Aggravation & Amelioration)")
        col_mod1, col_mod2 = st.columns(2)
        with col_mod1:
            worse_by = st.multiselect("Worse By (Aggravation)", [
                "Cold / Drafts", "Heat / Warm room", "Motion / Walking", "Rest / Inactivity",
                "Morning", "Evening / Night", "Eating / After meals", "Damp / Rain", "Touch / Pressure", "Consolation / Sympathy"
            ])
        with col_mod2:
            better_by = st.multiselect("Better By (Amelioration)", [
                "Warmth / Hot bath", "Cold applications", "Continued motion", "Absolute rest",
                "Fresh air", "Hard pressure / Massage", "Sleep", "Eating", "Bending double"
            ])

        st.subheader("5. Systemic Symptoms & Medical History")
        past_history = st.text_area("Past Medical History & Family History", placeholder="List past illnesses, surgeries, family conditions (Diabetes, Asthma, Cancer, Hypertension)...")

        submitted = st.form_submit_button("💾 Save Patient Consultation Record")

        if submitted:
            if not patient_name or not chief_complaint or gender == "Select" or thermal == "Select":
                st.error("⚠️ Please fill in all required fields (Name, Age, Gender, Chief Complaint, Thermal Preference).")
            else:
                record_id = f"PAT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                record_data = {
                    "id": record_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "patient_name": patient_name,
                    "age": age,
                    "gender": gender,
                    "phone": phone,
                    "occupation": occupation,
                    "visit_date": str(visit_date),
                    "chief_complaint": chief_complaint,
                    "sensation_type": sensation_type,
                    "onset_trigger": onset_trigger,
                    "affected_side": affected_side,
                    "thermal": thermal,
                    "sweat_pattern": sweat_pattern,
                    "thirst": thirst,
                    "appetite_cravings": appetite_cravings,
                    "food_aversions": food_aversions,
                    "sleep_posture": sleep_posture,
                    "temperament": temperament,
                    "mind_notes": mind_notes,
                    "worse_by": worse_by,
                    "better_by": better_by,
                    "past_history": past_history,
                    "prescription": ""
                }
                
                # Save JSON file
                json_path = os.path.join(DATA_DIR, f"{record_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(record_data, f, indent=2)
                
                # Save DB
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''INSERT INTO consultations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (record_id, record_data["timestamp"], patient_name, age, gender, phone,
                           chief_complaint, thermal, thirst, ", ".join(temperament), ", ".join(worse_by),
                           json.dumps(record_data), ""))
                conn.commit()
                conn.close()

                st.success(f"✅ Patient consultation record successfully saved! Record ID: **{record_id}**")
                st.info("Doctor can now view and prescribe remedies in the 'Doctor Review & Prescriber' tab.")

# ==================== TAB 2: DOCTOR REVIEW & PRESCRIBER ====================
with tab2:
    st.subheader("🩺 Clinical Review & Remedy Prescription Desk")
    
    # Load all records
    conn = sqlite3.connect(DB_PATH)
    df_records = pd.read_sql_query("SELECT id, timestamp, patient_name, chief_complaint FROM consultations ORDER BY timestamp DESC", conn)
    conn.close()

    if df_records.empty:
        st.warning("No saved patient records found. Complete a patient intake form in Tab 1 first.")
    else:
        patient_options = [f"{row['id']} - {row['patient_name']} ({row['timestamp']})" for _, row in df_records.iterrows()]
        selected_option = st.selectbox("Select Patient Case File", patient_options)
        selected_id = selected_option.split(" - ")[0]

        # Load selected JSON
        json_file = os.path.join(DATA_DIR, f"{selected_id}.json")
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                case_data = json.load(f)

            col_p1, col_p2 = st.columns([1, 1])
            
            with col_p1:
                st.markdown("### 📄 Patient Constitutional Profile")
                st.markdown(f"**Name:** {case_data['patient_name']} | **Age:** {case_data['age']} | **Gender:** {case_data['gender']}")
                st.markdown(f"**Contact:** {case_data['phone']} | **Occupation:** {case_data['occupation']}")
                st.markdown(f"**Chief Complaint:** {case_data['chief_complaint']}")
                st.markdown(f"**Sensations:** {', '.join(case_data['sensation_type'])}")
                st.markdown(f"**Onset / Cause:** {case_data['onset_trigger']}")
                
                st.markdown("#### Physical Generals & Temperament")
                st.markdown(f"• **Thermal:** {case_data['thermal']}")
                st.markdown(f"• **Thirst:** {case_data['thirst']}")
                st.markdown(f"• **Cravings:** {', '.join(case_data['appetite_cravings'])}")
                st.markdown(f"• **Mind / Mood:** {', '.join(case_data['temperament'])}")
                st.markdown(f"• **Worse By:** {', '.join(case_data['worse_by'])}")
                st.markdown(f"• **Better By:** {', '.join(case_data['better_by'])}")
                st.markdown(f"• **Past History:** {case_data['past_history']}")

            with col_p2:
                st.markdown("### 💡 Homeopathic Remedy Intelligence Assistant")
                
                # Rule-based Materia Medica Suggestion Logic
                remedy_hints = []
                worse_set = set(case_data['worse_by'])
                better_set = set(case_data['better_by'])
                mind_set = set(case_data['temperament'])
                thermal_str = case_data['thermal']
                thirst_str = case_data['thirst']

                if "Chilly (Sensitive to cold / Craves warmth)" in thermal_str and "Small sips frequently" in thirst_str and "Anxious / Restless" in mind_set:
                    remedy_hints.append(("Arsenicum Album", "Chilly, restless, anxious, thirst for small sips frequently, worse at night/cold."))
                
                if "Mild / Gentle / Weepy" in mind_set and "Thirstless" in thirst_str and "Fresh air" in better_set:
                    remedy_hints.append(("Pulsatilla Nigricans", "Mild, gentle, thirstless, changeable symptoms, better in open fresh air."))

                if "Motion / Walking" in worse_set and "Absolute rest" in better_set:
                    remedy_hints.append(("Bryonia Alba", "Greatly aggravated by least motion, better by rest and hard pressure, dry thirst for large quantities."))

                if "Cold / Drafts" in worse_set and "Rest / Inactivity" in worse_set and "Continued motion" in better_set:
                    remedy_hints.append(("Rhus Toxicodendron", "Joint stiffness worse on first motion/rest, better by continued motion and heat."))

                if "Irritable / Quick-tempered" in mind_set and "Fastidious / Perfectionist" in mind_set:
                    remedy_hints.append(("Nux Vomica", "Overwork, sedentary lifestyle, highly irritable, sensitive to cold/drafts."))

                if "Throbbing" in case_data['sensation_type'] and "Heat / Warm room" in worse_set:
                    remedy_hints.append(("Belladonna", "Sudden violent onset, throbbing pains, red flushed skin, aggravated by touch/light."))

                if not remedy_hints:
                    remedy_hints.append(("Sulphur", "Polychrest remedy for skin/systemic conditions, hot-blooded, craves sweets, worse standing."))
                    remedy_hints.append(("Calcarea Carbonica", "Chilly, fair, sweat on head/neck, craves eggs/sour, anxious temperament."))

                for remedy, desc in remedy_hints:
                    st.markdown(f"""
                    <div class="remedy-card">
                        <b>🌿 {remedy}</b><br>
                        <small>{desc}</small>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### ✍️ Doctor's Prescription Desk")
                with st.form("prescription_form"):
                    rx_remedy = st.text_input("Prescribed Remedy Name *", placeholder="e.g. Arsenicum Album 30C")
                    col_rx1, col_rx2 = st.columns(2)
                    with col_rx1:
                        rx_potency = st.selectbox("Potency", ["6C", "30C", "200C", "1M", "10M", "LM1", "Q Mother Tincture"])
                        rx_frequency = st.selectbox("Frequency", ["Single Dose", "BD (Twice daily)", "TDS (Three times daily)", "QID (Four times daily)", "SOS (As needed)"])
                    with col_rx2:
                        rx_duration = st.text_input("Duration", "7 Days")
                        rx_diet = st.text_input("Dietary / Lifestyle Advice", "Avoid raw onion, garlic, camphor, & strong mint")
                    
                    rx_notes = st.text_area("Clinical Notes & Follow-up Instructions", placeholder="Follow up in 2 weeks or if symptoms change...")
                    
                    prescribe_submit = st.form_submit_button("📌 Save Prescription & Generate Clinical Note")

                    if prescribe_submit:
                        if not rx_remedy:
                            st.error("Please enter a remedy name.")
                        else:
                            rx_summary = f"Remedy: {rx_remedy} ({rx_potency}) | Frequency: {rx_frequency} | Duration: {rx_duration} | Diet: {rx_diet} | Notes: {rx_notes}"
                            case_data["prescription"] = rx_summary
                            
                            # Update JSON
                            with open(json_file, "w", encoding="utf-8") as f:
                                json.dump(case_data, f, indent=2)
                            
                            # Update DB
                            conn = sqlite3.connect(DB_PATH)
                            c = conn.cursor()
                            c.execute("UPDATE consultations SET prescription = ? WHERE id = ?", (rx_summary, selected_id))
                            conn.commit()
                            conn.close()

                            st.success(f"✅ Prescription for {case_data['patient_name']} saved successfully!")
                            st.code(rx_summary, language="text")

# ==================== TAB 3: RECORDS DIRECTORY & ANALYTICS ====================
with tab3:
    st.subheader("📊 Saved Clinical Consultations & Database Analytics")
    
    conn = sqlite3.connect(DB_PATH)
    df_all = pd.read_sql_query("SELECT id, timestamp, patient_name, age, gender, phone, chief_complaint, thermal, thirst, mindset, modalities, prescription FROM consultations ORDER BY timestamp DESC", conn)
    conn.close()

    if df_all.empty:
        st.info("No consultation records found in database.")
    else:
        st.dataframe(df_all, use_container_width=True)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.metric("Total Patient Consultations", len(df_all))
            csv_data = df_all.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download All Consultations CSV",
                data=csv_data,
                file_name=f"homeopathy_consultations_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        with col_d2:
            prescribed_count = len(df_all[df_all['prescription'] != ""])
            st.metric("Completed Prescriptions", f"{prescribed_count} / {len(df_all)}")
