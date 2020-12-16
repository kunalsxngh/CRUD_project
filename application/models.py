from application import db

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendations = db.relationship('Recommendations', backref='review')


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    recommendations = db.relationship('Recommendations', backref='game')


class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id', nullable = False))