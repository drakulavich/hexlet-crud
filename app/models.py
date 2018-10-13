from app import db


class Article(db.Model):

    __tablename__ = "articles"

    post_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return '<name:{} \n{}>'.format(self.name, self.body)
