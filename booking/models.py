from datetime import datetime
from flask.globals import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from booking import db, login_manager
import jwt, time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order_info', backref='orderer', lazy='dynamic')
    
    def __repr__(self):
        return 'id={}, username={}, email={}, password_hash={}'.format(
            self.id, self.username, self.email, self.password_hash
        )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_jwt(self, expire=600):
        return jwt.encode(
            {
                'email': self.email,
                'exp': time.time()+expire
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_jwt(token):
        try:
            email = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email = email['email']
        except:
            return
        return User.query.filter_by(email=email).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Order_info(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_number = db.Column(db.String(32), unique=True, nullable=False)
    state = db.Column(db.String(16), nullable=False, default='Prepare')
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    state_code = db.Column(db.String(16))
    postcode = db.Column(db.String(16), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    shipping_method = db.Column(db.String(128), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    remark = db.Column(db.String(128))
    order_list = db.relationship('Order_list', backref='booking', lazy='dynamic')
    order_report = db.relationship('Report', backref='booking', lazy='dynamic')

class Order_list(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(32), db.ForeignKey('order_info.order_number'))
    sku = db.Column(db.String(16), db.ForeignKey('product.sku'))
    quantity = db.Column(db.Integer, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(16), unique=True, nullable=False)
    title = db.Column(db.String(128))
    picture = db.Column(db.LargeBinary(300))
    quantity = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    update_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ordered = db.relationship('Order_list', backref='product_detail', lazy='dynamic')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(32), db.ForeignKey('order_info.order_number'))
    tracking_number = db.Column(db.String(32), unique=True)
    shipping_date = db.Column(db.DateTime)
    delivery_fee = db.Column(db.Integer)
    materials_fee = db.Column(db.Integer)
    package_weight = db.Column(db.Integer)