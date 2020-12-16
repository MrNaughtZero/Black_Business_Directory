from flask import Flask, Blueprint, render_template

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')