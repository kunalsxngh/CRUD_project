from application import db

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendations = db.relationship('Recommendations', backref='reviews')


class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    recommendations = db.relationship('Recommendations', backref='games')


class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable = False)
    game = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)
