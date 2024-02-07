from datetime import datetime, timedelta

import streamlit as st
import extra_streamlit_components as stx
import jwt

from smit.smit_api import SmitApi

from authentication.auth_exceptions import AuthExceptionLogger, AuthCookieError

class CookieManager:
    """Cookie management for Streamlit application.

    Provides methods to set and get cookies,
    with a specific focus on authentication cookies. 
    Use the `extra_streamlit_components` `CookieManager` library to manage cookies 
    and the `jwt` library to create and verify JSON Web Tokens.

    Attributes
    ----------
    cookie_name : str
        The name of the cookie to be managed.
    key : str
        The secret key used for creating and verifying JWTs.
    cookie_expiry_days : float
        The number of days until the cookie expires.

    Example
    -------
    >>> cookie_manager = CookieManager('your-cookie-name', 'your-secret-key')
    >>> new_cookie = cookie_manager.create_cookie()
    """
    def __init__(self,
                 cookie_name: str,
                 key: str,
                 cookie_expiry_days: float=30.0,
                 ) -> None:
        
        self.cookie_name: str = cookie_name
        self.key: str = key
        self.cookie_expiry_days: float = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()
        
        self.api = st.session_state.auth_api

        self.exp_date = self._set_exp_date()
        
        # Use logger from SmitApi class
        self.logger = SmitApi().logger
        
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)
        
    def _log_exception(self, e: Exception) -> None:
            """
            Logs the given exception and its formatted error message.

            Args:
                e (Exception): The exception to be logged.

            Returns:
                None
            """
            formatted_error_message = AuthExceptionLogger().logging_input(e)
            st.session_state.smit_api.logger.error(formatted_error_message)        
            
    def _set_exp_date(self) -> str:
        """Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()
        
    def _token_encode(self) -> str:
        """Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        try:
            uid = st.session_state['id']
            username = st.session_state['username']

            return jwt.encode({'uid': uid,
                'username':username,
                'exp_date':self.exp_date}, self.key, algorithm='HS256')
        except Exception as e:
            self._log_exception(e)
            raise AuthCookieError('Encoding reauthentication cookie failed.') from e
            
            
    
    # todo: should work, self.token defined in _check_cookie()
    def _token_decode(self, token: str) -> str:
        """Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(token, self.key, algorithms=['HS256'])
        except Exception as e:
            self._log_exception(e)
            raise AuthCookieError('Decoding reauthentication cookie failed.') from e

    
    def check_cookie(self) -> str:
        """Check if cookie exists and log in.
        
        Retrieves the reauthentication cookie,
        decodes it, and checks if it's still valid. 
        If the cookie is valid and contains the 'uid' and 'username' fields,
        it retrieves the user's information from the API, 
        adds it to the session state, and sets the 'authentication_status' to True.

        Returns
        -------
        None

        Example
        -------
        >>> cookie_manager.check_cookie()
        """
        try:
            token = self.cookie_manager.get(self.cookie_name)
            if token is not None:
                token = self._token_decode(token)
                
                if token is not False:
                    if token['exp_date'] > datetime.utcnow().timestamp():
                        if 'uid' and 'username' in token:
                            self.logger.debug('Cookie found, logging in with username %s', token['username'])
                            # Add authentication schema attributes to session state
                            user_model = self.api.get_user(token['username'])
                            for key, value in user_model.items():
                                st.session_state[key] = value
                        return token['username']
                    else:
                        raise AuthCookieError('Reauthentication cookie expired.')
        except AuthCookieError as ae:
            raise ae
        except Exception as e:
            self._log_exception(e)
            raise e

                            
    def delete_cookie(self) -> bool:
        """Delete reauthentication cookie.
        
        Returns
        -------
        bool
            True on cookie deletion.
        """
        try:
            self.cookie_manager.delete(self.cookie_name)
            return True
        except Exception as e:
            self._log_exception(e)
            raise AuthCookieError('Deleting reauthentication cookie failed.') from e
    
    def create_cookie(self) -> bool:
        """Create reauthentication cookie.
        
        Use user id and username from session state to create a JWT cookie.
        
        Returns
        -------
        bool
            True if cookie is created, False otherwise.
        """
        try:
            token = self._token_encode()
            self.cookie_manager.set(
                self.cookie_name,
                token,
                expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
            return True
        except Exception as e:
            self._log_exception(e)
            raise AuthCookieError('Creating reauthentication cookie failed.') from e