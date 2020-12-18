from flask import Flask, Blueprint, request, url_for, redirect, flash, get_flashed_messages, render_template
from flask_login import login_required, current_user
from app.login_decorators import admin_required
from app.models import Category, Post, Book
from app.forms import CreateCategory, CreatePost, CreateBook, EditBook
from app.classes import Utilities, Uploads
import re

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
    Post(author=current_user.get_username(), title=request.form.get('title'), content=re.sub(r'\s+', '', request.form.get('content')), date_time=Utilities.post_timestamp(), status=request.form.get('status'), category=Category().custom_query('id', request.form.get('category')).category_name).add_post()

    flash('Your post has been created.')
    return redirect(url_for('admin_bp.posts'))

@admin_bp.route('/dashboard/edit/post/<postID>', methods=['GET'])
@admin_required
def edit_post(postID):
    query = Post().custom_query('id', postID)
    if not query:
        return redirect(url_for('admin_bp.dashboard'))
    return render_template('/admin/edit-post.html', form=CreatePost(), message=get_flashed_messages(), post=query)

@admin_bp.route('/dashboard/delete/post/<postID>', methods=['GET'])
@admin_required
def delete_post(postID):
    if not Post(id=postID).delete_post():
        return redirect(url_for('admin_bp.dashboard'))
    return redirect(url_for('admin_bp.posts'))

@admin_bp.route('/dashboard/bookstore', methods=['GET'])
@admin_required
def bookstore():
    return render_template('/admin/bookstore.html', books=Book.query.all())

@admin_bp.route('/dashboard/bookstore/new', methods=['GET'])
@admin_required
def create_book():
    return render_template('/admin/create-book.html', form=CreateBook(), message=get_flashed_messages())

@admin_bp.route('/dashboard/book/edit/<id>', methods=['GET'])
@admin_required
def edit_book(id):
    query = Book().custom_query('id', id)
    if not query:
        return redirect(url_for('admin_bp.dashboard'))
    return render_template('/admin/edit-book.html', form=EditBook(), book=query, message=get_flashed_messages())

@admin_bp.route('/test', methods=['POST'])
def test():
    return 'test'

@admin_bp.route('/dashboard/book/create/add', methods=['POST'])
@admin_required
def add_book():
    form = CreateBook()
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('admin_bp.create_book'))

    Book(book_title=request.form.get('name'), book_price=request.form.get('price'), slug=request.form.get('name').replace(' ', '-'), book_description=request.form.get('description'), referral_link=request.form.get('url'), book_img=Uploads(request.files['img'], 'app/static/images/books').save_upload()).add_book()

    return 'book added'