import streamlit as st
from st_pages import show_pages_from_config, add_page_title

from smit.core import Application
from smit.st_api import SmitBackend

show_pages_from_config()

add_page_title('Smit Home') 

st.write("## Welcome to Smit")
st.markdown(
    """ 
    ### Smart Meter Interface Tool   
    Download and plot your power usage
"""
)

# Initiate Smit Instance
@st.cache_resource
def load_smit() -> Application:
    """Cache backend init.
    """
    #st.session_state['user'] = Application()
    dummy = Application(True)
    return dummy

@st.cache_resource
def load_backend() -> SmitBackend:
    """Cache backend init.
    """
    backend = SmitBackend()
    return backend

def session_init(backend) -> None:
    """Add backend to current session

    Args:
        backend (Application): Instantiation of backend class.
    """
    for key, value in vars(backend).items():
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
    st.session_state.auth_tbl = users_db.query('SELECT * FROM auth;')
    st.session_state.logger.debug('Auth table queried')

# Load backend
backend = load_backend()
session_init(backend)

# Connect to auth table 
connect_users_db()

# Logout button
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

def log_out_click() -> None:
    """Clear session state on logout.
    """
    st.session_state['authentication_status'] = None
    st.session_state['username'] = None
    st.session_state['name'] = None
    st.session_state['password'] = None
    st.session_state['email'] = None
    st.session_state.logger.info('User logged out')
    
if st.session_state['authentication_status']:
    st.sidebar.button('Logout', key='btn_logout_main', on_click=log_out_click)

# Logging
st.session_state.logger.debug('--- Streamlit initialized ---')