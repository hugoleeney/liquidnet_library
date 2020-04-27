"""
Must have run the following in terminal:
from flashblog import db
db.create_all()
"""
from flaskblog import app


if __name__ == "__main__":

    app.run()
    # app.run(debug=True)
