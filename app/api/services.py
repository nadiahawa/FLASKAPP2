
from flask import request, jsonify
from functools import wraps
from app.models import User


def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args, **kwargs):
        token = request.headers.get('foxes-access-token')
        if not token:
            return jsonify({'access denied = no API token'}), 401
        if not User.query.filer_by(api_token=token).first():
             return jsonify({'invalid api = no API token'}), 403
        return api_route(*args, **kwargs)
    return decorator_function