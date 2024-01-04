import streamlit as st

# from webgui.strlit_main import load_smit

# if 'Login' not in st.session_state:
#     load_smit()

st.write(
    "### Backend instantiated with user:",
    st.session_state.Login['username']) 

st.write(
    "**Attributes**"
)

st.write(
    st.session_state
)
# st.write('User: ', st.session_state.Login['username'])

# app = st.session_state

# st.write('app:', app.Login)