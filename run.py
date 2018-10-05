"""
This module runs the application
"""

"""
This is the main module
"""
from flask import Flask
from api.routes.urls import Urls
from api.models.database_model import Databaseconn
from api.models.user_model import Users
from flask_jwt_extended import JWTManager
# import flasgger


APP = Flask(__name__)
# flasgger.Swagger(APP)
APP.config.from_object('api.config.DevelopmentConfig')

APP.config['JWT_SECRET_KEY'] = 'codeislove' 
jwt = JWTManager(APP)

@APP.before_first_request
def create_tables():
    table_handler=Databaseconn()
    table_handler.create_tables()
    user = Users()
    user.set_admin(1)



Urls.generate_url(APP)
if __name__ == '__main__':
    
    APP.run()