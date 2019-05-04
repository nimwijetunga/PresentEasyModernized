from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import util, image_handler
from util import authenticate_request


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models


@app.route('/')
def main():
    return "Welcome to Present Easy"


@app.route('/images')
@authenticate_request
def get_images(user_id):
	image_id = image_handler.create_image_and_add_to_cache('test_url', 100, 300)
	return jsonify({'status': 'Success', 'image_id': image_id})

@app.route('/add/images', methods=['POST'])
@authenticate_request
def add_images(user_id):
	body = request.get_json() or {}
	# should be a list of image uuids
	image_uuids = body.get('images')
	if not image_uuids or not isinstance(image_uuids, list):
		return jsonify({'status': 'Failed'}), 400
	user = db.session.query(models.User).filter_by(user_id=user_id).first()
	db.session.expunge(user)
	if not user:
		return jsonify({'status': 'Failed', 'msg': 'User Not Found'}), 400
	try:
		image_handler.fetch_images_from_redis_add_to_db(user, image_uuids)
		return jsonify({'status': 'Success', 'msg': 'Saved!'})
	except Exception as e:
		print(e)
		return jsonify({'status': 'Failed'}), 500

@app.route('/signup', methods=['POST'])
def signup():
	try:
		body = request.get_json()
		if not body:
			return jsonify({'status': 'Failed', 'token':None}), 400
		user_id = body.get('username')
		password = body.get('password')
		email = body.get('email')
		if not user_id or not password:
			return jsonify({'status': 'Failed', 'token': None}), 400
		user_exists = bool(db.session.query(models.User).filter_by(user_id=user_id).first())
		if user_exists:
			return jsonify({'status': 'Failed', 'token': None, 'msg': 'User Alrady Exists'}), 400
		password = util.encrypt_password(password)
		auth_token = util.encode_auth_token(user_id)
		user = models.User(user_id=user_id, password=password, email=email)
		db.session.add(user)
		db.session.commit()
		return util.get_response_with_cookie({'status': 'Success', 'token': auth_token}, 'auth_token', auth_token)
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonfiy({'status': 'Failed', 'token':None}), 500

@app.route('/login', methods=['POST'])
def login():
	try:
		body = request.get_json()
		if not body:
			return jsonify({'status': 'Failed', 'token':None}), 400
		user_id = body.get('username')
		password = body.get('password')
		if not user_id or not password:
			return jsonify({'status': 'Failed', 'token': None}), 400
		user = db.session.query(models.User).filter_by(user_id=user_id).first()
		if not user:
			return jsonify({'status': 'Failed', 'token': None, 'msg': 'User Does not Exists'}), 400
		if not util.is_valid_password(password, user.password):
			return jsonify({'status': 'Failed', 'token': None, 'msg': 'Invalid Password'}), 400
		auth_token = util.encode_auth_token(user_id)
		return util.get_response_with_cookie({'status': 'Success', 'token': auth_token}, 'auth_token', auth_token)
	except Exception as e:
		print(e)
		return jsonfiy({'status': 'Failed', 'token':None}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)