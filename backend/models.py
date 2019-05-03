from app import db
from sqlalchemy.dialects.postgresql import JSON

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String())

    def __init__(self, image_url):
        self.image_url = url

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.String(), primary_key=True)
	password = db.Column(db.String(), nullable=False)
	email = db.Column(db.String())

	def __init__(self, user_id, password, email):
		self.user_id = user_id
		self.password = password
		self.email = email