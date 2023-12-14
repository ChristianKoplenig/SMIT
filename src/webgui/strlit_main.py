import streamlit as st
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
def load_smit() -> None:
    """Assign Smit attributes to session state.
    """
    #st.session_state['user'] = Application()
    dummy = Application(True)
    
    for key, value in vars(dummy).items():
        st.session_state[key] = value
load_smit()

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
