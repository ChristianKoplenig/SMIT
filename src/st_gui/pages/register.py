import streamlit as st
from streamlit_extras.switch_page_button import switch_page
#import extra_streamlit_components as stx

# Custom modules
import st_auth.authenticate as stauth
from db.smitdb import SmitDb
from db.auth_schema import AuthDbSchema

# st.set_page_config(
#     page_title='User Management'
# )

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
email_addresses = ['a@b.com', 'b@a.com']

authenticator = stauth.Authenticate(
    cookie_name='streamlit-smit-app',
    key='cookey',
    preauthorized=email_addresses)

# Login form
if st.session_state['login_btn_clicked'] and not st.session_state['register_btn_clicked']:
    if not st.session_state['authentication_status']:
        authenticator.login('Login', 'main')

# Register user form
if st.session_state['register_btn_clicked'] and not st.session_state['login_btn_clicked']:
    try:
        if authenticator.register_user('Register new user'):
            # SmitDb(AuthDbSchema).create_user(st.session_state.username,
            #                              st.session_state.password)
            switch_page('home')

    except Exception as e:
        st.error(e)
        
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
            if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                st.success('Password modified successfully')
                st.write('Database update not implemented yet')
        except Exception as e:
            st.error(e)
    
    # Update user details
    with st.expander('Update user details'):
        try:
            if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
                st.success('User details modified successfully')
                st.write('Database update not implemented yet')
        except Exception as e:
            st.error(e)
    
    # Delete user
    with st.expander('Delete user'):
        st.write('Implementation needed')
        
        # Create form
        del_user = st.form('DeleteUser')
        del_user.subheader('Delete user')
        
        if st.session_state['username'] == del_user.text_input('Username'):
            uid = st.session_state['username']
            st.write('Logout and delete user from database')
            
            # Delete user from database
            SmitDb(AuthDbSchema).delete_where(AuthDbSchema.username, uid)

            # Delete user from session state
            #stx.CookieManager().delete('streamlit-smit-app', 'cookey', key='del_user_cookie')
            st.session_state['logout'] = True
            st.session_state['name'] = None
            st.session_state['username'] = None
            st.session_state['authentication_status'] = None
            del st.session_state['init']
            #del st.session_state['password']
            #del st.session_state['email']
            
            switch_page('home') 
        else:
            st.error('Username does not match')
        
        del_user.form_submit_button('Delete user')
