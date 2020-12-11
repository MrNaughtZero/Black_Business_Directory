from flask import Flask, Blueprint

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return 'index'