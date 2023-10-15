from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
import os

# ----------- Keys and Global Variables -----------
app = Flask(__name__)
app.config["SECRET_KEY"] = "isef" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] =  'static/data'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------- Database -----------
class Organizations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False)
    administrator = db.Column(db.String(120), nullable=False)
    administrator_contact = db.Column(db.String(120), nullable=False)
    verify_code = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    patients = db.relationship('Patients', backref='org')
    
    @property
    def password():
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    pre_disease = db.Column(db.String(255), nullable=False)
    note = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/experience")
def experience():
    return render_template("experience.html")


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
