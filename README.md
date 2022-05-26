# Flask Authentication API

[![Actions Status](https://github.com/hazzillrodriguez/flask-auth-api/workflows/Run%20Tests/badge.svg)](https://github.com/hazzillrodriguez/flask-auth-api/actions)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

This project was created for anyone looking for an Authentication API with a reset password feature.

## Installation

These instructions will get you a copy of the project up and running on your local machine.

1. Git clone or download the project files.
```
git clone https://github.com/hazzillrodriguez/flask-auth-api.git
cd flask-auth-api
```

2. Create and activate the virtual environment then install requirements.
```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```

3. Set the environment variables.
```
export FLASK_APP=run
export FLASK_ENV=development
```

4. Start Postgres or SQL Server database and update `SQLALCHEMY_DATABASE_URI` in `config.py`.
```
SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin@localhost/flask_auth_api'
```

5. Create the database.
```
flask shell
db.create_all()
```

6. Start the development web server.
```
flask run
```

This project contains a Swagger UI.

To view this API's Swagger UI, run this application, then navigate to `http://localhost:5000/docs`.<br>
You can test out this API entirely from the Swagger UI page.

## API Documentation

### Login and Sign up

- POST **/api/v1/auth/signup**

    Register a new user.<br>
    The body must contain a JSON object that defines the `email`, and `password` fields.<br>
    On success, a status code 201 (created) is returned.

    example:<br>
    ```
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"john@demo.com","password":"123456"}' http://127.0.0.1:5000/api/v1/auth/signup
    ```

- POST **/api/v1/auth/login**

    Log in and acquire token.<br>
    The body must contain a JSON object that defines the `email` and `password` fields.<br>
    On success, a status code 200 is returned. The body of the response contains a JSON object with `access_token` and `refresh_token`.

    example:<br>
    ```
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"john@demo.com","password":"123456"}' http://127.0.0.1:5000/api/v1/auth/login
    ```

### Refresh Token

- POST **/api/v1/auth/refresh**

    Acquire a refresh token.<br>
    Once you have logged in you will get a `refresh_token`, paste it under the authorization tab, and select bearer token.

    example:<br>
    ```
    curl -i -X POST http://127.0.0.1:5000/api/v1/auth/refresh \
        -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NzE3Nzg4OSwianRpIjoiOGUwMmQ3NzQtNDNmOC00YmY5LWExNDEtMDQ4ZDE2MTIzMjliIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjUsIm5iZiI6MTY0NzE3Nzg4OSwiZXhwIjoxNjQ5NzY5ODg5fQ.-36JvwwqL5DfOyNDPVeigxOpjyr0UqY61r94kZ0fk-E"
    ```

### Reset Password

#### Create a local SMTP server to test the email feature

Start an SMTP server in a new terminal.<br>
```
python -m smtpd -n -c DebuggingServer localhost:1025
```

**Note:** It does not send the email out to the target email server, it just discards the email and prints out the email content on the console. If you want to send an email to your SMTP server like Gmail, update the `MAIL_SERVER` configuration in `config.py`.

- POST **/api/v1/forgot-password**

    Request for a password reset.<br>
    The body must contain a JSON object that defines the `email` field.<br>
    On success, a status code 200 is returned.

    example:<br>
    ```
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"john@demo.com"}' http://127.0.0.1:5000/api/v1/forgot-password
    ```

    If the email is of the existing user, you can see the email in the terminal running the SMTP server as:

    ```html
    <p>Dear, User</p>
    <p>
        To reset your password
        <a href="http://localhost:3000/reset/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzgzOTU0ODUsIm5iZiI6MTU3ODM5NTQ4NSwianRpIjoiZTEyZDg3ODgtMTkwZS00NWI1LWI0YzYtZTdkMTYzZjc5ZGZlIiwiZXhwIjoxNTc4NDgxODg1LCJpZGVudGl0eSI6IjVlMTQxNTJmOWRlNzQxZDNjNGYwYmNiYiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.dLJnhYTYMnLuLg_cHDdqi-jsXeISeMq75mb-ozaNxlw">
            click here
        </a>.
    </p>
    <p>Alternatively, you can paste the following link in your browser's address bar:</p>
    <p>http://localhost:3000/reset/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzgzOTU0ODUsIm5iZiI6MTU3ODM5NTQ4NSwianRpIjoiZTEyZDg3ODgtMTkwZS00NWI1LWI0YzYtZTdkMTYzZjc5ZGZlIiwiZXhwIjoxNTc4NDgxODg1LCJpZGVudGl0eSI6IjVlMTQxNTJmOWRlNzQxZDNjNGYwYmNiYiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.dLJnhYTYMnLuLg_cHDdqi-jsXeISeMq75mb-ozaNxlw</p>
    <p>If you have not requested a password reset simply ignore this message.</p>
    <p>Sincerely</p>
    <p>Support Team</p>
    ```

    As you can see the URL format is:<br>
    `http://localhost:3000/reset-password/<reset_token>`, you need to copy this token and send it manually in your `/api/v1/reset-password` endpoint.

- POST **/api/v1/reset-password**

    Reset password.<br>
    The body must contain a JSON object that defines the `password` and `reset_token` fields.<br>
    Paste the `reset_token` you received in the `reset_token` field.<br>
    On success, a status code 200 is returned.

    example:<br>
    ```
    curl -i -X POST -H "Content-Type: application/json" -d '{"password":"user123","reset_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MzU1MTc5OSwianRpIjoiMzYyZmQwNGItNWQ0OC00ZGIwLTg0ZDktOTM3ZGI4M2U3ZDU4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2NTM1NTE3OTksImV4cCI6MTY1MzU5NDk5OX0.67U8rpyx5kWY9qy0zuLTbOBR0ji9gZS6JOGnJ1XIX-0"}' http://127.0.0.1:5000/api/v1/reset-password
    ```

    You should also get an email stating your password was reset successfully.

    ```html
    <p>Password reset was successful!</p>
    ```

## Running the Tests

To run all the tests at once, use the command:
```
python -m pytest -v
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Hazzill Rodriguez — [LinkedIn](https://www.linkedin.com/in/hazzillrodriguez/) — hazzillrodriguez@gmail.com

## Acknowledgments

* [Ssali Jonathan — Build a Full-Stack web app with Flask and ReactJS](https://www.youtube.com/watch?v=5aDfgcI8MHM&list=PLEt8Tae2spYkfEYQnKxQ4vrOULAnMI1iF)
* [Paurakh Sharma Humagain — Flask Rest API - Zero to Yoda](https://dev.to/paurakhsharma/series/3672)