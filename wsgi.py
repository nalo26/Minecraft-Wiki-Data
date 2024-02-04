import sys

from src import create_app
from src.fetching.fetch import fetch

app = create_app()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
        sys.exit(0)
    app.run()
