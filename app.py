import pickle
from pathlib import Path

import streamlit as st

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