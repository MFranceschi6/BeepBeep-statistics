from flask import jsonify


def bad_response(code, message):
    return jsonify({'response-code': code, 'message': message}), code


def existing_user(user_id=None, email=None):
    if user_id is not None:
        q = db.session.query(User).filter(User.id == user_id)
        return q.count() > 0
    elif email is not None:
        q = db.session.query(User).filter(User.email == email)
        return q.count() > 0
    else:
        return False

