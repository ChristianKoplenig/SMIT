"""Deleted code from db.smitdb.py
"""
    
    # Auth table specific methods
    # def init_auth(self) -> None:
    #     """
    #     Initializes the Smit auth table by creating the table and adding a dummy user.

    #     This method creates the necessary tables in the database for authentication purposes
    #     and adds a dummy user for testing purposes.
    #     """
    #     self.create_table()
    #     self.create_dummy_user()
        
    # def create_dummy_user(self) -> None:
    #     """
    #     Create a dummy user in the Smit auth table.
    #     """
    #     dummy = self.db_schema(
    #         username= 'dummy_user',
    #         password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
    #         email= 'dummy@dummymail.com',
    #         sng_username= 'dummy_sng_login',
    #         sng_password= 'dummy_sng_password',
    #         daymeter= '199996',
    #         nightmeter= '199997')

    #     with Session(self.engine) as session:
    #         session.add(dummy)
    #         session.commit()
            
    #     self.backend.logger.debug('Created dummy user in authentication table')

    # def create_user(self, username: str,
    #                 password: str,
    #                 email: str = None,
    #                 sng_username: str = None,
    #                 sng_password: str = None,
    #                 daymeter: int = None,
    #                 nightmeter: int = None) -> None:
    #     """
    #     Write a user to the Smit auth table.
    #     The input will be validated against the database authentication table schema.

    #     Parameters
    #     ----------
    #     username : str
    #         The username of the user.
    #     password : str
    #         The password of the user.
    #     email : str, optional
    #         The email of the user (default is None).
    #     sng_username : str, optional
    #         The energy provider username of the user (default is None).
    #     sng_password : str, optional
    #         The energy provider password of the user (default is None).
    #     daymeter : int, optional
    #         The day meter value of the user (default is None).
    #     nightmeter : int, optional
    #         The night meter value of the user (default is None).
    #     """
    #     user = self.db_schema(
    #         username= username,
    #         password= password,
    #         email= email,
    #         sng_username= sng_username,
    #         sng_password= sng_password,
    #         daymeter= daymeter,
    #         nightmeter= nightmeter)
        
    #     try:
    #         with Session(self.engine) as session:
    #             self.db_schema.model_validate(user)
    #             session.add(user)
    #             session.commit()
                
    #         self.backend.logger.info('Created user %s in authentication table', user.username)
        
    #     except ValidationError as e:
    #         raise AuthValidateError from e
           
    # def select_username(self, value: str) -> tuple:
    #     """
    #     From authentication table select one row by username.

    #     Parameters:
    #     - value (str): The value to search for in the 'username' column.

    #     Returns:
    #     - tuple: None or the selected row as tuple with columns as elements.
    #     """
    #     with Session(self.engine) as session:
    #         statement = select(self.db_schema).where(self.db_schema.username == value)
    #         select_row = session.exec(statement).one()
            
    #         if select_row is not None:
    #             return select_row
            
    #         return None
            
    # def select_all_usernames(self) -> list:
    #     """
    #     From authentication table select all usernames.

    #     Returns:
    #         list: All usernames from the authentication table.
    #     """
    #     with Session(self.engine) as session:
    #         statement   = select(self.db_schema.username)
    #         all_usernames: list = session.exec(statement).all()
    #         return all_usernames

