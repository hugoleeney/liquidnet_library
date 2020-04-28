from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PAGINATION_PER_PAGE'] = 20
db = SQLAlchemy(app)


from library import routes
