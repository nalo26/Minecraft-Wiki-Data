from .blocks import fetch_blocks
from .versions import fetch_versions

# BASE_URI = "https://minecraft.wiki/%s"
BASE_URI = "http://127.0.0.1:5000/%s"


def fetch():
    from .. import create_app, db

    app = create_app()
    with app.app_context():
        fetch_versions(BASE_URI, db)
        fetch_blocks(BASE_URI, db)


if __name__ == "__main__":
    fetch()
