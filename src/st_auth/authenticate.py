from cgi import print_directory
import bcrypt
import streamlit as st
# Import python modules
from db.schemas import AuthenticationSchema
from st_auth.cookie_manager import CookieManager

from st_auth.auth_exceptions import AuthFormError, AuthValidateError, AuthCreateError

class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot username, and modify user details widgets.
    """
    def __init__(self,
                 cookie_name: str,
                 key: str,
                 preauthorization: bool = False,
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
        
        # Connect to api
        self.api = st.session_state.auth_api

        if preauthorization:
            self.preauthorized: list = self.api.get_preauth_mails()
        else:
            self.preauthorized: list = []

        # Session state initialization
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None

        if 'username' in st.session_state:
            self.username: str = st.session_state['username']
            self.password: str = st.session_state['password']
            
        for variable in AuthenticationSchema.model_fields.keys():
            if variable not in st.session_state:
                st.session_state[variable] = None

        # Cookie management initialization
        self.cookie_manager = CookieManager(cookie_name, key)

    # done                        
    def _db_get_usernames(self) -> list:
        """ 
        Return list with all usernames from authentications table.
        
        Returns:
            list: All usernames from the authentications table.
        """
        all_users: list = self.api.read_all_users()
        return all_users
    # done
    def _clear_userdata(self) -> None:
        """
        Delete cookie and session state for logged in user.
        """
        self.cookie_manager.delete_cookie()
        
        # Use database schema to clear session state variabels    
        for key in AuthenticationSchema.model_fields.keys():
            st.session_state[key] = None
            
        st.session_state['authentication_status'] = None
    # done
    def _generate_extra_fields_inputform(self, new_values: dict, form: str) -> None:
        """
        Add extra fields from AuthDbSchema to input form.
        
        For each extra field in the AuthDbSchema a input field is added to the form.
        The fields `username` and `password` are excluded. This fields are needed for
        the user management on runtime and thus have to be managed as static fields.
        Additionally fields which are auto generated during writing data to the database
        are not included in the form.

        Args:
            new_values (dict): Input values from the form will be added to this dict.
            form (str): Name of the form from which the method will be called.
        """
        for each in AuthenticationSchema.model_fields:
            # Filter fields that are needed for authentication verfication and for database
            if (not each == 'username') and \
                (not each == 'password') and \
                (not each == 'id') and \
                (not each == 'created_on'):

                if 'password' in each:
                    new_values[each] = form.text_input(each, type='password')
                else:
                    new_values[each] = form.text_input(each)  
    # done                
    def _hash_pwd(self, password: str) -> str:
        """
        Hashes the plain text password.

        Args:
            password: str
                The plain text password to be hashed.
        
        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # done
    def _check_pw(self) -> bool:
        """Validate `self.password` against database.

        Returns:
            bool: Password check state.
        """
        db_user_row = self.api.get_user(self.username)
        self_bytes = self.password.encode()
        db_bytes = db_user_row['password'].encode()

        if not bcrypt.hashpw(self_bytes, db_bytes) == db_bytes:
            return False
        else:
            return True
    # done
    def _check_credentials(self) -> None:
        """
        Get userdata from database and add to session state.
        """
        if self.username in self._db_get_usernames():
            if self._check_pw():
                # Add authentication schema attributes to session state
                user_model = self.api.get_user(self.username)
                for key, value in user_model.items():
                    st.session_state[key] = value
                
                st.session_state['authentication_status'] = True
            else:
                st.session_state['authentication_status'] = False
                st.error('Password does not match')
                st.stop()
        else:
            st.session_state['authentication_status'] = False
            st.error('Username not in database')
            st.stop()
    # done
    def login(self, form_name: str, location: str='main') -> None:
        """Create login widget, call user validation.

        Args:
            form_name: str
                The rendered name of the login form.
            location: str
                The location of the login form i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            # Check if cookie exist and use for login
            self.username = self.cookie_manager.check_cookie()
            
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.username: str = login_form.text_input('Username').lower()
                self.password: str = login_form.text_input('Password', type='password')

                if login_form.form_submit_button('Login'):
                    try:
                        self._check_credentials()
                        # If no cookie is found, create cookie for the logged in user
                        self.cookie_manager.create_cookie()
                    except Exception as e:
                        st.error(e)
                        st.stop()
    # done
    def logout(self, button_name: str, location: str='main', key: str=None):
        """
        Create button and clear session state on logout.

        Args:
            button_name: str
                The rendered name of the logout button.
            location: str
                The location of the logout button i.e. main or sidebar.
            key: str
                Unique key for the logout button widget.
        """        
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name, key):
                self._clear_userdata()

        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                self._clear_userdata()
    # done
    def _update_password(self, reset_pwd: dict) -> bool:
        """
        Updates credentials dictionary with user's reset hashed password.

        Parameters:
            reset_pwd: dict
                Dictionary with plain text passwords from input form.
        """
        credentials: dict = self.api.get_user(self.username)
        self.password = reset_pwd['old']
        
        if self._check_pw():
            
            credentials['password'] = reset_pwd['new']
            
            unsafe_validated_credentials = self.api.validate_user_dict(credentials)
            
            if not 'validation_errors' in unsafe_validated_credentials:
                # Hash password
                credentials['password'] = self._hash_pwd(credentials['password'])
                
                # Update session state
                st.session_state['password'] = credentials['password']
                
                # Update database
                self.api.update_by_id(st.session_state['id'], 'password', credentials['password'])
                
                return True
            else:
                for each in unsafe_validated_credentials['validation_errors'].items():
                    st.error(f'{each}')
                return False
        else:
            st.error('Old password for logged in user is not correct')
            return False
    # done
    def reset_password(self, form_name: str, location: str='main') -> bool:
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
        old_password = reset_password_form.text_input('Current password', type='password')
        new_password = reset_password_form.text_input('New password', type='password')
        new_password_repeat = reset_password_form.text_input('Repeat password', type='password')

        if reset_password_form.form_submit_button('Reset'):
            if len(new_password) > 0:
                if new_password == new_password_repeat:
                    if old_password != new_password:
                        reset_pwd: dict = {
                            'old': old_password,
                            'new': new_password
                        }
                        if self._update_password(reset_pwd):
                            return True
                        else:
                            return False
                    else:
                        st.error('New and current password is the same')
                else:
                    st.error('New passwords do not match')
            else:
                st.error('Provide new password')
    # done
    def _register_credentials(self, new_credentials: dict) -> None:
        """
        Assign new credentials to session state and database.
        
        Values for fields containing `password` will be hashed before assignment.
        
        Args:
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
        
        self.username = new_credentials['username']
        self.password = new_credentials['password']
        
        for key, value in new_credentials.items():
            # Filter fields that are needed for authentication verfication and for database
            if (not key == 'username') and \
                (not key == 'password') and \
                (not key == 'id') and \
                (not key == 'created_on'):

                st.session_state[key] = value
        
        # Add new user to authentication table
        if self.api.write_user(new_credentials):
            st.info(f'User {new_credentials["username"]} successfully registered')

        self.cookie_manager.create_cookie()
    # done
    def register_user(self, form_name: str, location: str='main') -> None:
        """
        Create new user widget.
        
        Manage preauthorization and trigger credentials registration.
        
        Args:
            form_name: str
                The rendered name of the register new user form.
            location: str, optional
                The location of the register new user form i.e. main or sidebar. Default is 'main'.
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
        self._generate_extra_fields_inputform(new_values, register_user_form)
        
        if register_user_form.form_submit_button('Register'):
            
            if new_values['password'] == new_values['password_repeat']:
                # Delete password verification field
                del new_values['password_repeat']
                
                # Validate entered user credentials
                validated_credentials: dict[str, any] = self.api.validate_user_dict(new_values)
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
                            self.api.delete_preauth_mail(validated_credentials['email'])
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
    # done
    def update_user_details(self, form_name: str, location: str='main') -> bool:
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
        
        credentials: dict = self.api.get_user(self.username)
        new_values: dict = {}
        
        update_user_details_form.subheader(form_name)
        
        new_values['username'] = update_user_details_form.text_input('username').lower()
        self._generate_extra_fields_inputform(new_values, update_user_details_form)   

        if update_user_details_form.form_submit_button('Update'):
            # Write new values to credentials, validate credentials
            for key, value in new_values.items():
                if len(value) > 0:
                    credentials[key] = value
            
            # Validate with plain text passwords        
            try:
                # unsafe_validated_credentials = self.api.validate_user_dict(credentials)
                self.api.validate_user_dict(credentials)
                
                
                ######### do stuf if no exception
                #Hash passwords if keys with `password` are updated
                for key, value in new_values.items():
                    if len(value) > 0:
                        if 'password' in key:
                            credentials[key] = self._hash_pwd(value)             

                # Update session state
                for key, value in credentials.items():
                    st.session_state[key] = value

                # Update database
                for key, value in new_values.items():
                    if len(value) > 0:

                        ## try/except for database update
                        self.api.update_by_id(st.session_state['id'], key, value)
                
                return True
            
            except AuthValidateError as ve:
                raise ve
            
            except AuthCreateError as ce:
                raise ce
            
            
            
            
            
            
            
            # except Exception as e:
            #     # print(f' authenticator: {e}')
            #     # raise
            #     pass
            
            #if not 'validation_errors' in unsafe_validated_credentials:
            

            
            # Success message
            # st.write('__Updated credentials__')
            # for key, value in new_values.items():
            #     if len(value) > 0:
            #         st.success(f'Updated: {key} to: {value}')
            # # else:
            #     for key, value in unsafe_validated_credentials['validation_errors'].items():
            #         st.error(f'{value}')
            #     return False
    # done
    def delete_user(self, form_name: str, location: str='main') -> bool:
        """Delete user from session state and authentication table.
        
        """        
        # Create form
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            delete_user_form = st.form('Delete user')
        elif location == 'sidebar':
            delete_user_form = st.sidebar.form('Delete user')
        
        
        delete_user_form.subheader(form_name)
        
        form_input: str = delete_user_form.text_input('Username').lower()
        
        # Form logic    
        if delete_user_form.form_submit_button('Delete user'):
            if self.username == form_input:
                # Delete user from database
                self._clear_userdata()
                self.api.delete_user(self.username)
                # st.write('User deleted from database')
                # st.write('User logged out')
                return True
            else:
                # st.error('Username does not match')
                raise AuthFormError('Username does not match')