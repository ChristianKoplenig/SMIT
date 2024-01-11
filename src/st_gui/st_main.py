import streamlit as st
from st_pages import show_pages_from_config
from streamlit_extras.switch_page_button import switch_page

#from smit.core import Application
from smit.st_api import SmitBackend

show_pages_from_config()

# Session state variable initialization
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

st.session_state['login_btn_clicked'] = False
st.session_state['register_btn_clicked'] = False

# Say hello
st.markdown(
    """ 
    # Smart Meter Interface Tool   
    ### Download and plot your power usage
    ---
    """)
if st.session_state['authentication_status']:
    st.write(f'## Hello {st.session_state["username"]}!')
else:
    st.markdown(
        """
        ### Please login or register to continue
        """)

# Initiate Smit Instance
# @st.cache_resource
# def load_smit() -> Application:
#     """Cache backend init.
#     """
#     #st.session_state['user'] = Application()
#     dummy = Application(True)
#     return dummy

@st.cache_resource
def load_backend() -> SmitBackend:
    """Cache backend init.
    """
    smit_core = SmitBackend()
    return smit_core

def session_init(smit_core) -> None:
    """Add backend to current session

    Args:
        backend (Application): Instantiation of backend class.
    """
    for key, value in vars(smit_core).items():
        st.session_state[key] = value
    
    st.session_state.logger.debug('Streamlit session state init')


# Connect to fly.io smit database
# Add table with user data to session state
@st.cache_resource
def connect_users_db() -> None:
    """Fetch userdata from database.
    """
    # Database connection
    users_db = st.connection('flyio', type='sql')
    st.session_state.logger.debug('Connected to fly.io database')
    
    # Query database for authentication table
    st.session_state.auth_tbl = users_db.query('SELECT * FROM auth_dev;')
    st.session_state.logger.debug('Auth table queried')

# Load backend
backend = load_backend()
session_init(backend)

# Connect to auth table 
connect_users_db()

# Entry buttons    
if not st.session_state['authentication_status']:
    
    if st.button('Login', key='btn_login_main'):
        st.session_state['login_btn_clicked'] = True
        switch_page('user management')
        
    if st.button('Register', key='btn_register_main'):
        st.session_state['register_btn_clicked'] = True
        switch_page('user management')

# Logging
st.session_state.logger.debug('--- Streamlit initialized ---')