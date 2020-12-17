from application import app, db
from application.models import Reviews, Games
from application.forms import ReviewForm, GameForm
from flask import Flask, render_template, request, redirect, url_for

@app.route("/")
@app.route("/home")
def home():
    all_reviews = Reviews.query.all()
    all_games = Games.query.all()
    return render_template("home.html", all_reviews = all_reviews, all_games = all_games)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = ReviewForm()
    if request.method == "POST":
        if form.validate_on_submit():
            
            game_name = form.recommendations.data.name
            game = Games.query.filter_by(name=game_name).first()
            new_review = Reviews(
                author=form.author.data,
                body=form.body.data,
                rating=form.rating.data
            )
            db.session.add(new_review)
            db.session.commit()
            new_review.recommendations.append(game)
            db.session.add(game)
            db.session.commit()
            return  redirect(url_for("home"))
    
    return render_template('add.html', title="Create a task", form = form)

@app.route("/addgame", methods=["GET", "POST"])
def addgame():
    form = GameForm()
    all_games = Games.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            new_game = Games(
                name = form.name.data,
                genre = form.genre.data
            )
            db.session.add(new_game)
            db.session.commit()
            return  redirect(url_for("home"))
    return render_template('addgame.html', title="Add a game", form = form, all_games = all_games)


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = ReviewForm()
    review = Reviews.query.filter_by(id=id).first()
    if request.method == "POST":
        review.body = form.body.data
        review.rating = form.rating.data
        db.session.commit()
        return  redirect(url_for("home"))
    return render_template("update.html", form=form, title="Update Review", review = review)

@app.route("/updategame/<int:id>", methods=["GET", "POST"])
def updategame(id):
    form = GameForm()
    game = Games.query.filter_by(id=id).first()
    if request.method == "POST":
        game.name = form.name.data
        game.genre = form.genre.data
        return  redirect(url_for("home"))
    return render_template("updategame.html", form=form, title="Update Game", game = game)

@app.route("/delete/<int:id>")
def delete(id):
    review = Reviews.query.filter_by(id=id).first()
    db.session.delete(review)
    db.session.commit()
    return  redirect(url_for("home"))

@app.route("/deletegame/<int:id>")
def deletegame(id):
    game = Games.query.filter_by(id=id).first()
    db.session.delete(game)
    db.session.commit()
    return  redirect(url_for("home"))


