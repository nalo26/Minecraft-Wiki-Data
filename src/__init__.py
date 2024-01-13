import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    load_dotenv(".env")

    db_url = "%s://%s:%s@%s:%s/%s" % (
        os.getenv("DB_ENGINE"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASS"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    db.init_app(app)

    from .views.default import view as default_blueprint

    app.register_blueprint(default_blueprint)

    from .views.api import view as api_blueprint

    app.register_blueprint(api_blueprint)

    return app
