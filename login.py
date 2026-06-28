import streamlit as st

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    if not st.session_state.logged_in:

        st.title("🌾 Smart Paddy AI")

        username = st.text_input("Username (Admin only)")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Admin Login"):

                if username == "dharshu" and password == "admin123":

                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Invalid Admin Credentials")

        with col2:
            if st.button("Continue as User"):

                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.session_state.username = "Guest"
                st.rerun()

        st.stop()
