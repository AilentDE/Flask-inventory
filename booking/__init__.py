import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail

from booking.config import Config

db = SQLAlchemy()
migrate = Migrate( compare_type=True )
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()

from booking.route import index, login, logout, register_request, register, reset_password_request, reset_password, booking, progress

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register_request', 'register_request', register_request, methods=['GET', 'POST'])
    app.add_url_rule('/register/<token>', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/reset_password_request', 'reset_password_request', reset_password_request, methods=['GET', 'POST']) #考慮改用JS設置在login按鈕下方就好
    app.add_url_rule('/reset_password/<token>', 'reset_password', reset_password, methods=['GET', 'POST'])
    app.add_url_rule('/booking', 'booking', booking, methods=['GET', 'POST'])
    app.add_url_rule('/progress', 'progress', progress, methods=['GET', 'POST'])
    return app