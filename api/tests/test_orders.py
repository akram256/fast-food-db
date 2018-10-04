"""
    Module for making tests on the app for sign in
"""
import unittest
import json
import psycopg2
from run import APP
from api.models.user_model import Users
from api.models.order_model import Order_now
from api.models.menu_model import Menu_now
from . import *
import os
class TestViews(unittest.TestCase):
    """"
        Class for making tests on sign in
        params: unittest.testCase
    """

    def setUp(self):
        """
           Method for making the client object
        """
        APP.config.from_object('api.config.TestingConfig')
        self.client = APP.test_client
        with self.client() as client:
            down_tables = Users()
            down_tables.create_tables()
            self.post_token = post_auth_header(client)
            self.get_token = get_auth_header(client)

    def tearDown(self):
        """
           Method for deleting tables in the database object
        """
        with self.client():
            down_tables = Users()
            down_tables.delete_tables()
       
    def test_fetch_all_orders(self):
        """
           Method for testing get all orders by the admin
        """
        result = self.client().post('/api/v1/users/orders' ,content_type="application/json",data=json.dumps(ORDER),headers=self.get_token)
        self.assertEqual(result.status_code, 200)
        result = self.client().get('/api/v1/orders',headers=self.get_token)
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Orders', respond)
        self.assertIsInstance(respond, dict)
    
    def test_get_one_specific_order(self):
        """
            Method for testing to get only one specfic order by the admin
        """
        result = self.client().get('/api/v1/orders/1',content_type="application/json",data=json.dumps(ORDER),headers=self.get_token)
        result2 = self.client().get('/api/v1/orders/a')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result2.status_code, 404)
        self.assertIsInstance(respond, dict)

    def test_get_order_for_specific_user(self):
        """
            Method for testing to get orders for a particular user
        """
        result = self.client().get('/api/v1/users/orders',content_type="application/json",data=json.dumps(ORDER), headers=self.get_token)
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)

    def test_place_an__order(self):
        """
            Method for testing to place an order
        """
        result = self.client().post('/api/v1/users/orders')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)
    
    def test_post_with_an_empty_fields(self):
        """
            Method for testing the post function for empty fields to place an order
        """
        result = self.client().post('/api/v1/users/orders',
                                    content_type="application/json",
                                    data=json.dumps(dict(item_id="")))        
        
        respond = json.loads(result.data.decode("utf8"))
        self.assertIn('msg', respond)        
        self.assertTrue(result.json["msg"])

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
        result = self.client().post('/api/v1/menu',content_type="application/json",data=json.dumps(token_user),)
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code, 401)
        self.assertIsInstance(respond, dict)
    

    def test_updating_order_status(self):
        """
            Method for testing toupdate an order_status by admin
        """
       
        result = self.client().put('/api/v1/orders/1')
        respond = json.loads(result.data.decode("utf8"))
        self.assertEqual(result.status_code,401)
        self.assertIsInstance(respond, dict, )
        
