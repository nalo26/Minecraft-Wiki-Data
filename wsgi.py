import sys

from src import create_app
from src.fetching.fetch import fetch

app = create_app()

if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        fetch()
        sys.exit(0)
    app.run()
