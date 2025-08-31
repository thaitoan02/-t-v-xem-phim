from app import app
from db import db
from My_Model import User
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

with app.app_context():
    u = User.query.filter_by(username='admin').first()
    if not u:
        u = User(username='admin', password=pwd.hash('admin'), is_admin=True)
        db.session.add(u)
        action = 'created'
    else:
        u.password = pwd.hash('admin')   # đặt lại mật khẩu thành 'admin'
        u.is_admin = True               # đảm bảo là admin
        db.session.add(u)
        action = 'updated'
    db.session.commit()
    print(f'Admin user {action}: username=admin, password=admin')
