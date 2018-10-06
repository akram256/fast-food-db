"""
    Module for making tests on the app for sign in
"""
import unittest
import json
import psycopg2
from run import APP
from api.models.database_model import Databaseconn
from api.models.user_model import Users
from api.models.order_model import Order_now
from api.models.menu_model import Menu_now
from api.config import TestingConfig
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
            down_tables = Databaseconn()
            down_tables.create_tables()
            self.post_token = post_auth_header(client)
            self.get_token = get_auth_header(client)
            create_menu(client, self.post_token)

    def tearDown(self):
        """
           Method for deleting tables in the database object
        """
        with self.client():
            down_tables = Databaseconn()
            down_tables.delete_tables()

    def test_post_with_an_empty_without_a_token(self):
        """
            Method for testing the post function for checking a token
        """
        result = self.client().post('/api/v1/users/orders',
                                    content_type="application/json",
                                    data=json.dumps(dict(item_id="")))        
        
        respond = json.loads(result.data.decode("utf8"))
        self.assertIn('msg', respond)        
        self.assertTrue(result.json["msg"])

    def test_place_an__order(self):
        """
            Method for testing to place an order
        """
        result = self.client().post('/api/v1/users/orders',data=json.dumps(ORDER),headers=self.post_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 201)
        self.assertIn('message', respond)
        self.assertIsInstance(respond, dict)
    
    def test_adding_an_existing_item_on_menu(self):
        """
            Method for testing to add an item on to the menu by admin
        """
        result = self.client().post('/api/v1/menu',data=json.dumps(MENU_ITEM2),headers=self.post_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 400)
        self.assertIn('message', respond)
        self.assertIsInstance(respond, dict)


    def test_adding_an_item_on_menu(self):
        """
            Method for testing to add an item on to the menu by admin
        """
        result = self.client().post('/api/v1/menu',data=json.dumps(MENU_ITEM3),headers=self.post_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 201)
        self.assertIsInstance(respond, dict)
    
    def test_updating_with_empty_order_status_fields(self):
        """
            Method for testing to updating empty fields
        """
       
        result = self.client().put('/api/v1/orders/1', data=json.dumps(ORDER_NOW), headers=self.post_token)
        respond = json.loads(result.data.decode("utf8"))
        print(respond)
        self.assertEqual(result.status_code,400)
        self.assertIn('Missing status', respond)
        self.assertTrue(['Missing status'], 'order not updated')
        self.assertIsInstance(respond, dict, )

    def test_updating_order_status(self):
        """
            Method for testing to update an order_status by admin
        """
       
        result = self.client().put('/api/v1/orders/2', data=json.dumps(ORDER_STATUS), headers=self.post_token)
        respond = json.loads(result.data.decode("utf8"))
        print(respond)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(['message'], 'order has been updated' )
        self.assertIn('message', respond)
        self.assertIsInstance(respond, dict, )


    def test_fetch_all_orders(self):
        """
           Method for testing get all orders by the admin
        """
        result = self.client().get('/api/v1/orders',headers=self.get_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 401)
        self.assertIn('msg', respond)
        self.assertIsInstance(respond, dict)

    def test_getting_one_order(self):
        """
            This method tests for getting one order 
        """
        result = self.client().get('/api/v1/orders/1',headers=self.get_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 401)
        self.assertIn('msg', respond)
        self.assertIsInstance(respond, dict)

    def test_getting_all_items_on_the_menu(self):
        """
            This method tests for getting all items from the menu
        """
        result = self.client().get('/api/v1/menu',headers=self.get_token)
        respond = json.loads(result.data.decode("utf8"))
        print(str(respond))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Menu', respond)
        self.assertIsInstance(respond, dict)


    