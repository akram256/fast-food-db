"""
This module provides responses to url requests.
"""
import re
from flask import jsonify, request
from flask.views import MethodView
from api.models.user_model import Databaseconn
from api.models.user_model import Users
from api.models.menu_model import Menu_now
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
import flasgger

class Menu(MethodView):
    """
        this is a class method for items to be added and gotten from the menu
    """

    @flasgger.swag_from("../docs/get_add_items.yml")
    @jwt_required
    def post(self):
        """
            This is a method for posting a food_item on to the menu
        """
        is_admin = Users()
        add_menu = Menu_now()
        user_id = get_jwt_identity()
        
        is_admin_now = is_admin.check_admin(user_id)
        if user_id and is_admin_now :
            key = ("item_name",)
            if not set(key).issubset(set(request.json)):
                return jsonify({'message': 'Your request has Empty feilds'}), 400
       
            if not  request.json['item_name']:
                return jsonify({'message': "The fields should not be empty, Please fill it"}), 400
            new_item_data = add_menu.add_item_to_menu(str(user_id), request.json ['item_name'].strip())

            if new_item_data == 'item already exists on the menu':
                return jsonify({'message': "Sorry, the item already exist on the menu"}), 400
            return jsonify({'message': new_item_data}), 201
        return jsonify({'Alert':"Not Authorised to perform this task"})


    @flasgger.swag_from("../docs/get_all_items.yml")
    def get(self, item_id):
        """
            This method is for getting all food items on the menu
        """
        item_object =Menu_now()
        if item_id is None:
            
            menu = item_object.get_menu()
            if menu == "No items on the menu, items will be added soon":
                return jsonify({"Menu": menu}), 404
            return jsonify({"Menu": menu}), 200