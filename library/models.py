from library.main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(320), index=True, unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
class TokenData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_revoked = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.Integer, nullable=False)