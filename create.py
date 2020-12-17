from application import db
from application.models import Games

db.drop_all()
db.create_all()
new_game = Games(name = "None", genre = "None")
db.session.add(new_game)
db.session.commit()
