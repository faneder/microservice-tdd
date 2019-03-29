from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db


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
