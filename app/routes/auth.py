from flask import Flask, Blueprint, render_template, redirect, url_for, request, abort, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import AdminRegister, AdminLogin, AdminPasswordResetForm, AdminSetNewPassword

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/auth/setup', methods=['GET'])
def admin_setup_page():
    if User().custom_query('role', 'admin'):
        return abort(404)
    return render_template('/auth/setup.html', form=AdminRegister(), message=get_flashed_messages())

@auth_bp.route('/auth/setup/create/account', methods=['POST'])
def admin_create_account():
    if User().custom_query('role', 'admin'):
        return abort(404)

    form = AdminRegister()
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('auth_bp.admin_setup_page'))

    User(username=request.form.get('username'), email=request.form.get('email'), password=User().hash_password(request.form.get('password')), role='admin').create_user()

    flash('Admin Account Created. Please Login to continue')
    return redirect(url_for('auth_bp.auth_login_page'))

@auth_bp.route('/auth/login', methods=['GET'])
def auth_login_page():
    return render_template('/auth/login.html', message=get_flashed_messages(), form=AdminLogin())

@auth_bp.route('/auth/login/attempt', methods=['POST'])
def auth_login_attempt():
    query = User().login_attempt(request.form.get('username'), request.form.get('password'))
    if not query:
        flash('Incorrect Login Details')
        return redirect(url_for('auth_bp.auth_login_page'))
    
    login_user(query)
    return 'You are now logged in' ## Redirect to dashboard once created


@auth_bp.route('/auth/logout', methods=['GET'])
def auth_logout():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.auth_login_page'))
    logout_user()
    return redirect(url_for('auth_bp.auth_login_page'))

@auth_bp.route('/auth/password/reset', methods=['GET'])
def auth_password_reset():
    return render_template('/auth/password-reset.html', form=AdminPasswordResetForm(), message=get_flashed_messages())

@auth_bp.route('/auth/password/request', methods=['POST'])
def auth_request_password_reset():
    form = AdminPasswordResetForm()
    query = User().update_password_reset_code(request.form.get('email'))
    
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('auth_bp.auth_password_reset'))
    
    if not query:
        flash('Incorrect Email. Please try again')
        return redirect(url_for('auth_bp.auth_password_reset'))

    return redirect(url_for('auth_bp.auth_set_new_password', pid=query.pw_reset))

@auth_bp.route('/auth/set/new/password/<pid>', methods=['GET'])
def auth_set_new_password(pid):
    if not User().check_pw_reset_code(pid):
        return redirect(url_for('auth_bp.auth_login_page'))
    
    return render_template('auth/set-password.html', form=AdminSetNewPassword(), message=get_flashed_messages(), pid=pid)

@auth_bp.route('/auth/password/update/<pid>', methods=['POST'])
def auth_update_password(pid):
    query = User().custom_query('pw_reset', pid)
    form = AdminSetNewPassword()
    
    if not query:
        return redirect(url_for('auth_bp.auth_login_page'))
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('auth_bp.auth_set_new_password', pid=pid))
    
    User().update_password(pid, request.form.get('password'))

    flash('Password Updated. Please login.')
    return redirect(url_for('auth_bp.auth_login_page'))
