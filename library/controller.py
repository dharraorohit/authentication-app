import uuid
import logging
from library.models import User
from library.main import db
from werkzeug.security import generate_password_hash, check_password_hash
from library.utils import generate_token, revoke_token, decode_token
from library.response import CustomAPIException, NotFoundError, UnauthorizedError, BadRequest

PASSWORD_HASHMETHOD = 'pbkdf2:sha256'

class UserController():
    def signup(email, password):
        hashed_password = generate_password_hash(password, method=PASSWORD_HASHMETHOD)
        new_user = None
        try:
            user = User.query.filter_by(email=email).first()
        except Exception as e:
            logging.error(f"Error in getting user. Exception: {e}")
            raise Exception()
        
        if user:
            raise CustomAPIException(message="User already exists", status_code=409)
        
        try:
            new_user = User(public_id=str(uuid.uuid4()), email=email, password=hashed_password, admin=False)
            db.session.add(new_user) 
            db.session.commit()
        except Exception as e:
            logging.error(f"Error in creating User. Exception: {e}")
            raise Exception()
        
        return new_user
        
    def login(email, password):
        try:
            user = User.query.filter_by(email=email).first()
        except Exception as e:
            logging.error(f"Error in getting user with email. Exception: {e}")
            raise Exception()
        
        if not user:
            raise NotFoundError(message="User notfound")

        if check_password_hash(user.password, password):
            token = generate_token(user)
            return token

        raise UnauthorizedError(message="Invalid password")

    def revoke_token(token):
        token_payload = decode_token(token)
        tokendata_id = token_payload.get('id')
        if not tokendata_id:
            raise BadRequest(message="Invalid token")
        
        revoke_token(tokendata_id)

    def refresh_token(user):
        return generate_token(user)
