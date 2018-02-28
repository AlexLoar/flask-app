from flask import request, jsonify, Blueprint
# from . import users_api
from pony.orm.serialization import to_dict
from pony.orm import db_session
from pony.orm.core import ObjectNotFound

from jsonschema.exceptions import ValidationError

from src.utils.views import validate_data
from src.users.models import User, database as db
from src import app

users_api = Blueprint('users_api', __name__, url_prefix='/v1/users')


@users_api.route('/', methods=['GET'])
@db_session
def users():
    users = User.select().order_by(User.updated_at)
    users = to_dict(users)
    return jsonify(users), 200


@users_api.route('/<int:user_id>', methods=['GET'])
@db_session
def user(user_id):
    try:
        user = User[user_id]
        user = to_dict(user)
    except ObjectNotFound:
        msg = 'User ID {} not found'.format(user_id)
        app.logger.info(msg)
        return jsonify(dict(detail=msg)), 404
    return jsonify(user), 200


@users_api.route('/search', methods=['GET'])
@db_session
def search():
    search_name = request.args.get('keyword')
    users = User.select(lambda u: search_name in u.username)
    users = to_dict(users)
    return jsonify(users), 200


@users_api.route('/', methods=['POST'])
@db_session
def create_user():
    data = request.get_json()
    try:
        validate_data(data, 'user')
    except ValidationError as err:
        return jsonify(dict(detail=err.message))
    user = User(username=data.get("username"),
                email=data.get("email"),
                age=data.get("age"),
                phone=data.get("phone"),
                location=data.get("location")
                )
    try:
        db.commit()
        app.logger.info('User "{}" created successfully'.format(user.username))
        user = to_dict(user)
        return jsonify(user), 201
    except Exception as err:
        db.rollback()
        app.logger.info('There was an error trying to create an user: {}'.format(repr(err)))
        return jsonify(dict(detail='Invalid format')), 404


@users_api.route('/<int:user_id>', methods=['DELETE'])
@db_session
def delete_user(user_id):
    try:
        user = User[user_id]
        user_id, username = user.id, user.username
        user.delete()
        db.commit()
        app.logger.info('User "{}:{}" deleted successfully'.format(user_id, username))
        return jsonify(dict(detail='User deleted successfully')), 200
    except Exception as err:
        db.rollback()
        app.logger.warning('There was an error trying to delete the user "{}": {}'.format(user_id, repr(err)))
        return jsonify(dict(detail='Invalid format')), 404


@users_api.route('/<int:user_id>', methods=['PUT'])
@db_session
def update_user(user_id):
    data = request.get_json()
    try:
        validate_data(data, 'user')
    except ValidationError as err:
        return jsonify(dict(detail=err.message))
    try:
        user = User[user_id]
        user.set(**data)
        user = to_dict(user)
        db.commit()
        app.logger.warning('User "{}" updated successfully'.format(user_id))
        return jsonify(user), 200
    except Exception as err:
        app.logger.warning('There was an error trying to update the user "{}": {}'.format(user_id, repr(err)))
        return jsonify(dict(detail='Invalid format')), 404
