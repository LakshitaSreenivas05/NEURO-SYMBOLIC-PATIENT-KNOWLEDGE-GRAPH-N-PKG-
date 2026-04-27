import streamlit as st

st.set_page_config(
    page_title="N-PKG Portal",
    page_icon="",
    layout="wide"
)

# ==========================================
# GLOBAL STYLES
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"], [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .modern-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 28px;
        margin: 16px 0;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
    }
    
    .page-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
        text-align: center;
    }
    
    .page-subtitle {
        font-size: 1.125rem;
        color: #64748B;
        margin-bottom: 32px;
        text-align: center;
    }

    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1E293B;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    
    .patient-badge {
        display: inline-block;
        background: #E0E7FF;
        color: #4F46E5;
        font-weight: 600;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTH & SESSION MANAGEMENT
# ==========================================
from auth import init_session_state, check_timeout, refresh_activity, logout, render_login_page
from neo4j_handler import KnowledgeGraphManager

# Initialize all session state variables (runs only once)
init_session_state()

# Connect to Neo4j
kg = KnowledgeGraphManager()

# ── Security Gate: check for session expiry ──
check_timeout()

# ==========================================
# ROUTING
# ==========================================
if not st.session_state.logged_in:
    # Unauthenticated — show login page only
    render_login_page(kg)
else:
    # Authenticated — refresh activity timer
    refresh_activity()

    # Sidebar: user info + logout
    with st.sidebar:
        st.markdown(f"### Logged in as: {st.session_state.name}")
        st.markdown(f"Role: **{st.session_state.role.capitalize()}**")
        if st.session_state.role == "patient" and st.session_state.access_key:
            st.markdown(f"Access Key: **`{st.session_state.access_key}`**")
        st.button("Logout", on_click=logout, use_container_width=True)

    # ── Strict View Isolation ──
    # Dashboard modules are imported ONLY inside authenticated blocks.
    # An unauthenticated session never loads this code into memory.
    if st.session_state.role == "doctor":
        import doctor_view
        doctor_view.main(st.session_state.username)
    elif st.session_state.role == "patient":
        import paitent_interface
        paitent_interface.main(st.session_state.username)

# Cleanup
kg.close()
