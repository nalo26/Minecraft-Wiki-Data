from os import getenv

from flask.cli import FlaskGroup

from src import create_app, db
from src.database import create_database
from src.fetching.fetch import fetch

if getenv("FLASK_ENV") != "production":
    from dotenv import load_dotenv

    load_dotenv(".env")

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def run_create_db():
    with app.app_context():
        create_database(db)


@cli.command("fetch")
def run_fetch():
    fetch()


if __name__ == "__main__":
    cli()
