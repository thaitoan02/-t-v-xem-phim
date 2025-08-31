from flask import Flask, render_template, redirect, url_for, request, session, jsonify, abort, send_file
from io import BytesIO
import sqlite3
from db import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import OperationalError as SAOperationalError
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'  # Sử dụng SQLite cho đơn giản
app.config['JWT_SECRET_KEY'] = 'change_this_jwt_secret'  # replace in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
db.init_app(app)
login_manager = LoginManager(app)
JWTManager(app)
CORS(app, supports_credentials=True)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Import models
with app.app_context():
    from My_Model import User, Movie, Seat, Ticket

# Khai báo hàm user_loader cho Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Tạo trang chủ
@app.route('/')
def index():
    movies = Movie.query.all()  # Lấy tất cả phim từ cơ sở dữ liệu
    return render_template('index.html', movies=movies)

