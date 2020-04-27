"""
Must have run the following in terminal:
from library import db
db.create_all()
"""
import argparse

from library import app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='the port', default=5000)
    args = parser.parse_args()

    app.run(port=args.port)
    #app.run(debug=True, port=args.port)
