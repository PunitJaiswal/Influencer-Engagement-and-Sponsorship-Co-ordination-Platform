from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'app.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .sponsor import sponsor
    from .influencer import influencer

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(sponsor, url_prefix='/sponsor')
    app.register_blueprint(influencer, url_prefix='/influencer')

    from .models import Ad_request, Campaign, Influencer, Sponsor
    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view="auth.user_login"
    login_manager.login_view="auth.admin_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Check if the user ID belongs to an Influencer
        inf = Influencer.query.get(int(user_id))
        if inf.role=='Influencer':
            return inf

        # Check if the user ID belongs to a Sponsor
        spon = Sponsor.query.get(int(user_id))
        if spon.role=='sponsor':
            return sponsor

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            # Create all tables
            db.create_all()
            print('Created Database!')