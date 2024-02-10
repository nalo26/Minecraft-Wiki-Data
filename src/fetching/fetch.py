from .blocks import fetch_blocks
from .constants import BASE_URI
from .items import fetch_items
from .mobs import fetch_mobs
from .versions import fetch_versions


def fetch():
    from .. import create_app, db

    app = create_app()
    with app.app_context():
        fetch_versions(BASE_URI, db)
        fetch_items(BASE_URI, db)
        fetch_blocks(BASE_URI, db)
        fetch_mobs(BASE_URI, db)


if __name__ == "__main__":
    fetch()
