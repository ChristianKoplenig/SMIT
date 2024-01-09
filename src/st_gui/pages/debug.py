import streamlit as st

if 'username' in st.session_state:
    st.write(f"# username: {st.session_state['username']}")


st.write(f"# auth stat: {st.session_state['authentication_status']}")

st.write('## Session state')
for key, value in st.session_state.items():
    st.write(f'{key}: {value}')