from flask import request
from email_validator import validate_email, EmailNotValidError
from library.main import app
from library.utils import token_required
from library.controller import UserController
from library.response import BadRequest, response_2xx

# register route
@app.route('/signup', methods=['POST'])
def signup_user():
    """
    Creates a new user.
    """ 
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest("email and password are required")
    
    if not data or not data.get('email') or not data.get('password'):
        raise BadRequest("email and password are required")
    
    try:
        validate_email(data.get('email'))
    except EmailNotValidError:
        raise BadRequest("invalid email format")
    
    UserController.signup(data['email'], data['password'])
    
    return response_2xx(message="Sign-up successful", status_code=201)
    

# user login route
@app.route('/login', methods=['POST'])
def login():
    """
    Logs a user. Validates email and password, generates auth token.
    """
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest("email and password are required")
    
    if not data or not data.get('email') or not data.get('password'):
        raise BadRequest("email and password are required")
    
    token = UserController.login(data['email'], data['password'])
    return response_2xx(data={"token": token})
    

@app.route('/hello-world', methods=['GET'])
@token_required
def hello_world(current_user):
    return response_2xx(message=f"Hello {current_user.email}!")

@app.route('/revoke-token', methods=['DELETE'])
@token_required
def revoke_token(current_user):
    """
    Revokes a auth-token
    """
    token = request.headers.get('x-access-token')
    UserController.revoke_token(token)
    return response_2xx(message=f"Token revoked successfully")

@app.route('/refresh-token', methods=['GET'])
@token_required
def refresh_token(current_user):
    """
    Returns new token for a user.
    """
    token = UserController.refresh_token(current_user)
    return response_2xx(data={"token": token})
