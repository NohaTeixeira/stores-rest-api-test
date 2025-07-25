from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test','abcd' )

        self.assertEqual(user.username, 'test', "The username 'test' was not created")
        self.assertEqual(user.password, 'abcd', "The password 'abcd' was not created")
