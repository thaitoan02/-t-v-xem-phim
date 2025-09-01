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

# Đăng ký người dùng mới
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash password for users registered via web form
        hashed_pw = pwd_context.hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        try:
            db.session.commit()
        except SAOperationalError as e:
            # If the user table lacks 'is_admin' column, add it and retry
            msg = str(e)
            if 'no column named is_admin' in msg or 'has no column named is_admin' in msg:
                try:
                    # Get DB file path from SQLAlchemy engine
                    engine_url = db.engine.url
                    db_path = engine_url.database if hasattr(engine_url, 'database') else None
                    if not db_path:
                        db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', '')
                    if db_path and os.path.exists(db_path):
                        conn = sqlite3.connect(db_path)
                        cur = conn.cursor()
                        cur.execute("ALTER TABLE user ADD COLUMN is_admin INTEGER DEFAULT 0")
                        conn.commit()
                        cur.close()
                        conn.close()
                        # retry commit
                        db.session.commit()
                        return redirect(url_for('login'))
                except Exception:
                    db.session.rollback()
                    raise
            # re-raise if not handled
            db.session.rollback()
            raise
        return redirect(url_for('login'))

    return render_template('register.html')
