from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor



app = Flask(__name__, static_folder='./img')
app.config['SECRET_KEY'] = 'fd51538b5168f164a1b57b018e859e54fa9fdde7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['CKEDITOR_SERVE_LOCAL'] = True


db = SQLAlchemy(app)
ckeditor = CKEditor(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'gray-900'


from flaskblog import route