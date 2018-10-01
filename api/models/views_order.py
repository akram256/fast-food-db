"""
This module provides responses to url requests.
"""
import re
from flask import jsonify, request
from flask.views import MethodView
from api.controllers.db_views import GetAllOrder
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity



class SignUp(MethodView):
    """
       Class contains method plus all signup performances
    """
    def post(self):
        """
           Method for creating new user
           params: json requests
           response: json data
        """
        keys = ("user_name", "email", "password")
        if not set(keys).issubset(set(request.json)):
            return jsonify({'New user': 'Your request has Empty feilds'}), 400

        if request.json['user_name'] == "":
            return jsonify({'user_name': 'enter user_name'}), 400
        if (' ' in request.json['user_name']) == True:
            return jsonify({'message': 'user_name should not contain any spaces'}), 400

        if request.json['email'] == "":
            return jsonify({'email': 'enter email'}), 400

        if (' ' in request.json['email']) == True:
            return jsonify({'message': 'email should not contain any spaces'}), 400

        if request.json['password'] == "":
            return jsonify({'message': 'password should not contain any spaces'}), 400

        if (' ' in request.json['password']) == True:
            return jsonify({'Password': 'Password should not contain any spaces'}), 400

        if len(request.json['password']) < 8:
            return jsonify({'Password': 'Your password should be more than 8 digits'}), 400

        pattern = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
        if not re.match(pattern, request.json['email']):
            return jsonify({'email': 'Enter right format of email thanks'}), 400

        new_user = GetAllOrder()
        user_details = new_user.register_a_user(request.json['user_name'], request.json['email'], request.json['password'])
        if user_details == "email exits friend":
            return jsonify({'message': user_details}), 401

        return jsonify({'message': user_details}), 201


class Login(MethodView):
    """
       Class for logging in the user
    """
    def post(self):
        """
           Method for logging in  user
           params: json requests
           response: json data
        """
        keys = ("email", "password")

        if not set(keys).issubset(set(request.json)):
            return jsonify({'message': 'Your request has Empty feilds'}), 400

        if request.json["email"] == "":
            return jsonify({'message': 'Ennter email'}), 400

        if (' ' in request.json['email']) == True:
            return jsonify({'message': 'email should not contain any spaces'}), 400

        if request.json["password"] == "":
            return jsonify({'message': 'Enter password'}), 400

        login_user = GetAllOrder()
        user_id = login_user.fetch_password(request.json['email'], request.json['password'])

        if user_id:
            return jsonify({
                "access_token" : create_access_token(identity=user_id),
                "message": "User logged in successfully"
            }), 200

        return jsonify({"message": "Wrong username or passwerd"}), 401

class Getorder(MethodView):
    """
       Class to get all orders
       params: order_id
       respone: json data
    """
    def get(self, order_id):
        """
           get method for get order history
           param: route /api/v1/orders and /api/v1/orders/<int:order_id>
           response: json data get_all_orders() and self.get_one_order(order_id)
        """
        if order_id is None:
            order_object = GetAllOrder()
            orders_list = order_object.get_all_orders()
            if orders_list == "No orders available at the moment":
                return jsonify({"Orders": orders_list}), 404
            return jsonify({"Orders": orders_list}), 200

        order_object = GetAllOrder()
        orders_list = order_object.get_one_order(order_id)
        if orders_list == "No orders available at the moment":
            return jsonify({"Order": orders_list}), 404
        return jsonify({"Order": orders_list}), 200
    @jwt_required
    def put(self):
        """
            this method for putting or updating the order_status
        """
        if request.json["order_now"] == "":
            return jsonify({'Missing status': 'Please update the status'}), 400

        user_id = get_jwt_identity()
        order_status = GetAllOrder()
        new_order_status = order_status.update_order_status(str(user_id), request.json['order_status'].strip())

        if new_order_status:
            return jsonify({'message': new_order_status}), 200

    # def get(self, user_id):
    #     """
    #         this method returns orders for a particular user
    #     """
    #     if user_id:
    #         user_object = GetAllOrder()
    #         user_list = user_object.specific_user_order()
    #         if user_list== "user has not made orders yet":
    #             return jsonify({"orders":"No orders"}),404
    #         return jsonify({"orders":user_list}),200


class PlaceOrder(MethodView):
    """
        Method for placing an order
    """
    @jwt_required
    def post(self):
        """
            this is a method for placing an order
        """    
        if not request.json['item_id']:
            return jsonify({'message': "The fields should not be empty, Please fill it"}), 400

        if request.json["item_id"] == "":
            return jsonify({'Missing item': 'Please input the item_id'}), 400

        user_id = get_jwt_identity()
        new_order = GetAllOrder()
        new_order_data = new_order.place_new_order(str(user_id), request.json['item_id'].strip())

        if new_order_data:
            return jsonify({'message': "Hold on, order will be delivered shortly"}), 401
            return jsonify({'message': new_order_data}), 201

class Menu(MethodView):
    """
        this is a class method for items to be added and gotten from the menu
    """

    @jwt_required
    def post(self):
        """
            This is a method for posting a food_item on to the menu
        """
        if not request.json['item_name']:
            return jsonify({'message': "The fields should not be empty, Please fill it"}), 400

        user_id = get_jwt_identity()
     

        new_item = GetAllOrder()
        new_item_data = new_item.add_item_to_menu(str(user_id), request.json['item_name'].strip())

        if new_item_data == 'item already exists on the menu':
            return jsonify({'message': "Sorry, the item already exist on the menu"}), 401
        return jsonify({'message': new_item_data}), 201

    def get(self, item_id):
        """
            This method is for getting all food items on the menu
        """

        if item_id is None:
            item_object = GetAllOrder()
            menu = item_object.get_menu()
            if menu == "No items on the menu, items will be added soon":
                return jsonify({"Menu": menu}), 404
            return jsonify({"Menu": menu}), 200

        # item_object = GetAllOrder()
        # menu = item_object.get_menu(item_id)
        # if menu == "No items on the menu, items will be added soon":
        #     return jsonify({"Menu": menu}), 404
        # return jsonify({"Menu": menu}), 200