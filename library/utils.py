import jwt
import logging
from datetime import datetime, timedelta
from flask import request
from functools import wraps
from library.main import app, db
from library.models import User, TokenData
from library.response import BadRequest, UnauthorizedError

SECRET_KEY = app.config['SECRET_KEY']
TOKEN_ALGO = 'HS256'
TOKEN_EXPIRY_DAYS = app.config['TOKEN_EXPIRY_DAYS']
TOKEN_EXPIRY_HOURS = app.config['TOKEN_EXPIRY_HOURS']
TOKEN_EXPIRY_MIN = app.config['TOKEN_EXPIRY_MIN']


def generate_token(user):
    created_at = int(datetime.now().timestamp())
    try:
        #Saving TokenData to handle revoking of token
        token_data = TokenData(created_at=created_at)
        db.session.add(token_data) 
        db.session.commit()
    except Exception as e:
        logging.error("Error in creating TokenData. Exception: {e}")
        raise Exception()

    payload = {
        'public_id': user.public_id,
        'created_at': created_at,
        'id': token_data.id,
    }
    token = jwt.encode(payload, SECRET_KEY, TOKEN_ALGO) 

    return token

def revoke_token(tokendata_id):
    """
    Revokes token by marking is_revoked=True in TokenData against the token
    """
    try:
        token_data = TokenData.query.filter_by(id=tokendata_id).first()
    except Exception as e:
        logging.error(f"Error in getting token data from db. Exception: {e}")
        raise Exception()
    
    if not token_data:
        raise BadRequest(message="Invalid token")
    
    try:
        token_data.is_revoked = True
        db.session.add(token_data) 
        db.session.commit()
    except Exception as e:
        logging.error(f"Error in updating token data from db. Exception: {e}")
        raise Exception()

def is_expired(created_at):
    created_at_datetime = datetime.fromtimestamp(created_at)
    expiry_duration = timedelta(days=TOKEN_EXPIRY_DAYS, hours=TOKEN_EXPIRY_HOURS, minutes=TOKEN_EXPIRY_MIN)
    expiration_time = created_at_datetime + expiry_duration

    current_time = datetime.now()

    # Check if the token is expired
    if current_time > expiration_time:
        return True
    else:
        return False

def is_revoked(tokendata_id):
    try:
        tokendata = TokenData.query.filter_by(id=tokendata_id).first()
    except Exception as e:
        logging.error(f"Error in getting tokendata. Exception: {e}")
        raise Exception()

    if not tokendata:
        raise BadRequest(message="Invalid token")
    
    return tokendata.is_revoked
    
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGO])

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            raise UnauthorizedError("A valid token is missing!")
        
        payload = decode_token(token)
        if is_expired(payload['created_at']):
            raise UnauthorizedError("Expired token!")
        if is_revoked(payload['id']):
            raise UnauthorizedError("Revoked token!")

        try:
            current_user = User.query.filter_by(public_id=payload['public_id']).first()
        except Exception as e:
            logging.error(f"Error in getting User. Exception: {e}")
            raise Exception()

        if not current_user:
            raise UnauthorizedError("Invalid token!")

        return f(current_user, *args, **kwargs)
    
    return decorator