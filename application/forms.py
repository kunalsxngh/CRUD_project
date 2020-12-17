from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, NumberRange, InputRequired

class ReviewForm(FlaskForm):
    author = StringField('Author of the review',validators=[
        InputRequired(),
        Length(max=30)
    ])
    body = StringField('Body of the review',validators=[
        InputRequired(),
        Length(max=30)
        ])
    rating = IntegerField('Rating of the game (1-5)',validators=[
        InputRequired(),
        NumberRange(min=1, max=5)])

    submit = SubmitField('Save review')


class GameForm(FlaskForm):
    name = StringField('Name of the game',validators=[
        InputRequired(),
        Length(max=30)
    ])
    genre = StringField('Genre of the game',validators=[
        InputRequired(),
        Length(max=10)
    ])
    submit = SubmitField('Save Game')
