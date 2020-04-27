from library import db
from datetime import datetime
from ww import f



class Request(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(1000), nullable=False, unique=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f("User('{self.email}', '{self.title}', )")

