"""
Authentication and Role-based Session Management
Handles credentials verification, role permissions, and session lifecycle.
"""
import streamlit as st

# Hardcoded credentials as specified in system requirements
USERS = {
    "admin": {
        "password": "Akshay123",
        "role": "Admin",
        "name": "Akshay Sojitra",
        "title": "School Administrator / Principal"
    },
    "teacher": {
        "password": "teacher123",
        "role": "Teacher",
        "name": "Prof. Sharma",
        "title": "Senior Faculty & Class Teacher"
    }
}

def init_session():
    """Initialize essential session state parameters."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "full_name" not in st.session_state:
        st.session_state.full_name = None
    if "title" not in st.session_state:
        st.session_state.title = None

def login(username, password):
    """Authenticate credentials against stored accounts."""
    init_session()
    user_info = USERS.get(username.strip().lower())
    if user_info and user_info["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username.strip().lower()
        st.session_state.role = user_info["role"]
        st.session_state.full_name = user_info["name"]
        st.session_state.title = user_info["title"]
        return True, "Login successful!"
    return False, "Invalid username or password. Please try again."

def logout():
    """Clear session data and redirect to login state."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.full_name = None
    st.session_state.title = None
    st.rerun()

def is_admin():
    """Check if current session user has Administrator privileges."""
    return st.session_state.get("role") == "Admin"

def check_authentication():
    """
    Gatekeeper function to ensure pages are accessed only after logging in.
    Returns True if logged in, otherwise displays an authentication gate banner and stops execution.
    """
    init_session()
    if not st.session_state.get("logged_in", False):
        st.set_page_config(page_title="Access Restricted | Student Analytics", page_icon="🔒", layout="wide")
        st.warning("🔒 **Authentication Required**: Please log in through the Home page to access this system.")
        st.info("👈 Navigate to the **Home** (Main app) in the sidebar to log in with your credentials.")
        
        # Quick inline login fallback
        with st.expander("🔑 Quick Login from Current Page", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                u = st.text_input("Username", key="inline_user", placeholder="admin or teacher")
            with col2:
                p = st.text_input("Password", type="password", key="inline_pwd", placeholder="admin123 or teacher123")
            
            if st.button("Log In Now", type="primary", use_container_width=True):
                success, msg = login(u, p)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
            st.caption("Default Demo Accounts: `admin` / `admin123` (Admin) | `teacher` / `teacher123` (Teacher)")
        return False
    return True

def render_sidebar_auth():
    """Render user profile and logout controls in the Streamlit sidebar."""
    init_session()
    with st.sidebar:
        if st.session_state.get("logged_in", False):
            st.divider()
            role_badge = "🛡️ ADMIN" if is_admin() else "🧑‍🏫 TEACHER"
            st.markdown(f"### Current Session")
            st.markdown(f"**{st.session_state.get('full_name')}**")
            st.markdown(f"`{role_badge}` • *{st.session_state.get('title')}*")
            
            if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
                logout()
            st.divider()
