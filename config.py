import os

class BaseConfig(object):
	SECRET_KEY = 'o\xadlT\x97\x82\x1e[\xc6aeFv\x90\xdc\xcc'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'localhost'
	MAIL_PORT = 1025
	MAIL_USERNAME = 'customersupport@demo.com'
	MAIL_PASSWORD = ''

class TestConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin@localhost/flask_auth_api'

class ProductionConfig(BaseConfig):
	DEBUG = False