import streamlit as st

from webgui.strlit_main import load_smit

if 'Login' not in st.session_state:
    load_smit()

st.write(st.session_state.Login['username']) 

st.write('User: ', st.session_state.Login['username'])

app = st.session_state

st.write('app:', app.Login)