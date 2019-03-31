from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    response = {
        'status': 'fail',
        'message': 'Invalid payload.',
    }

    if not post_data:
        return jsonify(response), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    # check for existing user
    try:
        if User.query.filter(User.username == username).first():
            raise AssertionError('Sorry. Username is already in use')

        if User.query.filter(User.email == email).first():
            raise AssertionError('Sorry. Email is already in use')

        # add new user to DB
        new_user = User(
            username=username,
            email=email,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
        auth_token = new_user.encode_auth_token(new_user.id)
        response['status'] = 'success'
        response['message'] = 'Successfully registered.'
        response['auth_token'] = auth_token.decode()
        return jsonify(response), 201
    # handler errors
    except (exc.IntegrityError, AssertionError, ValueError) as e:
        db.session.rollback()
        response['message'] = 'Error: {}. '.format(e)
        return jsonify(response), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['auth_token'] = auth_token.decode()
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception:
        response_object['message'] = 'Plesase try again.'
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    authorization = request.headers.get('Authorization')
    response = {
        'status': 'fail',
        'message': 'Invalid token. Please log in again.'
    }
    if authorization:
        auth_token = authorization.split(' ')[1]
        decode_token = User.decode_auth_token(auth_token)
        if not isinstance(decode_token, str):
            response['status'] = 'success'
            response['message'] = 'Successfully logged out.'
            return jsonify(response), 200
        else:
            response['message'] = decode_token
            return jsonify(response), 401
    else:
        return jsonify(response), 403


@auth_blueprint.route('/auth/status', methods=['GET'])
def get_user_status():
    authorization = request.headers.get('Authorization')
    response = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if authorization:
        auth_token = authorization.split(' ')[1]
        token_res = User.decode_auth_token(auth_token)
        if not isinstance(token_res, str):
            user = User.query.filter_by(id=token_res).first()
            response['status'] = 'success'
            response['message'] = 'Success'
            response['data'] = user.to_json()
            return jsonify(response), 200
        response['message'] = token_res
        return jsonify(response), 401
    else:
        return jsonify(response), 401
