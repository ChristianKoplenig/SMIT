import streamlit as st
from authentication.auth_api import AuthApi
from db.models import AuthModel, ConfigSchema

# from st_pages import show_pages_from_config
# from streamlit_extras.switch_page_button import switch_page
# Database import
from db.smitdb import SmitDb

# Api import
from utils.logger import Logger

# show_pages_from_config()

# Initiate session state
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

st.session_state["login_btn_clicked"] = False
st.session_state["register_btn_clicked"] = False


# Connect SmitApi to session state
@st.cache_resource(ttl=600)
def smit_init() -> None:
    """Init backend api."""
    st.session_state.smit_api = Logger()
    st.session_state.smit_api.logger.info("Smit api added to session state")


# Add table connections to session state
@st.cache_resource(ttl=600)
def connect_db() -> None:
    """Connect database tables."""
    # Database connection
    st.session_state.auth_connection = SmitDb(AuthModel)
    st.session_state.config_connection = SmitDb(ConfigSchema)
    st.session_state.smit_api.logger.info(
        "All table connections added to session state"
    )


# Connect AuthApi to session state
@st.cache_resource(ttl=600)
def auth_init() -> None:
    """Init authentication api."""
    st.session_state.auth_api = AuthApi()
    st.session_state.smit_api.logger.info("Auth api added to session state")


smit_init()
connect_db()
auth_init()

# Say hello
st.markdown(
    """ 
    # Smart Meter Interface Tool   
    ### Download and plot your power usage
    ---
    """
)
if st.session_state["authentication_status"]:
    st.write(f'## Hello {st.session_state["username"]}!')
else:
    st.markdown(
        """
        ### Please login or register to continue
        """
    )

# Entry buttons
if not st.session_state["authentication_status"]:
    if st.button("Login", key="btn_login_main"):
        st.session_state["login_btn_clicked"] = True
        # switch_page('user management')
        st.switch_page("pages/register.py")

    if st.button("Register", key="btn_register_main"):
        st.session_state["register_btn_clicked"] = True
        # switch_page('user management')
        st.switch_page("register")

# Logging
st.session_state.smit_api.logger.debug("--- Streamlit initialized ---")


############# old code #############
# Initiate Smit Instance
# @st.cache_resource
# def load_smit() -> Application:
#     """Cache backend init.
#     """
#     #st.session_state['user'] = Application()
#     dummy = Application(True)
#     return dummy

# @st.cache_resource
# def load_backend() -> SmitBackend:
#     """Cache backend init.
#     """
#     smit_core = SmitBackend()
#     return smit_core


# Add table with user data to session state

# @st.cache_resource
# def connect_users_db() -> None:
#     """Fetch userdata from database.
#     """
#     # Database connection
#     users_db = st.connection('flyio', type='sql')
#     st.session_state.logger.debug('Connected to fly.io database')

#     # Query database for authentication table
#     st.session_state.auth_tbl = users_db.query('SELECT * FROM auth_dev;')
#     st.session_state.logger.debug('Auth table queried')


# # Connect to auth table
# connect_users_db()
