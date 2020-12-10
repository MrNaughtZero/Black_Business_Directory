from flask import Flask, Blueprint

app = Flask(__name__)
app.debug = True
app.secret_key ='3o730927309nwbdnbsdjhgsda097ougdskb29836iwfukjb'

from .routes import auth,admin,main
 
app.register_blueprint(auth.auth_bp) 
app.register_blueprint(admin.admin_bp) 
app.register_blueprint(main.main_bp) 

from app.database import setup_db

setup_db(app)

from flask_login import LoginManger

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)