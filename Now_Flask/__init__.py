from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)



app.secret_key = "super-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/programming'
db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] ='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'paramvirhans4470@gmail.com'
app.config['MAIL_PASSWORD'] = 'pikwyhlbqnvrtusi'

mail = Mail(app)

with app.app_context():
    db.create_all()

from Now_Flask import routes