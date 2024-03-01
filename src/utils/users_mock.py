"""Mock users for setup and testing."""
from typing import List

def valid_users() -> List[dict[str, str]]:
    """Return a dictionary of valid user data.

    Returns:
        List[dict[str, str]]: A list of dictionaries containing valid user data.
    """
    user1: dict[str, str] = {
        "username": "dummy_user",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$NxWNf7Vxcwv3I25r6T9TZQ$aSw0+lmoZPsaildOr93ted9qR/UQ3moG5pokYb9HEZo",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    user2: dict[str, str] = {
        "username": "dummy_user2",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$5pD+VDlNiib9xXyn8l4n9g$+L5Y8qWw4Y6EriSlIeYlXpIfUiHedtZkblDNEBv3jc8",
        "email": "dummy2@dummymail.com",
        "sng_username": "dummy2_sng_login",
        "sng_password": "dummy2_sng_password",
        "daymeter": "199994",
        "nightmeter": "199995",
    }
    user3: dict[str, str] = {
        "username": "aaaaa",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$zst3ATBqGuOhZaCTrORTXg$r7yDUiaNbS4GdHiCL8aUaT/whJ3j1PIbryc8CGyD5N0",
        "email": "a@a.com",
        "sng_username": "aaaaa",
        "sng_password": "dummy2_sng_password",
        "daymeter": "123123",
        "nightmeter": "123123",
    }

    good_users: List[dict[str, str]] = [user1, user2, user3]
    return good_users

def invalid_users() -> List[dict[str, str]]:
    """Return a dictionairy of invalid user data.

    Returns:
            List[dict[str, str]]: A list of dictionaries representing invalid users.
    """
    all_errors: dict[str, str] = {
        "username": "df",
        "password": "",
        "email": "dummydummymail.com",
        "sng_username": "du",
        "sng_password": "du",
        "daymeter": "string",
        "nightmeter": "199",
    }
    no_username: dict[str, str] = {
        "username": "",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    short_username: dict[str, str] = {
        "username": "abc",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    empty_pwd: dict[str, str] = {
        "username": "dummy_user",
        "password": "",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    meter_string: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "morethansix",
        "nightmeter": "199996",
    }
    meter_short: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "123",
        "nightmeter": "199996",
    }
    mail_invalid: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummydummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199997",
        "nightmeter": "199996",
    }
    sng_user_short: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "sng",
        "sng_password": "dummy_sng_password",
        "daymeter": "199997",
        "nightmeter": "199996",
    }
    bad_users: List[dict[str, str]] = [
        all_errors,
        no_username,
        short_username,
        empty_pwd,
        mail_invalid,
        meter_string,
        meter_short,
        sng_user_short,
    ]
    return bad_users


############# Debug ################
# from api.schemas import UserCreateSchema

# testlist = valid_test()

# for each in testlist:
#     user = UserCreateSchema.model_validate(each)
#     print(user)