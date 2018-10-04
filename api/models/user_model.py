"""
This module handlesusers and database
"""
import os
import psycopg2
import datetime
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash




class Users:
    
    """
        This method returns all 
        orders in a JSON format
        :return
    """
    
    def __init__(self):
        """
        This method creates the connection object 
        """
        try:
            from run import APP
            # postgresql://username:password@hostname/database
            if(os.getenv("FLASK_ENV")) == "Production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            elif(APP.config["TESTING"]):
                self.connection = psycopg2.connect('postgresql://postgres:12345@localhost/fastfud')
            else:
                self.connection = psycopg2.connect("postgresql://postgres:12345@localhost/fooddb")
                # self.connection = psycopg2.connect(dbname='fooddb',
                #                                    user='postgres',
                #                                    password='12345',
                #                                    host='localhost',
                #                                    port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            raise error
    

    def create_tables(self):
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
            
            for command in commands:
                self.cursor.execute(command)

        except(Exception, psycopg2.DatabaseError) as error:
            raise error
        

    def delete_tables(self):
        """
            this method is for dropping tables
        """
        table_names=['users','orders','menus']
        for name in table_names:
            self.cursor.execute("DROP TABLE IF EXISTS {} CASCADE".format(name))


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
       
    def get_user_with_id(self, user_id):
        """
           Method for getting an admin
        """

        self.cursor.execute("SELECT * FROM users WHERE user_id = '{}' AND is_admin = True".format(user_id))
        user_now = self.cursor.fetchone()
        return user_now



    