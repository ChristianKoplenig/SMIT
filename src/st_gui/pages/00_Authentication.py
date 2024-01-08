import streamlit as st

# Authenticate user
def authenticate_user():
    """_summary_
    """
    if st.session_state["authentication_status"]:
        st.session_state.authenticator.logout('Logout', 'sidebar', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

# Load Login Frame
st.session_state.authenticator.login('Login', 'main')

authenticate_user()