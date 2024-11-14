#!/usr/bin/env python3
""" A view for the session authentication method"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', strict_slashes=False, methods=['POST'])
def session_auth():
    """A new view for the endpoint /auth_session/login/
    using the session auth"""

    from api.v1.app import auth

    email, pwd = request.form.get('email'), request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            user_session = auth.create_session(user.id)
            # create a response using jsonify and set the cookie
            user = jsonify(user.to_json())
            user.set_cookie(getenv('SESSION_NAME'), user_session)
            return user
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout():
    """ To delete the session_id of a user instance"""

    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)
    else:
        return jsonify({}), 200
