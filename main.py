from flask import Flask
from applications.model import DB, User

def make_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///grocery.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'apple11'
    DB.init_app(app)
    app.app_context().push()
    return app

app = make_app()

from applications.user import *
from applications.admin import *


if __name__ == "__main__":
    DB.create_all()
    admin = User.query.filter_by(is_admin = True).first()
    if not admin:
        admin_new = User(name = "Manager", email = "admin@grocery.com", 
                         password = "0000", is_admin = True)
        DB.session.add(admin_new)
        DB.session.commit()
    app.run(debug = True)