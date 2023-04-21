from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)


BCRYPT = Bcrypt(app)


DATABASE = "recipes_schema"

app.secret_key = "pain"