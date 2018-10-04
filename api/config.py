"""
   Module for for defining the configurations
"""  
import os


class Config(object):
    """
       Method for defining the default environment
    """  
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'codeislove'
    # postgresql://username:password@hostname/database


class DevelopmentConfig(Config):
    """
       Method for defining the development environment
    """   
    DEBUG = True
    # TESTING = False
    # ENV = "development"
    # SECRET_KEY = 'codeislove'
    DATABASE_URL = 'postgresql://postgres:12345@localhost/fooddb'


class TestingConfig(Config):
    """
        method for defining the development environment
    """
    DEBUG = True
    TESTING = True
    FLASK_ENV = "TESTING"
    DATABASE_URL = 'postgresql://postgres:@localhost/fastfud'


# configurations = {
#     'default': Config,
#     'development':DevelopmentConfig,
#     'testing': TestingConfig

# }




    
