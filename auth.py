# auth.py – Google Sign-In + Admin Approval System for Streamlit

import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import os
from yaml.loader import SafeLoader

# Load Streamlit Auth config (admin login)
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Render login widget
name, authentication_status, username = authenticator.login(
    "Login", "main")

# Load or create users.json
USER_DB = "users.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

with open(USER_DB, "r") as f:
    users = json.load(f)

# Admin username from config.yaml
ADMIN_EMAIL = list(config['credentials']['usernames'].keys())[0]

# On successful login
if authentication_status:
    if username == ADMIN_EMAIL:
        st.success(f"Welcome Admin {name} 👑")
        st.subheader("User Approval Panel")

        pending = {k: v for k, v in users.items() if v == "pending"}
        approved = {k: v for k, v in users.items() if v == "approved"}

        st.write("### Pending Users")
        for user in pending:
            col1, col2 = st.columns(2)
            with col1:
                st.write(user)
            with col2:
                if st.button(f"Approve {user}"):
                    users[user] = "approved"
                    st.experimental_rerun()

        st.write("### Approved Users")
        for user in approved:
            st.write(f"✅ {user}")

        with open(USER_DB, "w") as f:
            json.dump(users, f)

    else:
        # Normal user login
        status = users.get(username, "pending")
        if status == "approved":
            st.success(f"Welcome {name} ✨")
            st.session_state.user_email = username
            st.session_state.user_name = name
        elif status == "pending":
            st.error("Your access is pending admin approval.")
        else:
            st.error("Access denied.")

# New user signup flow
elif authentication_status is False:
    st.error("Incorrect username or password.")
elif authentication_status is None:
    st.warning("Please enter your credentials.")
