# Database connection
from db.smitdb import SmitDb
# Database schema
from db.auth_schema import AuthDbSchema

class AuthModel:
    """
    Class for retrieving data from the authentication table.
    
    Methods:
        create_users_dict(db_all: list) -> dict: 
            Create a dictionary of users with their attributes.
        create_user_models(users: dict) -> dict: 
            Return dictionary with validated user models from AuthDbSchema.
        single_user_model(user: list) -> dict[str, str]: 
            Return unvalidated dictionary with single user data from authentication table.
        get_user(username: str) -> dict[str, any]: 
            Retrieves a user from the database based on the provided username.
    """
    def __init__(self):
        self.db_connection = SmitDb(AuthDbSchema)
        
        
    def create_users_dict(self, db_all: list) -> dict:
        """
        Create a dictionary of users with their attributes.

        Args:
            db_all (list): A list of user objects from the database.

        Returns:
            dict: A dictionary where the keys are user IDs and the values are dictionaries of user attributes.
        """

        # Generate dictionary with uid as primary key
        users = {}

        for user in db_all:

            dump = AuthDbSchema.model_dump(user)

            uid = dump['id']
            user_attributes = {}

            # Assign all user attributes to uid key
            for key in dump.keys():
                user_attributes[key] = dump[key]

            users.setdefault('uid', {}).setdefault(uid, user_attributes)
        return users

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

    def single_user_model(self, user: list) -> dict[str, str]:
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

######## work with all users ######## 

# # Connect to database
# db_connection = SmitDb(AuthDbSchema)
# # Create list with all users
# all_users_list = db_connection.select_all_usernames()

# print('-----All users list-----')
# print(all_users_list)

# if 'aaa' in all_users_list:
#     print(type(all_users_list))

#######
####### single row ########


# db_connection = SmitDb(AuthDbSchema)
# user_row = db_connection.select_username('dummy_user')

# model_val = AuthModel().get_user('aaa00')

# print('---- model outside ----')
# print(model_val['username'])


# user_model = single_user_model(user_row)

# # print('-----User row-----')
# print(user_row.password)

# for key, value in user_model.items():
#     #pass
#     # if not key.startswith('_'):
#         print(f'key: {key}, value: {value}')

# print('-----User dict-----')
# print(user_row.id)
# print('-----User model-----')
# print(user_model)
#print(user_model.id)


############


########## old ##########

# create_user = AuthDbSchema

# # Smit instance
# smit_db = create_user(
#     username= 'dummy_user',
#     password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
#     email= 'dummy@dummymail.com',
#     sng_username= 'dummy_sng_login',
#     sng_password= 'dummy_sng_password',
#     daymeter= 199996,
#     nightmeter= 199997)

# a = AuthCredentials(db_schema=smit_db)

# print(a.model_dump())

# for name, value in a.db_schema:
#     print(f"{name}: {value}")