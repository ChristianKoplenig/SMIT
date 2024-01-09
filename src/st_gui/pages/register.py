import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Custom modules
import st_auth.authenticate as stauth
from db.smit_db import write_user_to_db

def create_credentials_dict(db_table: st.dataframe) -> dict:
    """Create credentials dictionary from database.

    Args:
        db_auth (Database table): Iterable table with auth credentials.

    Returns:
        dict: Dictionary of credentials.
    """
    cred_dict = {}

    for row in db_table.itertuples():
        un = row.username
        n = row.sng_username
        p = row.password
        em = row.email
        
        # Append to dictionary
        cred_dict.setdefault('usernames', {}).setdefault(un, {'email': em, 'name': n, 'password': p})
    return cred_dict

# Initialize Authenticator
authenticator = stauth.Authenticate(
        create_credentials_dict(st.session_state.auth_tbl),
        'st_dummy_cookie',
        'cookey',
    )

# Register user form
try:
    if authenticator.register_user('Register new user', preauthorization=False):
        write_user_to_db(st.session_state.username, st.session_state.password)
        switch_page('home')

except Exception as e:
    st.error(e)