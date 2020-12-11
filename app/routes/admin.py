from flask import Flask, Blueprint, request, url_for, redirect, flash, get_flashed_messages, render_template
from flask_login import login_required, current_user
from app.login_decorators import admin_required
from app.models import Category, Post
from app.forms import CreateCategory, CreatePost
from app.classes import Utilities

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    return render_template('/admin/dashboard.html', message=get_flashed_messages())

@admin_bp.route('/dashboard/categories', methods=['GET'])
@admin_required
def category_page():
    return render_template('/admin/categories.html', cat=Category().fetch_all(), form=CreateCategory(), message=get_flashed_messages())

@admin_bp.route('/dashboard/categories/add', methods=['POST'])
@admin_required
def add_category():
    form = CreateCategory()
    
    if Category().custom_query('category_name', request.form.get('cat_name')):
        flash('Category Already Exists')
        return redirect(url_for('admin_bp.category_page'))
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('admin_bp.category_page'))
    
    Category(category_name=request.form.get('cat_name')).add_category()
    flash('Category Added')
    return redirect(url_for('admin_bp.category_page'))

@admin_bp.route('/dashboard/categories/remove/<cat_id>', methods=['GET'])
@admin_required
def remove_category(cat_id):
    Category(id=cat_id).delete_category()
    flash('Category Deleted')
    return redirect(url_for('admin_bp.category_page'))

@admin_bp.route('/dashboard/posts', methods=['GET'])
def posts():
    return render_template('/admin/posts.html', posts=Post().fetch_all(), message=get_flashed_messages())

@admin_bp.route('/dashboard/create/post', methods=['GET'])
def create_post():
    return render_template('/admin/create-post.html', form=CreatePost(), message=get_flashed_messages())

@admin_bp.route('/dashboard/add/post', methods=['POST'])
@admin_required
def add_post():
    form = CreatePost()
    
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('admin_bp.create_post'))
    
    Post(author=current_user.get_username(), title=request.form.get('title'), content=request.form.get('content'), date_time=Utilities.post_timestamp(), status=request.form.get('status'), category=request.form.get('category')).add_post()

    flash('Your post has been created.')
    return redirect(url_for('admin_bp.posts'))