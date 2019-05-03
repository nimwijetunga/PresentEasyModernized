from app import db
from sqlalchemy.dialects.postgresql import JSON
import redis
import os
import simplejson as json
import uuid

_IMAGES_REDIS_DB_NUM = 0
images_redis = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=_IMAGES_REDIS_DB_NUM)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    uuid = db.Column(db.String())

    def __init__(self, url, width, height):
        self.url = url
        self.width = width
        self.height = height
        self.uuid = str(uuid.uuid4())

    def add_image_to_cache(self):
    	key = 'image:%s' % self.uuid
    	image_info = {
    		'url': self.url,
    		'width': self.width,
    		'height': self.height
    	}
    	images_redis.set(key, json.dumps(image_info))
    	images_redis.expire(key, 60*60) # expire after an hour

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