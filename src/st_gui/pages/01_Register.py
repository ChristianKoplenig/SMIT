import streamlit as st
from st_gui.st_main import init_authenticator

try:
    while st.session_state.authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
        # st.session_state.authenticator = init_authenticator()
        st.write(f'Welcome *{st.session_state["name"]}*')


except Exception as e:
    st.error(e)

# if st.session_state["authentication_status"]:
#     st.session_state.authenticator.logout('Logout', 'sidebar', key='unique_key')
#     st.title('Some content')
#username = st.session_state['username']
#st.write(f'Welcome *{st.session_state["name"]}*')
# st.session_state.users_db.query(f'INSERT INTO auth (username) VALUES ("{username}");')

# st.session_state.authenticator.login('Login', 'main')
