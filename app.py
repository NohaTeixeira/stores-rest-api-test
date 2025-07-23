import os

from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
import hmac

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from models.user import UserModel  # <-- needed to validate user in /auth
app = Flask(__name__)
app.config['DEBUG'] = True

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'noha123'
app.config['JWT_SECRET_KEY'] = "your_secret_key"


# JWT and API setup
jwt = JWTManager(app)
api = Api(app)

#api setup
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# ✅ /auth endpoint
@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json() # 1. Get JSON data from the incoming POST request body
    username = data.get('username')  # 2. Extract the 'username' value from the JSON
    password = data.get('password')  # 3. Extract the 'password' value from the JSON

    user = UserModel.find_by_username(username) # 4. Look up a user in the database by that username

    # 5. If a user is found and the password matches (using secure comparison):
    if user and hmac.compare_digest(user.password, password):
        access_token = create_access_token(identity=user.id) # 6. Create a JWT access token for that user ID
        return jsonify(access_token=access_token), 200 # 7. Return the token as JSON with HTTP 200 OK

    # 8. If username not found or password doesn't match, return error message with HTTP 401 Unauthorized
    return jsonify({"message": "Invalid credentials"}), 401

from flask_jwt_extended.exceptions import JWTExtendedException

@app.errorhandler(JWTExtendedException)
def auth_error_handler(err): #error handler endpoint in flask, when ever a jwterror is raised inside of our application the off error handler will be called then we return a message
    return jsonify({'message': 'could not authorize. Did you include a valid Authorization header?'}), 401 #jsonfiy was entered to make sure we can send the message

#db init
if __name__ == '__main__':
    from db import db

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port=5000, debug=True)
