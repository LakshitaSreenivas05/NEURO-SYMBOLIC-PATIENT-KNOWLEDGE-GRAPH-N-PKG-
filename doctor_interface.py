import streamlit as st
import json
import sys

# Import your custom modules
from llm_validator import validate
from neo4j_handler import KnowledgeGraphManager
from live_audio import transcribe_live
from extract_entities import extract_entities
from structure_with_llm import structure_entities

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Clinical Portal",
    layout="wide"
)

# ==========================================
# PROFESSIONAL CSS (Light & Eye-Friendly)
# ==========================================
st.markdown("""
<style>
    /* Very light, soft background to reduce eye strain */
    .stApp { background-color: #F8F9FA; }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 400;
        color: #2C3E50;
        margin-bottom: 0px;
        border-bottom: 2px solid #E9ECEF;
        padding-bottom: 12px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #6C757D;
        margin-bottom: 30px;
        margin-top: 10px;
    }

    /* Clean Card Style with soft borders */
    .clinical-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #E9ECEF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    .section-heading {
        font-size: 1.15rem;
        font-weight: 600;
        color: #343A40;
        border-bottom: 1px solid #E9ECEF;
        padding-bottom: 10px;
        margin-bottom: 18px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .subsection-heading {
        font-size: 1rem;
        font-weight: 600;
        color: #495057;
        margin-top: 15px;
        margin-bottom: 8px;
    }

    /* Verdict Banners */
    .verdict-banner {
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid transparent;
    }
    .verdict-approved {
        background-color: #F1F8F1;
        border-color: #C8E6C9;
        border-left: 6px solid #2E7D32;
    }
    .verdict-conflict {
        background-color: #FFEBEE;
        border-color: #FFCDD2;
        border-left: 6px solid #C62828;
    }
    .verdict-review {
        background-color: #FFF8E1;
        border-color: #FFECB3;
        border-left: 6px solid #F9A825;
    }
    
    .verdict-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    .text-approved { color: #2E7D32; }
    .text-conflict { color: #C62828; }
    .text-review { color: #F9A825; }

    /* Tags */
    .data-tag {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin: 4px 4px 4px 0;
        font-weight: 500;
        background: #F1F3F5;
        color: #495057;
        border: 1px solid #DEE2E6;
    }
    .tag-med { background: #E3F2FD; color: #1565C0; border-color: #BBDEFB; }
    .tag-danger { background: #FFEBEE; color: #C62828; border-color: #FFCDD2; }
    .tag-warning { background: #FFF8E1; color: #F9A825; border-color: #FFECB3; }
    .tag-date { background: #F3E5F5; color: #6A1B9A; border-color: #E1BEE7; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA PROCESSING HELPERS
# ==========================================

def get_patient_list():
    try:
        kg = KnowledgeGraphManager()
        with kg.driver.session() as session:
            result = session.run("MATCH (p:Patient) RETURN p.name as name ORDER BY p.name")
            names = [record["name"] for record in result]
        kg.close()
        return names if names else []
    except:
        return []

def process_clinical_text_to_json(text):
    """Runs the NLP pipeline to convert unstructured text to structured patient JSON."""
    entities = extract_entities(text)
    raw_json = structure_entities(text, entities)
    try:
        match = re.search(r'\{.*\}', raw_json, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw_json)
    except Exception as e:
        st.error(f"Format Error: BioMistral did not return valid JSON. {e}")
        return None

def merge_patient_records(existing_data, new_data):
    """Merges new extracted data into the existing patient record."""
    return {
        "patient_name": existing_data.get("patient_name"),
        "age": new_data.get("age") or existing_data.get("age"),
        "gender": new_data.get("gender") or existing_data.get("gender"),
        "diseases": list(set(existing_data.get("diseases", []) + new_data.get("diseases", []))),
        "medications": list(set(existing_data.get("medications", []) + new_data.get("medications", []))),
        "allergies": list(set(existing_data.get("allergies", []) + new_data.get("allergies", []))),
        "symptoms": list(set(existing_data.get("symptoms", []) + new_data.get("symptoms", []))),
        "important_dates": list(set(existing_data.get("important_dates", []) + new_data.get("important_dates", []))),
        "warnings": list(set(existing_data.get("warnings", []) + new_data.get("warnings", [])))
    }

# ==========================================
# UI RENDERING HELPERS
# ==========================================

def render_patient_record(patient_data):
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Comprehensive Patient Medical Record</div>', unsafe_allow_html=True)

    # Demographics Row
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**Patient Name:**<br><span style='font-size:1.15rem; color:#2C3E50;'>{patient_data.get('patient_name', 'Unknown')}</span>", unsafe_allow_html=True)
    c2.markdown(f"**Current Age:**<br><span style='font-size:1.15rem; color:#2C3E50;'>{patient_data.get('age', 'N/A')}</span>", unsafe_allow_html=True)
    c3.markdown(f"**Biological Sex:**<br><span style='font-size:1.15rem; color:#2C3E50;'>{patient_data.get('gender', 'N/A')}</span>", unsafe_allow_html=True)
    
    st.write("---")

    # Clinical Data Columns
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="subsection-heading">Diagnosed Conditions</div>', unsafe_allow_html=True)
        items = patient_data.get("diseases", [])
        st.markdown(" ".join([f'<span class="data-tag">{i}</span>' for i in items]) if items else "_No conditions documented._", unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-heading">Active Medications</div>', unsafe_allow_html=True)
        items = patient_data.get("medications", [])
        st.markdown(" ".join([f'<span class="data-tag tag-med">{i}</span>' for i in items]) if items else "_No active medications._", unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-heading">Reported Symptoms</div>', unsafe_allow_html=True)
        items = patient_data.get("symptoms", [])
        st.markdown(" ".join([f'<span class="data-tag">{i}</span>' for i in items]) if items else "_No recent symptoms reported._", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="subsection-heading">Known Allergies</div>', unsafe_allow_html=True)
        items = patient_data.get("allergies", [])
        st.markdown(" ".join([f'<span class="data-tag tag-danger">{i}</span>' for i in items]) if items else "_No known allergies._", unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-heading">Clinical Warnings</div>', unsafe_allow_html=True)
        items = patient_data.get("warnings", [])
        st.markdown(" ".join([f'<span class="data-tag tag-warning">{i}</span>' for i in items]) if items else "_No critical warnings._", unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-heading">Important Dates</div>', unsafe_allow_html=True)
        items = patient_data.get("important_dates", [])
        st.markdown(" ".join([f'<span class="data-tag tag-date">{i}</span>' for i in items]) if items else "_No upcoming appointments._", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_validation_verdict(result):
    verdict = result.get("verdict")
    
    if verdict == "APPROVED":
        st.markdown("""
        <div class="verdict-banner verdict-approved">
            <h2 class="verdict-title text-approved">[ APPROVED ] Safe to Dispense</h2>
            <p style="margin:0; color:#2C3E50;">No contraindications or allergy conflicts detected against patient history.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif verdict == "CONFLICT":
        st.markdown(f"""
        <div class="verdict-banner verdict-conflict">
            <h2 class="verdict-title text-conflict">[ CONFLICT ] Prescription Blocked ({result.get('severity')})</h2>
            <p style="margin:0; color:#2C3E50;">Critical medical conflict detected. Review details below.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif verdict == "REVIEW":
        st.markdown("""
        <div class="verdict-banner verdict-review">
            <h2 class="verdict-title text-review">[ REVIEW REQUIRED ] Unverified Flags</h2>
            <p style="margin:0; color:#2C3E50;">AI flagged potential issues not strictly found in patient database. Manual clinical review required.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    if result.get("reasoning"):
        st.write("**Clinical Reasoning:**")
        st.info(result.get("reasoning"))

    confirmed = result.get("confirmed_conflicts", [])
    if confirmed:
        st.markdown('<div class="subsection-heading" style="color:#C62828;">Confirmed Conflicts</div>', unsafe_allow_html=True)
        for c in confirmed:
            st.error(f"**[{c.get('type')}] {c.get('drug')}** — {c.get('reason')}")

    unverified = result.get("unverified_flags", [])
    if unverified:
        st.markdown('<div class="subsection-heading" style="color:#F9A825;">Unverified Flags (Requires Review)</div>', unsafe_allow_html=True)
        for c in unverified:
            st.warning(f"**[{c.get('type')}] {c.get('drug')}** — {c.get('reason')}")

    if result.get("recommendation"):
        st.write("**Alternative Recommendation:**")
        st.success(result.get("recommendation"))


# ==========================================
# MAIN APPLICATION INTERFACE
# ==========================================

def main():
    st.markdown('<div class="main-title">Clinical Knowledge Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Neuro-Symbolic Patient Knowledge Graph (N-PKG)</div>', unsafe_allow_html=True)

    # Top level navigation
    tab1, tab2 = st.tabs(["Patient Records Management", "Prescription Validation"])

    # ---------------------------------------------------------
    # TAB 1: PATIENT RECORDS MANAGEMENT
    # ---------------------------------------------------------
    with tab1:
        patient_mode = st.radio("Select Action:", ["View / Update Existing Patient", "Add New Patient"], horizontal=True, label_visibility="collapsed")
        st.write("---")

        # ── MODE: VIEW / UPDATE ──
        if patient_mode == "View / Update Existing Patient":
            patient_list = get_patient_list()
            
            if not patient_list:
                st.info("No patients found in the database. Please add a new patient.")
            else:
                selected_patient = st.selectbox("Select Patient Record", options=patient_list)
                
                kg = KnowledgeGraphManager()
                patient_data = kg.get_patient(selected_patient)
                kg.close()

                if patient_data:
                    render_patient_record(patient_data)
                    
                    # Update Section
                    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Update Patient Record (Addendum)</div>', unsafe_allow_html=True)
                    st.write("Type clinical notes below, or use the microphone to dictate")