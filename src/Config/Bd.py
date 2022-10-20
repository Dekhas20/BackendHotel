from flask import Flask,render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/hialeah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# settings
app.secret_key = "claveSecreta"

#trabajamos con la bd 
db = SQLAlchemy(app)

ma = Marshmallow(app)
