import streamlit as st
import json
import sys
import re

# Import your custom modules
from llm_validator import validate
from neo4j_handler import KnowledgeGraphManager
from live_audio import transcribe_live
from extract_entities import extract_entities
from structure_with_llm import structure_entities

def dict_to_bullet_list(items):
    return "\n".join([f"- {i}" for i in items])

# ==========================================
# DATA PROCESSING HELPERS
# ==========================================

def get_patient_list(doctor_username):
    try:
        kg = KnowledgeGraphManager()
        patients = kg.get_patients_for_doctor(doctor_username)
        kg.close()
        return patients if patients else []
    except Exception as e:
        print(f"Error getting patient list: {e}")
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
        "warnings": list(set(existing_data.get("warnings", []) + new_data.get("warnings", []))),
        "scheduled_tests": list(set(existing_data.get("scheduled_tests", []) + new_data.get("scheduled_tests", [])))
    }

# ==========================================
# UI RENDERING HELPERS
# ==========================================

def clean_list(items):
    """Removes 'None', null, or empty strings from clinical lists."""
    if not items: return []
    return [str(i) for i in items if i and str(i).lower() not in ['none', 'null', '']]

def render_patient_record(patient_data):
    # Combine the card container and header into one call to avoid empty boxes
    st.markdown('<div class="modern-card"><div class="section-header">Comprehensive Patient Medical Record</div>', unsafe_allow_html=True)

    # Demographics Row with PII Masking
    c1, c2, c3 = st.columns(3)
    
    is_unlocked = st.session_state.get("pii_unlocked", False)
    
    with c1:
        val = patient_data.get('patient_name', 'Unknown') if is_unlocked else '`[REDACTED]`'
        st.markdown(f"**Patient Name:**<br><span style='font-size:1.15rem; color:#0F172A;'>{val}</span>", unsafe_allow_html=True)
    
    with c2:
        val = patient_data.get('age', 'N/A') if is_unlocked else '`[REDACTED]`'
        st.markdown(f"**Current Age:**<br><span style='font-size:1.15rem; color:#0F172A;'>{val}</span>", unsafe_allow_html=True)
        
    with c3:
        val = patient_data.get('gender', 'N/A') if is_unlocked else '`[REDACTED]`'
        st.markdown(f"**Biological Sex:**<br><span style='font-size:1.15rem; color:#0F172A;'>{val}</span>", unsafe_allow_html=True)
    
    st.write("---")

    if not st.session_state.get("pii_unlocked", False):
        st.warning(" Clinical data is redacted for privacy. Please reveal identity to view full record.")
        if st.button("Reveal Full Clinical Record", type="primary"):
            # Log the reveal event
            kg = KnowledgeGraphManager()
            kg.log_event(st.session_state.username, patient_data.get('patient_username'), 'PII_REVEALED')
            kg.close()
            
            st.session_state.pii_unlocked = True
            st.rerun()
    else:
        if st.button(" Mask Clinical Record"):
            st.session_state.pii_unlocked = False
            st.rerun()

        # Clinical Data Columns
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Diagnosed Conditions</div>', unsafe_allow_html=True)
            items = clean_list(patient_data.get("diseases", []))
            st.markdown(" ".join([f'<span class="data-tag" style="background:#E2E8F0; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;">{i}</span>' for i in items]) if items else "_No conditions documented._", unsafe_allow_html=True)
            
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Active Medications</div>', unsafe_allow_html=True)
            items = clean_list(patient_data.get("medications", []))
            st.markdown(" ".join([f'<span class="data-tag tag-med" style="background:#DBEAFE; color:#1E40AF; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;">{i}</span>' for i in items]) if items else "_No active medications._", unsafe_allow_html=True)
            
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Reported Symptoms</div>', unsafe_allow_html=True)
            items = clean_list(patient_data.get("symptoms", []))
            st.markdown(" ".join([f'<span class="data-tag" style="background:#F1F5F9; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;">{i}</span>' for i in items]) if items else "_No recent symptoms reported._", unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Known Allergies</div>', unsafe_allow_html=True)
            items = clean_list(patient_data.get("allergies", []))
            st.markdown(" ".join([f'<span class="data-tag tag-danger" style="background:#FEE2E2; color:#991B1B; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;">{i}</span>' for i in items]) if items else "_No known allergies._", unsafe_allow_html=True)
            
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Clinical Warnings</div>', unsafe_allow_html=True)
            items = clean_list(patient_data.get("warnings", []))
            st.markdown(" ".join([f'<div style="color:#B91C1C; font-weight:600; margin-top:4px;">{i}</div>' for i in items]) if items else "_No active warnings._", unsafe_allow_html=True)
            
            st.markdown('<div class="section-header" style="font-size:1.05rem; margin-top:15px; border-bottom:none;">Important Dates & Tests</div>', unsafe_allow_html=True)
            dates = clean_list(patient_data.get("important_dates", []))
            tests = clean_list(patient_data.get("scheduled_tests", []))
            
            display_items = []
            for d in dates:
                display_items.append(f'<span class="data-tag tag-date" style="background:#F3E8FF; color:#6B21A8; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;"> {d}</span>')
            for t in tests:
                display_items.append(f'<span class="data-tag tag-test" style="background:#ECFDF5; color:#065F46; padding:4px 10px; border-radius:6px; margin-right:6px; display:inline-block;">{t}</span>')
                
            st.markdown(" ".join(display_items) if display_items else "_No upcoming appointments or tests._", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_validation_verdict(result):
    if not result: return
    
    verdict = result.get("verdict", "UNKNOWN")
    severity = result.get("severity", "NONE")
    reasoning = result.get("reasoning", "No detailed reasoning provided.")
    
    # ── Header ──
    st.markdown("### Prescription Audit Result")
    
    # Status Alert based on verdict
    if verdict == "APPROVED":
        st.success(" **No Alerts Found**: The prescription does not conflict with known history.")
    elif verdict == "CONFLICT":
        st.error(f" **Alerts Found**: High-risk conflict detected ({severity} severity).")
    elif verdict == "REVIEW":
        st.warning(" **Review Required**: Possible moderate risks or insufficient data.")
    else:
        st.info(f" **Status**: {verdict} ({severity} severity)")

    # ── Detailed Reasoning ──
    st.markdown("####  Reasoning behind alerts found")
    st.info(reasoning)

    st.write("---")
    confirmed = result.get("confirmed_conflicts", [])
    if confirmed:
        st.markdown('<div class="section-header" style="color:#DC2626; font-size:1.1rem; border:none; margin-bottom:5px;"> Verified Graph Conflicts</div>', unsafe_allow_html=True)
        for c in confirmed:
            st.error(f"**[{c.get('type')}] {c.get('drug')}** — {c.get('reason')}")

    unverified = result.get("unverified_flags", [])
    if unverified:
        st.markdown('<div class="section-header" style="color:#D97706; font-size:1.1rem; border:none; margin-bottom:5px;"> LLM Edge-Case Flags (Unverified)</div>', unsafe_allow_html=True)
        for c in unverified:
            st.warning(f"**[{c.get('type')}] {c.get('drug')}** — {c.get('reason')}")


# ==========================================
# MAIN APPLICATION INTERFACE
# ==========================================

def main(doctor_username=None):
    st.markdown('<div class="page-title">Clinical Knowledge Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Neuro-Symbolic Patient Knowledge Graph (N-PKG)</div>', unsafe_allow_html=True)

    # Top level navigation
    tab1, tab2 = st.tabs(["Patient Records Management", "Prescription Validation"])

    # ---------------------------------------------------------
    # TAB 1: PATIENT RECORDS MANAGEMENT
    # ---------------------------------------------------------
    with tab1:
        patient_mode = st.radio("Select Action:", ["View / Update Existing Patient", "Link New Patient"], horizontal=True, label_visibility="collapsed")
        st.write("---")

        # ── MODE: VIEW / UPDATE ──
        if patient_mode == "View / Update Existing Patient":
            if not doctor_username:
                st.error("Authentication required.")
                return
                
            patient_list = get_patient_list(doctor_username)
            
            if not patient_list:
                st.info("You don't have any patients linked to your account. Please 'Link New Patient' using their access key.")
            else:
                patient_usernames = [p["username"] for p in patient_list]
                
                # Check for patient switch to re-mask PII
                selected_patient_username = st.selectbox("Select Patient Record", options=patient_usernames)
                
                if "last_selected_patient" not in st.session_state or st.session_state.last_selected_patient != selected_patient_username:
                    st.session_state.last_selected_patient = selected_patient_username
                    st.session_state.pii_unlocked = False
                    # Don't rerun here immediately to avoid infinite loops, the next render will have pii_unlocked=False anyway.
                
                kg = KnowledgeGraphManager()
                # Pass accessed_by to trigger the Audit Log
                patient_data = kg.get_patient(selected_patient_username, by_username=True, accessed_by=doctor_username)
                kg.close()

                if patient_data:
                    render_patient_record(patient_data)
                    
                    # ── Sidebar NLP Pipeline ──
                    with st.sidebar:
                        st.markdown("---")
                        st.markdown("### Clinical Dictation")
                        st.write("Update patient record via NLP.")
                        
                        if st.button(" Start Recording", type="primary", use_container_width=True):
                            st.session_state["raw_transcript"] = transcribe_live()
                        
                        if "raw_transcript" in st.session_state and st.session_state["raw_transcript"]:
                            update_text = st.text_area("Clinical Notes", value=st.session_state["raw_transcript"], height=150)
                        else:
                            update_text = st.text_area("Clinical Notes", height=150, placeholder="e.g. Patient presents with new symptoms... prescribed new medication...", label_visibility="collapsed")
                        
                        if st.button("Submit & Process NLP", type="primary"):
                            if update_text.strip():
                                with st.spinner("Processing clinical note via NLP pipeline..."):
                                    new_data = process_clinical_text_to_json(update_text)
                                    if new_data:
                                        updated_patient_data = merge_patient_records(patient_data, new_data)
                                        updated_patient_data["patient_username"] = selected_patient_username
                                        
                                        kg = KnowledgeGraphManager()
                                        kg.store_patient(updated_patient_data)
                                        kg.close()
                                        
                                        if "raw_transcript" in st.session_state:
                                            del st.session_state["raw_transcript"]
                                            
                                        st.success("Patient record updated successfully!")
                                        st.rerun()
                            else:
                                st.warning("Please enter or dictate clinical notes before updating.")

        # ── MODE: LINK NEW PATIENT ──
        elif patient_mode == "Link New Patient":
            st.markdown("### Provide Patient Access Key")
            st.info("Ask your patient for their 6-character access key from their portal to gain access to their medical records.")
            
            with st.form("link_patient_form"):
                access_key = st.text_input("Patient Access Key", max_chars=10).strip()
                submit_link = st.form_submit_button("Link Patient")
                
                if submit_link:
                    if not access_key:
                        st.error("Please enter an access key.")
                    else:
                        kg = KnowledgeGraphManager()
                        success, message = kg.link_doctor_patient(doctor_username, access_key)
                        kg.close()
                        if success:
                            st.success(message)
                        else:
                            st.error(f"Failed to link patient: {message}")

    # ---------------------------------------------------------
    # TAB 2: PRESCRIPTION VALIDATION
    # ---------------------------------------------------------
    with tab2:
        st.write("Cross-check new prescriptions against patient history to prevent adverse drug events.")
        
        patient_list = get_patient_list(doctor_username) if doctor_username else []
        if not patient_list:
            st.info("You must link a patient before validating prescriptions.")
        else:
            patient_usernames = [p["username"] for p in patient_list]
            selected_rx_patient_username = st.selectbox("Select Patient to Validate Against", options=patient_usernames, key="rx_patient")
            
            st.write("---")
            
            st.markdown("**Dictate or Type Prescription:**")
            st.caption("You can dictate both the drug and the patient's new condition (e.g., 'Patient has asthma, prescribing propranolol').")
            col_rec, col_stat = st.columns([1, 4])
            with col_rec:
                if st.button("Record Prescription & Analyze", help="Click to start dictating"):
                    raw_audio_text = transcribe_live()
                    if raw_audio_text:
                        with st.spinner("Extracting medical terms via BioMistral NLP..."):
                            extracted_data = process_clinical_text_to_json(raw_audio_text)
                            if extracted_data:
                                meds = extracted_data.get("medications", [])
                                conds = extracted_data.get("diseases", [])
                                st.session_state["rx_drug"] = ", ".join(meds) if meds else raw_audio_text
                                st.session_state["rx_condition"] = ", ".join(conds)
                            else:
                                st.session_state["rx_drug"] = raw_audio_text
                                st.session_state["rx_condition"] = ""
            
            # Default value from state if it exists (from dictation)
            default_rx = st.session_state.get("rx_drug", "")
            if "rx_condition" in st.session_state and st.session_state["rx_condition"]:
                # If we have both from dictation, combine them
                default_rx = f"Condition: {st.session_state['rx_condition']}. Prescribing: {default_rx}"
            
            prescription_text = st.text_area("New Prescription", value=default_rx, height=100, placeholder="e.g. Patient has asthma, prescribing Propranolol")
            
            if st.button("Validate Prescription", type="primary"):
                if "rx_drug" in st.session_state:
                    del st.session_state["rx_drug"]
                    del st.session_state["rx_condition"]
                
                if prescription_text.strip():
                    with st.spinner("Analyzing prescription via NLP..."):
                        # Extract medications and conditions from the single text box
                        extracted_rx = process_clinical_text_to_json(prescription_text)
                        
                        kg = KnowledgeGraphManager()
                        patient_data = kg.get_patient(selected_rx_patient_username, by_username=True, accessed_by=doctor_username)
                        kg.close()
                        
                        if patient_data:
                            # 1. Add any newly detected conditions to the validation context
                            if extracted_rx:
                                new_conds = extracted_rx.get("diseases", [])
                                if new_conds:
                                    patient_data["diseases"] = list(set(patient_data.get("diseases", []) + new_conds))
                            
                            # 2. Identify the drug to validate
                            drugs = extracted_rx.get("medications", []) if extracted_rx else []
                            drug_to_validate = drugs[0] if drugs else prescription_text
                            
                            with st.spinner(f"Validating '{drug_to_validate}' against history..."):
                                validation_result = validate(patient_data, drug_to_validate)
                            render_validation_verdict(validation_result)
                        else:
                            st.error("Error retrieving patient data for validation.")
                else:
                    st.warning("Please enter a prescription.")

if __name__ == "__main__":
    main()
