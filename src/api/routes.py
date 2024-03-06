"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/sign_up', methods=['POST'])
def manage_sign_up():

    request_data = request.get_json()

    if not 'email' in request_data:
        return jsonify({"error": "The email is not present"}), 400
    
    if not('password' in request_data) or not('passwordConfirmation' in request_data):
        return jsonify({"error": "The password or password confirmation is not present"}), 400

    email = request_data['email']
    password = request_data['password']
    password_confirmation = request_data['passwordConfirmation']

    if password != password_confirmation:
        return jsonify({"error": "Please verify that password is equal to your password confirmation field"}), 400
    
    user = User(email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit() 

    response_body = {
        "message": "The user was created without problem "
    }

    return jsonify(response_body), 200
