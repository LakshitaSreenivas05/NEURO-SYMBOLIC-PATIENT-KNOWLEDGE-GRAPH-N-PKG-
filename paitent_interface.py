import streamlit as st
import json
import re
from langchain_ollama import OllamaLLM
from neo4j_handler import KnowledgeGraphManager

# ==========================================
# PAGE CONFIG
# ==========================================
# st.set_page_config is handled in app.py

def dict_to_bullet_list(items):
    return "\n".join([f"- {item}" for item in items])

# ==========================================
# BioMistral — Generate Plain Language Summary
# ==========================================

def load_llm():
    # Switching to a smaller, highly optimized model that fits in 4GB VRAM
    return OllamaLLM(
        model="llama3.2", 
        temperature=0.1,
        format="json"
    )

def generate_patient_summary(patient_data):
    print("-> Calling Llama 3.2...")   
    llm = load_llm()
    print("-> LLM loaded!")             
    
    # ... keep your existing prompt exactly the same ...
    prompt = f"""<s>[INST]
Rewrite the following medical information in very simple, warm, easy-to-understand language.
Avoid medical jargon. Write as if explaining to someone with no medical knowledge.
Be reassuring and clear.

--- PATIENT MEDICAL DATA ---
Name        : {patient_data.get('patient_name')}
Age         : {patient_data.get('age')}
Gender      : {patient_data.get('gender')}
Conditions  : {patient_data.get('diseases', [])}
Medicines   : {patient_data.get('medications', [])}
Allergies   : {patient_data.get('allergies', [])}
Appointments: {patient_data.get('important_dates', [])}
Warnings    : {patient_data.get('warnings', [])}

Return ONLY this JSON and nothing else:
{{
    "greeting": "a warm one-sentence greeting using the patient's first name",
    "conditions_simple": [
        {{
            "condition": "original condition name",
            "explanation": "what this condition means in simple words (1-2 sentences)"
        }}
    ],
    "medicines_simple": [
        {{
            "name": "medicine name",
            "purpose": "what this medicine does in simple words",
            "instructions": "how and when to take it in simple words",
            "tip": "one helpful tip about this medicine"
        }}
    ],
    "allergies_simple": [
        {{
            "allergen": "what they are allergic to",
            "warning": "simple explanation of why to avoid it"
        }}
    ],
    "appointments_simple": ["list of appointments in plain language"],
    "warnings_simple": ["list of warnings rewritten in simple friendly language"],
    "general_advice": "2-3 sentences of warm general health advice for this patient"
}}
[/INST]</s>"""

    try:
        raw = llm.invoke(prompt)
        print("RAW LLM OUTPUT:", raw)  
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        st.error(f"LLM error: {e}")
        return None


# ==========================================
# RENDER FUNCTIONS
# ==========================================

