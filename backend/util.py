from flask import jsonify, make_response
from passlib.hash import sha256_crypt
import os
import jwt
import datetime


def send_json(status_code, body):
	return jsonify(body), status_code

def encrypt_password(password):
	return sha256_crypt.encrypt(password)

def is_valid_password(password, saved_password):
	return sha256_crypt.verify(password, saved_password)

def encode_auth_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        os.getenv('SECRET_KEY'),
        algorithm='HS256'
    )

