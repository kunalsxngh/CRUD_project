from application import db


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    recommendations = db.relationship("Reviews", backref='games', lazy='dynamic')


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    author = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    game = db.Column(db.Integer, db.ForeignKey('games.id'))


