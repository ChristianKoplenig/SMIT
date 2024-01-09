import streamlit as st
#from pydantic import BaseModel
import streamlit_pydantic as sp

from db.auth_schema import SmitAuth

data = sp.pydantic_form(key="my_form", model=SmitAuth)
if data:
    st.json(data.json())