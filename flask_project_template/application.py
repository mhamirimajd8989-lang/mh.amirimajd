from flask import Flask
from models import db
from log import logger

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from blueprints import main_bp
    app.register_blueprint(main_bp)

    logger.info("App created successfully")

    return app
