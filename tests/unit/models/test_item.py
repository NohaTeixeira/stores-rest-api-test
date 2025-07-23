from tests.unit.unit_base_test import UnitBaseTest
from models.item import ItemModel

class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel("Test Name", 9.99, 1)

        self.assertEqual(item.name, "Test Name","The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 9.99, "The price of the item after creation does not equal the constructor argument.")
        self.assertIsInstance(item.price, float)
        self.assertEqual(item.store_id, 1, "The store_id of the item after creation does not equal the constructor argument.")
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel("Test Name", 9.99, 1)
        expected = {'name': 'Test Name', 'price': 9.99}

        self.assertEqual(item.json(), expected,
                         f"The JSON export of the item is incorrect. Received {item.json()} expected {expected}")
