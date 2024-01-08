import streamlit as st
import streamlit_authenticator as stauth

from smit.core import Application

st.set_page_config(
    page_title="Smit",
)

st.write("# Welcome to Smit")
st.markdown(
    """ 
    ## Smart Meter Interface Tool   
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

def session_init(backend) -> None:
    """Add backend to current session

    Args:
        backend (Application): Instantiation of backend class.
    """
    for key, value in vars(backend).items():
        st.session_state[key] = value
    
    st.session_state.logger.debug('Streamlit session state init')


# Connect to fly.io smit database
# Use auth table
@st.cache_resource
def connect_users_db() -> None:
    """Connect to fly.io smit database.
    """
    # Database connection
    users_db = st.connection('flyio', type='sql')
    st.session_state.logger.debug('Connected to fly.io database')
    return users_db



######################
# Authenticator credentials dictionary
def create_credentials_dict(db_auth: st.connection) -> dict:
    """Create credentials dictionary from database.

    Args:
        db_auth (st.connection): Database connection.

    Returns:
        dict: Dictionary of credentials.
    """
    cred_dict = {}

    for row in db_auth.itertuples():
        un = row.username
        n = row.sng_username
        p = row.password
        em = row.email
        
        # Append to dictionary
        cred_dict.setdefault('usernames', {}).setdefault(un, {'email': em, 'name': n, 'password': p})
    return cred_dict

# Initialize Authenticator
def init_authenticator()  -> stauth.Authenticate:
    """Initialize authenticator instance.

    Args:
        db_auth (st.connection): Database connection.

    Returns:
        stauth.Authenticate: Authenticator instance.
    """
    db_auth = st.session_state.users_db.query('SELECT * FROM auth;', ttl="10m")
    authenticator = stauth.Authenticate(
        create_credentials_dict(db_auth),
        'st_dummy_cookie',
        'cookey',
    )
    return authenticator


######################

# Load backend
dummy = load_smit()
session_init(dummy)

# Connect to auth table 
st.session_state.users_db = connect_users_db()

# Load authenticator instance
#st.session_state.authenticator = init_authenticator()

# Logging
st.session_state.logger.debug('--- Streamlit initialized ---')

## Readme ##
# Get path for Readme file
# current_folder = Path(__file__)
# project_root = current_folder.parent.parent.parent
# readme = project_root / 'README.md'
# # Read markdown file 
# def read_markdown_file(markdown_file):
#     return Path(markdown_file).read_text()
# # Print page
# intro_markdown = read_markdown_file(readme)
# st.markdown(intro_markdown, unsafe_allow_html=True)

#st.sidebar.success("Page")
