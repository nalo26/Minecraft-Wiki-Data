from .versions import fetch_versions

# BASE_URI = "https://minecraft.wiki/w/%s"
BASE_URI = "http://127.0.0.1:5000/w/%s"


def fetch():
    from .. import create_app, db

    app = create_app()
    with app.app_context():
        fetch_versions(BASE_URI, db)


if __name__ == "__main__":
    fetch()
