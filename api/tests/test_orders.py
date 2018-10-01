"""
    Module for making tests on the app for sign in
"""
import unittest
import json
from api.run import APP
class TestViews(unittest.TestCase):
    """"
        Class for making tests on sign in
        params: unittest.testCase
    """

    def setUp(self):
        """
           Method for making the client object
        """
        self.client = APP.test_client

    def test_fetch_all_orders(self):
        """
           Method for testing get all orders by the admin
        """
        result = self.client().get('/api/v1/orders')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 404)
        self.assertIn('Orders', respond)
        self.assertIsInstance(respond, dict)
    
    def test_get_one_specific_order(self):
        """
            Method for testing to get only one specfic order by the admin
        """
        result = self.client().get('/api/v1/orders/1')
        result2 = self.client().get('/api/v1/orders/a')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result2.status_code, 404)
        self.assertIsInstance(respond, dict)

    def test_place_an__order(self):
        """
            Method for testing to place an order
        """
        result = self.client().post('/api/v1/users/orders')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)

    # def test_get_orders__for_specific_user(self):
    #     """
    #         Method for testing to get all orders for a specfic user
    #     """
    #     result = self.client().get('/api/v1/users/orders')
    #     respond = json.loads(result.data.decode("utf8"))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('orders', respond)
    #     self.assertIsInstance(respond, dict)

    def test_get_menu(self):
        """
            Method for testing to get the menu
        """
        result = self.client().get('/api/v1/menu')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Menu', respond)
        self.assertIsInstance(respond, dict)

    def test_adding_an_item_on_menu(self):
        """
            Method for testing to add an item on to the menu by admin
        """
        result = self.client().post('/api/v1/menu')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)

    def test_updating_order_status(self):
        """
            Method for testing toupdate an order_status by admin
        """
        result = self.client().put('/api/v1/orders/1')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)