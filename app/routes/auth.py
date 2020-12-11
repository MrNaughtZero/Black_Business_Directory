from flask import Flask, Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required
from app.models import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/auth/setup', methods=['GET'])
def admin_setup_page():
    if User().check_for_admin():
        return abort(404)
    return render_template('/auth/setup.html')

@auth_bp.route('/auth/login', methods=['GET'])
def auth_login_page():
    return render_template('/auth/login.html')

@auth_bp.route('/auth/login/attempt', methods=['POST'])
def auth_login_attempt():
    ## Process login page
    return 'Login Attempt'

@auth_bp.route('/auth/logout', methods=['GET'])
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for('auth_login_page'))

@auth_bp.route('/auth/password/reset', methods=['GET'])
def auth_password_reset():
    return render_template('/auth/password-reset.html')