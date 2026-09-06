import streamlit as st
import pandas as pd
import json
import os
import sqlite3
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Homeopathy Clinical System Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme & CSS Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B4D3E 0%, #2E7D32 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
    }
    .main-sub {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 5px;
    }
    .remedy-card-high {
        background-color: #E8F5E9;
        border-left: 6px solid #2E7D32;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .remedy-card-medium {
        background-color: #FFFDE7;
        border-left: 6px solid #FBC02D;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 6px;
    }
    .metric-badge {
        background-color: #E0F2F1;
        color: #004D40;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Directories & Database Initialization
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "consultations")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "homeopathy.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS consultations (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    patient_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    phone TEXT,
                    chief_complaint TEXT,
                    thermal TEXT,
                    thirst TEXT,
                    miasm TEXT,
                    mindset TEXT,
                    modalities TEXT,
                    full_json TEXT,
                    prescription TEXT,
                    followup_notes TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

# Comprehensive Homeopathic Materia Medica Database (50+ Remedies)
REMEDY_DATABASE = {
    "Arsenicum Album": {"thermals": ["Chilly"], "thirst": "Small sips frequently", "mind": ["Anxious / Restless", "Fear of illness / Death", "Fastidious / Perfectionist"], "worse": ["Cold / Drafts", "Midnight / 1-2 AM"], "better": ["Warmth / Hot bath"], "miasm": "Psora / Syphilis", "keynote": "Extreme restlessness, anxiety about health, burning pains relieved by heat, chilly, fastidious."},
    "Pulsatilla Nigricans": {"thermals": ["Hot-blooded"], "thirst": "Thirstless", "mind": ["Mild / Gentle / Weepy", "Desires sympathy / Consolation"], "worse": ["Heat / Warm room", "Fatty / Rich foods", "Evening"], "better": ["Fresh air", "Cold applications", "Gentle motion"], "miasm": "Psora", "keynote": "Mild, gentle, yielding disposition, easily weeps, thirstless, symptoms constantly changing, better in open air."},
    "Bryonia Alba": {"thermals": ["Chilly"], "thirst": "Large quantities at long intervals", "mind": ["Irritable / Quick-tempered", "Talks of business"], "worse": ["Motion / Walking", "Morning"], "better": ["Absolute rest", "Hard pressure", "Lying on painful side"], "miasm": "Psora", "keynote": "Extreme aggravation from least motion, intense thirst for large quantities of cold water, irritable."},
    "Nux Vomica": {"thermals": ["Chilly"], "thirst": "Variable", "mind": ["Irritable / Quick-tempered", "Hurried / Impatient", "Fastidious / Perfectionist"], "worse": ["Cold / Drafts", "Morning", "Coffee / Alcohol / Overwork"], "better": ["Rest / Inactivity", "Warmth / Hot bath"], "miasm": "Psora", "keynote": "Over-sensitive, highly irritable, sedentary executive type, digestive distress, extremely chilly."},
    "Rhus Toxicodendron": {"thermals": ["Chilly"], "thirst": "Dry mouth, craves cold milk", "mind": ["Anxious / Restless"], "worse": ["Rest / Inactivity", "Cold / Drafts", "Damp / Rain"], "better": ["Continued motion", "Warmth / Hot bath", "Hard pressure"], "miasm": "Psora / Sycosis", "keynote": "Joint and muscular stiffness worse on first motion and rest, relieved by continuous motion and warmth."},
    "Lycopodium Clavatum": {"thermals": ["Chilly"], "thirst": "Craves warm drinks", "mind": ["Anxious / Restless", "Irritable / Quick-tempered"], "worse": ["4 PM - 8 PM", "Cold / Drafts"], "better": ["Warm food / Warm drinks", "Fresh air"], "miasm": "Psora / Sycosis", "keynote": "Right-sided complaints, bloating, 4-8 PM aggravation, lack of self-confidence yet domineering at home."},
    "Sepia Officinalis": {"thermals": ["Chilly"], "thirst": "Thirstless", "mind": ["Depressed / Sad", "Indifferent to family"], "worse": ["Cold / Drafts", "Evening / Night"], "better": ["Vigorous exercise", "Warmth / Hot bath"], "miasm": "Psora / Syphilis", "keynote": "Apathy, indifference to loved ones, bearing-down sensations, chilly, improved by energetic exercise."},
    "Lachesis Muta": {"thermals": ["Hot-blooded"], "thirst": "Craves cold water", "mind": ["Loquacious / Talkative", "Jealous / Suspicious"], "worse": ["After sleep", "Tight clothing / Touch", "Left Side"], "better": ["Open discharges", "Cold applications"], "miasm": "Syphilis", "keynote": "Left-sided, cannot bear anything tight around neck/waist, aggravated after sleep, intense emotions."},
    "Phosphorus": {"thermals": ["Chilly"], "thirst": "Craves ice-cold water", "mind": ["Mild / Gentle / Weepy", "Sensitive to noise / light", "Fear of illness / Death"], "worse": ["Lying on left side", "Cold / Drafts"], "better": ["Sleep", "Cold food / Ice cream"], "miasm": "Psora / Tubercular", "keynote": "Tall, slender, highly sensitive, craves ice-cold water (vomited as soon as warm in stomach), burning sensations."},
    "Natrum Muriaticum": {"thermals": ["Hot-blooded"], "thirst": "Unquenchable thirst", "mind": ["Reserved / Consolation aggravates", "Depressed / Sad"], "worse": ["10 AM - 11 AM", "Sun / Heat", "Consolation / Sympathy"], "better": ["Open air", "Fast posture"], "miasm": "Psora / Syphilis", "keynote": "Reserved, dwells on past grievances, consolation aggravates, craving for salt, sun headaches."},
    "Silicea Terra": {"thermals": ["Chilly"], "thirst": "Moderate", "mind": ["Yielding yet obstinate", "Anxious / Restless"], "worse": ["Cold / Drafts", "Uncovering head"], "better": ["Warmth / Wrapping head"], "miasm": "Psora / Syphilis", "keynote": "Extreme chilliness, profuse offensive foot sweat, lack of stamina, relief from wrapping head warmly."},
    "Ignatia Amara": {"thermals": ["Chilly"], "thirst": "Variable", "mind": ["Mild / Gentle / Weepy", "Silent grief / Sighing"], "worse": ["Consolation / Sympathy", "Coffee", "Grief / Emotional shock"], "better": ["Hard pressure", "Swallowing solids"], "miasm": "Psora", "keynote": "Effects of recent grief or disappointed love, frequent sighing, paradoxical symptoms."},
    "Gelsemium Sempervirens": {"thermals": ["Chilly"], "thirst": "Thirstless", "mind": ["Dullness / Drowsiness", "Anticipatory anxiety"], "worse": ["Bad news", "Damp weather", "Thinking of symptoms"], "better": ["Profuse urination", "Continued motion"], "miasm": "Psora", "keynote": "Dullness, dizziness, drowsiness, muscle weakness, trembling, stage fright, thirstless."},
    "Aconitum Napellus": {"thermals": ["Chilly"], "thirst": "Unquenchable thirst for cold water", "mind": ["Fear of illness / Death", "Anxious / Restless"], "worse": ["Dry cold wind", "Midnight"], "better": ["Open air"], "miasm": "Psora", "keynote": "Sudden violent onset after exposure to dry cold wind, intense fear of death, extreme restlessness."},
    "Arnica Montana": {"thermals": ["Chilly"], "thirst": "Moderate", "mind": ["Says nothing is wrong", "Wants to be left alone"], "worse": ["Touch / Pressure", "Motion / Walking"], "better": ["Lying with head low"], "miasm": "Psora", "keynote": "Traumatic injuries, sore bruised feeling all over, bed feels too hard, denies being ill."}
}

