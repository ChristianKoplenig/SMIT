from pydantic import ValidationError
# Database connection
from db.smitdb import SmitDb
# Database schema
from db.auth_schema import AuthDbSchema, AuthConfigSchema

class AuthModel:
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
        self.db_connection = SmitDb(AuthDbSchema)
        self.config_connection = SmitDb(AuthConfigSchema)
        
        
    # def create_users_dict(self, db_all: list) -> dict:
    #     """
    #     Create a dictionary of users with their attributes.

    #     Args:
    #         db_all (list): A list of user objects from the database.

    #     Returns:
    #         dict: A dictionary where the keys are user IDs and the values are dictionaries of user attributes.
    #     """

    #     # Generate dictionary with uid as primary key
    #     users = {}

    #     for user in db_all:

    #         dump = AuthDbSchema.model_dump(user)

    #         uid = dump['id']
    #         user_attributes = {}

    #         # Assign all user attributes to uid key
    #         for key in dump.keys():
    #             user_attributes[key] = dump[key]

    #         users.setdefault('uid', {}).setdefault(uid, user_attributes)
    #     return users

    def create_user_models(self, users: dict) -> dict:
        """
        Return dictionary with validated user models from AuthDbSchema.

        Args:
            users (dict): A dictionary containing user data grouped by user id from auth table.

        Returns:
            dict: A dictionary containing user models, where the keys are user IDs and the values are the corresponding models.
        """
        models: dict = {}
        if 'uid' in users:
            for uid in users['uid'].values():
                models[uid['id']] = AuthDbSchema.model_validate(uid)
        return models

    def single_user_model(self, user: tuple) -> dict[str, any]:
        """
        Return unvalidated dictionary with single user data from authentication table.

        Args:
            user (list): Query result for single user from auth table.

        Returns:
            dict: A dictionary containing the user attributes as key, value pairs.
        """
        model: dict = {}
        model = AuthDbSchema.model_dump(user)
        return model


    # Get validated dict from db
    def get_user(self, username: str) -> dict[str, any]:
        """
        Retrieves a user from the database based on the provided username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict[str, any]: A dictionary representing the user's data.
        """
        row_db: tuple = self.db_connection.select_username(username)
        model_db: dict = self.single_user_model(row_db)
        
        validated_schema: AuthDbSchema = AuthDbSchema().model_validate(model_db)
        
        return validated_schema.model_dump()
    
    def validate_user_dict(self, user_dict: dict) -> dict[str, any]:
        """
        Validates a user dictionary.

        Args:
            user_dict (dict): Dict keys represent user data authentication table columns.

        Returns:
            dict[str, any]: A validated dictionary representing the user's data.
        """
        try:
            validated_dict: AuthDbSchema = AuthDbSchema.model_validate(user_dict)
            return validated_dict.model_dump()
        except ValidationError as e:
            error_messages = {'validation_errors': {}}
            for error in e.errors():
                field = error['loc'][0]
                error_message = error['msg']
                error_messages['validation_errors'][field] = error_message
            return error_messages

    def get_preauth_mails(self) -> list:
        """
        Retrieves the preauthorized email addresses from the database.

        Returns:
            list: A list of preauthorized email addresses.
        """
        return self.config_connection.read_column('preauth_mails')
    
    def delete_preauth_mail(self, email: str) -> None:
        """
        Delete email from preauthorization addresses.

        Args:
            email (str): The email address to delete.
        """
        self.config_connection.delete_where('preauth_mails', email)