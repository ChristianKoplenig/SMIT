import streamlit as st

# if not loaded; instantiate smit

st.write(
    "### Backend instantiated with user:",
    st.session_state.Login['username']) 

st.write(
    "**Attributes**"
)

st.write(
    st.session_state
)