"""
This module provides responses to url requests.
"""
import re
from flask import jsonify, request
from flask.views import MethodView
from api.models.user_model import Databaseconn
from api.models.user_model import Users
from api.models.order_model import Order_now
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity


class Getorder(MethodView):
    """
       Class to get all orders
       params: order_id
       respone: json data
    """
    @jwt_required
    def get(self, order_id):
        """
           get method for get order history
           param: route /api/v1/orders and /api/v1/orders/<int:order_id>
           response: json data get_all_orders() and self.get_one_order(order_id)
        """
        new_object = Users()
        new_order = Order_now()

        user_id = get_jwt_identity()
        is_admin = new_object.check_admin(user_id)
        if user_id and  is_admin:
            if order_id is None:
                orders_list = new_order.get_all_orders()
                if orders_list == "No orders available at the moment":
                    return jsonify({"Orders": orders_list}), 404
                return jsonify({"Orders": orders_list}), 200
            
            orders_list = new_order.get_one_order(order_id)
            if orders_list == "No orders available at the moment":
                return jsonify({"Order": "No orders found at the moment for the order_id"}), 404
            return jsonify({"Order": orders_list}), 200
        return jsonify({'Alert':"Not Authorised to perform this task"})

class GetSpecific(MethodView):
    @jwt_required
    def get(self,user_id,order_id=None):
        """
            this method returns orders for a particular user
        """
        specify_order = Order_now()
        user_id = get_jwt_identity()
        if user_id:
            user_list = specify_order.specify_user_order()
            if user_list== "user has not made orders yet":
                return jsonify({"orders":"No orders"}),404
            return jsonify({"orders":user_list}),200
        return jsonify ({"orders":"Not allowed to perform this task"})

class Update(MethodView):
    """
        Class to get all orders
       params: order_status
       respone: json data
    """
    @jwt_required
    def put(self,order_id):
        """
            this method for putting or updating the order_status
        """
        user = Users()
        update_order = Order_now()
        user_id = get_jwt_identity()
        is_admin_now = user.check_admin(user_id)
        if user_id and is_admin_now :
            keys = ("order_now",)
            if not set(keys).issubset(set(request.json)):
                return jsonify({'message': 'Your request has Empty feilds'}), 400

            if request.json["order_now"] == "":
                return jsonify({'Missing status': 'Please update the status'}), 400
            new_order_status = update_order.update_order_status(str(order_id), request.json['order_now'].strip())

            if new_order_status:
                return jsonify({'message': "Order_status has been updated"}), 200
            return jsonify({"message":'No order to update'})
        return jsonify({'Alert':"Not Authorised to perform this task"}),401

class PlaceOrder(MethodView):
    """
        Method for placing an order
    """
    @jwt_required
    def post(self):
        """
            this is a method for placing an order
        """   
        place_order = Order_now ()
        key = ("item_id",)

        if not set(key).issubset(set(request.json)):
            return jsonify({'message': 'Your request has Empty feilds'}), 400
        
        if not  request.json['item_id']:
            return jsonify({'Missing item': 'Please input the item_id'}), 400

        if  request.json['item_id'] == str:
            return jsonify({'Wrong input, You should input a number or int'})
        user_id = get_jwt_identity()
        new_order_data = place_order.place_new_order(str(user_id), request.json ['item_id'])
        if new_order_data:
            return jsonify({'message': new_order_data}), 201
        return jsonify({'message':'item_id does not exit'})
        
        
            

