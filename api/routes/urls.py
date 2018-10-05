"""
This module handels requests to urls.
"""
from flask.views import MethodView
from api.controllers.user_controller import SignUp, Login
from api.controllers.order_controller import PlaceOrder,Getorder,Update,GetSpecific
from api.controllers.menu_controller import Menu
# from models.db_link import linkdb


class Urls(object):
    """
    Class to generate urls
    """
      
    @staticmethod
    def generate_url(app):
        """
         Generates urls on the app context
        :param: app: takes in the app variable
        :return: urls
        """
        app.add_url_rule('/api/v1/auth/signup',
                         view_func=SignUp.as_view('Signup'), methods=['POST',])
        app.add_url_rule('/api/v1/auth/login',
                         view_func=Login.as_view('Login'), methods=['POST',])
        app.add_url_rule('/api/v1/orders',
                         view_func=Getorder.as_view('PlaceOrder'),
                         defaults={'order_id': None}, methods=['GET',])
        app.add_url_rule('/api/v1/orders/<int:order_id>',
                         view_func=Getorder.as_view('one_order'), methods=['GET',])
        app.add_url_rule('/api/v1/orders/<int:order_id>',
                         view_func=Update.as_view('update order'), methods=['PUT',])
        app.add_url_rule('/api/v1/users/orders',
                         view_func=GetSpecific.as_view('get order for specific user'), defaults={'order_id': None, 'user_id':None},methods=['GET',])
        app.add_url_rule('/api/v1/users/orders',
                         view_func=PlaceOrder.as_view('add order'), methods=['POST',])
        app.add_url_rule('/api/v1/menu',
                         view_func=Menu.as_view('add new item'), methods=['POST',])
        app.add_url_rule('/api/v1/menu',
                         view_func=Menu.as_view('get menu'),
                         defaults={'item_id': None}, methods=['GET',])

        
        