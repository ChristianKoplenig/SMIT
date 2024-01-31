import streamlit as st

# Database imports
from db.schemas import AuthenticationSchema

# Error handling
from pydantic import ValidationError
import db.db_exceptions as db_exc
from st_auth.auth_exceptions import (AuthExceptionLogger,
                                     AuthCreateError,
                                     AuthUpdateError,
                                     AuthWriteError,
                                     AuthReadError,
                                     AuthDeleteError,
                                     AuthValidateError,
                                     AuthFormError)

class AuthApi:
    """
    Class for retrieving data from the authentication table.
    
    Methods:
        create_users_dict(db_all: list) -> dict: 
            Create a dictionary of users with
                         their attributes.
        create_user_models(users: dict) -> dict: 
            Return dictionary with validated user models from AuthDbSchema.
        single_user_model(user: list) -> dict[str, str]: 
            Return unvalidated dictionary with single user data from authentication table.
        get_user(username: str) -> dict[str, any]: 
            Retrieves a user from the database based on the provided username.
    """
    def __init__(self):
        self.auth_connection = st.session_state.auth_connection
        self.config_connection = st.session_state.config_connection

        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        st.session_state.smit_api.logger.debug(msg)

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

    def _format_validation_error(self, e: ValidationError) -> str:
        error_messages = {'validation_errors': {}}
        for error in e.errors():
            field = error['loc'][0]
            error_message = error['msg']
            error_messages['validation_errors'][field] = error_message
        return error_messages  
         
    def read_all_users(self) -> list:
        """
        Generate list with entries from authentication table username column.
        
        Returns:
            list: All usernames in authentication table.
        """
        try:
            users: list = []
            users = self.auth_connection.read_column('username')
            return users
        
        except db_exc.DbReadError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthReadError('Read all users from authentication database table failed.') from e
        
    def single_user_model(self, user: tuple) -> dict[str, any]:
        """
        Return unvalidated dictionary with single user data from authentication table.

        Args:
            user (list): Query result for single user from auth table.

        Returns:
            dict: A dictionary containing the user attributes as key, value pairs.
        """
        try:
            model: dict = {}
            model = AuthenticationSchema.model_dump(user)
            return model
        
        except Exception as e:
            self._log_exception(e)
            raise AuthCreateError(f'Creation of user model dictionary for user: "{user}" failed.') from e

    def validate_user_dict(self, user_dict: dict) -> dict[str, any]:
        """
        Validates a user dictionary.

        Args:
            user_dict (dict): Dict keys represent user data authentication table columns.

        Returns:
            dict[str, any]: A validated dictionary representing the user's data.
        """
        try:
            validated_dict: AuthenticationSchema = AuthenticationSchema.model_validate(user_dict)
            return validated_dict.model_dump()
        
        except ValidationError as ve:
            raise AuthValidateError(ve) from ve
            
        except Exception as e:
            self._log_exception(e)
            raise AuthCreateError(f'Creation of user dictionary: "{user_dict}" failed.') from e

    def get_user(self, username: str) -> dict[str, any]:
        """
        Retrieves a user from the database based on the provided username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict[str, any]: A dictionary representing the user's data.
        """
        try:
            row_db: tuple = self.auth_connection.select_where('username', username)
            model_db: dict = self.single_user_model(row_db)
            validated_schema: AuthenticationSchema = AuthenticationSchema().model_validate(model_db)
            return validated_schema.model_dump()
        
        except db_exc.DbReadError as dbe:
            raise dbe
        
        except ValidationError as ve:
            raise AuthValidateError(ve) from ve
        
        except AuthCreateError as ae:
            raise ae
        
        except Exception as e:
            self._log_exception(e)
            raise AuthReadError(f'Failed to retrieve "{username}" from database.') from e
        
    # Todo: return values
    def write_user(self, new_user: dict) -> bool:
        """Validate and write user data to authentication table.

        Args:
            new_user (dict): User data, `username` and `password` are required.

        Returns:
            bool: True if validation and creation successful.
        """
        try:
            new_user_model: AuthenticationSchema = AuthenticationSchema.model_validate(new_user)
            self.auth_connection.create_instance(new_user_model)
            return True
        
        except ValidationError as ve:
            raise AuthValidateError(ve) from ve
        
        except db_exc.DbCreateError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthWriteError(f'Failed to write user: "{new_user}"') from e
        
    def update_by_id(self, uid: int, column: str, new_value: str) -> bool:
        """
        Update database entry with given value.

        Args:
            uid (int): The `id` of the user.
            column (str): The column to search in.
            new_value (str): The new entry value.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            row: AuthenticationSchema = self.auth_connection.select_where('id', uid)
            uid_data: dict = row.model_dump()
            update_column: str = column
            old_value = uid_data[column]
            self.auth_connection.update_where(update_column, old_value, new_value)
            return True
        
        except db_exc.DbReadError as dbe:
            raise dbe
        
        except AuthCreateError as ae:
            raise ae
        
        except db_exc.DbUpdateError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthUpdateError(f'Failed to update "{column}" for user id: {uid}') from e

    def delete_user(self, username: str) -> bool:
        """
        Deletes a user from the database.

        Args:
            username (str): The username for deletion.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.
        """
        try:
            self.auth_connection.delete_where('username', username)
            return True
        
        except db_exc.DbDeleteError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthDeleteError(f'Failed to delete user: "{username}" from database') from e
        
    # todo: implement data validation
    def get_preauth_mails(self) -> list:
        """
        Retrieves the preauthorized email addresses from the database.

        Returns:
            list: A list of preauthorized email addresses.
        """
        try:
            return self.config_connection.read_column('preauth_mails')
        
        except db_exc.DbReadError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthReadError('Failed to retrieve preauthorized emails from database.') from e
        
    # todo: implement data validation
    def delete_preauth_mail(self, email: str) -> None:
        """
        Delete email from preauthorization addresses.

        Args:
            email (str): The email address to delete.
        """
        try:
            self.config_connection.delete_where('preauth_mails', email)
        except db_exc.DbDeleteError as dbe:
            raise dbe
        
        except Exception as e:
            self._log_exception(e)
            raise AuthDeleteError(f'Failed to delete "{email}" from preauthorized list') from e

    
################# old ############################
    # def create_user_models(self, users: dict) -> dict:
    #     """
    #     Return dictionary with validated user models from AuthDbSchema.

    #     Args:
    #         users (dict): A dictionary containing user data grouped by user id from auth table.

    #     Returns:
    #         dict: A dictionary containing user models, where the keys are user IDs and the values are the corresponding models.
    #     """
    #     models: dict = {}
    #     if 'uid' in users:
    #         for uid in users['uid'].values():
    #             models[uid['id']] = AuthDbSchema.model_validate(uid)
    #     return models



