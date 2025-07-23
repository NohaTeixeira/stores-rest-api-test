from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self): #request to our api test client
        with self.app() as client:
            with self.app_context(): #we need it because our methods are saving and retrieving to db (register)
                response = client.post(
                    '/register',
                    data=json.dumps({'username': 'test', 'password': '<1234>'}), #json.dumps(...) converts your Python dictionary to a JSON string.
                    content_type='application/json') #content_type='application/json' sets the correct HTTP header. it teel a web server what a type of data we send - json
                 #sending a post request to our actual API and its received by our post method inside of UseRegistered class and run through it.

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data)) #This is the actual response returned by the Flask API.
                                                                                                 # request.data returns the raw response body (in bytes).
                                                                                   # json.loads(...) converts that raw JSON string into a Python dictionary so it can be compared.

    def test_registered_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data=json.dumps({'username': 'test', 'password': '<1234>'}),
                            content_type='application/json')
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '<1234>'}),
                                           headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys()) #It checks whether the 'access_token' exists in the response dictionary.


    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data=json.dumps({'username': 'test', 'password': '<1234>'}),
                            content_type='application/json')
                response = client.post(
                    '/register',
                    data=json.dumps({'username': 'test', 'password': '<1234>'}),
                    content_type='application/json')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'User already exists.'}, json.loads(response.data))
