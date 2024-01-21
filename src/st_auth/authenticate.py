from datetime import datetime, timedelta
import bcrypt
import jwt
import bcrypt
import pydantic
import streamlit as st
import extra_streamlit_components as stx

from st_auth.hasher import Hasher
#from .validator import Validator
#from .utils import generate_random_pw

#from .exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError

#import json

#### Pydantic
from db.auth_schema import AuthDbSchema
from st_auth.auth_api import AuthModel

#### Database
from db.smitdb import SmitDb

class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot username, and modify user details widgets.
    """
    def __init__(self,
                 #credentials: dict,
                 cookie_name: str,
                 key: str,
                 cookie_expiry_days: float=30.0,
                 preauthorization: bool = False,
                 #validator: Validator=None
                 ) -> None:
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        credentials: dict
            The dictionary of all attributes defined in the authentication schema, grouped by user id.
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        validator: Validator
            A Validator object that checks the validity of the username, name, and email fields.
        """
        #self.credentials = credentials
        #self.credentials['usernames'] = {key.lower(): value for key, value in credentials['usernames'].items()}
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        #self.preauthorized = preauthorized
        self.cookie_manager = stx.CookieManager()
        #self.validator = validator if validator is not None else Validator()
        
        # Get list with preauthorized mail adresses
        if preauthorization:
            self.preauthorized: list = AuthModel().get_preauth_mails()

        # DB connection
        self.db_connection = SmitDb(AuthDbSchema)
        self.db_all_users = self._db_get_usernames()
        
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        
        # Use Schema from user database to generate session state variabels    
        for variable in AuthDbSchema.model_fields.keys():
            if variable not in st.session_state:
                st.session_state[variable] = None
                
    def _db_get_usernames(self) -> list:
        """ Get dict containing all usernames from authentications table.
        """
        all_users = self.db_connection.select_all_usernames()
        return all_users

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'name':st.session_state['id'],
            'username':st.session_state['username'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_pw(self) -> bool:
        """Validate login form password.
        
        Check entered password against password from authentication table.

        Returns
        -------
        bool
            Password check state.
        """
        print('-----Check password-----')
        self.user_row = self.db_connection.select_username(self.username)
        self_bytes = self.password.encode()
        db_bytes = self.user_row.password.encode()
        
        try:
            if not bcrypt.hashpw(self_bytes, db_bytes) == db_bytes:
                print('Password does not match')
                return False
            return True
        except:
            raise Exception("Password does not match")

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'username' in self.token:
                            st.session_state['name'] = self.token['name']
                            st.session_state['username'] = self.token['username']
                            st.session_state['authentication_status'] = True
    
    def _check_credentials(self) -> None:
        """Validate user and add attributes to session state.
        """
        if self.username in self.db_all_users:
            if self._check_pw():
                # Add authentication schema attributes to session state
                user_model = AuthModel().get_user(self.username)
                for key, value in user_model.items():
                    st.session_state[key] = value
                    
                # Manage cookie
                self.exp_date = self._set_exp_date()
                self.token = self._token_encode()
                self.cookie_manager.set(self.cookie_name, self.token,
                    expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                
                st.session_state['authentication_status'] = True
            else:
                st.session_state['authentication_status'] = False
                st.error('Password does not match')
                st.stop()
        else:
            st.session_state['authentication_status'] = False
            st.error('Username not in database')
            st.stop()

    def login(self, form_name: str, location: str='main') -> None:
        """Create login widget, call user validation.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            #self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.username = login_form.text_input('Username').lower()
                self.password = login_form.text_input('Password', type='password')

                if login_form.form_submit_button('Login'):
                    self._check_credentials()

    def logout(self, button_name: str, location: str='main', key: str=None):
        """Create button and clear session state on logout.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        key: str
            Unique key for the logout button widget.
        """
        def _clear_session_state(self):
            """
            Clears session state on logout.
            """
            self.cookie_manager.delete(self.cookie_name)
            
            # Use Schema from user database to clear session state variabels    
            for variable in AuthDbSchema.model_fields.keys():
                st.session_state[variable] = None
                
            st.session_state['logout'] = True
            st.session_state['authentication_status'] = None
        
        
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name, key):
                _clear_session_state(self)

        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                _clear_session_state(self)
 
    def _update_password(self, username: str, password: str):
        """
        Updates credentials dictionary with user's reset hashed password.

        Parameters
        ----------
        username: str
            The username of the user to update the password for.
        password: str
            The updated plain text password.
        """
        self.credentials['usernames'][username]['password'] = Hasher([password]).generate()[0]

    def reset_password(self, username: str, form_name: str, location: str='main') -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        username: str
            The username of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        -------
        str
            The status of resetting the password.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')
        
        reset_password_form.subheader(form_name)
        self.username = username.lower()
        self.password = reset_password_form.text_input('Current password', type='password')
        new_password = reset_password_form.text_input('New password', type='password')
        new_password_repeat = reset_password_form.text_input('Repeat password', type='password')

        if reset_password_form.form_submit_button('Reset'):
            if self._check_credentials(inplace=False):
                if len(new_password) > 0:
                    if new_password == new_password_repeat:
                        if self.password != new_password: 
                            self._update_password(self.username, new_password)
                            return True
                        else:
                            raise ResetError('New and current passwords are the same')
                    else:
                        raise ResetError('Passwords do not match')
                else:
                    raise ResetError('No new password provided')
            else:
                raise CredentialsError('password')
    
    def _register_credentials(self, new_credentials: dict) -> None:
        """
        Assign new credentials to session state and to authentication table.
        
        Hash values for fields containing `password`.
        Add credentials to session state.
        Add new user to authentication table.
        

        Parameters
        ----------
            new_credentials: dict
                Input from register user form.

        """
        # Hash passwords
        for each in new_credentials:
            if 'password' in each:
                new_credentials[each] = self._hash_pwd(new_credentials[each])
        
        # Add credentials to session state
        st.session_state['username'] = new_credentials['username']
        st.session_state['password'] = new_credentials['password']
        st.session_state['authentication_status'] = True
        
        for key, value in new_credentials.items():
            # Filter fields that are needed for authentication verfication and for database
            if (not key == 'username') and \
                (not key == 'password') and \
                (not key == 'id') and \
                (not key == 'created_on'):

                st.session_state[key] = value
        
        # Add new user to authentication table
        new_user_model = AuthDbSchema.model_validate(new_credentials)
        self.db_connection.create_instance(new_user_model)
        
        st.info(f'User {new_credentials["username"]} successfully registered')

    def register_user(self, form_name: str, location: str='main') -> None:
        """
        Create new user widget.
        
        Manage preauthorization and trigger credentials registration 
        in authentication table.
        
        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str, optional
            The location of the register new user form i.e. main or sidebar. Default is 'main'.
        
        Returns
        -------
        None
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')
            
        # Create new variables placeholder dict
        new_values: dict = {}
        register_user_form.subheader(form_name)
        new_values['username'] = register_user_form.text_input('Username').lower()
        new_values['password'] = register_user_form.text_input('Password', type='password')
        new_values['password_repeat'] = register_user_form.text_input('Repeat password', type='password')
        self._get_extra_fields(new_values, register_user_form)
        if register_user_form.form_submit_button('Register'):
            
            if new_values['password'] == new_values['password_repeat']:
                # Delete password verification field
                del new_values['password_repeat']
                
                # Validate entered user credentials
                validated_credentials: dict[str, any] = AuthModel().validate_user_dict(new_values)
                if not 'validation_errors' in validated_credentials:                    
                    # If preauthorization is false, register user
                    if not self.preauthorized:                        
                        self._register_credentials(validated_credentials)
                        st.session_state['register_btn_clicked'] = False
                    # Validate entered email against self.preauthorized
                    else:
                        if validated_credentials['email'] in self.preauthorized:
                            self._register_credentials(validated_credentials)
                            st.session_state['register_btn_clicked'] = False
                            self.preauthorized.remove(validated_credentials['email'])
                            AuthModel().delete_preauth_mail(validated_credentials['email'])
                        else:
                            st.error('Email not in preauthorized list')
                            st.stop()
                else:
                    for key, value in validated_credentials['validation_errors'].items():
                        st.error(f'Field: {key} generated Error: {value}')
                    st.stop()
            else:
                st.error('Passwords do not match')
                st.stop()

    def _get_extra_fields(self, new_values: dict, form):
        for each in AuthDbSchema.model_fields:
            # Filter fields that are needed for authentication verfication and for database
            if (not each == 'username') and \
                (not each == 'password') and \
                (not each == 'id') and \
                (not each == 'created_on'):

                if 'password' in each:
                    new_values[each] = form.text_input(each, type='password')
                else:
                    new_values[each] = form.text_input(each)  
                    
    def _hash_pwd(self, password: str) -> str:
        """
        Hashes the plain text password.

        Parameters
        ----------
        password: str
            The plain text password to be hashed.
        Returns
        -------
        str
            The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _set_random_password(self, username: str) -> str:
        """
        Updates credentials dictionary with user's hashed random password.

        Parameters
        ----------
        username: str
            Username of user to set random password for.
        Returns
        -------
        str
            New plain text password that should be transferred to user securely.
        """
        self.random_password = generate_random_pw()
        self.credentials['usernames'][username]['password'] = Hasher([self.random_password]).generate()[0]
        return self.random_password

    def forgot_password(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot password widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot password form.
        location: str
            The location of the forgot password form i.e. main or sidebar.
        Returns
        -------
        str
            Username associated with forgotten password.
        str
            Email associated with forgotten password.
        str
            New plain text password that should be transferred to user securely.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_password_form = st.form('Forgot password')
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Forgot password')

        forgot_password_form.subheader(form_name)
        username = forgot_password_form.text_input('Username').lower()

        if forgot_password_form.form_submit_button('Submit'):
            if len(username) > 0:
                if username in self.credentials['usernames']:
                    return username, self.credentials['usernames'][username]['email'], self._set_random_password(username)
                else:
                    return False, None, None
            else:
                raise ForgotError('Username not provided')
        return None, None, None

    def _get_username(self, key: str, value: str) -> str:
        """
        Retrieves username based on a provided entry.

        Parameters
        ----------
        key: str
            Name of the credential to query i.e. "email".
        value: str
            Value of the queried credential i.e. "jsmith@gmail.com".
        Returns
        -------
        str
            Username associated with given key, value pair i.e. "jsmith".
        """
        for username, entries in self.credentials['usernames'].items():
            if entries[key] == value:
                return username
        return False

    def forgot_username(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot username widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot username form.
        location: str
            The location of the forgot username form i.e. main or sidebar.
        Returns
        -------
        str
            Forgotten username that should be transferred to user securely.
        str
            Email associated with forgotten username.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_username_form = st.form('Forgot username')
        elif location == 'sidebar':
            forgot_username_form = st.sidebar.form('Forgot username')

        forgot_username_form.subheader(form_name)
        email = forgot_username_form.text_input('Email')

        if forgot_username_form.form_submit_button('Submit'):
            if len(email) > 0:
                return self._get_username('email', email), email
            else:
                raise ForgotError('Email not provided')
        return None, email

    def _update_entry(self, username: str, key: str, value: str):
        """
        Updates credentials dictionary with user's updated entry.

        Parameters
        ----------
        username: str
            The username of the user to update the entry for.
        key: str
            The updated entry key i.e. "email".
        value: str
            The updated entry value i.e. "jsmith@gmail.com".
        """
        self.credentials['usernames'][username][key] = value

    def update_user_details(self, username: str, form_name: str, location: str='main') -> bool:
        """
        Creates a update user details widget.

        Parameters
        ----------
        username: str
            The username of the user to update user details for.
        form_name: str
            The rendered name of the update user details form.
        location: str
            The location of the update user details form i.e. main or sidebar.
        Returns
        -------
        str
            The status of updating user details.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            update_user_details_form = st.form('Update user details')
        elif location == 'sidebar':
            update_user_details_form = st.sidebar.form('Update user details')
        
        update_user_details_form.subheader(form_name)
        self.username = username.lower()
        field = update_user_details_form.selectbox('Field', ['Name', 'Email']).lower()
        new_value = update_user_details_form.text_input('New value')

        if update_user_details_form.form_submit_button('Update'):
            if len(new_value) > 0:
                if new_value != self.credentials['usernames'][self.username][field]:
                    self._update_entry(self.username, field, new_value)
                    if field == 'name':
                        st.session_state['name'] = new_value
                        self.exp_date = self._set_exp_date()
                        self.token = self._token_encode()
                        self.cookie_manager.set(self.cookie_name, self.token,
                        expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                    return True
                else:
                    raise UpdateError('New and current values are the same')
            if len(new_value) == 0:
                raise UpdateError('New value not provided')
