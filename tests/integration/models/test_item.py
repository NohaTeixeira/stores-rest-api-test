from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class ItemTest(BaseTest):
    def test_create_item(self):
        # testing if the item can be save to and upload from the db
        with self.app_context():
            StoreModel('test').save_to_db()
            item = ItemModel('test', 9.99, 1) # creates an item

            # check that the item didn't exist in the db
            self.assertIsNone(ItemModel.find_by_name('test'),
                              f"found an item with name {item.name}, but expected none")

            item.save_to_db()

            # check that the item exist in the db
            self.assertIsNotNone(ItemModel.find_by_name('test'),
                                 f"Didnt find an item with name {item.name}, but expected to")

            item.delete_from_db()

            # check that the item didn't exist in the db
            self.assertIsNone(ItemModel.find_by_name('test'),
                              f"found an item with name {item.name}, but expected None")

    def test_store_relationship(self):
        # validates the relationship between ItemModel and StoreModel
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 9.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')
