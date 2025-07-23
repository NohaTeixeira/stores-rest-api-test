from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password.
    """
    parser = reqparse.RequestParser() #It’s a tool that helps extract and validate data sent in an HTTP request (usually POST or PUT).It ensures that the data the client sends meets certain rules before your app processes it.
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self): #creating a user if the user is not already exist
        data = UserRegister.parser.parse_args() # returns a dictionary-like object. / an argument is a value that is passed to a function when the function is called

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists.'}, 400

        user = UserModel(**data) # This creates a new UserModel object using the data dictionary. Unpacking a dictionary means breaking it apart and passing its key-value pairs into a function or class — automatically matching keys to parameter names.
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
