from flask import Flask, Blueprint
from app.database import setup_db
from flask_login import LoginManager

app = Flask(__name__)
app.debug = True
app.config.from_envvar('APP_SETTINGS')

from .routes import auth,admin,main
 
app.register_blueprint(auth.auth_bp) 
app.register_blueprint(admin.admin_bp) 
app.register_blueprint(main.main_bp) 

setup_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)