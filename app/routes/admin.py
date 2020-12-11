from flask import Flask, Blueprint, request, url_for, redirect, flash, get_flashed_messages, render_template
from flask_login import login_required
from app.login_decorators import admin_required
from app.models import Category
from app.forms import CreateCategory

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