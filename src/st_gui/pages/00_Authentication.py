import streamlit as st
import streamlit_authenticator as stauth

# Database connection
st.write('# * from auth')
conn = st.connection('flyio', type='sql')
db_auth = conn.query('SELECT * FROM auth;', ttl="10m")

# Authenticator credentials dictionary
cred_dict = {}

for row in db_auth.itertuples():
    un = row.username
    n = row.sng_username
    p = row.password
    em = row.email
    
    # Append to dictionary
    cred_dict.setdefault('usernames', {}).setdefault(un, {'email': em, 'name': n, 'password': p})


for key, value in cred_dict.items():
    st.write(f'{key}: {value}')
    
# Initialize Authenticator
authenticator = stauth.Authenticate(
    cred_dict,
    'st_dummy_cookie',
    'cookey',
)
# Load Login Frame
authenticator.login('Login', 'main')

# Debug
st.session_state.logger.debug(f'S_AuthenticationStatus: {st.session_state["authentication_status"]}')
st.session_state.logger.debug(f'S_Name: {st.session_state["name"]}')

# Authenticate user
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
