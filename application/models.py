from application import db

recommendations_identifier = db.Table('recommendations',
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True) 
    author = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendations = db.relationship("Games", secondary=recommendations_identifier)


class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
