from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


database_name = 'mahali'
database_path = 'mysql://root:@localhost/mahali'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()