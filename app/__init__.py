from flask import Flask
from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER = './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ziuadyuqvrmsqa:b01dec97eab26eea918f972376a64692c78406e3f346a9c584d94999a9119925@ec2-54-204-44-140.compute-1.amazonaws.com:5432/d4n61v9fot917a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning


db = SQLAlchemy(app)


app.config.from_object(__name__)
filefolder = app.config['UPLOAD_FOLDER']
app.debug= True
from app import views