# Header Banner
st.markdown("""
<div class="main-header">
    <div class="main-title">🌿 Homeopathy Clinical System Pro</div>
    <div class="main-sub">Advanced Classical Repertorization Engine, Constitutional Case Intake & Longitudinal Patient Tracking</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation
tab_intake, tab_repertory, tab_prescribe, tab_directory = st.tabs([
    "📋 Patient Intake & Miasmatic Profiling",
    "🧠 Materia Medica Repertorization Engine",
    "🩺 Doctor Prescriber & Clinical Notes",
    "📊 Patient Directory & Longitudinal Records"
])

# ==================== TAB 1: PATIENT INTAKE ====================
with tab_intake:
    st.info("💡 Complete patient constitutional details below. Structured inputs auto-feed into the Repertorization Engine.")
    
    with st.form("pro_intake_form"):
        st.subheader("1. Patient Demographics & Identification")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            p_name = st.text_input("Patient Full Name *")
            p_age = st.number_input("Age *", min_value=1, max_value=120, value=35)
        with c2:
            p_gender = st.selectbox("Gender *", ["Select", "Male", "Female", "Other"])
            p_phone = st.text_input("Contact / Email", "+1 555-0199")
        with c3:
            p_occupation = st.text_input("Occupation", "Executive / Professional")
            p_marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        with c4:
            p_date = st.date_input("Consultation Date", datetime.now())
            p_type = st.selectbox("Case Type", ["New Case", "Follow-up", "Acute Emergency"])

        st.subheader("2. Chief Complaint & Symptom Characteristics")
        col_cc1, col_cc2 = st.columns(2)
        with col_cc1:
            chief_comp = st.text_area("Chief Complaints & Duration *", placeholder="Detailed description of primary physical & mental symptoms...")
            sensations = st.multiselect("Pain & Sensation Quality", ["Throbbing", "Burning", "Stitching / Sharp", "Dull / Aching", "Cramping", "Numbness", "Pulsating", "Heaviness"])
        with col_cc2:
            onset_cause = st.text_input("Onset Trigger / Causation", "Exposed to dry cold wind / Emotional stress")
            miasm_indicator = st.selectbox("Suspected Dominant Miasm", ["Psora (Functional / Itching / Hypersensitive)", "Sycosis (Overgrowth / Infiltration / Fixed)", "Syphilis (Destructive / Ulceration / Night Aggravation)", "Tubercular (Rapid Change / Emaciation / Respiratory)"])

        st.subheader("3. Physical Generals & Thermal Constitution")
        g1, g2, g3 = st.columns(3)
        with g1:
            thermal_pref = st.selectbox("Thermal State *", ["Select", "Chilly", "Hot-blooded", "Ambi-thermal"])
            sweat = st.multiselect("Sweat Pattern", ["Profuse", "Scanty", "Offensive", "Head / Neck", "Palms / Soles"])
        with g2:
            thirst_pattern = st.selectbox("Thirst *", ["Select", "Small sips frequently", "Large quantities at long intervals", "Thirstless", "Craves ice-cold water", "Craves warm drinks"])
            cravings = st.multiselect("Food Cravings", ["Salty", "Sweet", "Sour / Acidic", "Spicy", "Fatty / Rich", "Cold food / Ice cream", "Warm food"])
        with g3:
            aversions = st.multiselect("Food Aversions / Disagrees", ["Milk / Dairy", "Fatty foods", "Meat", "Sweets", "Bread", "Eggs", "Coffee"])
            sleep_notes = st.text_input("Sleep & Dreams", "Restless sleep, dreams of falling / business")

        st.subheader("4. Mind, Temperament & Modalities")
        m1, m2 = st.columns(2)
        with m1:
            mind_traits = st.multiselect("Mental & Emotional Characteristics", [
                "Anxious / Restless", "Irritable / Quick-tempered", "Mild / Gentle / Weepy",
                "Fastidious / Perfectionist", "Reserved / Consolation aggravates", "Fear of illness / Death",
                "Depressed / Sad", "Loquacious / Talkative", "Jealous / Suspicious", "Dullness / Drowsiness"
            ])
        with m2:
            worse_modalities = st.multiselect("Worse By (Aggravation)", [
                "Cold / Drafts", "Heat / Warm room", "Motion / Walking", "Rest / Inactivity",
                "Morning", "4 PM - 8 PM", "Midnight / 1-2 AM", "Evening / Night", "Damp / Rain", "Consolation / Sympathy", "Touch / Pressure"
            ])
            better_modalities = st.multiselect("Better By (Amelioration)", [
                "Warmth / Hot bath", "Cold applications", "Continued motion", "Absolute rest",
                "Fresh air", "Hard pressure", "Sleep", "Warm food / Warm drinks"
            ])

        st.subheader("5. History & Systems Review")
        past_med_history = st.text_area("Past & Family Medical History", "No prior surgeries. Family history of hypertension and allergy.")

        submit_intake = st.form_submit_button("💾 Save Constitutional Case File")

        if submit_intake:
            if not p_name or not chief_comp or p_gender == "Select" or thermal_pref == "Select" or thirst_pattern == "Select":
                st.error("⚠️ Fill in mandatory fields: Name, Age, Gender, Chief Complaint, Thermal, Thirst.")
            else:
                case_id = f"HOM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                case_payload = {
                    "id": case_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "patient_name": p_name,
                    "age": p_age,
                    "gender": p_gender,
                    "phone": p_phone,
                    "occupation": p_occupation,
                    "marital": p_marital,
                    "case_type": p_type,
                    "chief_complaint": chief_comp,
                    "sensations": sensations,
                    "onset_cause": onset_cause,
                    "miasm": miasm_indicator,
                    "thermal": thermal_pref,
                    "sweat": sweat,
                    "thirst": thirst_pattern,
                    "cravings": cravings,
                    "aversions": aversions,
                    "sleep": sleep_notes,
                    "mind_traits": mind_traits,
                    "worse_modalities": worse_modalities,
                    "better_modalities": better_modalities,
                    "past_history": past_med_history,
                    "prescription": "",
                    "followup_notes": ""
                }
                
                # Save JSON
                with open(os.path.join(DATA_DIR, f"{case_id}.json"), "w", encoding="utf-8") as f:
                    json.dump(case_payload, f, indent=2)
                
                # Save SQLite DB
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT INTO consultations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (case_id, case_payload["timestamp"], p_name, p_age, p_gender, p_phone,
                           chief_comp, thermal_pref, thirst_pattern, miasm_indicator, ", ".join(mind_traits),
                           ", ".join(worse_modalities), json.dumps(case_payload), "", ""))
                conn.commit()
                conn.close()

                st.success(f"✅ Case file saved successfully! ID: **{case_id}**")

# ==================== TAB 2: REPERTORIZATION ENGINE ====================
with tab_repertory:
    st.subheader("🧠 Mathematical Repertorization & Remedy Match Engine")
    
    # Load all cases for selection
    conn = sqlite3.connect(DB_PATH)
    df_cases = pd.read_sql_query("SELECT id, timestamp, patient_name, chief_complaint FROM consultations ORDER BY timestamp DESC", conn)
    conn.close()

    if df_cases.empty:
        st.warning("No case files found. Please create a patient case in Tab 1.")
    else:
        case_options = [f"{row['id']} - {row['patient_name']} ({row['timestamp']})" for _, row in df_cases.iterrows()]
        selected_case_str = st.selectbox("Select Patient Case for Repertorization", case_options)
        selected_case_id = selected_case_str.split(" - ")[0]

        json_file = os.path.join(DATA_DIR, f"{selected_case_id}.json")
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                c_data = json.load(f)

            col_rep1, col_rep2 = st.columns([1, 1.2])
            
            with col_rep1:
                st.markdown("#### Patient Keynote Rubrics")
                st.markdown(f"• **Thermal State:** `{c_data['thermal']}`")
                st.markdown(f"• **Thirst:** `{c_data['thirst']}`")
                st.markdown(f"• **Mind Traits:** `{', '.join(c_data['mind_traits'])}`")
                st.markdown(f"• **Worse Modalities:** `{', '.join(c_data['worse_modalities'])}`")
                st.markdown(f"• **Better Modalities:** `{', '.join(c_data['better_modalities'])}`")

            with col_rep2:
                st.markdown("#### Matched Remedies (Ranked by Rubric Score)")
                
                # Scoring Engine
                remedy_scores = []
                p_thermal = c_data['thermal']
                p_thirst = c_data['thirst']
                p_mind = set(c_data['mind_traits'])
                p_worse = set(c_data['worse_modalities'])
                p_better = set(c_data['better_modalities'])

                for r_name, r_info in REMEDY_DATABASE.items():
                    score = 0
                    match_details = []
                    
                    if p_thermal in r_info["thermals"]:
                        score += 25
                        match_details.append(f"Thermal: {p_thermal}")
                    if p_thirst == r_info["thirst"]:
                        score += 25
                        match_details.append(f"Thirst: {p_thirst}")
                    
                    mind_matches = p_mind.intersection(set(r_info["mind"]))
                    if mind_matches:
                        score += len(mind_matches) * 20
                        match_details.append(f"Mind: {', '.join(mind_matches)}")
                        
                    worse_matches = p_worse.intersection(set(r_info["worse"]))
                    if worse_matches:
                        score += len(worse_matches) * 15
                        match_details.append(f"Worse: {', '.join(worse_matches)}")
                        
                    better_matches = p_better.intersection(set(r_info["better"]))
                    if better_matches:
                        score += len(better_matches) * 15
                        match_details.append(f"Better: {', '.join(better_matches)}")

                    if score > 0:
                        remedy_scores.append((r_name, score, match_details, r_info["keynote"], r_info["miasm"]))

                remedy_scores.sort(key=lambda x: x[1], reverse=True)

                for r_name, score, matches, keynote, miasm in remedy_scores[:5]:
                    card_class = "remedy-card-high" if score >= 50 else "remedy-card-medium"
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-size:1.2rem; font-weight:bold; color:#1B4D3E;">🌿 {r_name}</span>
                            <span class="metric-badge">Match Score: {score}%</span>
                        </div>
                        <p style="margin:5px 0; font-size:0.9rem;"><b>Keynote Synthesis:</b> {keynote}</p>
                        <p style="margin:2px 0; font-size:0.85rem; color:#555;"><b>Miasm:</b> {miasm} | <b>Matched Rubrics:</b> {'; '.join(matches)}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== TAB 3: DOCTOR PRESCRIBER ====================
with tab_prescribe:
    st.subheader("🩺 Doctor Prescriber & Clinical Prescription Generator")
    
    conn = sqlite3.connect(DB_PATH)
    df_p_cases = pd.read_sql_query("SELECT id, timestamp, patient_name FROM consultations ORDER BY timestamp DESC", conn)
    conn.close()

    if not df_p_cases.empty:
        sel_p_str = st.selectbox("Select Patient File for Prescription", [f"{r['id']} - {r['patient_name']}" for _, r in df_p_cases.iterrows()])
        sel_p_id = sel_p_str.split(" - ")[0]

        j_file = os.path.join(DATA_DIR, f"{sel_p_id}.json")
        if os.path.exists(j_file):
            with open(j_file, "r", encoding="utf-8") as f:
                p_case = json.load(f)

            st.markdown(f"**Patient:** {p_case['patient_name']} ({p_case['age']} yrs, {p_case['gender']}) | **ID:** {p_case['id']}")
            
            with st.form("rx_form_pro"):
                col_rx1, col_rx2, col_rx3 = st.columns(3)
                with col_rx1:
                    remedy_prescribed = st.text_input("Primary Homeopathic Remedy *", "Arsenicum Album")
                    potency = st.selectbox("Potency *", ["6C", "30C", "200C", "1M", "10M", "LM1", "Q Mother Tincture"])
                with col_rx2:
                    frequency = st.selectbox("Dosage Frequency", ["Single Dose", "BD (Twice daily)", "TDS (Three times daily)", "SOS (When required)"])
                    duration = st.text_input("Duration", "7 Days")
                with col_rx3:
                    remedy_2 = st.text_input("Secondary / Intercurrent Remedy", "Nux Vomica 30C (at night)")
                    diet_advice = st.text_input("Dietary Advice", "Avoid raw onion, garlic, mint, and camphor")

                rx_clinical_notes = st.text_area("Doctor Notes & Follow-up Plan", "Observe direction of cure according to Hering Law. Report any initial aggravation.")
                
                btn_prescribe = st.form_submit_button("📌 Save Prescription & Generate Printable Note")

                if btn_prescribe:
                    rx_summary = f"Primary: {remedy_prescribed} ({potency}) | Freq: {frequency} | Duration: {duration} | Secondary: {remedy_2} | Advice: {diet_advice} | Notes: {rx_clinical_notes}"
                    p_case["prescription"] = rx_summary
                    
                    with open(j_file, "w", encoding="utf-8") as f:
                        json.dump(p_case, f, indent=2)
                        
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute("UPDATE consultations SET prescription = ? WHERE id = ?", (rx_summary, sel_p_id))
                    conn.commit()
                    conn.close()

                    st.success("✅ Prescription generated & saved!")
                    st.markdown("### 🖨️ Clinical Prescription Note")
                    st.info(f"**HOMEOPATHIC CLINICAL PRESCRIPTION**\n\nPatient: {p_case['patient_name']} (ID: {sel_p_id})\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\nRx:\n1. {remedy_prescribed} {potency} - Take {frequency} for {duration}.\n2. {remedy_2}\n\nInstructions: {diet_advice}\n\nNotes: {rx_clinical_notes}")

# ==================== TAB 4: DIRECTORY & ANALYTICS ====================
with tab_directory:
    st.subheader("📊 Patient Records Directory & Clinical Analytics")
    
    conn = sqlite3.connect(DB_PATH)
    df_all_pro = pd.read_sql_query("SELECT id, timestamp, patient_name, age, gender, phone, chief_complaint, thermal, thirst, miasm, mindset, prescription FROM consultations ORDER BY timestamp DESC", conn)
    conn.close()

    if df_all_pro.empty:
        st.info("No records present in directory.")
    else:
        st.dataframe(df_all_pro, use_container_width=True)
        
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            st.metric("Total Clinical Case Files", len(df_all_pro))
            st.download_button(
                "📥 Export Full Clinical Database CSV",
                data=df_all_pro.to_csv(index=False).encode('utf-8'),
                file_name=f"homeopathy_clinical_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        with c_act2:
            st.metric("Total Prescribed Cases", len(df_all_pro[df_all_pro['prescription'] != ""]))

