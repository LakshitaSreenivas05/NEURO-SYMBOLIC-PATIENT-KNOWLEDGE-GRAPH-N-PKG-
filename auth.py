import streamlit as st
import time

# ==========================================
# CONSTANTS
# ==========================================
SESSION_TIMEOUT = 900  # 15 minutes in seconds


# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================

def init_session_state():
    """Initialize all session state variables with safe defaults.
    Called once at startup before any UI is rendered."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.name = None
        st.session_state.access_key = None
        st.session_state.last_active = None
        st.session_state.pii_unlocked = False


def check_timeout():
    """Check if the current session has exceeded the inactivity timeout.
    If expired, clear session state and show a warning."""
    if st.session_state.logged_in and st.session_state.last_active is not None:
        elapsed = time.time() - st.session_state.last_active
        if elapsed > SESSION_TIMEOUT:
            # Session expired — clear everything
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.name = None
            st.session_state.access_key = None
            st.session_state.last_active = None
            st.session_state.pii_unlocked = False
            st.warning(" Your session has expired due to 15 minutes of inactivity. Please sign in again.")


def refresh_activity():
    """Update the last activity timestamp. Called at the top of every
    authenticated render cycle to keep the session alive."""
    st.session_state.last_active = time.time()


def logout():
    """Clear all session state variables and force a rerun."""
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.name = None
    st.session_state.access_key = None
    st.session_state.last_active = None
    st.session_state.pii_unlocked = False
    st.rerun()


# ==========================================
# LOGIN / SIGNUP UI
# ==========================================

def render_login_page(kg):
    """Render the authentication page with Sign In and Sign Up tabs.
    
    Args:
        kg: An active KnowledgeGraphManager instance for auth queries.
    """
    st.markdown("<div class='page-title'>Welcome to N-PKG</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Neuro-Symbolic Patient Knowledge Graph Portal</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs([" Sign In", " Sign Up"])

        # ── Sign In ──
        with tab1:
            st.markdown("<div class='section-header'>Login to your account</div>", unsafe_allow_html=True)
            with st.form("login_form"):
                role = st.selectbox("I am a:", ["Doctor", "Patient"])
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                submit = st.form_submit_button("Sign In", type="primary")
                if submit:
                    if not username or not password:
                        st.error("Please fill in both username and password")
                    else:
                        user_data, error = kg.authenticate_user(role.lower(), username, password)
                        if error:
                            st.error(error)
                        else:
                            st.session_state.logged_in = True
                            st.session_state.role = user_data["role"]
                            st.session_state.username = user_data["username"]
                            st.session_state.name = user_data["name"]
                            st.session_state.last_active = time.time()
                            st.session_state.pii_unlocked = False
                            if "access_key" in user_data:
                                st.session_state.access_key = user_data["access_key"]
                            st.success(f"Welcome back, {st.session_state.name}!")
                            st.rerun()

        # ── Sign Up ──
        with tab2:
            st.markdown("<div class='section-header'>Create a new account</div>", unsafe_allow_html=True)
            with st.form("signup_form"):
                new_role = st.selectbox("I am a:", ["Doctor", "Patient"])
                new_name = st.text_input("Full Name")
                new_username = st.text_input("Choose a Username")
                new_password = st.text_input("Choose a Password", type="password")

                submit_signup = st.form_submit_button("Sign Up", type="primary")
                if submit_signup:
                    if not new_name or not new_username or not new_password:
                        st.error("Please fill in all fields")
                    else:
                        success, message_or_key = kg.register_user(new_role.lower(), new_username, new_password, new_name)
                        if not success:
                            st.error(f"Registration failed: {message_or_key}")
                        else:
                            st.success("Account created successfully! You can now sign in.")
                            if new_role == "patient":
                                st.info(f"**IMPORTANT: Your Access Key is `{message_or_key}`.** Share this with your doctor so they can access your record.")
