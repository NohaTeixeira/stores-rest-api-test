from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
from db import db

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [], "The store's items length was not 0 even though no items were added")

    def test_writing_and_saving_to_db(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'), f"found a store with name {store.name}, but expected none")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'),f"Didnt find an item with name {store.name}, but expected to")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'), f"found a store with name {store.name}, but expected none")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 9.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1) #store.items.count() executes a database query to count how many items are linked to this store.Checks that the store has exactly one item associated with it.
            self.assertEqual(store.items.first().name, "test_item")

    def test_store_json_without_an_item(self):
        with self.app_context():
            store = StoreModel('test')
            expected = {
                "name": "test",
                "items": []
            }

        self.assertDictEqual(store.json(), expected, f"The JSON export of the store is incorrect. Received {store.json()} expected {expected}")

    def test_store_json_with_an_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 9.99, 1)

            # Save both store and item to the database
            store.save_to_db()
            item.save_to_db()

            # Commit the session to ensure changes are saved to the database
            db.session.commit()

            # Refresh the store to ensure it's attached to the session and relationships are loaded
            db.session.refresh(store)

            # Expected output with the item correctly linked to the store
            expected = {
                "name": "test",
                "items": [{"name": "test_item", "price": 9.99}]
            }

            # Assert that the store's JSON matches the expected result
            self.assertDictEqual(store.json(), expected, f"The JSON export of the store is incorrect. Received {store.json()} expected {expected}")
