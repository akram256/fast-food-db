"""
   Module for for defining the configurations
"""  
import os
class Config(object):
    """
       Method for defining the default environment
    """  
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'codeislove'

class DevelopmentConfig(Config):
    """
       Method for defining the development environment
    """   
    DEBUG = True
    TESTING = True
    ENV = "development"
    SECRET_KEY = 'codeislove'
<<<<<<< HEAD
class TestingConfig(Config):
    """
        method for defining the development environment
    """
    if os.getenv("Testing"):
        DATABASE_URL = 'postgres://postgres@host/fooddb'
    DEBUG = True
    TESTING = True
    ENV = "TESTING"
    SECRET_KEY = 'codeislove'
    DATABASE ='fooddb'




    
