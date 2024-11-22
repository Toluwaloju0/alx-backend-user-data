#!/usr/bin/env python3
"""A module to create a new route using flask"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

app = Flask(__name__)
auth_service = Auth()


@app.route('/', strict_slashes=False)
def home():
    """To get the home page for the new route"""

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """To create a new user"""

    email = request.form['email']
    password = request.form['password']

    try:
        auth_service.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """To log a user into the system"""

    try:
        email = request.form['email']
        password = request.form['password']
        if auth_service.valid_login(email, password) is False:
            abort(401)
        session_id = auth_service.create_session(email)

        # create the message to be returned and set the cookie
        message = jsonify({"email": email, "message": "logged in"})
        message.set_cookie("session_id", session_id)

        return message

    except (KeyError, NoResultFound, InvalidRequestError):
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """An endpoint to remove a user session"""

    session_id = request.cookies.get("session_id")

    user = auth_service.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    auth_service.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", strict_slashes=False)
def profile():
    """An endpoint to get a user profile using cookie"""

    session_id = request.cookies.get('session_id')

    user = auth_service.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """An endpoint to reset the users password using the session id"""

    email = request.form("email")
    try:
        reset_token = auth_service.get_reset_password_token(email)

        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """AN endpoint to update the users password"""

    email = request.form["email"]
    new_passsword = request.form["new_password"]
    reset_token = request.form["reset_token"]

    # Use auth_service to update the password
    auth_service.update_password(reset_token, new_password)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
