from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
    code = 500
    description = "Something went wrong"

class EmailAlreadyExistsError(HTTPException):
    code = 400
    description = "User with given e-mail address already exists"

class EmailDoesnotExistsError(HTTPException):
    code = 400
    description = "Couldn't find the user with given e-mail address"

class EmailIsInvalidError(HTTPException):
    code = 400
    description = "E-mail address is invalid"

class PasswordLengthError(HTTPException):
    code = 400
    description = "Password must be at least 6 characters"

class BadTokenError(HTTPException):
    code = 403
    description = "Invalid token"

class ExpiredTokenError(HTTPException):
    code = 401
    description = "Expired token"

class UnauthorizedError(HTTPException):
    code = 401
    description = "E-mail address or password is incorrect"