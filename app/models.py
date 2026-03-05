from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))  # NEW password column

    # Constructor to initialize and hash password
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)

    # Optional method to check password later
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Existing Flask-Login methods remain untouched
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  

    def __repr__(self):
        return '<User %r>' % (self.username)