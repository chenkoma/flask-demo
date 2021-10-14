from flask import Blueprint, jsonify
from model import User
user = Blueprint('user', __name__)


@user.route('/list')
def list_users():
    users = User.query.all()
    print(users)
    users_output = []
    for user in users:
        users_output.append(user.to_json())
    return jsonify(users_output)


@user.route('/details/<userid>')
def find_user(userid):
    user = User.query.get(userid)
    return jsonify(user.to_json())


@user.route('/add/<name>')
def add_name(name):
    user = User