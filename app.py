import pickle
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    home_page = st.Page(
        "views/home.py",
        title="Home",
        icon='🏠',
        #icon=":material/account_circle:",
        default=True,
    )
    info_page = st.Page(
        "views/info.py",
        title="Information",
        icon="📄",
    )
    file_upload_page = st.Page(
        "views/file_upload.py",
        title="Upload Files",
        icon="📂",
    )
    analysis_page = st.Page(
        "views/analysis.py",
        title="Analysis",
        icon="📊",
    )


    pg = st.navigation(
        {
            "Main": [home_page,info_page],
            "Answer Script Analysis": [file_upload_page, analysis_page],
        }
    )


# --- RUN NAVIGATION ---
    pg.run()