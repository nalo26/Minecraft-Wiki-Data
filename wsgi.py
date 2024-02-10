import sys
from os import getenv

from src import create_app
from src.fetching.fetch import fetch

app = create_app()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
        sys.exit(0)
    app.run(debug=bool(int(getenv("DEBUG", 0))), host=getenv("HOST"), port=getenv("PORT"))
