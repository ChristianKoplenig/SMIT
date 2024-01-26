import streamlit as st

# Custom modules
import st_auth.authenticate as stauth

authenticator = stauth.Authenticate(
    #preauthorization=True,
    cookie_name='streamlit-smit-app',
    key='cookey')

# Login form
if st.session_state['login_btn_clicked'] and not st.session_state['register_btn_clicked']:
    if not st.session_state['authentication_status']:
        authenticator.login('Login', 'main')

# Register user form
if st.session_state['register_btn_clicked'] and not st.session_state['login_btn_clicked']:
    try:
        authenticator.register_user('Register new user')
            #switch_page('home')

    except Exception as e:
        st.error(e)
# Login/Register button logic     
if st.session_state['authentication_status'] is None:
    st.write("# Please login or register")
    
    if st.button('Login', key='btn_login_register'):
        st.session_state['login_btn_clicked'] = True
        st.session_state['register_btn_clicked'] = False
        st.rerun()
        
    if st.button('Register', key='btn_register_register'):
        st.session_state['register_btn_clicked'] = True
        st.session_state['login_btn_clicked'] = False
        st.rerun()

## Logged in functionality
if st.session_state['authentication_status']:
    # Logout button
    authenticator.logout('Logout', 'main', key='btn_logout_register')
    
    # Reset password
    with st.expander('Reset Password'):
        try:
            if authenticator.reset_password('Enter new password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)
            st.stop()
    
    # Update user details
    with st.expander('Update user details'):
        
        try:
            if authenticator.update_user_details('Update user details'):
                st.success('User details modified successfully')
        
        except Exception as e:
            st.error(e)
            st.stop()
    
    # Delete user
    with st.expander('Delete user'):
        authenticator.delete_user('Confirm deletion')




################## old code ##################
# def create_credentials_dict(db_table: st.dataframe) -> dict:
#     """Create credentials dictionary from database.

#     Args:
#         db_auth (Database table): Iterable table with auth credentials.

#     Returns:
#         dict: Dictionary of credentials.
#     """
#     cred_dict = {}

#     for row in db_table.itertuples():
#         un = row.username
#         n = row.sng_username
#         p = row.password
#         em = row.email
        
#         # Append to dictionary
#         cred_dict.setdefault('usernames', {}).setdefault(un, {'email': em, 'name': n, 'password': p})
#     return cred_dict

# Initialize Authenticator
# @st.cache_resource
# def load_authenticator(auth_module: stauth.Authenticate) -> stauth.Authenticate:
#     """Cache backend init.
#     """
#     authenticator = auth_module(
#         'streamlit-smit-app',
#         'cookey')
#     return authenticator