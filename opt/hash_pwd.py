from streamlit_authenticator import Hasher as sta_hasher
dpwd = sta_hasher(['dummy_pwd']).generate()

print(dpwd[0])