def render_medicines(medications):
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"> Your Medications</div>', unsafe_allow_html=True)
    
    if not medications:
        st.write("_No active medications on record._")
    else:
        for med in medications:
            st.markdown(f"""
            <div style="background:#F0FDF4; border-left:5px solid #16A34A; border-radius:8px; padding:14px 18px; margin:8px 0;">
                <div style="font-size:1.1rem; font-weight:700; color:#16A34A;">{med.get('name', '').title()}</div>
                <div style="font-size:0.95rem; color:#475569; margin-top:4px;">{med.get('purpose', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_warnings(warnings):
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="color:#D97706;"> Clinical Warnings & Instructions</div>', unsafe_allow_html=True)
    
    if not warnings:
        st.write("No special warnings at this time. Continue taking your medication as prescribed.")
    else:
        for w in warnings:
            if "do not" in w.lower():
                st.markdown(f"""
                <div style="background:#FFFBEB; border-left:5px solid #D97706; border-radius:8px; padding:14px 18px; margin:8px 0; font-size:0.95rem; color:#1E293B;">
                    <strong> HIGH ALERT:</strong> {w}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#FFFBEB; border-left:5px solid #D97706; border-radius:8px; padding:14px 18px; margin:8px 0; font-size:0.95rem; color:#1E293B;">
                     {w}
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_allergies(allergies):
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="color:#DC2626;"> Allergies</div>', unsafe_allow_html=True)

    if not allergies:
        st.write("_No known allergies._")
        return

    for a in allergies:
        st.markdown(f"""
        <div style="background:#FEF2F2; border-left:5px solid #DC2626; border-radius:8px; padding:14px 18px; margin:8px 0; font-size:0.95rem; color:#444;">
            <strong> {a.get('allergen', '')}</strong><br>
            {a.get('warning', '')}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_appointments(appointments):
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="color:#2563EB;"> Upcoming Appointments</div>', unsafe_allow_html=True)

    if not appointments:
        st.write("_No upcoming appointments._")
        return

    for appt in appointments:
        st.markdown(f"""
        <div style="background:#EFF6FF; border-left:5px solid #2563EB; border-radius:8px; padding:14px 18px; margin:8px 0; font-size:0.95rem; color:#1E3A8A; font-weight:600;">
             {appt}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_conditions(conditions):
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="color:#475569;"> Health Conditions</div>', unsafe_allow_html=True)
    
    if not conditions:
        st.write("_No active health conditions._")
    else:
        for cond in conditions:
            st.markdown(f"""
            <div style="background:#F1F5F9; border-left:5px solid #64748B; border-radius:8px; padding:12px 18px; margin:8px 0; font-size:0.95rem; color:#334155;">
                <strong> {cond.get('condition', '').title()}</strong><br>
                {cond.get('explanation', '')}
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# MAIN APP
# ==========================================

def main(patient_username=None):

    # Header
    st.markdown('<div class="page-title"> Your Health Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">A simple, easy-to-read view of your medical record.</div>', unsafe_allow_html=True)
    st.write("---")

    # Sidebar
    with st.sidebar:
        st.markdown("###  Patient Portal")
        st.markdown("""
        This summary has been prepared by your doctor.

        It explains:
        - Your health conditions in simple words
        - Your medicines and how to take them
        - Things you are allergic to
        - Your next appointment
        - Important reminders

        ---
        If you have any questions, please ask your doctor or pharmacist.
        """)

        st.markdown("---")
        st.markdown("###  Emergency")
        st.error("If you feel unwell after taking any medicine — **call your doctor immediately**")

    # ── Generate Summary ─────────────────────────────────────────
    if patient_username:
        kg = KnowledgeGraphManager()
        patient_data = kg.get_patient(patient_username, by_username=True)
        kg.close()

        if not patient_data:
            st.error(f"Sorry, we couldn't find a summary for your account. Please consult your doctor to add your record.")
            return
            
        patient_name = patient_data.get('patient_name', patient_username)
        access_key = patient_data.get('access_key', 'Not Generated')

        st.info(f"**Your Access Key:** `{access_key}`  \nShare this key with your doctor so they can access your record.")

        # Generate button
        if st.button(" Show My Health Summary", type="primary", use_container_width=True):
            with st.spinner("Preparing your personalised health summary..."):
                summary = generate_patient_summary(patient_data)

            if not summary:
                st.error("Sorry, we couldn't generate your summary right now. Please try again.")
                return

            # ── Greeting ─────────────────────────────────────────
            st.markdown("---")
            greeting = summary.get("greeting", f"Hello {patient_name}!")
            st.markdown(f"""
            <div style="text-align:center; padding: 10px 0 20px 0;">
                <div class="patient-badge"> {patient_name}</div>
                <p style="font-size:1.15rem; color:#333; margin-top:10px;">
                    {greeting}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # ── Conditions ────────────────────────────────────────
            render_conditions(summary.get("conditions_simple", []))

            # ── Medicines ─────────────────────────────────────────
            render_medicines(summary.get("medicines_simple", []))

            # ── Warnings ─────────────────────────────────────────
            render_warnings(summary.get("warnings_simple", []))

            # ── Allergies ─────────────────────────────────────────
            render_allergies(summary.get("allergies_simple", []))

            # ── Appointments ──────────────────────────────────────
            render_appointments(summary.get("appointments_simple", []))

            # ── General Advice ────────────────────────────────────
            advice = summary.get("general_advice", "")
            if advice:
                st.markdown(f"""
                <div class="tip-box">
                     <strong>A note from your care team:</strong><br>
                    {advice}
                </div>
                """, unsafe_allow_html=True)

            # ── Footer ────────────────────────────────────────────
            st.markdown("---")
            st.markdown("""
            <p style="text-align:center; color:#888; font-size:0.85rem;">
                This summary was generated by N-PKG — Neuro-Symbolic Patient Knowledge Graph.<br>
                Always follow your doctor's advice. If you have questions, ask your pharmacist.
            </p>
            """, unsafe_allow_html=True)

    else:
        # Landing state
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#888;">
            <div style="font-size:4rem;"></div>
            <p style="font-size:1.1rem; margin-top:16px;">
                You must be logged in as a patient to view your summary.
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()