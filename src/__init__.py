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

    from .views.api import block_view, item_view, mob_view

    app.register_blueprint(mob_view)
    app.register_blueprint(block_view)
    app.register_blueprint(item_view)

    # Dynamic import of views
    # for filename in os.listdir(Path.joinpath(Path(__file__).parent, "views")):
    #     if filename.endswith(".py") and filename != "__init__.py":
    #         module = __import__(f"src.views.{filename[:-3]}", fromlist=["view"])
    #         app.register_blueprint(module.view)

    return app


def init_db():
    from .database import create_database

    app = create_app()
    with app.app_context():
        create_database(db)
