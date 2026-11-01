import streamlit as st
import requests
from firebase_admin import auth as firebase_auth
import firebase_config


def logout():
    st.session_state["authenticated"] = False
    st.session_state["admin_email"] = ""
    st.session_state["id_token"] = ""
    st.rerun()


def require_auth():

    # Get the authorised admin UID from secrets
    admin_uid = st.secrets["firebase"]["admin_uid"]

    # Check whether an existing session is valid
    if st.session_state.get("authenticated", False):

        id_token = st.session_state.get("id_token", "")

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            logged_in_uid = decoded_token.get("uid")

            if logged_in_uid != admin_uid:
                logout()

            st.sidebar.success(
                f"Logged in: {st.session_state.get('admin_email', '')}"
            )

            if st.sidebar.button(
                "🚪 Logout",
                use_container_width=True
            ):
                logout()

            return True

        except Exception:
            st.session_state["authenticated"] = False
            st.session_state["admin_email"] = ""
            st.session_state["id_token"] = ""

            st.warning(
                "Your login session has expired or is invalid. "
                "Please log in again."
            )

    # Login screen
    st.markdown(
        """
        <div style="
            text-align:center;
            padding:35px;
            border-radius:18px;
            background:linear-gradient(120deg,#17152f,#29205c,#153b65);
            border:1px solid rgba(160,140,255,0.3);
        ">
            <h1 style="color:white;">🔐 Attendify Admin Login</h1>
            <p style="color:#c9c5e8;">
                Sign in to manage student attendance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    _, login_col, _ = st.columns([1, 1.5, 1])

    with login_col:

        with st.form("admin_login_form"):

            email = st.text_input(
                "Admin Email",
                placeholder="Enter your admin email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if submitted:

            if not email or not password:
                st.warning("Please enter both email and password.")

            else:
                try:
                    api_key = st.secrets["firebase"]["apiKey"]

                    url = (
                        "https://identitytoolkit.googleapis.com/v1/"
                        "accounts:signInWithPassword"
                        f"?key={api_key}"
                    )

                    response = requests.post(
                        url,
                        json={
                            "email": email,
                            "password": password,
                            "returnSecureToken": True
                        },
                        timeout=20
                    )

                    result = response.json()

                    if response.status_code == 200:

                        # Confirm this is the authorised admin
                        if result.get("localId") != admin_uid:
                            st.error(
                                "Access denied. This account is not "
                                "authorised as the Attendify administrator."
                            )
                            return False

                        # Verify the Firebase ID token on the server
                        decoded_token = firebase_auth.verify_id_token(
                            result["idToken"]
                        )

                        if decoded_token.get("uid") != admin_uid:
                            st.error("Admin verification failed.")
                            return False

                        st.session_state["authenticated"] = True
                        st.session_state["admin_email"] = result.get(
                            "email", email
                        )
                        st.session_state["id_token"] = result["idToken"]

                        st.success("Login successful!")
                        st.rerun()

                    else:
                        error_message = result.get(
                            "error", {}
                        ).get("message", "UNKNOWN_ERROR")

                        st.error(f"Firebase Error: {error_message}")

                except Exception:
                    st.error(
                        "Unable to verify your login. Please check "
                        "your Firebase configuration and try again."
                    )

    return False