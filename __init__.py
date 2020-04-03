from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config

# initialize additional Flask tools with this app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# define which route is the login view
login_manager.login_view = 'users.login'
# define the login_message_category.  Which translates
# to the HTML class that the login_required message will have
login_manager.login_message_category = 'info'

mail = Mail()


# this is the main entrypoint of the application
# run.py calls this function to 'create' the app
def create_app(config_class=Config):
    # initialize certain settings within application
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import Blueprints and
    # register on this app 
    from .users.routes import users
    from .posts.routes import posts
    from .main.routes import main
    from .errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app