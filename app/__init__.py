from flask import Flask

from flask_restx import Api
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.models import User
from app.exts import db, mail

from app.resources.auth import auth_namespace
from app.resources.reset_password import reset_password_namespace

def create_app():
	app = Flask(__name__)
	# Configuration
	if app.config['ENV'] == 'development':
		app.config.from_object('config.DevelopmentConfig')
	else:
		app.config.from_object('config.ProductionConfig')

	db.init_app(app)
	mail.init_app(app)

	migrate = Migrate(app, db)

	JWTManager(app)
	CORS(app)

	api = Api(app, title='Authentication API', version='1.0', doc='/docs')
	api.add_namespace(auth_namespace, path='/api/v1/auth')
	api.add_namespace(reset_password_namespace, path='/api/v1/')

	@app.shell_context_processor
	def make_shell_context():
		return { 'db': db, 'User': User }

	return app