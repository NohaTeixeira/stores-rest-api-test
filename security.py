import hmac #
from models.user import UserModel

def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username and password.
    :param username: Users's username in sting format.
    :param password: users'un-encrypted password in string format.
    :return: a UserModel object if authentication was successful, None otherwise.
    """

    user = UserModel.find__by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when a user chas already authenticated, and Flask-JWT
    verified their authentication header is correct.
    :param payload: A dict with 'identity' key which is the user id.
    :return: a UserModel object
    """

    user_id = payload['identity']
    user = UserModel.find_by_id(user_id)
