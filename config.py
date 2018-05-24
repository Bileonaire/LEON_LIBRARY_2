"""Contains various settings for each process of development
"""
import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testing.db')

class Config(object):
    """Base class with all the constant config variables"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "!@#_)&^%$$epic8^%%$#@#%^&*(&^&"


class TestingConfig(Config):
    """Contains additional config variables required during testing"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1Lomkones.@localhost/library_testing'


class DevelopmentConfig(Config):
    """Contains additional config variables required during development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1Lomkones.@localhost/LEON-LIBRARYV2'

class ProductionConfig(Config):
    """Contains additional config variables required during production"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1Lomkones.@localhost/LEON-LIBRARYV2'    
