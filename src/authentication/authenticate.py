import bcrypt
import streamlit as st
from db.db_exceptions import DatabaseError, DbReadError, DbUpdateError

# Import python modules
from db.models import AuthModel
from utils.cookie_manager import CookieManager

# Exception handling
from authentication.auth_exceptions import (
    AuthCreateError,
    AuthFormError,
    AuthReadError,
    AuthValidateError,
)


class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password,
    forgot username, and modify user details widgets.
    """

    def __init__(
        self,
        cookie_name: str,
        key: str,
        preauthorization: bool = False,
    ) -> None:
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        """

        # Connect to api
        self.api = st.session_state.auth_api

        if preauthorization:
            self.preauthorized: list = self.api.get_preauth_mails()
        else:
            self.preauthorized: list = []

        # Session state initialization
        if "authentication_status" not in st.session_state:
            st.session_state["authentication_status"] = None

        if "username" in st.session_state:
            self.username: str = st.session_state["username"]
            self.password: str = st.session_state["password"]

        for variable in AuthModel.model_fields.keys():
            if variable not in st.session_state:
                st.session_state[variable] = None

        # Cookie management initialization
        self.cookie_manager = CookieManager(cookie_name, key)

    def _db_get_usernames(self) -> list:
        """
        Return list with all usernames from authentications table.

        Returns:
            list: All usernames from the authentications table.
        """
        try:
            all_users: list = self.api.read_all_users()
            return all_users
        except Exception as e:
            raise e

    def _clear_userdata(self) -> None:
        """
        Delete cookie and session state for logged in user.
        """
        try:
            self.cookie_manager.delete_cookie()
            # Clear all session state variables
            for field in AuthModel.model_fields:
                st.session_state[field] = None
        except Exception as e:
            raise e

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
        for each in AuthModel.model_fields:
            # Except user management and auto generated fields
            if (
                (not each == "username")
                and (not each == "password")
                and (not each == "id")
                and (not each == "created_on")
            ):
                if "password" in each:
                    new_values[each] = form.text_input(each, type="password")
                else:
                    new_values[each] = form.text_input(each)

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

    def _check_pw(self) -> bool:
        """Validate `self.password` against database.

        Returns:
            bool: Password check state.
        """
        try:
            db_user_row = self.api.get_user(self.username)
            self_bytes = self.password.encode()
            db_bytes = db_user_row["password"].encode()

            if not bcrypt.hashpw(self_bytes, db_bytes) == db_bytes:
                return False
            else:
                return True
        except AuthReadError as ae:
            raise ae
        except Exception as e:
            raise DatabaseError(e, "Raised by Authenticator._check_pwd()") from e

    def _check_credentials(self) -> bool:
        """
        Get userdata from database and add to session state.

        This method checks the credentials provided by the user against the database.
        It verifies if the username exists in the database and if the password matches.
        If the credentials are valid, it retrieves the user data from the API and adds
        it to the session state.

        Returns:
            bool: True if the credentials are valid and the user data is added to the
            session state, False otherwise.

        Raises:
            AuthFormError: If the username is not found in the database or if the
            password does not match.
            Exception: If an error occurs while retrieving the user data from the API.
        """
        if not self.username in self._db_get_usernames():
            raise AuthFormError("Username not in database")
        if not self._check_pw():
            raise AuthFormError("Password does not match")
        else:
            try:
                user_model = self.api.get_user(self.username)
                for key, value in user_model.items():
                    st.session_state[key] = value
                return True
            except Exception as e:
                raise DatabaseError(
                    e, "Raised by Authenticator._check_credentials()"
                ) from e

    def login(self, form_name: str, location: str = "main") -> bool:
        """Create login widget, call user validation.

        Args:
            form_name: str
                The rendered name of the login form.
            location: str, optional
                The location of the login form i.e. main or sidebar. Default is 'main'.

        Returns:
            bool:
                True if the login is successful, False otherwise.

        Raises:
            ValueError:
                If the location is not 'main' or 'sidebar'.
            AuthFormError:
                If there is an error within the authentication form.
            Exception:
                Pass through any other error during the login process.
        """
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            login_form = st.form("Login")
        elif location == "sidebar":
            login_form = st.sidebar.form("Login")

        try:
            self.username = self.cookie_manager.check_cookie()

            if not self.username:
                login_form.subheader(form_name)
                self.username: str = login_form.text_input("Username").lower()
                self.password: str = login_form.text_input("Password", type="password")

                if login_form.form_submit_button("Login"):
                    try:
                        self._check_credentials()
                        self.cookie_manager.create_cookie()
                        return True
                    except AuthFormError as ae:
                        raise ae
                    except Exception as e:
                        raise e
            else:
                # Login in with cookie
                return True
        except Exception as e:
            raise e

    def logout(self, button_name: str, location: str = "main", key: str = None) -> bool:
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
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            if st.button(button_name, key):
                self._clear_userdata()
                return True

        elif location == "sidebar":
            if st.sidebar.button(button_name, key):
                self._clear_userdata()
                return True

    def _update_password(self, reset_pwd: dict) -> bool:
        """
        Updates credentials dictionary with user's reset hashed password.

        Parameters:
            reset_pwd: dict
                Dictionary with plain text passwords from input form.
        """
        credentials: dict = self.api.get_user(self.username)
        self.password = reset_pwd["old"]

        if self._check_pw():
            credentials["password"] = reset_pwd["new"]

            try:
                self.api.validate_user_dict(credentials)
                # Hash password
                credentials["password"] = self._hash_pwd(credentials["password"])
                # Update session state
                st.session_state["password"] = credentials["password"]
                # Update database
                try:
                    self.api.update_by_id(
                        st.session_state["id"], "password", credentials["password"]
                    )
                except Exception as e:
                    raise DatabaseError(
                        e, "Raised by Authenticator._update_password()"
                    ) from e
                return True
            except AuthValidateError as ve:
                raise ve
            except Exception as e:
                raise e
        else:
            raise AuthFormError("Old password for logged in user is not correct")

    def reset_password(self, form_name: str, location: str = "main") -> bool:
        """
        Create password reset widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the password reset form.
        location: str, optional
            The location of the password reset form i.e. main or sidebar. Default is 'main'.

        Returns
        -------
        bool
            The status of resetting the password process.
        """
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            reset_password_form = st.form("Reset password")
        elif location == "sidebar":
            reset_password_form = st.sidebar.form("Reset password")

        reset_password_form.subheader(form_name)
        old_password: str = reset_password_form.text_input(
            "Current password", type="password"
        )
        new_password: str = reset_password_form.text_input(
            "New password", type="password"
        )
        new_password_repeat: str = reset_password_form.text_input(
            "Repeat password", type="password"
        )

        if reset_password_form.form_submit_button("Reset"):
            if len(new_password) <= 3:
                raise AuthFormError("New password > 3")

            if new_password != new_password_repeat:
                raise AuthFormError("New passwords do not match")

            if old_password != new_password:
                reset_pwd: dict = {"old": old_password, "new": new_password}
                if self._update_password(reset_pwd):
                    return True
                else:
                    return False
            else:
                raise AuthFormError("New and current password is the same")

    def _register_credentials(self, new_credentials: dict) -> None:
        """
        Assign new credentials to session state and database.

        Values for fields containing `password` will be hashed before assignment.

        Args:
            new_credentials: dict
                Input from register user form.
        """
        try:
            # Hash passwords
            for each in new_credentials:
                if "password" in each:
                    new_credentials[each] = self._hash_pwd(new_credentials[each])

            # Add credentials to session state
            st.session_state["username"] = new_credentials["username"]
            st.session_state["password"] = new_credentials["password"]

            self.username = new_credentials["username"]
            self.password = new_credentials["password"]

            for key, value in new_credentials.items():
                # Except authentication and database fields
                if (
                    (not key == "username")
                    and (not key == "password")
                    and (not key == "id")
                    and (not key == "created_on")
                ):
                    st.session_state[key] = value

            # Register new user
            self.api.write_user(new_credentials)
            self.cookie_manager.create_cookie()
        except Exception as e:
            raise DatabaseError(
                e, "Raised by Authenticator._register_credentials()"
            ) from e

    def register_user(self, form_name: str, location: str = "main") -> bool:
        """
        Create new user widget.

        Manage preauthorization and trigger credentials registration.

        Args:
            form_name: str
                The rendered name of the register new user form.
            location: str, optional
                The location of the register new user form i.e. main or sidebar. Default is 'main'.
        """
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            register_user_form = st.form("Register user")
        elif location == "sidebar":
            register_user_form = st.sidebar.form("Register user")

        # Create new variables placeholder dict
        new_values: dict = {}
        register_user_form.subheader(form_name)
        new_values["username"] = register_user_form.text_input("Username").lower()
        new_values["password"] = register_user_form.text_input(
            "Password", type="password"
        )
        new_values["password_repeat"] = register_user_form.text_input(
            "Repeat password", type="password"
        )
        self._generate_extra_fields_inputform(new_values, register_user_form)

        if register_user_form.form_submit_button("Register"):
            if new_values["password"] != new_values["password_repeat"]:
                raise AuthFormError("Passwords do not match")
            elif new_values["username"] in self._db_get_usernames():
                raise AuthFormError("Username already in database")
            else:
                del new_values["password_repeat"]

                try:
                    # Validate entered user credentials
                    validated_credentials: dict[str, any] = self.api.validate_user_dict(
                        new_values
                    )

                    if not self.preauthorized:
                        try:
                            self._register_credentials(validated_credentials)
                            return True
                        except Exception as e:
                            raise e
                    # Validate entered email against self.preauthorized
                    else:
                        if validated_credentials["email"] in self.preauthorized:
                            try:
                                self._register_credentials(validated_credentials)
                                self.preauthorized.remove(
                                    validated_credentials["email"]
                                )
                                self.api.delete_preauth_mail(
                                    validated_credentials["email"]
                                )
                                return True
                            except Exception as e:
                                raise e
                        else:
                            raise AuthFormError("Email is not preauthorized")
                except AuthValidateError as ve:
                    raise ve
                except Exception as e:
                    raise e

    def update_user_details(self, form_name: str, location: str = "main") -> bool:
        """
        Creates a update user details widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the update user details form.
        location: str, optional
            The location of the update user details form i.e. main or sidebar. Default is 'main'.

        Returns
        -------
        bool
            True on success.

        Raises
        ------
        ValueError
            If the location is not 'main' or 'sidebar'.
        DatabaseError
            If there is an error reading or updating the database.
        AuthValidateError
            If there is an error validating the user credentials.
        AuthCreateError
            If there is an error creating the user.

        Notes
        -----
        This method creates a form for updating user details. It takes the form name and location as parameters.
        The form is rendered either in the main area or in the sidebar, depending on the location parameter.
        The user can input new values for the username and other fields, and click the 'Update' button to update the user details.
        The method validates the user credentials and updates the database with the new values.
        If any errors occur during the process, the corresponding exceptions are raised.

        Example
        -------
        To update user details in the main area:

        >>> update_user_details('Update user details', 'main')

        To update user details in the sidebar:

        >>> update_user_details('Update user details', 'sidebar')
        """
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            update_user_details_form = st.form("Update user details")
        elif location == "sidebar":
            update_user_details_form = st.sidebar.form("Update user details")

        try:
            credentials: dict = self.api.get_user(self.username)
        except DbReadError as dbe:
            raise DatabaseError(
                dbe, "Raised by Authenticator.update_user_details()"
            ) from dbe

        new_values: dict = {}

        update_user_details_form.subheader(form_name)

        new_values["username"] = update_user_details_form.text_input("username").lower()
        self._generate_extra_fields_inputform(new_values, update_user_details_form)

        if update_user_details_form.form_submit_button("Update"):
            # Write new values to credentials
            # All credential fields must be filled for vailidation
            for key, value in new_values.items():
                if len(value) > 0:
                    credentials[key] = value

            try:
                # Validate with plain text passwords
                self.api.validate_user_dict(credentials)

                for key, value in new_values.items():
                    if len(value) > 0:
                        if "password" in key:
                            credentials[key] = self._hash_pwd(value)

                for key, value in credentials.items():
                    st.session_state[key] = value

                # Update database
                for key, value in new_values.items():
                    if len(value) > 0:
                        try:
                            self.api.update_by_id(st.session_state["id"], key, value)
                        except DbUpdateError as dbe:
                            raise DatabaseError(
                                dbe, "Raised by Authenticator.update_user_details()"
                            ) from dbe

                # Cookie management
                self.cookie_manager.delete_cookie()  # Delete old cookie
                self.cookie_manager.create_cookie()

                return True
            except AuthValidateError as ve:
                raise ve
            except AuthCreateError as ce:
                raise ce

    def delete_user(self, form_name: str, location: str = "main") -> bool:
        """Delete user from session state and authentication table."""
        # Create form
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            delete_user_form = st.form("Delete user")
        elif location == "sidebar":
            delete_user_form = st.sidebar.form("Delete user")

        delete_user_form.subheader(form_name)

        form_input: str = delete_user_form.text_input("Username").lower()

        # Form logic
        if delete_user_form.form_submit_button("Delete user"):
            if self.username == form_input:
                self._clear_userdata()
                try:
                    self.api.delete_user(self.username)
                except Exception as e:
                    raise DatabaseError(
                        e, "Raised by Authenticator.delete_user()"
                    ) from e
                return True
            else:
                raise AuthFormError("Username does not match")
