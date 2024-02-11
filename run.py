from os import getenv

from src import create_app

if getenv("FLASK_ENV") != "production":
    from dotenv import load_dotenv

    load_dotenv(".env")

app = create_app()

if __name__ == "__main__":  # DEV ENVIRONMENT
    app.run(host=getenv("WEB_HOST"), port=getenv("WEB_PORT"))
