from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:123@localhost/ProjectDB')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize DB connection for direct psycopg2 use (if needed)
if 'DATABASE_URL' in os.environ:
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
else:
    db_conn_string = "dbname='ProjectDB' user='postgres' host='127.0.0.1' password='123'"
    conn = psycopg2.connect(db_conn_string)

roles = ["none", "doctor", "patient"]
print(roles)
mysession = {"state": "initializing", "role": "Not assigned", "id": 0, "age": 202212}
print(mysession)

from clinic.Login.routes import Login
from clinic.Patient.routes import Patient
from clinic.Doctor.routes import Doctor
app.register_blueprint(Login)
app.register_blueprint(Patient)
app.register_blueprint(Doctor)

# Ensure user loader callback is defined
from clinic.models import load_user
