"""
This module runs the application
"""

"""
This is the main module
"""
from flask import Flask
from api.routes.urls import Urls
from flask_jwt_extended import JWTManager


APP = Flask(__name__)
APP.config.from_object('api.config.DevelopmentConfig')

APP.config['JWT_SECRET_KEY'] = 'codeislove' 
jwt = JWTManager(APP)

APP.env = 'development'
APP.testing = True

Urls.generate_url(APP)
if __name__ == '__main__':
    
    APP.run(debug = True)