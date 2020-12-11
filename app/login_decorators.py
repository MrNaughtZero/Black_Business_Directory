from functools import wraps
from flask import g, request, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (not current_user.is_authenticated) or (current_user.get_role() != 'admin'):
            return redirect(url_for('auth_bp.auth_login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function