"""
This module handles orders
"""
import os
import psycopg2
import datetime
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash




class GetAllOrder(MethodView):
    
    """
        This method returns all 
        orders in a JSON format
        :return
    """
    
    def __init__(self):
        """
        This method creates tables in the PostgreSQL database.
        It connects to the database and creates tables one by one
        for command in commands:
        cur.execute(command)
        """
        commands = (
            """
            CREATE TABLE if not exists "users" (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(80) NOT NULL,
                    is_admin BOOLEAN NULL DEFAULT TRUE
                    
                )
            """,
            """
            CREATE TABLE if not exists "menus" (
                    item_id SERIAL PRIMARY KEY,
                    item_name VARCHAR (255) NOT NULL,
                    user_id integer,
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id),
                    item_date TIMESTAMP DEFAULT NOW()
                    
                    
                )
            """,
            """
            CREATE TABLE if not exists "orders" (
                    order_id SERIAL PRIMARY KEY,
                    order_now VARCHAR (255) DEFAULT 'New',
                    user_id integer,
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id),
                    item_id integer,
                    FOREIGN KEY (item_id)
                    REFERENCES menus(item_id),
                    order_date TIMESTAMP DEFAULT NOW()
                    
                    
          
                )
            """,)

        try:
            if(os.getenv("FLASK_ENV")) == "Production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            else:
                self.connection = psycopg2.connect(dbname='fooddb',
                                                   user='postgres',
                                                   password='12345',
                                                   host='localhost',
                                                   port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            for command in commands:
                self.cursor.execute(command)
        except(Exception, psycopg2.DatabaseError) as error:

            raise error

    def register_a_user(self, username, email, password):
        """
           Method for registering a user
        """
  

        self.cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        check_email = self.cursor.fetchone()
        hashed_password = generate_password_hash(password, method='sha256')
        if check_email:
            return "This email already exists, Please use another email"

        insert_user = "INSERT INTO users(username, email, password) VALUES('"+username+"', '"+email+"', '"+hashed_password+"')"
        self.cursor.execute(insert_user)
        return "Account successfully created, Please login "

    def fetch_password(self, email, password):
        """
           Method for fetching the user_password
        """
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            if user[2] == email and check_password_hash(user[3], password):
                return user[0]
        return None  

    def get_all_orders(self):
        """
           Method for getting all orders
        """
        order_query= "SELECT * FROM orders"
        self.cursor.execute(order_query)
        keys = ["order_id", "order_now","user_id","item_id" ,"order_date"]
        orders = self.cursor.fetchall()
        order_list = []
        for order in orders:
            order_list.append(dict(zip(keys, order)))
        if not order_list:
            return "No orders available at the moment"
        return order_list

    def get_one_order(self, inserted_order_id):
        """
           Method for getting a specific order using an inserted_order_id
        """
        self.cursor.execute("SELECT * FROM orders WHERE order_id = %s", [inserted_order_id])
       

        keys = ["order_id", "user_id", "item_id","order_now", "order_date"]
        order = self.cursor.fetchone()
        if not order:
            return "Order not available at the moment"

    def update_order_status(self,order_id,order_now):
        """
             this is a method for updating an order_status
        """
        self.cursor.execute("SELECT * FROM orders WHERE order_id = '%s'" % order_id)
        check_status = self.cursor.fetchone()
        if not check_status:
            return "No order"
        put_status_query = "UPDATE  orders SET order_now = %s WHERE order_id = %s;"
        self.cursor.execute(put_status_query,(order_now,order_id, ))
        update_status = self.cursor.rowcount
        return jsonify ({'message':update_status})


    def specify_user_order(self):
        """
            this method is for getting orders for a specific user
        """
        order_query_user= "SELECT * FROM orders"
        self.cursor.execute(order_query_user)
        keys =["order_id","user_id","item_id","item_name"]
        orders = self.cursor.fetchall()
        specfic_list = []
        for order in orders:
            specfic_list.append(dict(zip(keys, order)))
        if not specfic_list:
            return "user has not made orders yet"
        return specfic_list
        
    def place_new_order(self, user_id, item_id):
        """
           Method for placing an order
           params: order_now
        """
       
        self.cursor.execute("SELECT * FROM orders WHERE item_id= %s",(item_id, ) )
        data=self.cursor.fetchone()
        print(data)
        add_order_query = "INSERT INTO orders(user_id, item_id) VALUES( %s,%s);"

        self.cursor.execute(add_order_query,(user_id,item_id,))
        return "Order has been Placed successfully"

    def add_item_to_menu(self, user_id, item_name):

        self.cursor.execute("SELECT * FROM menus WHERE item_name = %s",[item_name])
        check_item_on_menu = self.cursor.fetchone()
        if check_item_on_menu:
            return 'item already exists on the menu'
        add_item_query = "INSERT INTO menus(user_id,item_name) VALUES('"+user_id+"','"+item_name+"')"
        self.cursor.execute(add_item_query)
        return "Meal has been successfully added to the menu"
        
        
    def get_menu(self):
        """
           Method for getting the menu by an admin
        """
        item_query= "SELECT * FROM menus"
        self.cursor.execute(item_query)
        keys = ["item_id","item_name" ]
        menus = self.cursor.fetchall()
        menu_list = []
        for item in menus:
            menu_list.append(dict(zip(keys, item)))
        if not menu_list:
            return "No items on the menu, items will be added soon"
        return menu_list