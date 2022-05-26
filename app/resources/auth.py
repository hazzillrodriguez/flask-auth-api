from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace, fields

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app.resources.errors import InternalServerError, EmailAlreadyExistsError, EmailIsInvalidError, PasswordLengthError, UnauthorizedError
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.exts import db
import validators

auth_namespace = Namespace('auth', description='A namespace for authentication')

login_model = auth_namespace.model(
	'Login', {
		'email': fields.String,
		'password': fields.String
	}
)

signup_model = auth_namespace.model(
	'Signup', {
		'email': fields.String,
		'password': fields.String
	}
)

@auth_namespace.route('/login')
class LoginResource(Resource):
	@auth_namespace.expect(login_model)
	def post(self):
		try:
			body = request.get_json()
			user = User.query.filter_by(email=body.get('email')).first()
			if user and check_password_hash(user.password, body.get('password')):
				access_token = create_access_token(identity=user.id)
				refresh_token = create_refresh_token(identity=user.id)
				return jsonify({
					'access_token': access_token, 'refresh_token': refresh_token
				})
			else:
				raise UnauthorizedError

		except UnauthorizedError:
			raise UnauthorizedError

		except Exception as e:
			raise InternalServerError

@auth_namespace.route('/signup')
class SignupResource(Resource):
	@auth_namespace.expect(signup_model)
	def post(self):
		try:
			body = request.get_json()
			email = body.get('email')
			user = User.query.filter_by(email=email).first()
			if user:
				raise EmailAlreadyExistsError

			if not validators.email(email):
				raise EmailIsInvalidError

			if len(body.get('password')) < 6:
				raise PasswordLengthError

			hashed_password = generate_password_hash(body.get('password'))
			db.session.add(User(email=email, password=hashed_password))
			db.session.commit()
			return make_response(jsonify({
				'message': 'Your account has been created.'
			}), 201)
		except EmailAlreadyExistsError:
			raise EmailAlreadyExistsError

		except EmailIsInvalidError:
			raise EmailIsInvalidError

		except PasswordLengthError:
			raise PasswordLengthError

		except Exception as e:
			raise InternalServerError

@auth_namespace.route('/refresh')
class RefreshResource(Resource):
	@jwt_required(refresh=True)
	def post(self):
		current_user = get_jwt_identity()
		new_access_token = create_access_token(identity=current_user)
		return make_response(jsonify({'access_token': new_access_token}), 200)