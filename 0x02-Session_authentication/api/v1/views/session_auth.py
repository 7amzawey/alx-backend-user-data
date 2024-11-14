#!/usr/bin/env python3
"""Module of Users views."""
from os import getenv
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """Get api/v1/auth_session/login."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password) is not True:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())

    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response
