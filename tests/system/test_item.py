from http.client import responses

from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp() #is calling the setUp() method from the parent class (BaseTest), so that any logic defined there runs before adding more setup code in the child class (ItemTest).
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()

                # Authenticates the user and gets a JWT token.
                auth_request = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'content-type': 'application/json'})  # Headers are key-value pairs sent along with every HTTP request or response. They provide extra information about the request or the response — like who the user is, what kind of data is being sent, or how it should be interpreted.

                # Extracts the token from the login response.
                auth_token = json.loads(auth_request.data)['access_token']

                # Prepares headers with the token.
                self.access_token = f'Bearer {auth_token}'
                self.headers = {'Authorization': self.access_token}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

            self.assertEqual(response.status_code, 401) #401=Unauthorized

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers=self.headers) #self.headers includes the JWT access token in the Authorization header — which tells the server:"This request is from a logged-in (authenticated) user."
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test',
                                      headers=self.headers)

                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.delete('/item/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test',
                                       data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       content_type='application/json',
                                       headers=self.headers)

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.post('/item/test',
                                       data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       content_type='application/json',
                                       headers=self.headers)

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test',
                                      data=json.dumps({'price': 19.99, 'store_id': 1}),
                                      content_type='application/json',
                                      headers=self.headers)

                self.assertEqual(response.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99) #This calls your model method to retrieve the item named 'test' from the database.
                self.assertDictEqual({'name': 'test', 'price': 19.99},
                                     json.loads(response.data))


    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)

                response = client.put('/item/test',
                                      data=json.dumps({'price': 19.99, 'store_id': 1}),
                                      content_type='application/json',
                                      headers=self.headers)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price,19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test', 'price': 19.99}]},
                                     json.loads(response.data))
