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
                self.connection = psycopg2.connect(dbname='fast_food-DB',
                                                   user='akram',
                                                   password='12345',
                                                   host='localhost',
                                                   port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            for command in commands:
                self.cursor.execute(command)
        except(Exception, psycopg2.DatabaseError) as error:

            raise error

    